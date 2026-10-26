---
name: reconstruct-services-data
description: Implement reconstruction contracts across domain logic, APIs, persistence, asynchronous work, and integrations. Use when a replacement must preserve business invariants, durable state, or observable protocol behavior; skip UI-only work and investigations that do not request implementation.
---

# Reconstruct services and data

Build a complete domain operation across its real service and persistence boundaries. The replacement's physical design is an engineering choice unless inspected artifacts establish the original design.

Read the [common contract](../reconstruct-orchestrate/references/common-contract.md) before the first work unit. This skill belongs to the complete reconstruction library.

## Inputs and outputs

Require a repository baseline, requirement/scenario IDs, interface and state contracts, ownership/authorization rules, invariants, side effects, accepted design decisions, and relevant evidence from [specify](../reconstruct-specify/SKILL.md). Resolve a missing high-impact invariant before committing to a schema or irreversible side effect.

Produce working service/data changes, schema and migration changes where needed, contract fixtures, executed checks, and a concise record of operational dependencies. Return changed API/state contracts to specify and [experience](../reconstruct-experience/SKILL.md).

## Procedure

1. Trace the selected operation through entry point, actor, authorization, validation, state read, mutation, side effects, and response. Identify the single owner of each invariant and durable record.
2. Reuse existing code and storage architecture where suitable. Choose the smallest design that meets consistency, durability, query, and deployment requirements; do not add queues, caches, or services without a concrete need.
3. Define method/path or message contract, input normalization, error categories, status codes, pagination/sort behavior, and compatibility policy. Treat captured endpoint coverage as finite. Version synthetic contracts separately from observed ones.
4. Enforce identity, object ownership, tenant boundaries, and business authorization at the trusted boundary. Verify denied requests cause no protected side effects. Client visibility is not an authorization check.
5. Implement durable state with appropriate constraints and transaction boundaries. Cover uniqueness, relations, decimal/rounding rules, time handling, deletion, retention, and history when relevant. Specify how derived indexes and caches recover from missed updates.
6. For migrations, test a representative existing schema/data fixture and a fresh database. Define rollback or forward repair and backup requirements according to risk; an irreversible migration needs an explicit recovery plan before execution.
7. Model external effects and asynchronous transitions explicitly. Specify retry limits, timeout ownership, idempotency scope/expiry, ordering, cancellation, and duplicate handling. Use the relevant section of [conditional workflows](references/conditional-workflows.md) for jobs, collaboration, AI, mobile, or desktop behavior.
8. Implement the complete slice and exercise it with synthetic data. Check output and post-operation state; include reload/restart, invalid input, denied access, duplicate operations, and failure paths selected by risk.
9. Compare to the scoped reference contract. If an observation contradicts a design assumption, register the discrepancy and route it through specify before spreading the assumption into other slices.

## Acceptance evidence

- The operation satisfies its input/output contract and state invariants, including relevant failure cases.
- Required persistence survives a new connection or process as appropriate; in-memory fixtures are not described as durable storage.
- Authorization is enforced for the resource and action, including cross-user/tenant cases where applicable.
- Tests use the actual persistence/integration boundary when making claims about that boundary. Stub-only results remain explicitly scoped.
- Side effects cannot silently duplicate or disappear within the promised recovery model; concurrency tests exercise the claimed ordering or conflict rule.
- Schema changes have recorded compatibility and recovery evidence proportional to their risk.

## Recovery and handoff

When a dependency is unavailable, use a contract adapter or test double only for work that it can validate. Record which production capability is incomplete; never mark a simulated payment, job, notification, or model call as a functioning integration. On ambiguous duplicate outcomes, reconcile using an operation identifier before retrying an external effect.

Escalate incompatible contracts, data-loss risks, and unresolved ownership to [orchestrate](../reconstruct-orchestrate/SKILL.md). Send threat/reliability questions to [assure](../reconstruct-assure/SKILL.md), executed results to [verify](../reconstruct-verify/SKILL.md), and configuration, migrations, job controls, and recovery requirements to [operate](../reconstruct-operate/SKILL.md).
