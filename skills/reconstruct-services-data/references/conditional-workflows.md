# Conditional service and state workflows

Read only the section matching the product. These are design questions and verification probes, not claims about the original implementation.

## Jobs and external effects

Describe the operation state machine, durable trigger, lease/ownership, retry budget, terminal failure, cancellation, and repair action. Determine what happens if a worker stops before the effect, after the effect, or before acknowledging completion. Deduplication must cover the effect, not merely receipt of the message. A transactional outbox or another recovery protocol may be appropriate when a database commit and event delivery must stay consistent; select it from the actual failure requirement.

Test duplicate delivery, worker interruption, poisoned input, downstream timeout, and a successful retry using bounded local or sandbox fixtures. Record whether guarantees are at-most-once, at-least-once, or narrower observable promises. Do not claim exactly-once effects without establishing the end-to-end boundary.

## Concurrency and collaboration

Define the conflicting operations and the intended invariant before choosing locks, optimistic versions, merge rules, or replicated state. For edits, specify conflict visibility, ordering, reconnect behavior, offline changes, snapshots, and permission revocation during a session. Test two controlled clients with known initial state and deliberate interleaving; final values alone may miss invalid intermediate effects.

Do not infer a CRDT, OT algorithm, or database isolation level merely from a successful collaborative edit. An independent implementation may meet the same observable conflict contract.

## AI systems

Define model/tool interfaces, streaming events, cancellation, retrieval provenance, context limits, usage/cost budgets, error taxonomy, and tool authorization. Treat retrieved content and model outputs as untrusted inputs. Validate structured outputs before effects; handle partial streams and interrupted tool calls.

Separate deterministic protocol tests from stochastic quality evaluation. Record model identifier/configuration, prompt or prompt digest, fixtures, sample count, scoring method, and acceptance threshold. Use repeated trials when variability matters. A similar response does not establish recovery of a hidden prompt, model weights, private training data, or reasoning.

## Mobile and offline

Separate local durable state, pending mutations, server authority, and derived caches. Specify conflict resolution, authentication expiry, device permissions, background limits, process eviction, and interrupted uploads. Exercise restart, reconnect, duplicate sync, clock skew, and schema upgrades with synthetic fixtures. Do not equate an online emulator test with device-wide compatibility.

## Desktop and native integration

Map process boundaries, IPC message validation, filesystem ownership, local storage, native dependencies, startup/shutdown, and updater behavior. Verify path handling and untrusted IPC inputs at the privileged boundary. Exercise interrupted writes, restart recovery, file locks, and version compatibility where relevant. Follow the investigation skill for artifact analysis; recovered pseudocode is not original source or runtime proof.

## Commerce or other irreversible workflows

Model reservation, commit, expiry, compensation, and reconciliation separately. Money movement, inventory, refunds, and notifications have different authorities and failure states. Use service sandboxes or controlled fixtures for failure injection. Record a concrete execution plan and follow existing user authorization before any real external effect; do not assume a reconstruction request authorizes purchases or production changes.
