# Requirements and coverage matrix

This matrix maps intended coverage before implementation. A row is **design-mapped**, not verified. Actual validation belongs in the evaluation results and final status report. Source references point to numbered sections in [the main instruction](../REVERSE-ENGINEERING-MAIN.md) or [the mission prompt](../prompt.md).

Skill abbreviations: **O** `reconstruct-orchestrate`; **I** `reconstruct-investigate`; **S** `reconstruct-specify`; **X** `reconstruct-experience`; **D** `reconstruct-services-data`; **A** `reconstruct-assure`; **V** `reconstruct-verify`; **P** `reconstruct-operate`. The first named skill owns the outcome; supporting skills do not duplicate ownership.

## Main instruction: section-by-section traceability

| ID | Source | Intended outcome | Weakness or execution gap | Proposed improvement / owners | Evidence needed to validate the system |
| --- | --- | --- | --- | --- | --- |
| SRC-00 | Role and mission | Reconstruct meaningful system behavior within access | Persona list is not execution machinery | O routes from target and deliverable; I establishes observable scope | A short product request produces a bounded feature/evidence inventory before speculative implementation |
| SRC-01 | §1 Success | Relevant fidelity dimensions assessed independently | No explicit applicability or denominator representation | S records relevant dimensions; V reports enumerated scenario counts | UI-only and API-only scenarios omit irrelevant domains with reasons; no universal fidelity score |
| SRC-02 | §2 Authority and reality | Match tools, repository, artifacts, and permission to task | No capability failure or recovery contract | O discovers capabilities; I uses supported evidence paths | Missing REA/browser access produces a concrete fallback or blocker, never a fictional inspection |
| SRC-03 | §3 Control plane | Persistent coherent project knowledge | Multiple documents can drift or duplicate existing records | O owns minimal shared state and maps existing artifacts | Resume preserves current slice, scope, decisions, and next action |
| SRC-03a | §3.1 Evidence | Provenance, class, confidence, version, limitations | Classification can be mistaken for verification status | I preserves evidence provenance; V links proof separately | An inferred database choice remains inference; a static finding is not reported as observed execution |
| SRC-03b | §3.2 Unknowns | Actionable uncertainty with impact and access needs | No clear bounded retry or inaccessible-question policy | I ranks discriminating experiments; O defers inaccessible internals explicitly | Repeated tool failure stops after diagnosing unchanged blocker; useful independent work continues |
| SRC-03c | §3.3 Traceability | Evidence → requirement → decision → code → test → result | No link validation or changed-input invalidation | O maintains stable IDs; S and V complete the chain | Dangling IDs and unsupported verified claims are detected; changed evidence reopens affected review |
| SRC-04 | §4 Product map | Features include state, dependencies, errors, and side effects | Exhaustive inventory could delay a first working slice | I makes coarse map; S expands next critical journey | A deletion journey includes related records/indexes/notifications where supported |
| SRC-05 | §5 Scientific investigation | Small experiments distinguish hypotheses | Experiment and negative-search boundaries lack a record contract | I records question, input, method, observation, interpretation, limitations | A failed bounded search is not generalized to global absence |
| SRC-06 | §6 Hidden system | Investigate relevant subsystems beyond UI | Checklist breadth lacks routing depth | I activates the relevant owner; detailed coverage below | Representative workflows include permission, persistence, async, and failure probes |
| SRC-07 | §7 Prioritization | Spend effort on consequential reachable uncertainty | Multiplicative scores can imply false precision | O uses documented qualitative ranking, blockers, and dependencies | Architectural uncertainty outranks cosmetic polish; inaccessible low-value details do not loop |
| SRC-08 | §8 Specification | Contracts, invariants, acceptance scenarios, coherent architecture | No input completeness check for a slice | S defines sufficient slice contract and records alternatives | A slice cannot proceed on invented authorization semantics without a declared safe design choice |
| SRC-09 | §9 Vertical slices | Complete incremental behavior with tests and persistence | Documentation-only progress or scaffolding can look complete | X/D implement end-to-end slice; V executes appropriate checks | Actual reload/persistence and permission behavior tested; mocks disclosed |
| SRC-10 | §10 Differential lab | Controlled comparisons and actionable differences | Oracle, normalization, and fixture governance missing | V records comparison conditions and deviations | Generated IDs normalized only when irrelevant; permission/timing semantics remain asserted |
| SRC-10a | §10A–G Comparison types | Visual, behavioral, contract, data, temporal, failure, operational tests | A passing subset might be generalized | V selects relevant modes with explicit denominators | Results identify tested conditions, untested cases, failed scenarios, environment limits |
| SRC-10b | §10 Discrepancies | Every important mismatch has an engineering owner | A mismatch record may lack a reproducer | V links expected/actual evidence and regression scenario; O prioritizes | A deliberate failing case becomes an open discrepancy, not a weakened assertion |
| SRC-11 | §11 Production readiness | Reproducibility, delivery, telemetry, recovery, capacity | Checklist may overfit service infrastructure | P selects controls by deployment; A/V review risk and evidence | Local-only example skips cloud; service example distinguishes configured from executed restore/rollback |
| SRC-12 | §12 Multi-agent reasoning | Independent work with common findings and integration | Missing file ownership, stale-output, conflict merge rules | O assigns bounded ownership and single integration authority | Dependent workers wait; contradictions remain visible; sequential fallback works |
| SRC-13 | §13 Controlled iteration | Close largest gap; avoid infinite polish | No operational distinction between investigation stop and project stop | O checkpoints and chooses next gap from test evidence | Failed critical scenario returns to implementation; inaccessible gap is recorded without falsely completing project |
| SRC-14 | §14 Fidelity report | Truthful status and bounded coverage | Evidence, progress, and blockers share status vocabulary | V derives result claims; O reports separate axes and explicit limits | No test run means unverified; one passing path does not verify the entire subsystem |
| SRC-15 | §15 Hard rules | Prevent fake backend, invented infrastructure, and false success | Repeated prohibitions without checks can be ignored | Shared contract plus specific validation/evaluation cases | Fabricated pass, simulated persistence, or unsupported infrastructure claim is rejected in evaluation |
| SRC-16 | §16 Execution | Make real progress, preserve state, hand off accurately | Massive generation and plan-only behavior remain possible | O selects next complete slice and ends with actual artifacts/results | An actionable task changes implementation and runs available checks; blockers have concrete next actions |
| SRC-17 | §17 Final objective | Best justified reconstruction with honest unknowns | Benefit remains aspirational without evaluation | O/V assess scoped release conditions and system limitations | Final report separates implemented, tested, assumed, blocked, and deferred work |

## Hidden-system subsections

| Source | Primary owner | Required contract / finding | Verification focus |
| --- | --- | --- | --- |
| §6A UI and interaction | X, I | Route/state map; client/server state boundary | Navigation, loading/error states, keyboard and responsive behavior |
| §6B APIs and protocols | D, I/S | Observed/documented contracts; auth context; protocol lifecycle | Schema/errors/pagination/rate limits; reconnect, ordering, or streaming when relevant |
| §6C Domain logic | S, D/I | Examples, decision tables, invariants, state machines | Valid/invalid transitions and calculation boundary cases |
| §6D Data and persistence | D, S/I | Conceptual model, ownership, lifecycle, consistency | Reload, uniqueness, deletion, retention, relation and transaction invariants |
| §6E Concurrency/async | D, V/I | Idempotency, ordering, retries, cancellation, conflict contract | Duplicate delivery, partial failure, concurrent edit, delayed completion |
| §6F Networking/infrastructure | P, I/S | Observable protocol facts; independently chosen topology | TLS/configuration/connection behavior under authorized conditions |
| §6G Observability/operations | P, A/V | Replacement telemetry, SLOs, redaction, retention, costs | Request correlation, diagnostic usefulness, alert and redaction checks |
| §6H Security/privacy | A, D/X | Trust boundaries, access rules, sensitive-data lifecycle | Denied operations, tenant separation, invalid input, session handling |
| §6I Performance/resilience | V, P/A | Workload, budgets, environment, failure/recovery criteria | Comparable latency/throughput/resource measurements; controlled failure recovery |
| §6J Product-specific layers | I, S | Product-relevant hidden semantics | Collaboration conflicts; commerce state; AI distribution/tool behavior; mobile offline; desktop IPC |

## All 20 fidelity dimensions

Each dimension is assessed for applicability before it becomes required work. “Not applicable” needs a scope reason; “not observed” is an evidence gap, not proof of absence.

| ID | Dimension from §1 | Owners | Required evidence / acceptance example |
| --- | --- | --- | --- |
| F01 | Visual and interaction fidelity | X, V | Controlled viewport/font screenshots plus actual interaction transitions |
| F02 | Features and journeys | S, X/D/V | Enumerated in-scope journeys with happy path, denial/error, and completion evidence |
| F03 | Business/domain semantics | S, D/V | Decision examples, state invariants, and boundary-case results |
| F04 | API compatibility | D, V | Contract source and equivalent request/response/error comparison |
| F05 | Authentication, authorization, tenancy | A, D/V | Identity/role matrix and cross-role/cross-tenant negative tests |
| F06 | Persistence and consistency | D, V | Reload/restart persistence, relationships, uniqueness, transaction outcomes |
| F07 | Concurrency and state transitions | D, V | Concurrent operations, stale writes, ordering, and conflict outcomes |
| F08 | Jobs, queues, retries, scheduling | D, V/P | Real execution, retry bounds, duplicate delivery, cancellation, backlog and recovery |
| F09 | Real-time collaboration | D, X/V | Multiple clients, reconnect, divergence/conflict, and convergence checks |
| F10 | Integrations and side effects | D, A/V | Authorized sandbox contract; deduplication, failure/recovery; disclosed test doubles |
| F11 | Search, indexing, caching, generated artifacts | D, V | Query/index freshness, invalidation, tenant scope, artifact content and lifecycle |
| F12 | Networking/protocols | I, D/P/V | Captured or documented protocol behavior; bounded connection lifecycle tests |
| F13 | Performance and resource behavior | V, P/D/X | Workload, baseline, environment, distribution, budgets; observed original vs replacement target |
| F14 | Failure, resilience, recovery | A, D/P/V | Failure model; controlled timeout/outage/partial-failure and recovery evidence |
| F15 | Security, privacy, auditability | A, D/P/V | Threat boundaries, least privilege, secret/redaction checks, retained audit semantics |
| F16 | Telemetry and diagnostics | P, V | Structured event fields, correlation, metrics/traces as relevant, alert/runbook checks |
| F17 | Deployment/configuration/release | P, V/A | Reproducible build, configuration/secrets separation, migration, release/rollback evidence |
| F18 | Accessibility/localization/device compatibility | X, V | Keyboard/focus/semantics, locale/time-zone and supported viewport/device checks |
| F19 | AI behavior when relevant | S, D/X/V/A | Versioned prompts/model interfaces, streaming/tool calls, retrieval fixtures, repeated nondeterministic evaluation |
| F20 | Maintainability/testability/operational readiness | O, S/P/V | Setup and architecture decisions, regression checks, owner/runbook, known limitations |

## Mission requirements beyond the main instruction

| Mission section | Required system behavior | Proposed artifact / owner | Validation evidence needed |
| --- | --- | --- | --- |
| §1–3 | Analyze before designing; preserve valuable principles and identify gaps | This analysis and matrix | All source sections accounted for; interpretation separated from design |
| §4 | Cohesive meaningful skills with justified boundaries | Skill index and architecture / O | No uncovered domain or needless skill-per-technology fragmentation |
| §5 | Selective orchestration, dependencies, reconciliation, sequential fallback | Routing and shared state / O | Routing, blocked-dependency, conflicting-finding, and single-agent scenarios |
| §6 | Consistent purpose, trigger, input, output, workflow, gate, handoff | Eight skill entrypoints and shared contract | Structural validation plus realistic execution |
| §7 | Eight adaptable lifecycle stages | Workflow and feedback paths / O | New evidence can reopen specification; implementation/verification iterate |
| §8 | Correctness, architecture, data, security, tests, reliability, delivery, UX | Specialist ownership above | Representative scenarios require the relevant concerns, not every concern universally |
| §9 | No invented facts or false success | Provenance and result requirements / I/V | Missing evidence and failed-tool cases preserve unverified status |
| §10 | Selective authoritative research and platform conventions | Research notes, skill format, installer | Sources support actual design decisions; real environment conventions inspected |
| §11 | Graceful partial execution | Checkpoint/handoff and essential-first routing / O | Context-constrained run retains useful progress and unmet requirements |
| §12A | Reverse-engineering analysis | Source analysis and coverage matrix | Both files exist and are grounded in supplied inputs |
| §12B | Skill architecture | Index, dependency map, context-sharing rules | Routes and handoffs are actionable, links resolve |
| §12C | Usable skill implementations | Native skill folders and supporting resources | Each skill validates and can be located/read in target environment |
| §12D | Usage documentation | Installation, new-project guide, examples, extension rules | Installation exercise and walk-through from a clean sample project |
| §12E | Validation/evaluation | Scenario corpus, automated checks, evaluation record | Actual results retained, limitations and failed cases reported |
| §14 | Staged execution and persistent progress | Implementation record and final status | Source understanding precedes authoring; revised weaknesses have evidence |

## Mission lifecycle mapping

| Mission stage | Entry condition | Owner and output | Feedback path |
| --- | --- | --- | --- |
| 1 Discovery | User goal and accessible workspace | O/I: target, scope, capabilities, initial evidence | Missing access narrows claims and creates a blocker |
| 2 Reconstruction | Identified target and evidence | I/S: feature/dependency map and hypotheses | Conflicts trigger a discriminating experiment |
| 3 Specification | Enough evidence for the next meaningful slice | S: requirement, state/contract, scenario, assumptions | New observations revise versioned requirements |
| 4 Architecture/planning | Defined contracts and consequential uncertainty | S/O/A: decisions, dependencies, risk and slice order | Invalidated assumption reopens decision |
| 5 Incremental implementation | Sufficient slice contract | X/D/P as relevant: coherent code and configuration | Discovered gaps return to I/S |
| 6 Verification/refinement | Executable slice or inspectable deliverable | V: executed results, discrepancies, coverage | Failed scenarios return to owning implementation skill |
| 7 Production preparation | Intended deployment and release conditions | P/A/V: delivery, telemetry, security/recovery evidence | Unmet controls block only the relevant readiness claim |
| 8 Delivery/handoff | Scope criteria met or explicit partial boundary | O: artifacts, setup, results, limitations, next actions | Next session resumes from persisted state |

## Mission acceptance criteria and required proof

These are the ten criteria in `prompt.md` §13. Completion status must be assigned from the delivered implementation and actual evaluation, not from this design matrix.

| AC | Criterion | Design response | Proof required before acceptance |
| --- | --- | --- | --- |
| AC-01 | Capture essential intent and valuable knowledge | Source-section and fidelity-dimension mappings | Source review finds no material omission; skills preserve evidence, hidden semantics, iteration |
| AC-02 | Improve coverage without preserving repetition | Shared contract; freshness, gates, recovery, oracle governance | Central principles are referenced, not copied wholesale; additions solve listed gaps |
| AC-03 | Meaningful reusable responsibilities | Eight capability boundaries | Each skill has distinct activation and deliverables; sample tasks route selectively |
| AC-04 | Explicit routing, dependencies, shared state | Orchestrator, dependency handoff, persistent records | Routing/dependency/state checks and a resumable workflow succeed |
| AC-05 | Evidence-driven investigation and iterative implementation | I → S → X/D → V feedback loop | A realistic case creates evidence, a slice, an executed check, and a recorded discrepancy or result |
| AC-06 | Architecture/data/API/security/testing/deployment/operations coverage | S/D/A/V/P ownership and conditional references | All relevant dimensions are owned and represented in representative workflows |
| AC-07 | Measurable gates and evidence for claims | Result provenance, scope-bound status and validation | Unsupported verified claim is rejected; real results substantiate reported passes |
| AC-08 | Adapt to types/stacks/complexity | Product-specific routes and relevance assessment | UI, API, desktop/mobile or AI examples avoid one-size-fits-all infrastructure |
| AC-09 | Practical under resource/capability limits | Small shared state, selective loading, sequential mode | Missing-tool, unavailable-target, and context-resume evaluations retain useful progress |
| AC-10 | Maintainable, extensible, evaluated, reusable | Installation/extension docs, native folders, focused checks, scenario rubric | Clean install, link/contract checks, tests, and an actual independent behavioral evaluation |

The mission's broader claim—better engineering outcomes than a generic prompt—requires comparative trials across real projects. Passing the deliverable criteria or a few scenarios does not establish that general claim.
