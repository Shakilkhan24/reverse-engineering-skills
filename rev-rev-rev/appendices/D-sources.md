# পরিশিষ্ট D · উৎস, সীমা ও মূল লেখার মানচিত্র

## এই বই কী থেকে তৈরি

প্রধান ভিত্তি তোমার দেওয়া [INSTRUCTION.md](../INSTRUCTION.md)—তার ২৪ অধ্যায়, আরিফ–নীরার গল্প, RelayDesk case study এবং evidence-driven reconstruction দর্শন। মূল ফাইল অক্ষত রাখা হয়েছে। এই সংস্করণে নতুন dry run, concrete contract, executable lab, Python figure, workbook ও reading interface যোগ হয়েছে।

মূল লেখার idea ও নতুন implementation আলাদা: SQLite schema, `actor/workspace/key` deduplication, status transition policy এবং fake provider এই tutorial-এর design। কোনো বাস্তব reference application থেকে এগুলো আবিষ্কৃত হয়নি।

## মূল অধ্যায় থেকে নতুন অধ্যায়ে

| মূল লেখার বিষয় | নতুন পাঠ | যোগ হওয়া অনুশীলন/উপকরণ |
|---|---|---|
| ১ · Surface/System | [০১](../chapters/01-surface-system.md) | layered figure, scope contract |
| ২ · Investigation | [০২](../chapters/02-reconnaissance.md) | ৩০ মিনিটের recon ও baseline |
| ৩ · Evidence | [০৩](../chapters/03-evidence.md) | JSON record, traceability figure |
| ৪ · Inventory | [০৪](../chapters/04-product-map.md) | feature card ও journey matrix |
| ৫ · Scientific investigation | [০৫](../chapters/05-experiments.md) | hypothesis table, priority chart |
| ৬ · UI | [০৬](../chapters/06-ui-state.md) | outcome_unknown, optimistic conflict |
| ৭ · API | [০৭](../chapters/07-api-contract.md) | error JSON, cursor dry run |
| ৮ · Business logic | [০৮](../chapters/08-domain-rules.md) | transition ও decision table |
| ৯ · Data | [০৯](../chapters/09-data-lifecycle.md) | deletion ও stale-event timeline |
| ১০ · Concurrency/queues | [১০](../chapters/10-time-concurrency.md) | SQL condition, outbox crash windows |
| ১১ · Network | [১১](../chapters/11-network.md) | fingerprint সীমা, stream timeline |
| ১২ · Security | [১২](../chapters/12-security.md) | actor/resource tests |
| ১৩ · Observability | [১৩](../chapters/13-observability.md) | trace plot, SLI arithmetic |
| ১৪ · Performance | [১৪](../chapters/14-performance.md) | latency, backlog, retry plots |
| ১৫ · Architecture | [১৫](../chapters/15-architecture.md) | alternatives ও teaching ADR |
| ১৬ · Implementation | [১৬](../chapters/16-vertical-lab.md) | executable SQLite lab |
| ১৭ · Verification | [১৭](../chapters/17-verification.md) | oracle, heatmap, discrepancy |
| ১৮ · Four scenarios | [১৮](../chapters/18-four-worlds.md) | চারটি domain-specific dry run |
| ১৯ · Multi-agent | [১৯](../chapters/19-agent-direction.md) | task contract ও steering |
| ২০ · Production | [২০](../chapters/20-production.md) | migration ও restore rehearsal |
| ২১ · Fidelity | [২১](../chapters/21-fidelity.md) | দুই denominator ও release gate |
| ২২ · ৩০ দিন | [২২](../chapters/22-practice-plan.md) | প্রতিদিনের artifact, timeline |
| ২৩ · Daily loop | [২৩](../chapters/23-daily-loop.md) | handoff ও incident walkthrough |
| ২৪ · Heuristics | [২৪](../chapters/24-field-guide.md) | ২৫টি review প্রশ্ন |

## প্রামাণ্য technical references

নিচের উৎসগুলো ২০২৬-১০-২৯ তারিখে দেখা হয়েছে। এগুলো নির্দিষ্ট semantics বুঝতে সাহায্য করে; RelayDesk scenario-গুলো তাদের case study নয়। পাঠে সংশ্লিষ্ট দাবির পাশেও link আছে।

| উৎস | এই বইয়ে কেন প্রাসঙ্গিক |
|---|---|
| [RFC 9110: HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110.html) | method semantics ও conditional requests |
| [RFC 9457: Problem Details](https://www.rfc-editor.org/rfc/rfc9457.html) | machine-readable HTTP error shape |
| [PostgreSQL transaction isolation](https://www.postgresql.org/docs/current/transaction-iso.html) | database-specific concurrency semantics |
| [AWS transactional outbox](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html) | dual-write gap ও duplicate delivery |
| [OWASP authorization](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html) | permission enforcement principles |
| [W3C keyboard accessibility](https://www.w3.org/WAI/WCAG22/Understanding/keyboard.html) | keyboard-operable functionality |
| [OpenTelemetry traces](https://opentelemetry.io/docs/concepts/signals/traces/) | spans ও related operation context |
| [Google SRE monitoring](https://sre.google/sre-book/monitoring-distributed-systems/) | service signals ও diagnosis |
| [AWS retries/backoff/jitter](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/) | retries-এর চাপ ও timing |
| [Python sqlite3](https://docs.python.org/3/library/sqlite3.html) | local file database ও transaction API |

## ডেটার তিনটি পরিচয়

**Conceptual:** layer, evidence chain, state machine, data ownership ও failure diagrams। এগুলোর geometry কোনো measurement নয়।

**Synthetic:** `data/`-র latency, queue, retry, priority, verification matrix ও fidelity counts। এগুলো শিক্ষার জন্য বানানো; real app-এর benchmark বা test report নয়।

**Executed local result:** `reports/lab-results.json` এবং verification artifacts। এগুলো এই repository-র lab ও document validation-এর ফল; real reference-এর equivalence proof নয়।

## এই সংস্করণের scope

এই বই product behavior, reconstruction workflow এবং AI-agent collaboration শেখায়। Native binary analysis, assembly, firmware, advanced OT/CRDT algorithm, formal verification ও real payment integration-এর গভীর কোর্স আলাদা লাগবে। এখানে তাদের সীমা চিহ্নিত করে প্রয়োজনীয় প্রশ্ন শেখানো হয়েছে।

দ্বিতীয় সংস্করণে ২২টি নতুন বাংলা দৃশ্য যোগ হয়েছে: form-এর screenshot mockup, request-এর খাম, retry-এর রসিদ, workspace-এর দরজা, before/after comparison ও ছোট conversation। এগুলো শিক্ষামূলক illustration; বাস্তব product-এর screenshot নয়। Lab snapshot-টি চালানো `reports/lab-results.json` থেকে নেওয়া। সব মিলিয়ে ৩৬টি visual আছে। Statistical chart-এর technical label ইংরেজিতে; নতুন দৃশ্যের label বাংলায়। ছবি ছাড়াও সংলগ্ন text/table-এ মূল অর্থ পাওয়া যায়।

<!-- book-navigation -->

---

[← সরাসরি ব্যবহারযোগ্য agent prompts](../appendices/C-prompts.md) · [সূচি](../README.md)
