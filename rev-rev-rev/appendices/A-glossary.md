# পরিশিষ্ট A · বাংলা–ইংরেজি ধারণার অভিধান

একই শব্দ ভিন্ন tool-এ সামান্য ভিন্ন অর্থে ব্যবহৃত হতে পারে। এখানে বইয়ের অর্থ দেওয়া হলো। Definition-এর সঙ্গে একটি প্রশ্ন মনে রাখলে মুখস্থের বোঝা কমে।

| শব্দ | এই বইয়ে অর্থ | নিজেকে প্রশ্ন |
|---|---|---|
| Reverse engineering | evidence দিয়ে অজানা system-এর model তৈরি | কী জানলাম, কী অজানা? |
| Reconstruction | প্রয়োজনীয় আচরণ পূরণ করে replacement তৈরি | কোন contract পূরণ হলো? |
| Fidelity | নির্ধারিত ক্ষেত্রে reference-এর সঙ্গে মিল | কোন dimension-এ মিল? |
| Observable behavior | বাইরে থেকে দেখা ফল/interaction | কোন account ও condition-এ? |
| Evidence | claim মূল্যায়নের artifact/observation | অন্য কেউ যাচাই করতে পারবেন? |
| Provenance | তথ্য কোথা থেকে এসেছে তার ইতিহাস | source ও method কী? |
| Observation | সরাসরি দেখা ঘটনা | ব্যাখ্যা মিশে গেছে কি? |
| Inference | evidence থেকে সম্ভাব্য ব্যাখ্যা | অন্য ব্যাখ্যা আছে? |
| Assumption | কাজ এগোতে সাময়িকভাবে ধরা বিষয় | ভুল হলে কী বদলাবে? |
| Hypothesis | পরীক্ষা দিয়ে মূল্যায়নযোগ্য ব্যাখ্যা | কী ফল predict করে? |
| Controlled experiment | relevant variables নিয়ন্ত্রিত রেখে পরীক্ষা | কোন variable বদলেছে? |
| Confounder | ফলের বিকল্প কারণ তৈরি করা factor | network/hardware আলাদা? |
| Information gain | অনিশ্চয়তা কমানোর ক্ষমতা | কোন hypothesis আলাদা হবে? |
| Traceability | evidence থেকে result পর্যন্ত সম্পর্ক | requirement-এর test কোথায়? |
| Contract | input, outcome, errors ও শর্তের প্রতিশ্রুতি | failure-এ কী হবে? |
| Acceptance criterion | গ্রহণযোগ্য ফলের পরীক্ষাযোগ্য শর্ত | pass/fail বলা যায়? |
| Oracle | expected behavior নির্ধারণের ভিত্তি | expected কে ঠিক করেছে? |
| Invariant | নির্দিষ্ট scope-এ বজায় রাখার শর্ত | কোন operation ভাঙতে পারে? |
| State machine | state ও allowed transition-এর model | কোন move নিষিদ্ধ? |
| Authoritative state | কোনো বিষয়ের নির্ধারিত সত্যের উৎস | conflict-এ কাকে মানবে? |
| Projection | অন্য state থেকে তৈরি representation | rebuild করা যায়? |
| Cache invalidation | stale copy পুনর্ব্যবহার বন্ধ করা | কোন cache key প্রভাবিত? |
| Eventual consistency | delay-এর পরে specified convergence-এর model | delay ও failure-এর policy কী? |
| Transaction | এক unit হিসেবে commit/rollback হওয়া কাজ | atomic boundary কোথায়? |
| Race condition | timing/ordering অনুযায়ী ফল বদলানো | কোন interleaving ক্ষতিকর? |
| Lost update | এক update অন্য update ঢেকে হারানো | stale copy overwrite করেছে? |
| Optimistic concurrency | expected version মেলালে write | conflict কীভাবে প্রকাশিত? |
| Idempotency | replay-এ intended effect অনিচ্ছাকৃতভাবে না বাড়া | logical operation identity কী? |
| Deduplication | একই identity-র duplicate চিনে সামলানো | scope ও retention কী? |
| Outbox | domain change-এর সঙ্গে durable outgoing record | send/ack gap কীভাবে সামলাবে? |
| At-least-once delivery | delivery পুনরায় হতে পারে এমন guarantee | consumer duplicate-safe? |
| Reconciliation | আলাদা খাতার state মিলিয়ে repair | source of truth কোনটি? |
| Backoff | retry-এর আগে বিরতি বাড়ানো | bounded আছে? |
| Jitter | retry delay-তে randomness | synchronized burst কমছে? |
| Authentication | actor identity প্রতিষ্ঠা | তুমি কে? |
| Authorization | resource/action-এর অনুমতি | এই কাজ করতে পারো? |
| Tenant | data/permission-এ আলাদা customer boundary | query scope ঠিক? |
| Trust boundary | ভিন্ন আস্থার অংশের সংযোগ | input কোথায় যাচাই? |
| Observability | internal behavior বোঝার signal ব্যবস্থা | complaint থেকে cause খুঁজবে? |
| Span | trace-এর একটি timed operation | parent/link সঠিক? |
| SLI | service behavior-এর মাপ | numerator/denominator কী? |
| SLO | SLI-এর নির্দিষ্ট target ও window | লক্ষ্য, না achieved result? |
| Tail latency | distribution-এর ধীর দিকের সময় | p95/p99 কোন method-এ? |
| Throughput | সময়প্রতি সম্পন্ন কাজ | success ও failure আলাদা? |
| Saturation | resource capacity-র ওপর চাপ | queue/connection pool ভরছে? |
| Vertical slice | একটি outcome-এর প্রয়োজনীয় সব layer | end-to-end result আছে? |
| Mock/Fake | নিয়ন্ত্রিত test substitute | কোন reality বাদ যাচ্ছে? |
| Differential test | reference ও replacement-এর তুলনা | equivalent condition আছে? |
| Regression test | আগের bug ফিরে এলে ধরার পরীক্ষা | symptom নয়, contract যাচাই? |
| ADR | decision ও rationale-এর সংক্ষিপ্ত record | কখন পুনর্বিবেচনা? |
| RPO | গ্রহণযোগ্য data-loss window-এর লক্ষ্য | recoverable point কী? |
| RTO | recovery সময়ের লক্ষ্য | drill-এ কত লেগেছে? |
| Runbook | নির্দিষ্ট incident-এর কাজের নির্দেশ | কে কী করবেন? |

<!-- book-navigation -->

---

[← মাঠের খাতা: ২৫টি স্মরণসূত্র](../chapters/24-field-guide.md) · [সূচি](../README.md) · [অনুশীলন, উত্তর ও capstone rubric →](../appendices/B-workbook.md)
