# Using the library

## Installation and invocation

From the library root, run `python3 tools/install.py --dry-run`, inspect the destination, then
`python3 tools/install.py`. This installs local copies under `~/.agents/skills`. The installer
refuses all collisions before copying; it never updates existing skill folders silently.
For another environment, use `--dest` with its documented discovery path. The instructions
can be read directly from this workspace before installation.

All eight folders must remain siblings because shared references live under
`reconstruct-orchestrate`. The format is portable Markdown, while `agents/openai.yaml` is
optional Codex UI metadata. Another platform may need explicit registration or manual
reading of SKILL.md; do not assume cross-skill invocation APIs exist.

## New project

1. Identify the target, available materials, output repository, desired scope, constraints,
   and intended runtime. Put secrets in the environment's secret mechanism, not the prompt.
2. Invoke `$reconstruct-orchestrate`. It inspects the repository and available capabilities,
   reuses maintained records, and selects relevant specialists.
3. Agree scope through the task context. The state field `scope_accepted` records established
   scope; it does not require a new confirmation when your request already establishes it.
4. Define one meaningful slice and its scenarios. Implement and execute checks, then compare
   with the reference where evidence supports comparison. Repeat by priority.
5. Review a bounded report: implemented work, actual current results, assumptions, differences,
   blocked checks, and next actions. No global fidelity score is produced.

For a new machine-checked record, the parent project directory must already exist:

```bash
python3 ~/.agents/skills/reconstruct-orchestrate/scripts/project_state.py init ./reconstruction --target "My application" --version "reference-build-17"
python3 ~/.agents/skills/reconstruct-orchestrate/scripts/project_state.py validate ./reconstruction/state.json
python3 ~/.agents/skills/reconstruct-orchestrate/scripts/project_state.py report ./reconstruction/state.json
```

Read [state format](../skills/reconstruct-orchestrate/references/state-format.md) before editing.
The initial ledger is valid and incomplete. Add concrete records after investigation; there
are no prefilled successes. Before executing a scenario, capture its `fingerprint`; after
execution retain the actual output, hash it, and record the run. Run `gate` for finite scoped
readiness. A failed gate is expected while work remains incomplete.

## Resume and constrained environments

Ask: “Use `$reconstruct-orchestrate` to resume from `reconstruction/state.json` and its
checkpoint. Recheck current source/reference identities before reusing results.” The agent
loads the active slice and next action rather than replaying the entire original prompt.

Without Python, maintain the same evidence/requirement/decision/scenario/result links in
existing documents and review the gates manually. Without parallel workers, use the same
handoffs sequentially. Without browser/REA/network access, use supported local sources,
record the specific missing capability, and keep affected claims unverified. Do not make
a prototype appear more complete by omitting required outcomes from the denominator.

## Example workflows

| Request | Relevant path | Concrete verification | Expected limitation |
| --- | --- | --- | --- |
| Rebuild an authorized task web app | Investigate → specify → experience + services-data → verify; assure for ownership; operate for release | Create/edit/reload, cross-user denial, duplicate submission, browser states, selected recovery | Captured APIs do not enumerate private endpoints |
| Match a local CLI's observable behavior | Investigate source/execution → specify → services-data → verify | Output/error codes, new-process persistence, duplicate/conflict behavior, filesystem failures | No web/cloud stack needed; finite tested inputs only |
| Reconstruct a desktop import feature from a package | Investigate with relevant advertised REA route → specify → experience/services-data → verify | File parsing, IPC boundaries, restart, corrupted input, version differences | Static pseudocode does not prove runtime behavior |
| Specify an export feature from a screenshot description only | Investigate available evidence → specify | Review provenance, open questions, provisional contract and future test plan | UI label does not establish CSV schema or backend behavior |
| Rebuild a streaming AI client | Investigate visible protocol → specify → experience/services-data → assure → verify | Stream event ordering, cancellation, tool boundaries, bounded repeated quality trials | Hidden prompt/model internals remain unknown |
| Prepare an existing reconstruction for deployment | Specify relevant release criteria → assure/operate → verify | Clean build, migration/restore drill, health/readiness, telemetry and rollback | Prepared deployment is not a deployed service |

These are routing examples, not demonstrations already performed. Executed examples and
their evidence are identified separately in the [validation report](validation-report.md).

## Updating and removing

The workspace is the authored source; installed folders are copies. Validate edits here
first. For an update, stop active work using the installed library, back up only its eight
`reconstruct-*` folders outside the discovery directory, compare local modifications, then
move those named folders out of discovery and run the installer again. Keep the backup
until the new version is validated. There is deliberately no destructive `--force` option.

To remove, move only those eight named folders out of the discovery directory. Do not
delete unrelated skills or the existing `reverse-engineer-anything` skill. Keep project
reconstruction records; removing a skill does not invalidate their historical evidence.
No configuration edits are needed for a normal install/removal.
