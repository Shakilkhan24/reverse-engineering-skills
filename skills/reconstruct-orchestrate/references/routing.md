# Routing and dependencies

Start with the requested outcome and actual uncertainty, not a technology keyword. These
are artifact dependencies, not mandatory full-project phase completions. Always allow
verification to send a bounded question back to investigation or specification.

| Skill | Invoke when | Required input | Output consumed next | Skip when |
| --- | --- | --- | --- | --- |
| [investigate](../../reconstruct-investigate/SKILL.md) | A relevant reference behavior is unknown, conflicting, or stale | Explicit target, question, access boundary | Evidence, feature/dependency inventory, bounded unknowns → specify | Existing evidence answers the scoped question |
| [specify](../../reconstruct-specify/SKILL.md) | Evidence needs a testable contract or a changed requirement needs architecture | User outcome, evidence/unknowns, repository constraints | Requirements, scenarios, decisions, slice dependencies → implement/verify | A current contract already governs the small change |
| [experience](../../reconstruct-experience/SKILL.md) | A UI or device journey needs implementation | State/interaction contract, assets, supported environments | Working experience, scenario traces → verify | Headless product or no experience change |
| [services-data](../../reconstruct-services-data/SKILL.md) | Domain, API, persistence, jobs, or integration behavior must change | Contract, ownership/invariants, failure cases | Complete service/data slice, migrations/tests → verify | Presentation-only behavior without these dependencies |
| [assure](../../reconstruct-assure/SKILL.md) | Trust boundaries, sensitive data, irreversible effects, resilience risks, or an explicit audit require review | Risk scope, flows, contracts, implementation where present | Threats, risk requirements, findings → specify/implementation/verify | An ordinary low-risk edit with no relevant risk change |
| [verify](../../reconstruct-verify/SKILL.md) | A slice or claim needs empirical acceptance, differential checks, or regression triage | Defined scenarios, runnable replacement, reference evidence if comparing | Runs, differences, bounded status → orchestrate/investigate | Research-only work without implementation claims; still review evidence |
| [operate](../../reconstruct-operate/SKILL.md) | Deployment, packaging, telemetry, recovery, capacity, or handoff is in scope | Deployment destination, build/config contract, risk requirements | Reproducible release/runbooks/recovery evidence → verify/delivery | No change to delivery/operational behavior; retain existing run instructions |

## Profiles

- **Minimal:** one narrow workflow or constrained environment. Keep scope, evidence links,
  acceptance scenarios, and checkpoint in one small record. Investigate only decision-changing
  unknowns; specify the slice; invoke applicable implementation skill; run focused checks.
  Lack of tools reduces verified scope, not the honesty standard.
- **Standard:** several features or persistent service. Maintain explicit API/state contracts,
  dependency order, negative cases, and regression coverage. Add assure for actual security
  boundaries and operate for the intended release. Compare each completed slice.
- **High assurance:** high-consequence state, multi-tenant isolation, irreversible external
  actions, or demanding release criteria. Add early risk review, independent verification,
  concurrency/failure experiments, restore/rollback exercises, and measured operational
  criteria. Do not label this formal certification.

## Sequencing rules

1. Before collection, identify the exact target. Before implementation, define the relevant
   expected result. Before a completion claim, execute its checks.
2. Architecture/security uncertainties that can invalidate dependent work come first.
   UI and service code may proceed in parallel after their shared contract is settled.
3. Assure can run before design and again after changed trust boundaries. Operate can set
   release constraints early; deployment exercises require a runnable candidate.
4. Do not wait for a full product inventory to implement one well-understood high-value slice.
   Do not let that slice erase unknown workflows from the inventory.
5. Route a mismatch according to cause: absent evidence → investigate; ambiguous contract →
   specify; defect → owning implementation skill; bad fixture/environment → verify/operate.
6. Analysis-only requests end with findings and limitations. A public screenshot supports
   visible observations; it cannot unlock hidden service claims. A UI-only request remains
   UI-only even if this library can build backend systems.

The machine-readable [skill map](skill-map.json) inventories the same boundaries. It is
metadata for validation and planning, not executable cross-skill invocation.
