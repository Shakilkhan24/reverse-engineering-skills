# Provisional export specification

Only the reported label and list association are source-backed. The following is an independent candidate design, not recovered LedgerDesk behavior. No code, original CSV or executed product test is included.

## Inputs and unresolved prerequisites

A future host supplies a frozen ordered snapshot, an explicitly agreed ordered column projection, and a trusted authorization decision. Actual invoice column names and data types remain unresolved; none is fabricated from the button label. Resolve the field projection, privacy rules, consumer requirements, and host/platform before implementing an integrated export. The serializer must not fetch hidden pages or expand scope implicitly.

## Candidate output and data behavior

For a future text projection, propose UTF-8 without BOM, comma delimiters, CRLF record separators, quoting every field and doubling embedded quotes. Preserve permitted values exactly with no numeric conversion, invented defaults or locale-dependent rounding. An empty authorized snapshot produces the agreed header only. Filename, actual business fields, formula handling and consumer compatibility must be decided explicitly before release; these are not known original semantics.

## State and failure behavior

Use idle → validating → serializing → delivering → succeeded → idle. Denial, validation failure, serialization failure or delivery failure produces a visible failure and returns to idle; a canceled save dialog produces cancellation, not success. Suppress another activation during validating/serializing/delivering. A later activation starts a new attempt with a new snapshot. Invoice state never changes. Offer no partial file on failure.

Authorization must be enforced by a trusted host boundary before offering bytes. A visible control is not evidence of permission enforcement. Host roles, tenants, API routes, storage and topology remain undecided. No protection or security compliance has been tested.

## Acceptance and handoff

Six future scenarios S-001–S-006 in state.json cover entry point, exact snapshot scope, text round-trip, denial, failure/retry and duplicate activation. All are planned; zero have executed. S-001 requires actual reference evidence; S-004 requires a resolved authority model. The others can test an explicitly independent implementation only after implementation is requested.

The next engineering dependency is evidence or an explicit independent column/authority contract, not scaffolding an app from the label. New evidence may supersede these choices and must invalidate affected comparisons.
