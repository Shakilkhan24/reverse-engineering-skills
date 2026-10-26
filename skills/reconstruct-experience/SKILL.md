---
name: reconstruct-experience
description: Reconstruct an application's interface and interaction behavior from observed journeys and explicit contracts. Use for reconstruction work involving UI states, responsive layouts, accessibility, localization, or device behavior; skip backend-only work and isolated cosmetic edits without a reconstruction objective.
---

# Reconstruct experience

Deliver complete user journeys whose rendered states and transitions match the scoped evidence. Own presentation and client state; coordinate server authority and durable state with services-data.

Read the [common contract](../reconstruct-orchestrate/references/common-contract.md) before the first work unit. This skill belongs to the complete reconstruction library.

## Inputs and outputs

Require the selected requirement and scenario IDs, target/version, relevant screenshots or interaction evidence, route/state map, repository conventions, and contracts from [specify](../reconstruct-specify/SKILL.md). If evidence is limited to screenshots, mark transitions, permissions, and persistence as unresolved rather than treating them as observed.

Produce working UI changes, an updated client-state model where necessary, reusable visual tokens, scenario-linked checks, and a handoff listing changed contracts, discrepancies, and untested device/accessibility conditions. Use existing project documentation; [templates](../reconstruct-orchestrate/references/templates.md) provide optional formats.

## Procedure

1. Select one meaningful journey, including its entry point, preconditions, completion state, and recovery path. Review existing components and test setup before changing them.
2. Enumerate its reachable states: empty, loading, populated, validation failure, unauthorized, expired session, dependency failure, and interrupted submission as applicable. Separate local input state, URL/navigation state, cached server state, and durable records.
3. Measure the reference conditions that affect comparison: viewport, zoom, fonts, locale, device input, user role, data, and target version. Record unavailable conditions. Extract shared spacing, typography, color, and component behavior from evidence without redesigning unrelated screens.
4. Bind controls to the agreed contracts. Preserve server validation and authorization; handle rejected optimistic updates. Use production integrations and persistence when required by the journey. Clearly label a prototype or mock when those are outside scope.
5. Implement navigation, keyboard/focus behavior, form labels and errors, status announcements, and responsive reflow alongside the visual work. Preserve focus through dialogs, validation, and asynchronous updates; avoid conveying state by color alone.
6. For localization or device requirements, exercise long text, right-to-left layout when applicable, date/time zones, locale-aware formatting, touch targets, reduced motion, offline recovery, and lifecycle transitions. Select cases from the actual product rather than imposing every case.
7. Run the journey against the replacement, then compare with equivalent reference evidence. Inspect browser/device output when available. Include reload, back/forward navigation, and failure recovery where they affect the contract.
8. Register meaningful mismatches and fix their causes. Repeat affected checks after changes; route new behavioral uncertainty to [investigate](../reconstruct-investigate/SKILL.md).

## Acceptance evidence

- All enumerated states for this slice have a defined behavior; core controls perform their advertised actions.
- Persistence and permission-dependent behavior survive the applicable reload, role, and rejection checks.
- Visual comparisons identify their environment and tolerated differences. A matching screenshot establishes only the pictured state.
- Keyboard and accessibility checks cover the selected journey. Automated checks alone do not establish complete accessibility conformance.
- Responsive/device claims identify tested viewport and device conditions. Unavailable browsers remain untested.

Use agreed accessibility criteria and record the selected standard/version. [WCAG 2.2](https://www.w3.org/TR/WCAG22/) supplies testable web accessibility criteria; applicability and any conformance claim require a defined scope.

## Recovery and handoff

If browser access is missing, continue with component/state tests and repository checks, but keep visual/runtime claims unverified. If assets or fonts are unavailable, use an explicit substitute and register the difference. If the API contract changes, stop dependent UI integration long enough to reconcile it through specify; independent layout work can continue.

Pass code paths, requirement/scenario IDs, environment, executed results, and unresolved differences to [verify](../reconstruct-verify/SKILL.md). Return the next useful slice to [orchestrate](../reconstruct-orchestrate/SKILL.md); do not mark an entire experience complete from one successful journey.
