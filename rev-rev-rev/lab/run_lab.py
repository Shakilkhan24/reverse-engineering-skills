"""Run: python3 lab/run_lab.py --output reports/lab-results.json"""
import argparse
import json
import tempfile
from pathlib import Path
from relaydesk import DomainError, FakeProvider, Store


def run():
    with tempfile.TemporaryDirectory() as temp:
        db = Path(temp) / "tickets.db"
        s = Store(db)
        p = FakeProvider(Path(temp) / "provider.db")
        try:
            s.add_member("alice", "ws_a")
            s.add_member("bob", "ws_b")
            first = s.create_ticket("alice", "ws_a", "Login failure", "k1")
            replay = s.create_ticket("alice", "ws_a", "Login failure", "k1")
            result = {"kind":"executed_local_teaching_lab", "network_calls":0,
                      "duplicate_submission":{"same_id":first["id"] == replay["id"], "ticket_count":s.count("tickets")}}
            s.close()
            s = Store(db)
            result["reopen"] = {"persisted":s.get_ticket("alice", "ws_a", first["id"])["title"] == "Login failure"}
            for label, action in [
                ("cross_workspace", lambda: s.get_ticket("bob", "ws_a", first["id"])),
                ("changed_payload", lambda: s.create_ticket("alice", "ws_a", "Changed", "k1"))]:
                try:
                    action()
                    result[label] = {"error":None}
                except DomainError as error:
                    result[label] = {"error":error.code}
            s.transition("alice", "ws_a", first["id"], 1, "in_progress")
            try:
                s.transition("alice", "ws_a", first["id"], 1, "resolved")
            except DomainError as error:
                result["stale_update"] = {"error":error.code,"version":s.get_ticket("alice", "ws_a", first["id"])["version"]}
            try:
                s.deliver(p, crash_after_send=True)
            except RuntimeError:
                result["ack_gap"] = {"provider_effects":p.count(), "pending_events":s.pending()}
            s.deliver(p)
            result["worker_retry"] = {"provider_effects":p.count(), "pending_events":s.pending()}
            result["limitations"] = ["No HTTP/UI/authentication", "Fake provider guarantees durable deduplication", "No real email or queue", "No throughput benchmark"]
            return result
        finally:
            s.close()
            p.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = json.dumps(run(), ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(report, encoding="utf-8")
    print(report, end="")
