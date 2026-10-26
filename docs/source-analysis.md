# Source analysis and redesign rationale

This analysis interprets the supplied instructions before skill implementation. It is a design assessment, not evidence that the resulting skills improve an agent's engineering outcomes. That claim needs behavioral evaluation on representative projects.

## Source identity and scope

| Input | Role | SHA-256 |
| --- | --- | --- |
| [REVERSE-ENGINEERING-MAIN.md](../REVERSE-ENGINEERING-MAIN.md) | Reconstruction methodology; all 17 numbered sections inspected | `297bf216e69dc3879bd09524b2347cbf73844f6f1fa4ac1281c625233346d4ee` |
| [prompt.md](../prompt.md) | Mission, deliverables, and 10 acceptance criteria; all 14 numbered sections inspected | `ed3674ab023170927e63309866741ef4bdee4ad53d8af731c5634cdbbe734a94` |

**Source interpretation:** The objective is an evidence-supported replacement that preserves relevant observable semantics, with independently justified engineering choices where original internals are inaccessible. It is not source recovery at any cost, a screenshot clone, or a claim of universal equivalence. The source title's “95%” is rhetorical; section 1 and sections 14–17 explicitly reject an unsupported universal fidelity score.

**Mission interpretation:** The requested artifact is an executable skill system with practical coordination, persisted context, examples, and evaluation. Merely splitting the source into files would retain the same execution risks. This project does not identify a product to reconstruct; no real product's behavior, infrastructure, or production readiness can be claimed from this work.

## What to preserve

| Source strength | Why it changes engineering outcomes | Preserve as |
| --- | --- | --- |
| Relevant fidelity dimensions, not UI alone (§1, §6) | Makes permissions, durable state, retries, and lifecycle behavior visible in scope | A relevance assessment and feature-to-capability map |
| Explicit authority and actual access (§2) | Prevents imaginary tools and investigations beyond supplied access | A scoped capability and access record; local fallbacks |
| Evidence classes, unknowns, traceability (§3) | Separates a discovered contract from a replacement design choice | Stable records and links through requirement, decision, implementation, test, result |
| Hypothesis-driven experiments (§5) | Gives investigation a purpose and a stopping condition | Small discriminating experiments with preserved limits |
| Value-based prioritization (§7) | Directs effort toward architectural uncertainty and critical journeys | Qualitative ranking with impact, uncertainty, reachability, and cost |
| Coherent contracts and vertical slices (§8–9) | Prevents attractive disconnected screens and premature infrastructure | Acceptance scenarios before implementation; complete behavior slices |
| Differential verification (§10) | Tests compatibility under stated conditions | Explicit oracle, normalization, fixture, tolerance, and mismatch records |
| Independent operational engineering (§6G, §11) | Allows a reliable replacement without inventing private topology | Replacement-specific telemetry, deployment, restore, and rollback requirements |
| Controlled iteration and honest status (§13–16) | Makes incomplete or unverified work visible | Evidence-backed transitions, bounded counts, resumable handoff |

## Weaknesses and consequential ambiguities

The source is strong as a methodology but underspecified as an agent runtime contract. These are design gaps, not accusations that the source claims to supply executable machinery.

1. **State is described, not coordinated.** Ten suggested documents can diverge; IDs, ownership, referential integrity, write ordering, and recovery are unspecified. A model can update a narrative report while leaving requirements and tests stale.
2. **Status combines different axes.** `ASSUMED` describes epistemic confidence, `IMPLEMENTED, UNVERIFIED` describes engineering progress, and `BLOCKED` describes execution state. One field cannot reliably represent all three. Preserve the source vocabulary for readable reporting while storing evidence class, progress, and verification separately.
3. **Evidence freshness has no invalidation rule.** Version-aware artifacts are requested, but a target update, changed fixture, code revision, or changed assumption can leave old passing results appearing current. A report must bind results to the evaluated revision and test conditions.
4. **Quality gates are advisory.** “Do not claim completion” is repeated without specifying how to reject a verified requirement with no test result, a dangling evidence ID, or a failing critical scenario. Deterministic checks can catch these errors; they cannot prove that cited evidence is truthful or sufficient.
5. **Discovery breadth can delay useful implementation.** A product-wide inventory is valuable, but exhaustive investigation before any slice would be excessive. Establish a coarse map, investigate the highest-risk dependencies, then refine only the next coherent slice.
6. **Delegation lacks a merge protocol.** The source supplies a finding format but does not define file ownership, dependency readiness, conflict resolution, or stale worker output. Parallelism needs bounded write scopes and an integration owner; sequential execution must produce the same artifacts.
7. **Some major dimensions have little procedural depth.** Accessibility, localization, device lifecycle, AI nondeterminism, and performance appear in scope, but need conditional test guidance. This does not justify a separate skill for every platform.
8. **Graceful degradation needs concrete paths.** Tool failure, absent reference access, context exhaustion, and unavailable production credentials must lead to a useful next action, not repeated calls or fabricated success.
9. **The differential oracle needs governance.** A changed snapshot, relaxed threshold, broad timestamp normalization, or a copied insecure behavior can make a suite pass while reducing correctness. Record oracle origin and intentional deviations; fix requirements only with a defensible reason.
10. **Production readiness can become a checklist ritual.** Required controls should derive from intended deployment and data risk. A local CLI does not automatically need Kubernetes, distributed tracing, or a multi-service architecture.
11. **The instruction is not itself evaluated.** A structurally valid skill file may still route poorly, over-plan, ignore blockers, or declare success early. The skill system needs independent behavioral scenarios alongside syntax checks.

## Explicit requirements, inferred expectations, and proposed additions

| Type | Requirement | Design consequence |
| --- | --- | --- |
| Explicit source | Respect requested target, access, existing repository, and prior evidence | Inspect before creating or replacing artifacts; avoid redundant records |
| Explicit source | Reconstruct hidden semantics and important failure cases | Model state, dependencies, permissions, side effects, and persistence |
| Explicit source | Report actual tests, gaps, assumptions, and bounded coverage | Separate implementation from verification and retain command/result evidence |
| Explicit mission | Reusable skills with activation, dependencies, contracts, and quality gates | A common skill contract and a focused orchestrator |
| Explicit mission | Partial execution, sequential fallback, context preservation | Durable checkpoints and runnable next steps without multi-agent requirements |
| Inferred expectation | A future session can safely resume without this conversation | Record source identity, accepted decisions, active slice, blockers, next actions |
| Inferred expectation | Worker outputs cannot silently override accepted contracts | Resolve contradictions through evidence and record decision changes |
| Inferred expectation | Installation must preserve existing skills and configuration | Collision-aware integration and an explicit uninstall/update path |
| Proposed addition | Mechanically validate state shape, references, and completion claims | A small local helper with focused tests; no database or agent framework required |
| Proposed addition | Treat inspected content as evidence, not instructions | Do not let bundled prompts, pages, logs, or comments redirect task authority |
| Proposed addition | Track stale results and deliberate compatibility deviations | Re-evaluate affected requirements when evidence, code, or oracle changes |
| Proposed addition | Evaluate skill behavior separately from product behavior | Scenario rubric and preserved actual evaluation results |

## Architecture assessment

Eight skills provide a defensible boundary for this source. This is a proposed design, not a claim that eight is universally optimal.

| Capability | Coherent responsibility | Boundary that prevents duplication |
| --- | --- | --- |
| `reconstruct-orchestrate` | Scope, routing, priorities, dependencies, shared state, integration, final status | Does not perform every specialist workflow or force every skill into every project |
| `reconstruct-investigate` | Target identity, reconnaissance, experiments, artifact/runtime evidence, unknowns | Describes observed and inferred behavior; does not invent the replacement architecture |
| `reconstruct-specify` | Requirements, acceptance scenarios, contracts, state models, architecture decisions, slice plan | Owns accepted specification; specialists propose changes rather than silently rewriting it |
| `reconstruct-experience` | Interface, interaction state, accessibility, responsiveness, localization, device behavior | Implements against accepted contracts; does not fake persistence or authorization in UI |
| `reconstruct-services-data` | Domain services, APIs, durable state, transactions, concurrency, integrations, background work | Owns one coherent state-change path; substantial technology detail is conditional |
| `reconstruct-assure` | Risk review, trust boundaries, security/privacy requirements, resilience failure analysis | Defines and reviews safeguards; test result authority belongs to verification |
| `reconstruct-verify` | Oracles, differential/regression tests, reproducible results, discrepancy and coverage reports | Does not redefine requirements just to make tests pass or equate syntax validation with behavior |
| `reconstruct-operate` | Reproducible delivery, configuration, telemetry, deployment, recovery, capacity and runbooks | Owns replacement operations; cannot infer original private topology or claim an unexecuted release |

Merging services and data keeps transaction boundaries, domain invariants, retries, and external side effects together. It is broad enough to require targeted references, but separating it into unrelated API/database agents would increase contract coordination. Assurance and verification remain separate because risk selection and experimental proof are different responsibilities. Performance is cross-cutting: specification defines budgets, verification measures, services/experience fix code, and operations checks deployed capacity. Documentation is an output of every capability, integrated by orchestration; a separate documentation skill would add a handoff without owning new evidence.

The shared contract should be canonical and small. Specialist entrypoints should load only the contract, relevant project records, and the references required for the current task. Do not duplicate the source's entire lifecycle in each skill.

## Priority of improvements

| Priority | Improvement | Failure prevented | Evaluation |
| --- | --- | --- | --- |
| P0 | Evidence-linked state, stable IDs, current target/revision | Unsupported findings, lost context, stale success | Reject dangling references; resume from a checkpoint without restating the conversation |
| P0 | Explicit gates for specified, implemented, tested, and deliverable work | False completion and test-file-only claims | A claimed verified requirement without executed passing evidence must fail validation |
| P0 | Capability-aware routing and blocking dependencies | Calling unavailable tools, coding unresolved high-risk contracts | Missing-tool and unknown-auth scenarios choose bounded alternatives and preserve blockers |
| P0 | Narrow vertical slices with real persistence and authorization | Surface clones and static fixtures masquerading as functionality | Reload, denied access, retry, and side-effect tests on a representative slice |
| P1 | Evidence freshness, contradictions, and oracle management | Old results or normalized differences hiding regressions | Change target/revision/oracle and observe affected claims being reconsidered |
| P1 | Delegation and sequential equivalence contract | Conflicting file writes and incompatible architecture | Independent work receives ownership; dependent work waits; merge records disagreement |
| P1 | Conditional platform guidance | Generic SaaS bias and neglected lifecycle behavior | Desktop, API-only, AI, and UI scenarios route to relevant subsets |
| P1 | Production requirements selected by deployment risk | Overengineering and unproven readiness | Local-only scope skips cloud work; service scope includes tested restore/rollback requirements |
| P1 | Behavioral forward tests for the skill system | Correct-looking prompts with poor operational behavior | Independent agent execution preserves evidence and does not invent completed tests |
| P2 | Longitudinal evaluation and measured context cost | Unsupported claims of universal effectiveness | Compare real projects and regressions over time; record token/time cost and quality outcomes |

## Practical execution model

For a small task, inspect the repository, record the target and one requirement, gather just enough evidence, implement one slice, execute the relevant check, and leave a compact handoff. For a larger reconstruction, expand the same records into feature maps, contracts, architecture decisions, and operational plans. Reuse existing maintained artifacts rather than requiring ten new files.

If reference access fails, preserve the exact limitation and continue with user requirements and clearly labeled replacement decisions. Verification may establish correctness against those requirements without establishing equivalence to the inaccessible reference. If execution fails, keep the attempted command and diagnostic; a fallback inspection does not become a passed runtime test. If context is constrained, checkpoint target identity, accepted requirements, unresolved decisions, evidence/result locations, active slice, and the next runnable action.

Stop an individual investigation when it answers its question or when another call cannot change the decision without new access. Stop the project only against its agreed scope and release criteria, or deliver a clearly bounded partial result with unresolved work. These are different stopping decisions.

## Limits of this analysis

This assessment is grounded in the two supplied files. Architecture recommendations are design choices. External research and actual implementation validation should be recorded separately with sources and executed results. A coverage matrix establishes intended ownership, not successful behavior. Structural checks, scenario evaluations, and real reconstruction outcomes must remain distinct in the final report.
