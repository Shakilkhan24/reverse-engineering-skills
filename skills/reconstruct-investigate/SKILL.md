---
name: reconstruct-investigate
description: Reverse-engineer and explain an identified reference product's behavior and structure from authorized source, artifacts, captures, documentation, or runtime experiments. Use whether the goal is pure analysis or resolving reconstruction uncertainties; do not infer private internals from screenshots or run REA for ordinary source-repository reading.
---

# Investigate the reference

Produce a bounded, version-aware account of behavior and structure, as complete as the
available access allows, that can answer an analysis question or guide a replacement.
Read the [shared contract](../reconstruct-orchestrate/references/common-contract.md).

## Inputs and boundaries

Require an explicit target or already-bound investigation, a question/outcome, available
access, and existing evidence. If only an ambiguous app name is supplied, resolve from
task context or ask which target; do not choose a convenient fixture. Identify which
evidence is source, public documentation, screenshot, capture, local package, or runtime.
Source reading is usually enough for source-defined implementation questions. Runtime
execution and remote writes remain within the user's established authorization.

## Procedure

1. Inspect prior ledgers, target digest/version, captures, and saved analysis. Reuse matching
   evidence and record stale inputs. Build a surface map of reachable features, actors, entities,
   workflows, interfaces, side effects, and operational boundaries, marking each region explored,
   partial, or dark (no permitted route). The map, not a single answer, tracks how complete the
   analysis is; keep dark and undiscovered areas visible rather than silently dropping them.
2. Select the highest-impact unanswered question. Write competing hypotheses and the
   smallest experiment that would distinguish them. Define a bounded search/stop condition.
3. Route to an available evidence source using [target routes](references/target-routes.md).
   When REA is installed and relevant, read its current skill and advertised schemas; reuse
   retained evidence IDs. Do not assume tool names, provider availability, or live execution.
4. Inspect static artifacts before runtime when they answer the question, and push each source
   down its [extraction depth ladder](references/target-routes.md) to the ceiling the question
   needs rather than stopping at the first visible answer. For browser work, separate DOM/client
   implementation, network observations, server response behavior, and inaccessible server
   internals. Preserve raw excerpts and locations, not just conclusions.
5. For authorized probes, control role, fixture, version, environment, and action sequence.
   Useful discriminators include reload, repeated submission, conflicting edits, invalid
   input, stale sessions, pagination boundaries, delayed completion, and interrupted recovery.
   Select only probes relevant to the product and permitted side effects.
6. Record observations, documented statements, derivations, inferences, and unknowns with
   separate IDs. A missing string within a selected module does not prove feature absence.
   An observed endpoint does not enumerate all APIs. Trace an important feature through
   inputs, state changes, persistence, outputs, and indirect effects where evidence allows.
   Corroborate independent sources of different kinds to strengthen a conclusion; this raises
   confidence, and can reach DERIVED when the combined derivation is reproducible, but promotes
   nothing to OBSERVED beyond what was directly inspected. Infer hidden structure from observed
   behavior using the [inference ladder](references/target-routes.md); such structure stays
   INFERRED until a discriminating probe confirms it.
7. Reconcile contradictions by identity/context first, then a discriminating follow-up.
   Do not repeat an unchanged analysis or failed tool call without a specific new reason.
8. Update the surface map and high-impact unknowns. Stop when the scoped question is answered,
   or, for an analysis-to-the-limit goal, when every reachable region is explored to its ceiling
   and every dark region has a recorded reason it is inaccessible with the available access —
   that is "absolute for this access," not a convenient first answer. Send supported contracts
   to [specify](../reconstruct-specify/SKILL.md). Distinguish inaccessible internals from
   cheaply answerable unknowns; recommend independent design for the former.

## Outputs and acceptance

Deliver evidence records, the surface map with its explored/partial/dark regions and their
ceilings, an unknowns register with next actions, and a concise answer per question. Use the
[evidence and worker templates](../reconstruct-orchestrate/references/templates.md).
Every material conclusion needs a source, classification, target identity, limitations,
and affected requirement. A decompilation can support a static code finding, not proof of
all runtime behavior or recovery of original source. Answered/partial/unresolved status
must cover the entire scoped question list.

## Failure and handoff

If a tool, credential, host OS, or target is unavailable, preserve the exact blocker and
continue with supported sources. A saved capture can support historical findings; it cannot
establish current live behavior. If important uncertainty remains before dependent design,
return it to [orchestrate](../reconstruct-orchestrate/SKILL.md) with impact, required access,
and the smallest useful next step. Close any analysis session this work owns when finished,
following that provider's lifecycle; do not close a user's unrelated runtime.
