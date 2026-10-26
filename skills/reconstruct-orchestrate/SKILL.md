---
name: reconstruct-orchestrate
description: Coordinate evidence-driven software reconstruction across investigation, specifications, implementation, verification, and delivery. Use for rebuilding an identified reference product or resuming a reconstruction project; do not impose this lifecycle on an ordinary small code edit.
---

# Coordinate reconstruction

Turn the requested scope into working, tested slices while preserving what is known,
assumed, and inaccessible. This skill coordinates the library; it is not an autonomous
scheduler and does not supply REA, browser access, credentials, or deployment tools.

## Contract and inputs

Read [the common contract](references/common-contract.md) once per working context.
Inspect the user's target, source materials, repository instructions, existing work,
access boundaries, expected deliverable, and available tools. Reuse maintained project
records. Ask only for a missing decision that materially blocks the current work.
An analysis-only request stays analysis-only. An implementation request requires code
and executed checks when the environment supports them.

## Start or resume

1. Identify the target precisely: name plus version, local artifact digest, revision,
   or capture date. Do not select a nearby fixture or another installed app as target.
2. Inspect repository structure, dirty work, tests, build commands, and existing
   reconstruction state. Record capabilities as available, unavailable, or untested.
   Discover tools before relying on them; skip REA setup for ordinary source analysis.
3. Establish a bounded scope and relevant fidelity dimensions. Select a profile from
   [routing](references/routing.md). Record essential outcomes, explicit exclusions,
   operational destination, and stopping criteria; do not infer a deadline or budget.
4. Create or update a compact scope document and state ledger. For a new project,
   `python3 <this-skill>/scripts/project_state.py init <new-record-directory> --target <name> --version <identity>`
   initializes a ledger without overwriting existing records. Read
   [state format](references/state-format.md) before editing it. If Python is absent,
   use the same fields in maintained documents and check gates manually.
5. On resume, read the checkpoint, current target/replacement identity, latest test
   results, unresolved high-impact gaps, and pending actions. Verify files still exist.
   Invalidate affected results after target, code, fixture, or contract changes.

## Run one useful cycle

1. Rank uncertainties and work by user impact, consequence, information gain,
   dependencies, effort, and reachability. Investigate architecture-invalidating or
   data/security risks before polishing. A numeric score is optional, never precision.
2. Select only the relevant specialist from [routing](references/routing.md); read
   its SKILL.md before applying it. Shared artifacts are the invocation interface.
   Without cross-skill tooling, read and execute that procedure in this agent.
3. Give each task an outcome, requirement/evidence IDs, read/write scope, inputs,
   acceptance scenarios, and a stopping condition using [templates](references/templates.md).
4. Require the necessary predecessor artifacts, not completion of every earlier
   phase. Resolve one uncertain contract before implementing its dependent slice;
   independent established work may continue.
5. Build a coherent vertical slice across the actual layers, exercise its persistence,
   permissions, failures, and user outcome where relevant, then compare with evidence.
6. Reconcile differences: strengthen evidence, correct implementation, revise an
   assumption explicitly, or retain a blocker. Do not weaken acceptance to hide failure.
7. Update IDs, decisions, code locations, scenario results, discrepancies, and checkpoint.
   Run `project_state.py validate <state.json>` and `report <state.json>` where available.
8. Continue with the most valuable remaining gap. Stop at the agreed scope, an actual
   resource limit, or a documented blocker; preserve independently useful progress.

## Parallel execution, when supported

Parallelize only independent questions with settled shared interfaces. Assign distinct
files/worktrees and evidence snapshots; one integration owner writes the shared ledger.
Workers return evidence-linked findings and patches, not competing unreviewed architectures.
Use the [task/result contract](references/templates.md). Check provenance and prerequisites
before merging. Preserve conflicting observations; resolve with a discriminating experiment
or mark the claim disputed. A majority of agents is not evidence. Run integration checks
after merges. Fall back to the same sequence in one agent when delegation is absent.

## Gates and delivery

- **Ready to investigate:** explicit target, bounded question, permitted access.
- **Ready to implement:** requirement, expected outcomes, relevant contract/invariants,
  dependencies, and explicit assumptions; no unresolved critical decision hidden in code.
- **Ready to verify:** executable slice, controlled fixtures, current identities, expected
  outcomes, and comparable reference observations or an explicitly independent contract.
- **Scoped readiness:** all required scenarios have current passing evidence and relevant
  security, accessibility, operations, and recovery conditions are accounted for. Use
  `project_state.py gate <state.json>` to check recorded evidence. Its success is a finite
  ledger check, not global equivalence or automatic deployment authorization.

For analysis deliverables, check question coverage and evidence limitations instead of
pretending implementation gates passed. For partial delivery, retain the full denominator
and explain blocked/deferred requirements. End with investigated facts, code delivered,
checks actually run, limitations/assumptions, and the next three useful actions (or state
that no required work remains). Do not call a prototype production-ready.
