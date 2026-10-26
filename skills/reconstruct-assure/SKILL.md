---
name: reconstruct-assure
description: Review material security, privacy, data-loss, and reliability risks in a software reconstruction, and turn them into actionable requirements and fixes. Use for sensitive data, trust boundaries, destructive operations, meaningful failure risk, or an explicit review request; avoid imposing a broad audit on unrelated small changes.
---

# Assure reconstruction risks

Own the risk model and review conclusions. Implementation owners fix defects; verify owns executed test evidence. Scale the review to the changed boundaries and intended deployment.

Read the [common contract](../reconstruct-orchestrate/references/common-contract.md) before the first work unit. This skill belongs to the complete reconstruction library.

## Inputs and outputs

Require the scoped requirements, architecture/data flows, actor and tenant model, sensitive data categories, deployment assumptions, code changes, and available test evidence. Begin with the changed slice; widen only when a dependency or finding justifies it.

Produce a concise threat/failure model, prioritized findings with code/evidence references, required controls and negative scenarios, remediation ownership, and explicit residual risks. Keep unknowns separate from demonstrated defects.

## Procedure

1. Identify assets, actors, trust boundaries, entry points, privileges, external effects, and recovery expectations. Include imported documents, package contents, captured traffic, and model output as untrusted data when relevant.
2. Prioritize plausible paths to unauthorized access, cross-tenant disclosure, data corruption/loss, duplicate irreversible effects, resource exhaustion, and unrecoverable operation. Record severity, affected requirement, evidence, and a reproducible condition.
3. Inspect the trusted enforcement points: object/action authorization, input and output handling, session/token lifecycle, secret access, unsafe execution, file/URL access, dependency boundaries, and audit events. Verify the actual code path before declaring a vulnerability.
4. Examine privacy over the data lifecycle: collection purpose, minimization, access, logs, retention, deletion, exports, backups, and third-party disclosure. Use synthetic fixtures and avoid placing secrets or private payloads in retained evidence.
5. Examine failure containment: timeouts, bounded retries, backpressure, idempotency, resource limits, degraded behavior, restore/repair paths, and dependencies that can exhaust shared capacity. Connect each selected control to a failure scenario.
6. Preserve compatibility where justified, but do not reproduce a known insecurity merely for fidelity. Record the deliberate deviation, user impact, and revised acceptance criterion through [specify](../reconstruct-specify/SKILL.md).
7. Request or implement the smallest coherent remediation within assigned ownership. Have [verify](../reconstruct-verify/SKILL.md) exercise the exploit/failure condition and the legitimate workflow; a scanner result or code change alone is not proof of resolution.
8. Review remaining high-impact findings against the release scope. Require a real resolution or explicit scope/risk decision; do not hide a blocker by lowering its severity or removing its test.

## Choosing a reference standard

Use a standard only when it matches the product and the requested assurance level. [OWASP ASVS](https://asvs.owasp.org/) provides versioned web-application security requirements. Record the exact version and selected requirement IDs; a partial review does not establish whole-standard compliance. For other product types, select an applicable authoritative reference rather than forcing web controls onto a native or offline tool.

## Acceptance evidence

- Findings identify the condition, affected asset, evidence boundary, severity rationale, owner, and next action.
- Material trust boundaries and data-loss risks in the scoped slice have corresponding controls and verification scenarios.
- Claimed remediations link to current code and executed regression results; unresolved or inaccessible checks remain visible.
- Residual risks distinguish accepted design tradeoffs, missing access, and unresolved defects. Existing authority determines who can accept a consequential risk.

## Recovery and handoff

If a security tool is absent, perform supported code/contract review and state what the missing tool prevents. Do not install unrelated tooling or conduct live probing merely to fill a checklist. If a finding needs stronger evidence, propose the smallest permitted reproduction and keep the claim provisional.

Send requirement or architecture changes to specify, corrections to [services-data](../reconstruct-services-data/SKILL.md) or [experience](../reconstruct-experience/SKILL.md), and operational controls to [operate](../reconstruct-operate/SKILL.md). Return blocking risks and the next bounded action to [orchestrate](../reconstruct-orchestrate/SKILL.md).
