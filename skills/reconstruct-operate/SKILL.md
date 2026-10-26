---
name: reconstruct-operate
description: Make a reconstructed application reproducible and operable through configuration, delivery, telemetry, recovery, and deployment evidence. Use when deployment or operational readiness is in scope; skip local prototypes and source-only analyses that do not need those capabilities.
---

# Operate the replacement

Design operations for the replacement's actual requirements. Do not claim that chosen infrastructure or telemetry reproduces inaccessible internals of the original.

Read the [common contract](../reconstruct-orchestrate/references/common-contract.md) before the first work unit. This skill belongs to the complete reconstruction library.

## Inputs and outputs

Require deployment scope and authority, current implementation/revision, accepted architecture, external dependencies, data/migration requirements, verification results, and service/recovery targets. Use existing deployment conventions before introducing a platform.

Produce reproducible build/run configuration, release and recovery procedures, appropriate automated delivery checks, telemetry definitions, executed drill evidence, and known operational limits. Separate prepared artifacts, tested deployment, and actual production deployment in the handoff.

## Procedure

1. Identify the operating environment, operator, expected workload, availability requirements, cost envelope, and permitted destinations. For a local application, this may be packaging, upgrades, diagnostics, and backup; cloud hosting is not presumed.
2. Make dependencies, build inputs, runtime versions, configuration, and required secrets explicit. Use lockfiles/artifact identities and appropriate secret injection. Test setup from a clean environment when feasible; document unavailable dependencies.
3. Select delivery topology from the agreed behavior, capacity, and team constraints. Add containers, infrastructure code, orchestration, or managed services only when their value is concrete. Review least privilege, network exposure, TLS, storage durability, and supply-chain controls appropriate to the deployment.
4. Define the release sequence: build, tests, artifact identity, migration compatibility, deploy, health/readiness, smoke checks, observation window, and rollback/forward repair. Distinguish a process being alive from its ability to serve safely. Do not run destructive migrations before a usable recovery path exists.
5. Define operational signals from critical journeys and failure modes: structured events, request/operation correlation, latency/error/throughput metrics, queue depth or age, dependency health, and traces where they help diagnosis. Bound label cardinality, sample volume, retention, sensitive data, and telemetry cost.
6. Translate service targets into measurable indicators and windows. Define alert conditions, owner, actionable runbook, and recovery check; do not choose an impressive SLO with no measurement or response plan. Include capacity/cost thresholds when workload growth matters.
7. Exercise selected failure/recovery drills in a controlled authorized environment: restart, failed dependency, exhausted capacity, migration failure, rollback, backup restore, or data deletion as applicable. Verify restored data and behavior, not merely a successful backup command.
8. Prepare a concrete release plan and complete reversible local validation. Execute external deployment only within existing user authorization and host permissions; otherwise request the missing approval for that concrete action. Preserve already-given authorization rather than adding a new ceremony.
9. After any authorized deployment, record destination, artifact/revision, time, command/service result, smoke tests, and recovery status. If deployment was only prepared, say so explicitly.

## Telemetry reference

[OpenTelemetry signals](https://opentelemetry.io/docs/concepts/signals/) distinguish logs, metrics, and traces that can reveal different aspects of runtime behavior. Use compatible instrumentation when it meets the project need; the skill does not require a particular backend or collector.

## Acceptance evidence

- A new operator can build/run or deploy using recorded inputs and configuration without undocumented secrets or manual state.
- Delivery checks exercise the intended environment and state their boundary; a local build is not a successful deployment.
- Selected failure conditions produce usable diagnostics and reach their documented recovery outcome.
- Backup/restore, migration repair, and rollback claims cite executed drills; untested procedures remain unverified.
- Data retention, redaction, dependency maintenance, incident ownership, and resource/cost limits are specified where relevant.

## Recovery and handoff

When cloud or production access is unavailable, finish locally testable configuration, runbooks, and deployment artifacts. Record the exact blocked external checks and next action. After ambiguous deployment or migration outcomes, inspect actual state before retrying. If a drill fails, retain its evidence, recover within the authorized boundary, and block the corresponding readiness claim.

Send architecture changes to [specify](../reconstruct-specify/SKILL.md), operational risks to [assure](../reconstruct-assure/SKILL.md), and run/drill evidence to [verify](../reconstruct-verify/SKILL.md). Return the release recommendation, remaining limits, and next bounded action to [orchestrate](../reconstruct-orchestrate/SKILL.md).
