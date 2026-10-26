# Maintaining and extending the library

Change a skill when a demonstrated task or failure needs different behavior. Avoid adding
a new skill merely for a framework or tool. Preserve the original input files as provenance;
edit the library and its rationale rather than silently rewriting source intent.

1. Identify the owning capability and expected user outcome. Prefer a conditional reference
   under that owner when the workflow is specialized but has the same inputs/outputs.
2. Change the smallest relevant instruction. Shared evidence, status, and handoff invariants
   belong in the coordinator's common contract, not copied into every entrypoint.
3. Keep the SKILL.md trigger discriminating. Add required inputs, output shape, acceptance,
   recovery, and handoff implications for a genuinely new workflow.
4. Update the skill map, routing table, coverage mapping, usage examples, and evaluation
   scenario when the boundary changes. Installation dependencies must remain acyclic;
   workflow feedback loops are allowed.
5. If state semantics change, increment schema version, specify migration behavior, and
   test old-state rejection or migration. Do not reinterpret stored PASS records silently.
6. Validate frontmatter with the available skill-creator validator; run the library checker
   and helper tests. Use an isolated independent scenario when the behavior change warrants
   it. Keep actual outputs, failures, corrections, and the tested source identities.
7. Update the validation report with precisely what ran and what remains untested. Install
   only after comparing existing installed copies and preserving user edits.

## Validation commands

```bash
python3 tools/validate_library.py
python3 -m unittest discover -s tests -v
```

When skill-creator is available, also run its `scripts/quick_validate.py <skill-folder>` for
each skill. That external validator is a development check, not a runtime dependency of
the library. UI metadata can be regenerated with its generator for new files; preserve
existing policy/dependency fields when editing an already customized file.

## Evaluation discipline

Use [scenarios and rubric](../evaluation/scenarios.md) to evaluate routing, dependencies,
evidence, context recovery, and truthful completion. Supply evaluators with realistic user
requests and minimum raw artifacts, not the intended answer. Keep evaluation writes isolated
from authored skills. Review actual artifacts, revise only supported defects, and rerun
affected tests. A scenario dry-run is not equivalent to executing a reconstructed product.

Longer-term evaluation should compare several real reconstructions with a generic-prompt
baseline under equivalent model/tool/budget conditions. Track critical journey completion,
escaped defects, false verification claims, data/security failures, time/context cost, and
handoff quality. This release does not establish statistically reliable superiority.
