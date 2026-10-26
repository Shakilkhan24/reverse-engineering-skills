#!/usr/bin/env python3
"""Validate reconstruction records and evaluate a finite, evidence-linked gate.

This tool reads records; it neither runs tests nor authenticates claims made by
an agent. Only init writes files, and it never overwrites an existing path.
"""
from __future__ import annotations

import argparse
from datetime import datetime
import hashlib
import json
from pathlib import Path
import re
import sys

SCHEMA_VERSION = 1
CLASSES = {"OBSERVED", "DOCUMENTED", "DERIVED", "INFERRED", "ASSUMED", "UNKNOWN", "CONTRADICTED"}
STATUSES = {"VERIFIED", "PARTIALLY VERIFIED", "IMPLEMENTED, UNVERIFIED", "ASSUMED", "BLOCKED", "NOT IMPLEMENTED"}
PRIORITIES = {"critical", "high", "normal", "low"}
RESULTS = {"PASS", "FAIL", "SKIPPED", "BLOCKED"}
ID = re.compile(r"^[A-Za-z][A-Za-z0-9_-]{0,79}$")
HASH = re.compile(r"^[0-9a-f]{64}$")
UNSET = {"", "unset", "unknown", "unidentified"}


def timestamp(value):
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError("timezone is required")
    return parsed


def initial_state(target, version):
    return {
        "schema_version": SCHEMA_VERSION,
        "project": {"target": target, "target_version": version,
                    "replacement_revision": "UNSET", "scope_accepted": False},
        "evidence": [], "requirements": [], "decisions": [], "scenarios": [],
        "runs": [], "unknowns": [], "discrepancies": [],
        "checkpoint": {"summary": "Discovery has not yet been performed.",
                       "next_action": "Inspect target identity, access, repository and existing evidence.",
                       "blockers": []},
    }


def validate(state):
    """Return structural and referential errors; incomplete states remain valid."""
    errors = []

    def field(record, key, kind, location, nonempty=False):
        value = record.get(key)
        # bool is an int subclass; use exact types to avoid accepting it as a version.
        if type(value) is not kind:
            errors.append(f"{location}.{key}: expected {kind.__name__}")
            return None
        if nonempty and not value.strip():
            errors.append(f"{location}.{key}: must not be blank")
        return value

    def choice(record, key, choices, location):
        value = field(record, key, str, location, True)
        if value is not None and value not in choices:
            errors.append(f"{location}.{key}: expected one of {', '.join(sorted(choices))}")

    def strings(record, key, location):
        values = field(record, key, list, location)
        if values is not None:
            if any(type(v) is not str or not v.strip() for v in values):
                errors.append(f"{location}.{key}: expected nonblank strings")
            elif len(values) != len(set(values)):
                errors.append(f"{location}.{key}: duplicate entries")
        return values

    if type(state) is not dict:
        return ["state: expected object"]
    if field(state, "schema_version", int, "state") != SCHEMA_VERSION:
        errors.append(f"state.schema_version: supported version is {SCHEMA_VERSION}")
    project = field(state, "project", dict, "state")
    if project is not None:
        for key in ("target", "target_version", "replacement_revision"):
            field(project, key, str, "project", True)
        field(project, "scope_accepted", bool, "project")
    checkpoint = field(state, "checkpoint", dict, "state")
    if checkpoint is not None:
        for key in ("summary", "next_action"):
            field(checkpoint, key, str, "checkpoint", True)
        strings(checkpoint, "blockers", "checkpoint")

    groups = {}
    all_ids = set()
    for name in ("evidence", "requirements", "decisions", "scenarios", "runs", "unknowns", "discrepancies"):
        records = field(state, name, list, "state")
        groups[name] = {}
        for index, record in enumerate(records or []):
            location = f"{name}[{index}]"
            if type(record) is not dict:
                errors.append(f"{location}: expected object")
                continue
            ident = field(record, "id", str, location, True)
            if ident is not None:
                if not ID.fullmatch(ident):
                    errors.append(f"{location}.id: invalid stable identifier")
                if ident in all_ids:
                    errors.append(f"{location}.id: duplicate {ident}")
                all_ids.add(ident)
                groups[name][ident] = record
            if name == "evidence":
                for key in ("claim", "source", "target_version", "method", "limitations"):
                    field(record, key, str, location, True)
                choice(record, "classification", CLASSES, location)
                choice(record, "freshness", {"current", "stale"}, location)
                choice(record, "confidence", {"high", "medium", "low"}, location)
                value = field(record, "captured_at", str, location, True)
                if value:
                    try:
                        timestamp(value)
                    except ValueError:
                        errors.append(f"{location}.captured_at: expected ISO 8601 timestamp with timezone")
            elif name == "requirements":
                for key in ("description", "dimension"):
                    field(record, key, str, location, True)
                choice(record, "priority", PRIORITIES, location)
                choice(record, "status", STATUSES, location)
                choice(record, "claim_type", {"equivalence", "independent"}, location)
                field(record, "required", bool, location)
                for key in ("evidence", "decisions", "implementation", "scenarios"):
                    strings(record, key, location)
                if record.get("required") is False:
                    field(record, "defer_reason", str, location, True)
            elif name == "decisions":
                field(record, "decision", str, location, True)
                field(record, "rationale", str, location, True)
                strings(record, "evidence", location)
            elif name == "scenarios":
                for key in ("requirement", "description", "expected"):
                    field(record, key, str, location, True)
            elif name == "runs":
                for key in ("scenario", "target_version", "replacement_revision", "command", "environment"):
                    field(record, key, str, location, True)
                choice(record, "result", RESULTS, location)
                digest = field(record, "contract_sha256", str, location, True)
                if digest and not HASH.fullmatch(digest):
                    errors.append(f"{location}.contract_sha256: expected lowercase SHA-256")
                choice(record, "comparison", {"equivalent", "independent", "not-comparable"}, location)
                value = field(record, "executed_at", str, location, True)
                if value:
                    try:
                        timestamp(value)
                    except ValueError:
                        errors.append(f"{location}.executed_at: expected ISO 8601 timestamp with timezone")
                artifact = record.get("artifact")
                if artifact is not None:
                    if type(artifact) is not dict:
                        errors.append(f"{location}.artifact: expected object or null")
                    else:
                        path = field(artifact, "path", str, location + ".artifact", True)
                        digest = field(artifact, "sha256", str, location + ".artifact", True)
                        if path and (Path(path).is_absolute() or ".." in Path(path).parts or "\\" in path):
                            errors.append(f"{location}.artifact.path: use a relative path inside the state directory")
                        if digest and not HASH.fullmatch(digest):
                            errors.append(f"{location}.artifact.sha256: expected lowercase SHA-256")
                elif "artifact" not in record:
                    errors.append(f"{location}.artifact: required, use null if no output was recorded")
            else:
                field(record, "description", str, location, True)
                choice(record, "severity", PRIORITIES, location)
                choice(record, "status", {"open", "resolved", "deferred"}, location)
                strings(record, "requirements", location)
                strings(record, "evidence", location)
                field(record, "next_action", str, location, True)
                if record.get("status") in ("deferred", "resolved"):
                    field(record, "rationale", str, location, True)
                if record.get("status") == "resolved" or "resolution_evidence" in record:
                    strings(record, "resolution_evidence", location)
                if record.get("status") == "resolved":
                    if not record.get("resolution_evidence"):
                        errors.append(f"{location}.resolution_evidence: resolution needs evidence")

    # Do not traverse ill-typed records; references are meaningful only after schema checks.
    if errors:
        return errors

    def links(values, destination, location):
        for value in values:
            if value not in groups[destination]:
                errors.append(f"{location}: unknown {destination} ID {value}")

    for req in groups["requirements"].values():
        for key, destination in (("evidence", "evidence"), ("decisions", "decisions"), ("scenarios", "scenarios")):
            links(req[key], destination, f"{req['id']}.{key}")
        for sid in req["scenarios"]:
            scenario = groups["scenarios"].get(sid)
            if scenario and scenario["requirement"] != req["id"]:
                errors.append(f"{req['id']}.scenarios: {sid} belongs to {scenario['requirement']}")
    for scenario in groups["scenarios"].values():
        links([scenario["requirement"]], "requirements", scenario["id"])
        req = groups["requirements"].get(scenario["requirement"])
        if req and scenario["id"] not in req["scenarios"]:
            errors.append(f"{scenario['id']}: missing reciprocal requirement link")
    for run in groups["runs"].values():
        links([run["scenario"]], "scenarios", run["id"])
    for decision in groups["decisions"].values():
        links(decision["evidence"], "evidence", decision["id"])
    for name in ("unknowns", "discrepancies"):
        for item in groups[name].values():
            links(item["requirements"], "requirements", item["id"])
            links(item["evidence"], "evidence", item["id"])
            links(item.get("resolution_evidence", []), "evidence", item["id"])
    return errors


def contract_fingerprint(state, scenario_id):
    """Bind a run to its scenario, requirement and supporting evidence/design."""
    scenario = next(s for s in state["scenarios"] if s["id"] == scenario_id)
    requirement = next(r for r in state["requirements"] if r["id"] == scenario["requirement"])
    decisions = sorted((d for d in state["decisions"] if d["id"] in requirement["decisions"]), key=lambda d: d["id"])
    evidence_ids = set(requirement["evidence"])
    for decision in decisions:
        evidence_ids.update(decision["evidence"])
    payload = {
        "target": state["project"]["target"],
        "scenario": scenario,
        "requirement": {k: requirement[k] for k in ("id", "description", "dimension", "claim_type", "implementation")},
        "decisions": decisions,
        "evidence": sorted((e for e in state["evidence"] if e["id"] in evidence_ids), key=lambda e: e["id"]),
    }
    return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def artifact_problem(artifact, root):
    if artifact is None:
        return "no recorded output artifact"
    try:
        resolved = (root / artifact["path"]).resolve()
        resolved.relative_to(root.resolve())
        if not resolved.is_file():
            return "output artifact is missing or not a file"
        digest = hashlib.sha256()
        with resolved.open("rb") as stream:
            for chunk in iter(lambda: stream.read(65536), b""):
                digest.update(chunk)
        if digest.hexdigest() != artifact["sha256"]:
            return "output artifact hash does not match"
    except (OSError, ValueError, RuntimeError):
        return "output artifact is unreadable or escapes the state directory"
    return None


def report(state, root):
    errors = validate(state)
    if errors:
        return {"valid": False, "ready": False, "errors": errors}
    project = state["project"]
    evidence = {e["id"]: e for e in state["evidence"]}
    decisions = {d["id"]: d for d in state["decisions"]}
    latest = {}
    for index, run in enumerate(state["runs"]):
        if (run["target_version"] == project["target_version"] and
                run["replacement_revision"] == project["replacement_revision"]):
            order = (timestamp(run["executed_at"]), index)
            if run["scenario"] not in latest or order > latest[run["scenario"]][0]:
                latest[run["scenario"]] = (order, run)
    rows = []
    passed_scenarios = 0
    scenario_count = 0
    for req in state["requirements"]:
        reasons = []
        if req["status"] != "VERIFIED":
            reasons.append(f"declared status is {req['status']}")
        if not req["implementation"]:
            reasons.append("no implementation references")
        if not req["evidence"]:
            reasons.append("no supporting evidence")
        if not req["decisions"]:
            reasons.append("no design decision references")
        related_evidence = set(req["evidence"])
        for did in req["decisions"]:
            related_evidence.update(decisions[did]["evidence"])
        for eid in sorted(related_evidence):
            item = evidence[eid]
            if item["freshness"] != "current" or item["target_version"] != project["target_version"]:
                reasons.append(f"{eid}: stale evidence or target version mismatch")
            if item["classification"] in {"UNKNOWN", "CONTRADICTED"}:
                reasons.append(f"{eid}: {item['classification']} cannot support verification")
            if req["claim_type"] == "equivalence" and item["classification"] not in {"OBSERVED", "DOCUMENTED", "DERIVED"}:
                reasons.append(f"{eid}: {item['classification']} cannot establish equivalence")
        if not req["scenarios"]:
            reasons.append("no acceptance scenarios")
        scenario_results = []
        for sid in req["scenarios"]:
            problem = None
            run = latest.get(sid, (None, None))[1]
            if run is None:
                problem = "no run for current target version and replacement revision"
            elif run["contract_sha256"] != contract_fingerprint(state, sid):
                problem = "run was recorded for a different contract/evidence snapshot"
            elif run["result"] != "PASS":
                problem = f"latest current run is {run['result']}"
            elif run["comparison"] != ("equivalent" if req["claim_type"] == "equivalence" else "independent"):
                problem = f"comparison is {run['comparison']} for {req['claim_type']} claim"
            else:
                problem = artifact_problem(run["artifact"], root)
            scenario_results.append({"id": sid, "passed": problem is None, "run": run["id"] if run else None, "reason": problem})
            if problem:
                reasons.append(f"{sid}: {problem}")
            if req["required"]:
                scenario_count += 1
                passed_scenarios += problem is None
        rows.append({"id": req["id"], "required": req["required"], "claim_type": req["claim_type"],
                     "declared_status": req["status"], "verified": not reasons, "reasons": reasons,
                     "scenarios": scenario_results, "defer_reason": req.get("defer_reason")})
    required = [row for row in rows if row["required"]]
    blockers = []
    if not project["scope_accepted"]:
        blockers.append("scope has not been established from the user request/context")
    for key in ("target", "target_version", "replacement_revision"):
        if project[key].strip().lower() in UNSET:
            blockers.append(f"project.{key} needs a meaningful identity")
    if not required:
        blockers.append("scope contains no required requirements")
    blockers.extend(f"{row['id']}: {reason}" for row in required for reason in row["reasons"])
    unresolved = []
    for group in ("unknowns", "discrepancies"):
        for item in state[group]:
            affects_scope = not item["requirements"] or any(r["id"] in item["requirements"] for r in required)
            consequential = affects_scope and item["severity"] in {"critical", "high"}
            if item["status"] != "resolved":
                unresolved.append({"kind": group, **item})
                if consequential:
                    blockers.append(f"{item['id']}: {item['severity']} {item['status']} {group} affects required scope")
            elif consequential:
                for eid in item["resolution_evidence"]:
                    resolved_by = evidence[eid]
                    if (resolved_by["freshness"] != "current" or resolved_by["target_version"] != project["target_version"]
                            or resolved_by["classification"] not in {"OBSERVED", "DOCUMENTED", "DERIVED"}):
                        blockers.append(f"{item['id']}: resolution evidence {eid} is stale or does not establish resolution")
    blockers.extend(f"tool/dependency blocker: {value}" for value in state["checkpoint"]["blockers"])
    return {
        "valid": True, "ready": not blockers, "target": project["target"],
        "target_version": project["target_version"], "replacement_revision": project["replacement_revision"],
        "coverage": {"required_requirements": len(required), "verified_required_requirements": sum(r["verified"] for r in required),
                     "required_scenarios": scenario_count, "passing_current_required_scenarios": passed_scenarios},
        "requirements": rows, "unresolved": unresolved, "blockers": blockers,
        "next_action": state["checkpoint"]["next_action"],
        "limitation": "Finite recorded-scope gate; not global fidelity, proof of record authenticity, complete discovery, or automatic production approval.",
    }


def init_directory(path, target, version):
    if not target.strip() or not version.strip():
        raise ValueError("target and version must not be blank")
    # mkdir is an atomic claim of a new destination, even against another process.
    path.mkdir(parents=False, exist_ok=False)
    try:
        (path / "artifacts").mkdir()
        temporary = path / ".state.json.tmp"
        with temporary.open("x", encoding="utf-8") as stream:
            json.dump(initial_state(target, version), stream, indent=2)
            stream.write("\n")
        temporary.replace(path / "state.json")
    except Exception:
        # Keep partial output for diagnosis. Never delete a path another actor may have touched.
        raise
    return path / "state.json"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    init = sub.add_parser("init", help="Create a new state directory; its parent must exist")
    init.add_argument("path", type=Path)
    init.add_argument("--target", required=True)
    init.add_argument("--version", required=True)
    fingerprint = sub.add_parser("fingerprint", help="Print the current scenario contract SHA-256")
    fingerprint.add_argument("state", type=Path)
    fingerprint.add_argument("scenario")
    for command in ("validate", "report", "gate"):
        sub.add_parser(command).add_argument("state", type=Path)
    args = parser.parse_args(argv)
    try:
        if args.command == "init":
            print(init_directory(args.path, args.target, args.version))
            return 0
        with args.state.open(encoding="utf-8") as stream:
            state = json.load(stream)
        if args.command == "fingerprint":
            errors = validate(state)
            if errors:
                raise ValueError("; ".join(errors))
            if not any(s["id"] == args.scenario for s in state["scenarios"]):
                raise ValueError(f"unknown scenario {args.scenario}")
            print(contract_fingerprint(state, args.scenario))
            return 0
        if args.command == "validate":
            errors = validate(state)
            print(json.dumps({"valid": not errors, "errors": errors}, indent=2))
            return 1 if errors else 0
        result = report(state, args.state.parent)
        print(json.dumps(result, indent=2))
        return 1 if not result["valid"] or (args.command == "gate" and not result["ready"]) else 0
    except (OSError, ValueError) as exc:
        print(json.dumps({"valid": False, "ready": False, "error": str(exc)}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
