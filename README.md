# Reconstruction Skills

An eight-skill library for investigating an identified software product, specifying its
behavior, building coherent replacement features, and checking bounded compatibility claims.
It turns the supplied [mission](prompt.md) and [reconstruction protocol](REVERSE-ENGINEERING-MAIN.md)
into reusable agent procedures with shared state, tested helpers, and explicit limitations.

## Start here

Use the coordinator for a new or resumed reconstruction:

```text
Use $reconstruct-orchestrate to reconstruct [identified target/version] in [repository].
Reference materials: [paths or authorized URLs]. Prioritize [workflows].
Constraints: [runtime, access, intended deployment, and exclusions].
```

For analysis only, say so. For a narrow change, invoke the relevant specialist directly;
it reads the same shared contract without requiring every phase.

## Install

Requires Python 3.10+ for optional local helpers. The instructions can also be followed
manually. From this directory:

```bash
python3 tools/validate_library.py
python3 -m unittest discover -s tests -v
python3 tools/install.py --dry-run
python3 tools/install.py
```

The installer copies all eight sibling folders to `~/.agents/skills`, refuses existing
names, and leaves other skills and configuration alone. Use `--dest /chosen/skills` for
another host's actual discovery directory. Install the entire library: specialists refer
to the coordinator's shared resources. No MCP server, REA engine, Python package, account,
or credential is installed. Instructions and tool capabilities are separate.

Current Codex guidance lists `~/.agents/skills` for user skills and `.agents/skills` for
repository skills. If a new skill does not appear, restart Codex. Other hosts need their
own discovery integration. [Official skill documentation](https://learn.chatgpt.com/docs/build-skills)

See [usage](docs/usage.md) for updates, removal, manual operation, and project examples.
The actual local installation and validation status is recorded in [validation report](docs/validation-report.md).

## Skills

| Skill | Responsibility | Typical trigger |
| --- | --- | --- |
| [reconstruct-orchestrate](skills/reconstruct-orchestrate/SKILL.md) | Scope, routing, dependencies, shared state, integration | New or resumed multi-step reconstruction |
| [reconstruct-investigate](skills/reconstruct-investigate/SKILL.md) | Evidence, experiments, feature discovery, unknowns | Unsettled reference behavior |
| [reconstruct-specify](skills/reconstruct-specify/SKILL.md) | Behavior contracts, architecture, acceptance, slice plan | Evidence needs an implementable contract |
| [reconstruct-experience](skills/reconstruct-experience/SKILL.md) | UI, interaction state, accessibility, responsive/device behavior | A user journey needs implementation |
| [reconstruct-services-data](skills/reconstruct-services-data/SKILL.md) | Domain, APIs, persistence, concurrency, jobs, integrations | A complete operation crosses service/state boundaries |
| [reconstruct-assure](skills/reconstruct-assure/SKILL.md) | Consequential security, privacy, reliability review | Trust boundaries or material failure risks |
| [reconstruct-verify](skills/reconstruct-verify/SKILL.md) | Executed checks, comparison, discrepancies, bounded reports | A slice or claim needs verification |
| [reconstruct-operate](skills/reconstruct-operate/SKILL.md) | Builds, deployment, telemetry, recovery, capacity | Delivery or operational behavior is in scope |

## What makes the system executable

- A [routing contract](skills/reconstruct-orchestrate/references/routing.md) selects relevant
  workstreams and requires the artifacts needed by the next task. One agent can execute
  the entire sequence; multi-agent execution is optional.
- A [shared contract](skills/reconstruct-orchestrate/references/common-contract.md) distinguishes
  observations, documentation, inferences, and replacement choices. Evidence, implementation,
  and verification are separate records.
- A [state helper](skills/reconstruct-orchestrate/scripts/project_state.py) checks references,
  current scenario results, target/replacement identities, contract fingerprints, and retained
  result hashes. It refuses a green gate for an empty or incomplete required scope.
- Compact [templates](skills/reconstruct-orchestrate/references/templates.md) preserve
  requirements, worker handoffs, decisions, discrepancies, and resumable checkpoints.

## Documentation and evaluation

- [বাংলা dry-run গল্প: skills ও REA দিয়ে একটি পণ্য নির্মাণ](docs/dry-run-story-bn.md)
- [Source analysis](docs/source-analysis.md) and [coverage matrix](docs/coverage-matrix.md)
- [Architecture and design decisions](docs/architecture.md)
- [Research and rationale](docs/research.md)
- [Usage and example workflows](docs/usage.md)
- [Extension and maintenance](docs/maintenance.md)
- [Evaluation scenarios and rubric](evaluation/scenarios.md)
- [Executed validation and acceptance status](docs/validation-report.md)

The helper validates recorded evidence, not its truthfulness or completeness. Passing a
finite suite does not establish global equivalence or production readiness. Broader,
comparative evaluations are needed to measure whether this library consistently improves
outcomes over a generic prompt.
