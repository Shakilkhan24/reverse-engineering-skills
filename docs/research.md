# Research that informed the design

Sources were consulted on 2026-10-25. These are narrow design inputs, not copied manuals or
claims that the library has earned certification. The supplied source remains the basis
of the reconstruction methodology.

| Source | Established guidance used | Resulting design choice |
| --- | --- | --- |
| [Agent Skills specification](https://agentskills.io/specification) | Skills use a named directory and SKILL.md frontmatter, with optional supporting resources and progressive disclosure. | Standard folders, concise entrypoints, conditional references, checked names/links. |
| [Official OpenAI skill documentation](https://learn.chatgpt.com/docs/build-skills) | Descriptions drive discovery; Codex supports local skill locations and optional UI metadata. | Bounded trigger descriptions, generated agents/openai.yaml, installation into the documented user directory. |
| [WCAG 2.2](https://www.w3.org/TR/WCAG22/) | Web accessibility has explicit success criteria beyond visual similarity. | Experience work selects applicable criteria, preserves manual/runtime limits, and does not claim full conformance from an automated scan. |
| [OWASP ASVS](https://asvs.owasp.org/) | Web security requirements can be referenced by versioned identifiers and selected verification scope. | Assurance records exact standard/version and selected controls; partial review is not whole-standard compliance. |
| [OpenTelemetry signals](https://opentelemetry.io/docs/concepts/signals/) | Different telemetry signals expose different aspects of runtime activity. | Operations derives relevant logs, metrics, and traces from failure modes without mandating a telemetry vendor. |

The installed skill-creator guidance was also inspected for naming, concise scope, local
validation, UI metadata, and independent forward testing. The installed REA skill was read
to preserve tool discovery, target identity, summary-first evidence reuse, and static/runtime
boundaries. No REA analysis or setup was required for this skill-authoring task.

The shared JSON ledger, contract fingerprints, eight-skill boundary, profiles, and task merge
protocol are design decisions from this implementation. They are not requirements attributed
to the external standards. A dependency-free helper was chosen because deterministic link
and freshness checks directly address false completion without adding an agent framework.
