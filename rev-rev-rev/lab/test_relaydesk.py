import tempfile
import threading
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from relaydesk import DomainError, FakeProvider, Store


class ContractTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / "tickets.db"
        self.s = Store(self.path)
        self.addCleanup(lambda: self.s.close())
        self.s.add_member("alice", "ws_a")
        self.s.add_member("bob", "ws_b")
        self.provider_path = Path(self.tmp.name) / "provider.db"

    def create(self):
        return self.s.create_ticket("alice", "ws_a", "Login failure", "k1")

    def test_01_persistence_after_reopen(self):
        ticket = self.create()
        self.s.close()
        self.s = Store(self.path)
        self.assertEqual(self.s.get_ticket("alice", "ws_a", ticket["id"]), ticket)

    def test_02_same_key_replays_one_ticket_and_event(self):
        self.assertEqual(self.create(), self.create())
        self.assertEqual([self.s.count(t) for t in ["tickets", "requests", "outbox"]], [1, 1, 1])

    def test_03_changed_payload_conflicts(self):
        self.create()
        with self.assertRaisesRegex(DomainError, "key_payload_mismatch"):
            self.s.create_ticket("alice", "ws_a", "Different title", "k1")
        self.assertEqual(self.s.count("tickets"), 1)

    def test_04_cross_workspace_read_and_write_denied(self):
        ticket = self.create()
        for operation in [lambda: self.s.get_ticket("bob", "ws_a", ticket["id"]),
                          lambda: self.s.transition("bob", "ws_a", ticket["id"], 1, "in_progress"),
                          lambda: self.s.create_ticket("bob", "ws_a", "Bad", "k2")]:
            with self.assertRaisesRegex(DomainError, "forbidden"):
                operation()
        with self.assertRaisesRegex(DomainError, "not_found"):
            self.s.get_ticket("bob", "ws_b", ticket["id"])
        self.assertEqual(self.s.get_ticket("alice", "ws_a", ticket["id"])["version"], 1)

    def test_05_stale_version_rejected(self):
        ticket = self.create()
        self.s.transition("alice", "ws_a", ticket["id"], 1, "in_progress")
        with self.assertRaisesRegex(DomainError, "version_conflict"):
            self.s.transition("alice", "ws_a", ticket["id"], 1, "resolved")

    def test_06_invalid_transition_preserves_state(self):
        ticket = self.create()
        with self.assertRaisesRegex(DomainError, "invalid_transition"):
            self.s.transition("alice", "ws_a", ticket["id"], 1, "closed")
        self.assertEqual(self.s.get_ticket("alice", "ws_a", ticket["id"]), ticket)

    def test_07_precommit_fault_rolls_back_every_record(self):
        with self.assertRaisesRegex(RuntimeError, "injected_before_commit"):
            self.s.create_ticket("alice", "ws_a", "Fault", "k1", fail_before_commit=True)
        self.assertEqual([self.s.count(t) for t in ["tickets", "requests", "outbox"]], [0, 0, 0])
        self.create()
        self.assertEqual(self.s.count("tickets"), 1)

    def test_08_provider_ack_gap_survives_reopen(self):
        self.create()
        p = FakeProvider(self.provider_path)
        try:
            with self.assertRaises(RuntimeError):
                self.s.deliver(p, crash_after_send=True)
            self.assertEqual((p.count(), self.s.pending()), (1, 1))
        finally:
            p.close()
        self.s.close()
        self.s = Store(self.path)
        p = FakeProvider(self.provider_path)
        try:
            self.s.deliver(p)
            self.assertEqual((p.count(), self.s.pending()), (1, 0))
        finally:
            p.close()

    def test_09_provider_failure_leaves_pending_work(self):
        self.create()
        class Unavailable:
            def send(self, *_):
                raise ConnectionError("provider_unavailable")
        with self.assertRaises(ConnectionError):
            self.s.deliver(Unavailable())
        self.assertEqual((self.s.count("tickets"), self.s.pending()), (1, 1))

    def test_10_overlapping_duplicate_requests(self):
        barrier = threading.Barrier(2)
        def submit(_):
            other = Store(self.path)
            try:
                barrier.wait(timeout=5)
                return other.create_ticket("alice", "ws_a", "Same", "parallel")["id"]
            finally:
                other.close()
        with ThreadPoolExecutor(2) as pool:
            ids = list(pool.map(submit, range(2)))
        self.assertEqual(len(set(ids)), 1)
        self.assertEqual((self.s.count("tickets"), self.s.count("outbox")), (1, 1))

    def test_11_overlapping_versioned_updates(self):
        ticket = self.create()
        barrier = threading.Barrier(2)
        def update(_):
            other = Store(self.path)
            try:
                barrier.wait(timeout=5)
                try:
                    other.transition("alice", "ws_a", ticket["id"], 1, "in_progress")
                    return "accepted"
                except DomainError as error:
                    return error.code
            finally:
                other.close()
        with ThreadPoolExecutor(2) as pool:
            results = list(pool.map(update, range(2)))
        self.assertCountEqual(results, ["accepted", "version_conflict"])

    def test_12_validation_boundaries(self):
        for bad in ["", " ", "x" * 121, None, 1]:
            with self.assertRaisesRegex(DomainError, "invalid_title"):
                self.s.create_ticket("alice", "ws_a", bad, "invalid")
        for index, title in enumerate(["x", "x" * 120]):
            self.s.create_ticket("alice", "ws_a", title, str(index))
        self.assertEqual(self.s.count("tickets"), 2)

    def test_13_key_scope_is_actor_and_workspace(self):
        first = self.create()
        second = self.s.create_ticket("bob", "ws_b", "Login failure", "k1")
        self.assertNotEqual(first["id"], second["id"])

    def test_14_replay_returns_original_response_after_transition(self):
        ticket = self.create()
        self.s.transition("alice", "ws_a", ticket["id"], 1, "in_progress")
        self.assertEqual(self.create(), ticket)
        self.assertEqual(self.s.get_ticket("alice", "ws_a", ticket["id"])["version"], 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
