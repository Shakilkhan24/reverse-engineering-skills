# পরিশিষ্ট B · অনুশীলন, উত্তর ও capstone rubric

আগে নিজে লিখে তারপর উত্তর খোলো। কোনো উত্তর হুবহু মুখস্থ করা জরুরি নয়; reasoning ও scope ঠিক থাকা জরুরি। Markdown viewer `<details>` সমর্থন না করলে নিচের উত্তর সরাসরি দেখা যেতে পারে।

## অধ্যায়ের ২৪টি প্রশ্নের উত্তর

<details>
<summary>Q01 · Toast-এর পরে persistence যাচাই</summary>

একবার reload করে একই resource পড়ো; তারপর অন্য অনুমোদিত session বা নতুন connection থেকে পড়ো। প্রথমটি client-only state বাদ দিতে সাহায্য করে, দ্বিতীয়টি একই cache-এর ওপর নির্ভরতা কমায়। তবু disk failure recovery বা database vendor প্রমাণ হয় না।
</details>

<details>
<summary>Q02 · দ্বিতীয় service বানানোর আগে</summary>

Existing service-এর contract/callers, tests ও প্রমাণিত defect জানতে হবে। Reuse বা ছোট fix যথেষ্ট কি না দেখো। শুধু নাম পছন্দ হচ্ছে না বলে parallel implementation বানালে policy divergence হতে পারে।
</details>

<details>
<summary>Q03 · nginx থেকে Python?</summary>

Header value হলো observed; Python backend claim evidence-বিহীন hypothesis/assumption। nginx Python, Java, Go বা অন্য origin-এর সামনে থাকতে পারে। এটি supported inference-ও নয়, যদি অতিরিক্ত evidence না থাকে।
</details>

<details>
<summary>Q04 · Search-এর hidden work</summary>

সম্ভাব্য dependency: tenant filtering, indexing/projection, cache ও pagination। Failure: stale result এবং revoked user-এর result leak। Exact index vendor না জেনেও freshness ও isolation-এর contract লেখা যায়।
</details>

<details>
<summary>Q05 · Cache না index?</summary>

Authorized fresh detail read, search response, client cache-bypass observation এবং পাওয়া গেলে index/worker telemetry তুলনা করবে। Browser refresh-এর পরও delay থাকলে কিছু client-only explanation দুর্বল হয়। শুধু delay দিয়ে Elasticsearch বা queue architecture নিশ্চিত করা যায় না।
</details>

<details>
<summary>Q06 · Timeout-এর পরে input মুছে দেওয়া</summary>

Server ইতিমধ্যে commit করে থাকতে পারে। User আবার নতুন operation পাঠালে duplicate হয়; input মুছলে unresolved কাজের context-ও হারায়। Pending intent ও operation identity রাখো, ফল reconcile করো, তারপর confirmation দেখাও।
</details>

<details>
<summary>Q07 · Changed payload, same key</summary>

User নতুন title চেয়েছেন অথচ পুরোনো success পেলে তিনি নতুন intent সম্পন্ন হয়েছে ভাবতে পারেন। Scoped key-এর সঙ্গে payload fingerprint মেলানো এবং mismatch-এ নির্দিষ্ট conflict দেওয়া একটি পরিষ্কার contract।
</details>

<details>
<summary>Q08 · Delete-এর scope</summary>

কার কাছে অদৃশ্য—সাধারণ user না admin? কোথায়—detail, search, export, attachment? কখন—commit-এর সঙ্গে সঙ্গে না documented delay-এর পরে? Audit ও backup-এর retention policy আলাদা বিষয়।
</details>

<details>
<summary>Q09 · Database delete, search remains</summary>

Search মৃত resource দেখাতে পারে; title/body leak করতে পারে; dashboard count mismatch হতে পারে। Detail endpoint deny করলেও search snippet-এ তথ্য প্রকাশিত হতে পারে। Tombstone/version ও derived cleanup-এর contract যাচাই করো।
</details>

<details>
<summary>Q10 · Outbox-এর counterexample</summary>

Worker provider-এ email পাঠাল; delivered mark লেখার আগে crash। Outbox pending, তাই retry আবার send করতে পারে। Provider deduplication বা অন্য explicit delivery policy ছাড়া exactly-once external effect দাবি করা যাবে না।
</details>

<details>
<summary>Q11 · ২ সেকেন্ড response</summary>

Client-side network timing ও server trace-এর operation spans চাইবে। Database query/lock timing থাকলে DB hypothesis মূল্যায়ন করা যায়। Server span দ্রুত কিন্তু client wait দীর্ঘ হলে network/proxy/client দিকও দেখবে।
</details>

<details>
<summary>Q12 · Export worker-এর global query</summary>

Background path tenant boundary এড়িয়ে private data export করতে পারে। Actor/tenant context durable job payload বা trusted lookup থেকে নিয়ে worker-এ permission policy প্রয়োগ করতে হবে। Detail endpoint pass এই আলাদা পথ verify করে না।
</details>

<details>
<summary>Q13 · API success বনাম notification</summary>

Create outcome complete হতে পারে, কিন্তু notification-সহ journey অসম্পূর্ণ। Eligible notification-এর delivery success/freshness, oldest pending age এবং failure ratio আলাদা SLI হতে পারে। প্রতিটির window ও denominator লিখবে।
</details>

<details>
<summary>Q14 · Mean এবং backlog</summary>

শেষ পাঁচটি request ১,৫০০ ms নিয়েছে, যা mean আড়াল করেছে। ১০ মিনিট শেষে backlog ২০; ১১তম মিনিটে ৪ আসে, ১০টি process হয়; শেষে ১৪। Chart-এর recurrence থেকে হিসাবটি পুনরায় করা যায়।
</details>

<details>
<summary>Q15 · Async worker কেন</summary>

Ticket save-এর response দ্রুত চাই, আর email কয়েক মুহূর্ত পরে গ্রহণযোগ্য—এটি সম্ভাব্য requirement। নতুন tests: pending durability, duplicate delivery, retry, provider outage, ordering ও recovery। Queue যোগ করলেই এগুলো পাওয়া যায় না।
</details>

<details>
<summary>Q16 · ১৪ test পাসে যা বলা যাবে না</summary>

Real authentication secure, production throughput sufficient, real email exactly once—কোনোটিই পরীক্ষিত নয়। Power loss recovery, browser accessibility ও multi-region concurrency-ও lab-এর scope-এর বাইরে।
</details>

<details>
<summary>Q17 · Timestamp normalization</summary>

Independent run-এ generated creation time আলাদা হওয়া expected হলে raw equality বাদ দেওয়া উপযোগী। কিন্তু expiry, ordering, deadline, timezone বা freshness contract পরীক্ষায় timestamp মুছে দিলে মূল bug লুকাবে।
</details>

<details>
<summary>Q18 · একটি scenario-এর নমুনা</summary>

Offline note: invariant—acknowledged local save clean app restart-এ হারাবে না। Timeline—offline edit → local save → restart → reconnect → server confirm। Limitation—device storage corruption বা uninstall পরীক্ষা হয়নি।
</details>

<details>
<summary>Q19 · পাঁচ লাইনের assignment</summary>

১. Scope: create/read ticket slice। ২. Context: existing service ও observed contract পড়ো। ৩. Invariant: workspace isolation ও durable persistence। ৪. Verify: reload, invalid actor, timeout replay; actual results দাও। ৫. Handoff: changed files, remaining unknown, next three actions।
</details>

<details>
<summary>Q20 · Backup সবুজ</summary>

Backup job configured/executed বলা যেতে পারে, যদি log থাকে। Recovery capability `IMPLEMENTED, UNVERIFIED` অথবা `NOT RUN` verification status পাবে। Next action: isolated restore drill, integrity check ও measured recovery time।
</details>

<details>
<summary>Q21 · দুই denominator</summary>

“৫০টি defined scenario-এর ৪২টি pass”—৮৪%। “চালানো ৪৫টির মধ্যে ৪২টি pass”—প্রায় ৯৩.৩৩%। দ্বিতীয় বাক্যের সঙ্গে ২ blocked ও ৩ not implemented জানাবে। Critical failed scenario-ও আলাদা বলবে।
</details>

<details>
<summary>Q22 · সাত দিনের mini-plan</summary>

১ scope; ২ evidence/unknown; ৩ UI/API contract; ৪ state/data; ৫ ছোট slice; ৬ failure/permission tests; ৭ discrepancy ও report। Feature সংখ্যা কমাও, evidence→verification loop বাদ দিও না।
</details>

<details>
<summary>Q23 · Progress statement</summary>

“REQ-01 reopen test পাস করেছে”; “D-03 stale list bug reproduce ও root cause confirmed”; “U-07 original retry behavior এখনও অজানা, EXP-04 প্রস্তুত।” প্রতিটির পাশে artifact path ও actual run context যোগ করলে report reviewable হবে।
</details>

<details>
<summary>Q24 · পাঁচ নিয়মের মূল্যায়ন</summary>

প্রতিটি নিয়মের জন্য একটি concrete failure এবং সেটি ধরার observable test থাকা চাই। “ভালো code লিখব” যথেষ্ট নয়। “Same-key retry-এ count বাড়বে না; দুই overlapping request চালিয়ে ID ও outbox count মিলাব”—এটি কার্যকর উত্তর।
</details>

## গোয়েন্দা চ্যালেঞ্জ ১: Report-এর ভুল ধরো

Agent-এর report:

> “সব feature 100% complete। API 200 দিয়েছে। Screenshot reference-এর মতো। Redis ব্যবহার করেছি কারণ original-এ nginx header ছিল। সব tests pass হওয়ার কথা।”

নিজে অন্তত পাঁচটি সমস্যা বের করো।

<details>
<summary>সমাধানের ইঙ্গিত ও নমুনা</summary>

Denominator নেই; 200 durable outcome প্রমাণ নয়; screenshot behavior proof নয়; nginx থেকে Redis inference ভিত্তিহীন; “pass হওয়ার কথা” executed result নয়। Corrected report-এ scope, actual tests, evidence classification, remaining unknown এবং real/mock boundary চাইবে।
</details>

## গোয়েন্দা চ্যালেঞ্জ ২: তিনটি failure window

একটি ticket commit হয়েছে। Worker email পাঠাচ্ছে। তিনবার আলাদা failure inject করার plan লেখো: commit-এর আগে, send-এর আগে, send-এর পরে ack-এর আগে। প্রতিটি run-এ ticket count, outbox pending ও provider effect count predict করো।

| Window | Ticket | Pending | Provider effect |
|---|---:|---:|---:|
| commit-এর আগে exception | ০ | ০ | ০ |
| commit-এর পরে send হয়নি | ১ | ১ | ০ |
| send হয়েছে, ack হয়নি | ১ | ১ | ১ |

Lab-এর fake provider-এ retry-এর পরে শেষ row হয় ১, ০, ১। Real provider duplicate-safe না হলে শেষ সংখ্যা ২ হতে পারে। Table হলো expected model; execution evidence আলাদা জমা দেবে।

## Capstone: ছোট support workflow পুনর্নির্মাণ

**Target:** নিজের অনুমোদিত ছোট app অথবা এই local service lab। **Outcome:** দুই workspace-এর user ticket তৈরি ও valid status transition করতে পারবেন; replay duplicate তৈরি করবে না। UI যোগ করলে loading, validation, conflict ও unresolved outcome দৃশ্যমান করবে।

### Deliverable pack

1. Scope: included/excluded journey, actor, environment।
2. অন্তত আটটি evidence record; implemented behavior-এর সঙ্গে গুলিয়ে ফেলবে না।
3. অন্তত পাঁচটি unknown; প্রতিটির impact ও next action।
4. API/service contract, state table ও তিনটি invariant।
5. একটি ADR, একটি verified slice, দুইটি reproduced discrepancy।
6. Actual verification report ও source-linked handoff।

### মূল্যায়ন rubric

| বিষয় | পয়েন্ট | পূর্ণ পয়েন্টের জন্য |
|---|---:|---|
| Scope ও evidence | ২০ | claim-এর context, artifact, limitation |
| Contracts ও domain | ২০ | positive/negative state ও invariant |
| Implementation | ২০ | real persistence, clear mock boundary |
| Verification | ২৫ | failure, permission, concurrency ও executed result |
| Reporting ও recovery | ১৫ | honest denominator, remaining gaps, recovery plan |

এটি শেখার rubric; production certification নয়। **Critical gate:** cross-workspace data leak বা acknowledged data loss unresolved থাকলে score বেশি হলেও release-ready বলা যাবে না।

### Teach-back challenge

তিন মিনিটে একজন বন্ধুকে timeout, retry ও outbox বোঝাও। তিনি যদি জিজ্ঞেস করেন “তাহলে email একবারই যাবে?”, তুমি যেন নির্দিষ্ট guarantee ও limitation দিয়ে উত্তর দিতে পারো। ব্যাখ্যা করতে গিয়ে কোথায় আটকে যাও, সেখানেই পরের learning task।

<!-- book-navigation -->

---

[← বাংলা–ইংরেজি ধারণার অভিধান](../appendices/A-glossary.md) · [সূচি](../README.md) · [সরাসরি ব্যবহারযোগ্য agent prompts →](../appendices/C-prompts.md)
