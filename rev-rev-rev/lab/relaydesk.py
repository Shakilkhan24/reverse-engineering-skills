"""Teaching service, NOT a web server. Trusted actor comes from the caller.

SQLite serializes writers here. This demonstrates contracts and crash windows,
not the performance or isolation of a production distributed database.
"""
import hashlib
import json
import sqlite3
import uuid
from contextlib import contextmanager


class DomainError(Exception):
    def __init__(self, code):
        self.code = code
        super().__init__(code)


class Store:
    def __init__(self, path):
        self.db = sqlite3.connect(path, timeout=10, isolation_level=None)
        self.db.row_factory = sqlite3.Row
        self.db.execute("PRAGMA foreign_keys = ON")
        self.db.executescript("""
            CREATE TABLE IF NOT EXISTS members (
                actor TEXT, workspace TEXT, PRIMARY KEY(actor, workspace));
            CREATE TABLE IF NOT EXISTS tickets (
                id TEXT PRIMARY KEY, workspace TEXT NOT NULL,
                title TEXT NOT NULL, status TEXT NOT NULL, version INTEGER NOT NULL);
            CREATE TABLE IF NOT EXISTS requests (
                actor TEXT, workspace TEXT, key TEXT, fingerprint TEXT NOT NULL,
                response TEXT NOT NULL, PRIMARY KEY(actor, workspace, key));
            CREATE TABLE IF NOT EXISTS outbox (
                id TEXT PRIMARY KEY, payload TEXT NOT NULL, delivered INTEGER NOT NULL DEFAULT 0);
        """)

    def close(self):
        self.db.close()

    @contextmanager
    def transaction(self):
        self.db.execute("BEGIN IMMEDIATE")
        try:
            yield
            self.db.commit()
        except BaseException:
            self.db.rollback()
            raise

    def add_member(self, actor, workspace):
        self.db.execute("INSERT OR IGNORE INTO members VALUES (?, ?)", (actor, workspace))

    def authorize(self, actor, workspace):
        if not self.db.execute("SELECT 1 FROM members WHERE actor=? AND workspace=?",
                               (actor, workspace)).fetchone():
            raise DomainError("forbidden")

    def get_ticket(self, actor, workspace, ticket_id):
        self.authorize(actor, workspace)
        row = self.db.execute("SELECT * FROM tickets WHERE id=? AND workspace=?",
                              (ticket_id, workspace)).fetchone()
        if row is None:
            raise DomainError("not_found")
        return dict(row)

    def create_ticket(self, actor, workspace, title, key, fail_before_commit=False):
        if not isinstance(title, str) or not 1 <= len(title.strip()) <= 120:
            raise DomainError("invalid_title")
        if not isinstance(key, str) or not 1 <= len(key) <= 128:
            raise DomainError("invalid_key")
        title = title.strip()
        fingerprint = hashlib.sha256(json.dumps({"title": title}, sort_keys=True).encode()).hexdigest()
        with self.transaction():
            self.authorize(actor, workspace)
            old = self.db.execute(
                "SELECT * FROM requests WHERE actor=? AND workspace=? AND key=?",
                (actor, workspace, key)).fetchone()
            if old:
                if old["fingerprint"] != fingerprint:
                    raise DomainError("key_payload_mismatch")
                return json.loads(old["response"])
            ticket = {"id": "t_" + uuid.uuid4().hex, "workspace": workspace,
                      "title": title, "status": "open", "version": 1}
            self.db.execute("INSERT INTO tickets VALUES (:id,:workspace,:title,:status,:version)", ticket)
            self.db.execute("INSERT INTO outbox (id,payload) VALUES (?,?)",
                            ("evt_" + uuid.uuid4().hex, json.dumps({"kind":"ticket_created", "ticket_id":ticket["id"]})))
            self.db.execute("INSERT INTO requests VALUES (?,?,?,?,?)",
                            (actor, workspace, key, fingerprint, json.dumps(ticket)))
            if fail_before_commit:
                raise RuntimeError("injected_before_commit")
        return ticket

    def transition(self, actor, workspace, ticket_id, expected_version, new_status):
        allowed = {"open": {"in_progress"}, "in_progress": {"resolved"},
                   "resolved": {"closed", "in_progress"}, "closed": set()}
        with self.transaction():
            old = self.get_ticket(actor, workspace, ticket_id)
            if old["version"] != expected_version:
                raise DomainError("version_conflict")
            if new_status not in allowed[old["status"]]:
                raise DomainError("invalid_transition")
            cursor = self.db.execute(
                "UPDATE tickets SET status=?, version=version+1 WHERE id=? AND workspace=? AND version=?",
                (new_status, ticket_id, workspace, expected_version))
            if cursor.rowcount != 1:
                raise DomainError("version_conflict")
            result = self.get_ticket(actor, workspace, ticket_id)
        return result

    def count(self, table):
        if table not in {"tickets", "requests", "outbox"}:
            raise ValueError("unsupported table")
        return self.db.execute("SELECT COUNT(*) FROM " + table).fetchone()[0]

    def pending(self):
        return self.db.execute("SELECT COUNT(*) FROM outbox WHERE delivered=0").fetchone()[0]

    def deliver(self, provider, crash_after_send=False):
        # One worker in this lab. Real workers also need claiming/leases and retry policy.
        rows = self.db.execute("SELECT * FROM outbox WHERE delivered=0 ORDER BY id").fetchall()
        for row in rows:
            provider.send(row["id"], row["payload"])
            if crash_after_send:
                raise RuntimeError("injected_after_external_side_effect")
            self.db.execute("UPDATE outbox SET delivered=1 WHERE id=?", (row["id"],))


class FakeProvider:
    """Separate durable DB models a provider WITH an idempotency guarantee.

    No email or network call is made. Real providers may not offer this guarantee.
    """
    def __init__(self, path):
        self.db = sqlite3.connect(path, isolation_level=None)
        self.db.execute("CREATE TABLE IF NOT EXISTS receipts (event_id TEXT PRIMARY KEY, payload TEXT)")

    def send(self, event_id, payload):
        self.db.execute("INSERT OR IGNORE INTO receipts VALUES (?, ?)", (event_id, payload))

    def count(self):
        return self.db.execute("SELECT COUNT(*) FROM receipts").fetchone()[0]

    def close(self):
        self.db.close()
