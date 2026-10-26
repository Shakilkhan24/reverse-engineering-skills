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
