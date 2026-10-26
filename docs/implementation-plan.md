# Implementation record

## Scope
Build and install a reusable skill library from `prompt.md` and `REVERSE-ENGINEERING-MAIN.md`. This project builds the engineering workflow; it does not reconstruct an unidentified third-party application.

## Decisions (2026-10-25)
- Eight skills: orchestrate, investigate, specify, experience, services-data, assure, verify, operate. Names use the `reconstruct-` prefix to avoid replacing the existing REA skill.
- Standard SKILL.md files with optional Codex UI metadata. Shared contracts live in reconstruct-orchestrate; all eight folders form one installable library. Core is a required sibling dependency, not an assumed cross-skill API.
- Keep routing and state helpers deterministic and dependency-free (Python standard library). Instructions remain usable manually when Python or shell is unavailable.
- Reuse REA only when an actual target and relevant advertised tools exist. No REA setup or target selection is needed to author this library.
- Sequential execution is the default fallback. Parallel workers need bounded inputs and separate write ownership; the integrator alone merges shared state.
- A finite gate checks trace links and current recorded results. It cannot prove an agent's honesty, complete requirement discovery, or global equivalence.
- Workspace is not a Git repository; do not initialize Git or publish anything as an incidental task.

## Phases
1. Source analysis and coverage mapping — complete; all source sections, 20 fidelity dimensions, and 10 mission acceptance criteria mapped.
2. Shared contracts and architecture — complete; eight capability boundaries and shared artifact contracts documented.
3. Skill and helper implementation — complete; eight skills, optional UI metadata, state helper, installer, and library checker created.
4. Structural checks, negative gate tests, scenario evaluations — complete: 35 tests and all eight skill format checks passed; independent CLI trial passed 7 scenarios/78 paired invocations; missing-access case completed sequentially. Helper review findings fixed.
5. Revision, local installation, delivery report — complete: eight skills installed, 24 file hashes checked, host discovery observed, retained results and validation report written.

## Interruption recovery
The first independent evaluations were interrupted by the agent service's usage limit.
Their temporary directories did not survive continuation. The subsequent CLI evaluation
completed and was archived before another interruption. The missing-access attempt remained
partial and was completed sequentially in a fresh isolated workspace, then archived. No lost
temporary result is counted as passed. Final evidence is under `evaluation/results/`; source
prompt hashes still match. The continued host catalog confirms all eight installed skills.

## Resume
Delivery is complete. Read docs/validation-report.md for actual results and limits, and
docs/usage.md to start a reconstruction. Future work is optional broader evaluation rather
than an unfinished installation task. The two input prompts remain unchanged.
