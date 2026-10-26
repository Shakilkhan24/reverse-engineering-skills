---
name: reconstruct-investigate
description: Discover and explain an identified reference product's behavior using authorized source, artifacts, captures, documentation, or runtime experiments. Use to resolve reconstruction uncertainties; do not infer private internals from screenshots or run REA for ordinary source-repository reading.
---

# Investigate the reference

Produce a bounded, version-aware account of behavior that can guide a replacement.
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
   evidence and record stale inputs. List reachable features, actors, entities, workflows,
   interfaces, side effects, and operational boundaries; retain undiscovered areas explicitly.
2. Select the highest-impact unanswered question. Write competing hypotheses and the
   smallest experiment that would distinguish them. Define a bounded search/stop condition.
3. Route to an available evidence source using [target routes](references/target-routes.md).
   When REA is installed and relevant, read its current skill and advertised schemas; reuse
   retained evidence IDs. Do not assume tool names, provider availability, or live execution.
4. Inspect static artifacts before runtime when they answer the question. For browser work,
   separate DOM/client implementation, network observations, server response behavior, and
   inaccessible server internals. Preserve raw excerpts and locations, not just conclusions.
5. For authorized probes, control role, fixture, version, environment, and action sequence.
   Useful discriminators include reload, repeated submission, conflicting edits, invalid
   input, stale sessions, pagination boundaries, delayed completion, and interrupted recovery.
   Select only probes relevant to the product and permitted side effects.
6. Record observations, documented statements, derivations, inferences, and unknowns with
   separate IDs. A missing string within a selected module does not prove feature absence.
   An observed endpoint does not enumerate all APIs. Trace an important feature through
   inputs, state changes, persistence, outputs, and indirect effects where evidence allows.
7. Reconcile contradictions by identity/context first, then a discriminating follow-up.
   Do not repeat an unchanged analysis or failed tool call without a specific new reason.
8. Update the feature/dependency inventory and high-impact unknowns. Send supported contracts
   to [specify](../reconstruct-specify/SKILL.md). Distinguish inaccessible internals from
   cheaply answerable unknowns; recommend independent design for the former.

## Outputs and acceptance

Deliver evidence records, an inventory with explored/unexplored boundaries, an unknowns
register with next actions, and a concise answer per question. Use the
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
