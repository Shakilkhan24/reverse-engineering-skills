---
name: reconstruct-verify
description: Verify a software reconstruction against explicit scenarios and reference evidence using executed behavioral, contract, data, visual, failure, or performance checks. Use for differential testing, regression diagnosis, fidelity reporting, or release claims; skip investigations with no implementation or claim to evaluate.
---

# Verify reconstruction claims

Establish exactly which claims passed under which conditions. Own test design, execution records, discrepancy reporting, and scoped verification status; implementation ownership remains with the relevant specialist.

Read the [common contract](../reconstruct-orchestrate/references/common-contract.md) before the first work unit. This skill belongs to the complete reconstruction library.

## Inputs and outputs

Require requirement/scenario IDs, target and replacement identities, acceptance criteria, expected outcomes, relevant evidence and its limitations, runnable code, and available test capabilities. Review missing scenarios before testing; a narrow suite cannot justify a broad subsystem claim.

Produce executed run records, retained outputs, reproducible discrepancies, a verification matrix, and a report with explicit scenario denominators. Follow [state format](../reconstruct-orchestrate/references/state-format.md) for machine-checkable records and [templates](../reconstruct-orchestrate/references/templates.md) for human handoffs.

## Procedure

1. Freeze the compared versions, fixture identities, environment, and contract revision for this run. If the original is inaccessible, identify whether each expected outcome comes from a retained observation, documentation, an inference, or an independent requirement.
2. Select checks by risk and claim: domain/unit checks for invariants, integration checks for actual boundaries, end-to-end checks for journeys, and differential checks when equivalent reference observations exist. Cover relevant denied access, invalid input, persistence, interruption, duplicates, concurrency, and recovery.
3. Define normalization and tolerances before comparison. Normalize only irrelevant volatile values; preserve identity relationships, ordering, time semantics, authorization, and other contractually meaningful differences.
4. Control visual comparisons with matching data, viewport, browser/font conditions, and state. Control API comparisons with matching actor, inputs, headers, response schema/errors, and side-effect checks. Control concurrency with deliberate interleavings rather than sleeps that merely hope for a race.
5. For performance claims, define workload, concurrency, duration, warmup, sample size, hardware/service limits, latency distribution, throughput, errors, and resource use. Distinguish a replacement engineering target from measured original behavior. Never equate unlike environments without disclosing the difference.
6. Execute the selected tests. Preserve command or manual procedure, environment, timestamp, identities, exit/result status, and output artifact. A build passing establishes buildability; a test file existing establishes no executed result.
7. Investigate failures by separating fixture/environment defects from product differences. Register expected versus actual behavior, severity, evidence, affected requirements, suspected cause, owner, and regression scenario. Do not remove an assertion merely to improve the pass count.
8. Have the owner fix the cause, then rerun affected scenarios and justified regression checks. Preserve failed attempts; a later current failure supersedes an earlier passing result for the same scenario.
9. Report current passing scenarios over all required enumerated scenarios, with blocked/skipped/untested counts and unresolved differences. Separate verified independent requirements from evidence-supported equivalence. Run the project's finite state gate when available; review its limitations before making a release recommendation.

## Acceptance evidence

- Each verified requirement is supported by current executed results for all of its required scenarios.
- Result artifacts exist and identify the tested version/environment. Stale evidence, changed code, or changed acceptance conditions trigger review and relevant re-execution.
- A discrepancy is closed only when its correction and corresponding regression result are recorded.
- Flaky or quarantined tests remain visible in the denominator until their nondeterminism is understood; quarantine is not a pass.
- The report distinguishes test coverage, implementation coverage, assumptions, and unknown target behavior. It does not convert them into a universal fidelity percentage.

## Recovery and handoff

If a required tool cannot run, retain the failure output, classify the affected checks as blocked, and execute independent checks that remain useful. Static reasoning can narrow a defect but cannot replace a claimed runtime test. For nondeterministic AI or distributed behavior, define repeated trials and an acceptance rule before interpreting outcomes.

Return evidence gaps to [investigate](../reconstruct-investigate/SKILL.md), ambiguous requirements to [specify](../reconstruct-specify/SKILL.md), defects to their implementation owner, and the largest remaining gap to [orchestrate](../reconstruct-orchestrate/SKILL.md). Coordinate operational drills with [operate](../reconstruct-operate/SKILL.md) and risk interpretation with [assure](../reconstruct-assure/SKILL.md).
