---
name: reconstruct-specify
description: Convert reference evidence and reconstruction goals into testable behavior contracts, architecture decisions, and vertical slices. Use when requirements or consequential design choices are unsettled; reuse existing contracts for routine implementation changes.
---

# Specify behavior and replacement architecture

Make the next implementation slice unambiguous without pretending to know inaccessible
internals. Read the [shared contract](../reconstruct-orchestrate/references/common-contract.md).

## Inputs and dependencies

Read the user's intended outcomes, relevant inventory and evidence from
[investigate](../reconstruct-investigate/SKILL.md), unresolved questions, repository design,
deployment constraints, and existing requirements. A user requirement can justify an
independent replacement capability even when the reference is inaccessible; mark that
basis explicitly. Do not label guessed APIs or a chosen physical schema as discoveries.

## Procedure

1. Enumerate relevant fidelity dimensions and required journeys, including hidden dependencies
   and indirect effects. Mark each requirement essential, optional, or deferred with rationale.
   Keep the scope denominator visible; avoid manufacturing requirements for irrelevant layers.
2. For each high-value slice, define the behavior with the
   [specification template](../reconstruct-orchestrate/references/templates.md): actors,
   preconditions, inputs/outputs, state transitions, invariants, persistence, authorization,
   side effects, duplicate semantics, timing/order, errors, and recovery. Link each to evidence
   or an explicit independent decision. Record assumptions separately from verified facts.
3. Write acceptance scenarios before implementation: happy path plus relevant denial,
   reload/restart, invalid input, duplicate, boundary, concurrency, and dependency failure cases.
   Define fixtures, expected observations, tolerances, and what constitutes comparability.
4. Decide each uncertainty: investigate now; implement a provisional minimum contract;
   choose independent robust design; defer explicitly; or request truly blocking access.
   Prioritize uncertainties affecting architecture, security, data loss, or core outcomes.
5. Choose the simplest architecture satisfying the contracts and operational constraints.
   Assess consistency, ownership, query/access patterns, throughput, failure boundaries,
   maintainability, and cost. Retain working repository conventions. Compare alternatives
   when the choice is consequential; do not force microservices, queues, or cloud services.
6. Define interfaces, entity identity/ownership, transaction boundaries, migrations, indexes,
   integration contracts, error taxonomy, and config/secrets boundaries as applicable.
   Conceptual entities needed for compatibility do not reveal the original physical schema.
7. Consult [assure](../reconstruct-assure/SKILL.md) for consequential trust/failure boundaries
   and [operate](../reconstruct-operate/SKILL.md) for relevant release constraints. These can
   inform architecture before implementation; they need not become separate projects.
8. Split into coherent vertical slices ordered by actual dependencies and value. Each slice
   names its requirement IDs, owned files, contracts, acceptance scenarios, and reviewable
   completion boundary. Parallelize only after shared interfaces are settled.

## Outputs and quality gate

Deliver a behavioral specification, API/data/state contracts when relevant, decision records,
scenario definitions, and an ordered slice backlog. Index them in the project state using
[state format](../reconstruct-orchestrate/references/state-format.md). An implementation-ready
slice has testable outcomes, explicit assumptions, defined dependencies, and no hidden
high-consequence decision. The architecture is a replacement design justified by requirements,
not a claim about recovered internals. A diagram is optional when it clarifies ownership or flow.

## Recovery and handoff

When two requirements conflict, identify the conflicting evidence and user consequence;
resolve from authority/context or escalate the smallest necessary decision. Do not silently
drop one. New evidence may revise a contract; supersede decisions, invalidate affected runs,
and notify owners. Send UI work to [experience](../reconstruct-experience/SKILL.md), domain/data
work to [services-data](../reconstruct-services-data/SKILL.md), and scenario definitions to
[verify](../reconstruct-verify/SKILL.md). Update the orchestrator with residual uncertainty
and what work can proceed independently.
