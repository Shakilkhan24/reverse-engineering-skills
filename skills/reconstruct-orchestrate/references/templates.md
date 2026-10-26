# Compact working templates

Use these fields within existing documents or tickets; do not create every template for
every project. Structured IDs link to [state-format.md](state-format.md). Detailed artifacts
can live in project-native locations and be referenced by stable path/anchor.

## Scope and capability record

Target/identity; requested deliverable; authoritative repository; access mode; relevant
fidelity dimensions; required outcomes; exclusions/deferred work and rationale; intended
runtime/deployment; constraints; established authorization; discovered tool capabilities
(available/unavailable/untested with evidence); acceptance/stopping conditions; owner.

## Feature and behavioral specification

Feature ID / requirement IDs / user outcome / entry points / actors and authorization /
preconditions / inputs and validation / outputs / state transitions / persistence and
invariants / side effects and duplicate behavior / async ordering and timing tolerances /
errors and recovery / dependencies / reference evidence / independent design decisions /
unresolved hypotheses / acceptance scenario IDs and fixtures.

## Evidence or experiment

Question → competing hypotheses → permitted smallest discriminating experiment → target
identity and controlled inputs → tool/method → raw artifact/digest → observation → interpretation
and classification → confidence → coverage/limitations → affected IDs → next action.
Include a documented source's version and exact section; do not call it runtime observation.

## Architecture decision

Decision ID; affected requirements; context and constraints; alternatives and tradeoffs;
chosen replacement design; evidence vs assumptions; ownership/interfaces/data consistency;
testable consequences; rollback/reversibility; superseded decision if any.

## Worker task / handoff

Task ID; bounded question; evidence snapshot and target/replacement identities; requirement
IDs; predecessor artifacts; permitted tools/actions; owned files and prohibited shared writes;
deliverables; acceptance checks; budget/stop condition if supplied; unresolved dependencies.

Return: question → evidence IDs/artifacts → conclusion → confidence → limitations → open
questions → recommended action; add code changes, commands/results, and state delta where
applicable. Integrator validates links, reconciles conflicts, merges, and runs affected checks.

## Difference / risk / unknown

Stable ID; expected and actual behavior (unknown where unestablished); evidence; severity
and user consequence; affected requirements; root cause or competing hypotheses; required
access/next experiment; correction owner; regression scenario; disposition and rationale;
verification status. Deferred means explicitly retained outside completed scope, not fixed.

## Verification record

Scenario ID; precise expected observations and oracle; reference target/version; replacement
revision; fixtures; command or manual procedure; environment and date; actual results;
raw output artifact and digest; PASS/FAIL/SKIPPED/BLOCKED; comparison equivalent/independent/
not-comparable; mismatches; normalization and tolerance rationale. A manual check must also
preserve concrete steps, actual observations, and their artifact; do not invent a CLI command.

## Checkpoint and fidelity report

Checkpoint: current goal/slice; identities; authoritative artifact index; completed work;
latest results; important assumptions; unresolved blockers; safe next action; recovery/setup
commands; pending external actions and authorization context; next three useful actions.

Report each relevant dimension independently: enumerated requirements/scenarios; implemented
count; current passing count and denominator; status; mismatches; missing evidence; unknowns;
operational limits. Separate compatibility claims from independently verified design. Keep
deferred items and incomplete critical journeys visible. Do not compute global percent similarity.
