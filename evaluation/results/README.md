# Retained evaluation evidence

- [validation-commands.json](validation-commands.json): actual unit-test and library-check output.
- [skill-format-validation.json](skill-format-validation.json): eight skill-creator validation results.
- [helper-review.md](helper-review.md): independent findings and tested fixes.
- [installation.json](installation.json): installed file identities and observed host discovery.
- [cli/replacement/evaluation-result.md](cli/replacement/evaluation-result.md): completed independent
  CLI reconstruction; source, replacement, runner, fixtures and raw outputs are retained.
- [cli-parent-review.json](cli-parent-review.json): integration review of source/replacement digests
  and the copied ledger's current finite gate.
- [missing-access/evaluation-result.md](missing-access/evaluation-result.md): sequential integration
  evaluation of an analysis-only request with no reference runtime access.

Paths and commands inside historical logs identify the original evaluation workspaces. They
are preserved as provenance, even when a temporary directory no longer exists. Retained copies
are the durable evidence. The CLI runner resolves reference/replacement files relative to its
directory; its helper path points to this workspace and may need updating after relocation.
Run a copy in an isolated workspace to reproduce the trial without modifying the archived
state. The same applies to any new missing-access evaluation.

Synthetic unit-test records establish helper predicates, not real product behavior. Planned
scenarios are catalogued in [scenarios.md](../scenarios.md); unexecuted scenarios must not be
counted as passing evaluations. See [the validation report](../../docs/validation-report.md)
for the exact completed scope and limitations.
