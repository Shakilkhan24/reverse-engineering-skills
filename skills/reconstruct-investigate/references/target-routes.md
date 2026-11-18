# Evidence routing by target

Tools named here are capability examples, not a guarantee that the current host advertises
them. Discover actual tools and follow installed provider guidance. This library does not
install REA, engines, debuggers, or browsers as a side effect of investigation.

| Input and question | First useful route | Preserved evidence and limit |
| --- | --- | --- |
| Complete source repository | Normal search, source reading, existing tests | File/revision/line and executed result; source alone may not reflect deployed behavior |
| Screenshots or design reference | Inspect images and visible states | Viewport/state/version; no hidden interactions, persistence, or backend inferred as fact |
| Public or authorized browser | Available browser inspection; controlled user journey | Role, input, screenshots, network records; no claim about private topology |
| API docs or schema | Read exact version and relevant operations | Documented contract; implementation compatibility needs separate checks |
| HAR/SAZ/packet trace | Format-aware offline parser or advertised REA capture tool | Original digest, selected records/ordinals, redactions, truncation; no automatic URL fetch/replay |
| Electron/JavaScript bundle or ASAR | Installed REA JavaScript workflow, summary first; otherwise static inventory | Module identities, source ranges, retained evidence; strings are leads, not behavior |
| Native executable/library | Installed REA native workflow and relevant available provider | Artifact hash, static findings/pseudocode, provider limits; execution needs separate scope |
| APK/managed assembly/firmware/WASM | Installed corresponding REA route or supported format-aware tooling | Target-specific metadata/code boundaries; unavailable engines remain a blocker |
| Database snapshot | Read-only schema and narrowly scoped synthetic/permitted rows | Snapshot/WAL consistency, table/query boundaries; do not copy private production data |
| User-owned runtime | Relevant passive browser/Electron/debugger workflow if available | Explicit process/target, lifecycle, observed actions; do not broaden to unrelated processes |

When tools are absent, use a useful supported fallback, or document precisely what cannot
be established. Consult the existing `reverse-engineer-anything` skill's recovery guide
only for an actual REA blocker. For large retained results use summaries, stable evidence
references, and focused pages instead of repeating the producer. Protect source digests
across pages and distinguish transport truncation from analysis coverage.

## Extraction depth ladders

Each route has a ladder of increasing depth and a ceiling the available access cannot cross.
"Absolute" understanding of a target is reaching the ceiling of every reachable source, not
inventing what lies beyond it. Climb only as far as the scoped question needs; record where
you stopped and why. The classification beside each rung is the strongest class that rung can
support by itself (see the [shared contract](../../reconstruct-orchestrate/references/common-contract.md)).

- **Source repository.** Entry points and routes (OBSERVED) → call graph for the target
  feature → config, feature flags, migrations, and existing tests as executable spec →
  build/CI for deploy-time behavior. Ceiling: runtime-only configuration, injected secrets,
  server state, and live data are not in the tree; source is not proof of deployed behavior.
- **Screenshots or design reference.** Visible layout and extractable tokens (OBSERVED) →
  enumerated visible states → transitions between pictured states (INFERRED only). Ceiling:
  persistence, authorization, timing, and any backend are not pictured — mark them dark, do
  not narrate them as seen.
- **Authorized browser.** Rendered DOM and client bundle (OBSERVED) → network request/response
  shapes and status/error taxonomy → client state transitions under controlled journeys →
  cache/timing behavior from headers and repeated requests. Ceiling: server internals, physical
  schema, and other tenants are inaccessible; a response documents a contract, not a topology.
- **API docs or schema.** Operations, types, auth model, and declared errors (DOCUMENTED).
  Ceiling: documented is not implemented; corroborate against a capture or an authorized probe
  before treating a documented contract as behavior.
- **HAR / SAZ / packet trace.** Endpoint inventory (OBSERVED, for the capture) → request/response
  schemas, auth and headers → sequencing and state carried between calls → exercised error cases.
  Ceiling: only what the capture exercised; an unseen endpoint is unproven, not absent; never
  fetch or replay a captured URL or side effect.
- **Electron / JavaScript bundle or ASAR.** Unpack and module inventory → sourcemap or beautified
  source → framework, routes, and IPC or privileged-call sites → config and secret handling.
  Ceiling: minified or bundled semantics are partial, server-side logic is absent, and strings
  are leads, not behavior.
- **Native executable / library.** Metadata, imports, and strings (OBSERVED) → function boundaries
  → pseudocode of the target routines → recovered data structures → authorized dynamic trace.
  Ceiling: decompiler pseudocode is a derivation, never original source; optimization, inlining,
  packing, and anti-analysis bound what static work can establish.
- **APK / managed assembly / firmware / WASM.** The corresponding laddered route for the format,
  gated by engine availability. Ceiling: an unavailable engine or an unsupported format is a
  recorded blocker, not a reason to guess.
- **Database snapshot.** Schema, constraints, and indexes (OBSERVED) → relationships → a narrow
  set of synthetic or permitted rows. Ceiling: application-level invariants are not all in the
  schema; do not read or copy private production data.
- **User-owned runtime.** Passive observation → lifecycle states → controlled permitted actions.
  Ceiling: bounded to the explicit process; do not broaden to unrelated processes or data.

## Triangulation across sources

The strongest reverse-engineering conclusions corroborate independent sources of different kinds.
A static string plus a captured endpoint plus one authorized runtime probe establishes a behavior
far better than any one alone. Corroboration raises confidence and can lift a hypothesis to DERIVED
when the combined derivation is reproducible from identified inputs; it never promotes anything to
OBSERVED except the parts directly inspected. Record each corroborating source's own ID and limit.
Agreement among several agents, or several documents repeating one origin, is not corroboration.
When sources conflict, reconcile by identity and context first, then by a discriminating probe;
preserve both observations until one is ruled out.

## Inference ladder: behavior to structure

These inferences are legitimate and valuable, and all stay INFERRED until verified. Each must name
the observable it rests on, and must not be built upon as if observed:

- API field shapes and relations → a conceptual data model (never the original physical schema).
- Error taxonomy and rejected inputs → validation and authorization rules.
- Response headers, timing, and repeated-request behavior → caching, pagination, and async models.
- Observed transitions → a state machine bounded by the paths actually seen; unseen transitions
  stay unknown, not forbidden.
- Idempotency, ordering, and duplicate handling → inferred only from controlled repeat/interleave
  probes, not from a single success.

Verify a load-bearing inference with the smallest discriminating experiment before a dependent slice
relies on it; route the surviving contract to [specify](../../reconstruct-specify/SKILL.md).

## Coverage and the extraction ceiling

Maintain a surface map that marks each feature, actor, entity, interface, and side effect as
explored (pushed to its ceiling), partial (some rungs climbed, named gap remaining), or dark
(no permitted route). The analysis is as complete as access allows — "absolute for this access" —
when every reachable region is explored to its source ceiling and every dark region has a recorded
reason it is inaccessible with the available access, not when a convenient answer was found first.
A negative result holds only within its stated search bounds: a missing string in a selected module,
or an endpoint unseen in a capture, is a bounded negative, never proof of absence. Report coverage as
these explored/partial/dark regions with their ceilings; do not collapse it into a single percentage.
