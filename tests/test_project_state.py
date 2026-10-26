"""Behavioral tests for the finite state gate. Fixtures are synthetic records."""
import contextlib
from copy import deepcopy
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "skills/reconstruct-orchestrate/scripts/project_state.py"
spec = importlib.util.spec_from_file_location("project_state", SCRIPT)
ps = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ps)


class ProjectStateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.state = ps.initial_state("Owned task app", "snapshot-001")
        self.state["project"].update(replacement_revision="commit-abc", scope_accepted=True)
        self.state["evidence"] = [{
            "id": "E-001", "classification": "OBSERVED", "claim": "Task survives reload",
            "source": "authorized recording 001", "target_version": "snapshot-001",
            "method": "create synthetic task then reload", "limitations": "One browser, one role",
            "confidence": "high", "freshness": "current", "captured_at": "2026-10-25T10:00:00Z"}]
        self.state["decisions"] = [{"id": "D-001", "decision": "Store tasks transactionally",
                                    "rationale": "Meet persistence behavior", "evidence": ["E-001"]}]
        self.state["requirements"] = [{
            "id": "R-001", "description": "Saved task survives reload", "dimension": "persistence",
            "priority": "high", "status": "VERIFIED", "claim_type": "equivalence", "required": True,
            "evidence": ["E-001"], "decisions": ["D-001"], "implementation": ["src/tasks.py"], "scenarios": ["S-001"]}]
        self.state["scenarios"] = [{"id": "S-001", "requirement": "R-001",
                                    "description": "Create a synthetic task and reload", "expected": "Task remains visible"}]
        self.artifact = self.root / "test-output.txt"
        self.artifact.write_text("synthetic test fixture: one scenario passed\n")
        self.state["runs"] = [self.run_record()]

    def run_record(self, ident="T-001", **changes):
        run = {"id": ident, "scenario": "S-001", "target_version": "snapshot-001",
               "replacement_revision": "commit-abc", "command": "python -m unittest tests.test_reload",
               "environment": "Synthetic fixture; Python 3.12 on Linux", "executed_at": "2026-10-25T10:01:00Z",
               "result": "PASS", "comparison": "equivalent",
               "contract_sha256": ps.contract_fingerprint(self.state, "S-001"),
               "artifact": {"path": "test-output.txt", "sha256": hashlib.sha256(self.artifact.read_bytes()).hexdigest()}}
        run.update(changes)
        return run

    def check_not_ready(self, substring=None):
        result = ps.report(self.state, self.root)
        self.assertFalse(result["ready"], result)
        if substring:
            self.assertIn(substring, json.dumps(result))
        return result

    def test_current_fully_linked_record_passes_finite_gate(self):
        result = ps.report(self.state, self.root)
        self.assertTrue(result["ready"], result)
        self.assertEqual(result["coverage"], {"required_requirements": 1, "verified_required_requirements": 1,
                                             "required_scenarios": 1, "passing_current_required_scenarios": 1})

    def test_empty_accepted_scope_never_passes(self):
        self.state = ps.initial_state("Target", "v1")
        self.state["project"].update(scope_accepted=True, replacement_revision="r1")
        self.check_not_ready("no required requirements")

    def test_different_target_with_same_version_invalidates_previous_run(self):
        self.state["project"]["target"] = "Different application"
        self.check_not_ready("different contract/evidence snapshot")

    def test_scenario_fixture_digest_change_invalidates_previous_run(self):
        self.state["scenarios"][0]["fixture_sha256"] = "a" * 64
        self.state["runs"] = [self.run_record()]
        self.assertTrue(ps.report(self.state, self.root)["ready"])
        self.state["scenarios"][0]["fixture_sha256"] = "b" * 64
        self.check_not_ready("different contract/evidence snapshot")

    def test_optional_resolution_evidence_is_validated_for_open_gaps(self):
        gap = {"id": "U-001", "description": "Low priority unknown", "severity": "low",
               "status": "open", "requirements": [], "evidence": [],
               "next_action": "Investigate later"}
        self.state["unknowns"] = [gap]
        for malformed in (None, 4, {}, [4], [[]]):
            with self.subTest(value=malformed):
                gap["resolution_evidence"] = malformed
                result = ps.report(self.state, self.root)
                self.assertFalse(result["valid"])
                self.assertFalse(result["ready"])
                self.assertIn("resolution_evidence", json.dumps(result))

    def test_unaccepted_scope_and_unset_revision_block(self):
        self.state["project"].update(scope_accepted=False, replacement_revision="UNSET")
        self.check_not_ready("needs a meaningful identity")

    def test_every_acceptance_scenario_is_required(self):
        self.state["requirements"][0]["scenarios"].append("S-002")
        self.state["scenarios"].append({"id": "S-002", "requirement": "R-001",
                                       "description": "Reload after process restart", "expected": "Task remains visible"})
        result = self.check_not_ready("S-002")
        self.assertEqual(result["coverage"]["passing_current_required_scenarios"], 1)
        self.assertEqual(result["coverage"]["required_scenarios"], 2)

    def test_stale_or_wrong_version_evidence_blocks(self):
        original = deepcopy(self.state)
        for updates in ({"freshness": "stale"}, {"target_version": "older-version"}):
            self.state = deepcopy(original)
            self.state["evidence"][0].update(updates)
            self.check_not_ready("stale evidence")

    def test_target_and_replacement_changes_invalidate_runs(self):
        original = deepcopy(self.state)
        for key in ("target_version", "replacement_revision"):
            self.state = deepcopy(original)
            self.state["project"][key] = "new-identity"
            self.check_not_ready("no run for current")

    def test_contract_edit_invalidates_previous_success(self):
        self.state["scenarios"][0]["expected"] = "Task remains visible and assigned to owner"
        self.check_not_ready("different contract/evidence snapshot")

    def test_status_change_does_not_change_contract_fingerprint(self):
        old = ps.contract_fingerprint(self.state, "S-001")
        self.state["requirements"][0]["status"] = "IMPLEMENTED, UNVERIFIED"
        self.assertEqual(old, ps.contract_fingerprint(self.state, "S-001"))
        self.check_not_ready("declared status")

    def test_latest_current_failure_wins_even_when_list_is_out_of_order(self):
        failed = self.run_record("T-002", result="FAIL", executed_at="2026-10-25T10:03:00Z")
        self.state["runs"].insert(0, failed)
        self.check_not_ready("latest current run is FAIL")

    def test_latest_skipped_or_blocked_run_never_passes(self):
        for outcome in ("SKIPPED", "BLOCKED"):
            self.state["runs"] = [self.run_record(result=outcome, artifact=None)]
            self.check_not_ready(f"latest current run is {outcome}")

    def test_latest_tie_uses_last_record(self):
        self.state["runs"].append(self.run_record("T-002", result="FAIL"))
        self.check_not_ready("latest current run is FAIL")

    def test_missing_tampered_or_absent_artifact_cannot_pass(self):
        self.artifact.unlink()
        self.check_not_ready("artifact is missing")
        self.artifact.write_text("changed content")
        self.check_not_ready("hash does not match")
        self.state["runs"][0]["artifact"] = None
        self.check_not_ready("no recorded output")

    def test_artifact_path_traversal_and_external_symlink_fail(self):
        self.state["runs"][0]["artifact"]["path"] = "../outside.txt"
        self.assertTrue(ps.validate(self.state))
        external = self.root.parent / (self.root.name + "-outside.txt")
        external.write_text("outside")
        self.addCleanup(external.unlink)
        link = self.root / "link.txt"
        link.symlink_to(external)
        self.state["runs"][0]["artifact"] = {"path": "link.txt", "sha256": hashlib.sha256(external.read_bytes()).hexdigest()}
        self.check_not_ready("escapes the state directory")

    def test_assumptions_inferences_unknowns_do_not_prove_equivalence(self):
        for classification in ("INFERRED", "ASSUMED", "UNKNOWN", "CONTRADICTED"):
            self.state["evidence"][0]["classification"] = classification
            self.state["runs"] = [self.run_record()]
            self.check_not_ready("cannot")

    def test_independent_design_can_be_tested_without_equivalence_claim(self):
        self.state["requirements"][0]["claim_type"] = "independent"
        self.state["evidence"][0]["classification"] = "ASSUMED"
        self.state["runs"] = [self.run_record(comparison="independent")]
        result = ps.report(self.state, self.root)
        self.assertTrue(result["ready"], result)
        self.assertEqual(result["requirements"][0]["claim_type"], "independent")

    def test_not_comparable_result_never_establishes_equivalence(self):
        self.state["runs"][0]["comparison"] = "not-comparable"
        self.check_not_ready("not-comparable")

    def test_missing_links_duplicate_ids_and_orphans_fail(self):
        original = deepcopy(self.state)
        for mutate in (
            lambda s: s["requirements"][0]["evidence"].append("E-missing"),
            lambda s: s["decisions"][0].update(id="E-001"),
            lambda s: s["requirements"][0].update(scenarios=[]),
        ):
            self.state = deepcopy(original)
            mutate(self.state)
            self.assertTrue(ps.validate(self.state))
            self.check_not_ready()

    def test_malformed_types_report_errors_instead_of_crashing(self):
        original = deepcopy(self.state)
        for mutate in (
            lambda s: s.update(requirements={}),
            lambda s: s["requirements"][0].update(evidence=[{}]),
            lambda s: s["project"].update(scope_accepted="true"),
            lambda s: s.update(schema_version=True),
            lambda s: s["runs"][0].update(artifact=[]),
            lambda s: s["runs"][0].update(executed_at="2026-10-25T10:00:00"),
            lambda s: s["unknowns"].append({"id": "U-1", "status": []}),
        ):
            self.state = deepcopy(original)
            mutate(self.state)
            self.assertTrue(ps.validate(self.state))
            self.check_not_ready()

    def test_empty_acceptance_or_no_implementation_cannot_be_verified(self):
        self.state["scenarios"] = []
        self.state["runs"] = []
        self.state["requirements"][0].update(scenarios=[], implementation=[])
        self.check_not_ready("no acceptance scenarios")

    def test_high_gap_blocks_even_if_deferred_and_low_gap_remains_visible(self):
        gap = {"id": "U-001", "description": "Concurrent writes untested", "severity": "high",
               "status": "deferred", "rationale": "No test harness yet", "requirements": ["R-001"],
               "evidence": ["E-001"], "next_action": "Add concurrency test"}
        self.state["unknowns"] = [gap]
        self.check_not_ready("high deferred")
        gap["severity"] = "low"
        result = ps.report(self.state, self.root)
        self.assertTrue(result["ready"], result)
        self.assertEqual(len(result["unresolved"]), 1)

    def test_resolved_high_gap_requires_current_resolution_evidence(self):
        old = deepcopy(self.state["evidence"][0])
        old.update(id="E-old", freshness="stale")
        self.state["evidence"].append(old)
        self.state["unknowns"] = [{"id": "U-001", "description": "Concurrent writes untested",
            "severity": "high", "status": "resolved", "rationale": "Historical test result",
            "requirements": ["R-001"], "evidence": [], "resolution_evidence": ["E-old"],
            "next_action": "Recheck when target changes"}]
        self.check_not_ready("resolution evidence E-old is stale")

    def test_tool_blocker_is_visible_and_blocks_readiness(self):
        self.state["checkpoint"]["blockers"] = ["Browser unavailable for required accessibility checks"]
        self.check_not_ready("Browser unavailable")

    def test_init_refuses_existing_directory_without_touching_content(self):
        location = self.root / "project"
        created = ps.init_directory(location, "Target", "v1")
        original = created.read_bytes()
        with self.assertRaises(FileExistsError):
            ps.init_directory(location, "Changed", "v2")
        self.assertEqual(created.read_bytes(), original)
        self.assertEqual(ps.validate(json.loads(original)), [])

    def test_cli_report_incomplete_is_success_but_gate_fails(self):
        state_file = self.root / "state.json"
        self.state["runs"] = []
        state_file.write_text(json.dumps(self.state))
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(ps.main(["report", str(state_file)]), 0)
            self.assertEqual(ps.main(["gate", str(state_file)]), 1)
            self.assertEqual(ps.main(["validate", str(state_file)]), 0)

    def test_cli_reports_bad_json_and_unknown_scenario(self):
        state_file = self.root / "state.json"
        state_file.write_text("{")
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(ps.main(["gate", str(state_file)]), 2)
        state_file.write_text(json.dumps(self.state))
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(ps.main(["fingerprint", str(state_file), "S-absent"]), 2)


if __name__ == "__main__":
    unittest.main()
