# ২২ · ৩০ দিনের কাজভিত্তিক অনুশীলন

৩০ দিনে সর্বজ্ঞ হওয়ার প্রতিশ্রুতি নেই। লক্ষ্য হলো একটি repeatable engineering loop হাতে পাওয়া। প্রতিদিনের সময় তোমার সুবিধামতো; একটি phase-এর artifact দুর্বল থাকলে calendar-এর জন্য পরের phase-এ দৌড়ানোর দরকার নেই।

![৩০ দিনের আটটি phase ও নির্দিষ্ট deliverable-এর সময়সূচি](../assets/figures/14-practice.png)

## দিনভিত্তিক কাজ

| দিন | কাজ | দিনের শেষে দেখানোর জিনিস |
|---|---|---|
| ১ | ছোট অনুমোদিত target বাছাই | scope paragraph |
| ২ | তিন user journey দেখো | route/state notes |
| ৩ | repository baseline | commands + actual results |
| ৪ | দশটি observation লেখো | evidence ledger |
| ৫ | পাঁচটি unknown বাছো | impact + next experiment |
| ৬ | একটি controlled experiment | hypothesis/result/limit |
| ৭ | create UI states | state table |
| ৮ | happy API request | request/response contract |
| ৯ | error ও boundary cases | error matrix |
| ১০ | reload ও keyboard journey | capture + discrepancy |
| ১১ | entity ownership | conceptual data map |
| ১২ | state transitions | valid/invalid pairs |
| ১৩ | decision table | permission/rule cases |
| ১৪ | deletion ও concurrency | failure timelines |
| ১৫ | architecture alternatives | ছোট ADR |
| ১৬ | ছোট slice implementation | callable behavior |
| ১৭ | durable persistence | reopen check |
| ১৮ | slice verification | executed tests + limits |
| ১৯ | reference comparison | matching conditions |
| ২০ | discrepancy diagnosis | suspected/confirmed cause |
| ২১ | fix ও regression | failing-before/passing-after evidence |
| ২২ | verification matrix | unknown ঘর দৃশ্যমান |
| ২৩ | workspace boundary | negative tests |
| ২৪ | retry/concurrency | same-key ও stale-version cases |
| ২৫ | dependency failure | pending/recovery report |
| ২৬ | observability ও restore plan | diagnostic/recovery artifact |
| ২৭ | clean build/migration rehearsal | result অথবা explicit blocker |
| ২৮ | release gates | critical scenario status |
| ২৯ | fidelity report | denominator + limitations |
| ৩০ | আরেকজনকে teach-back | demo + next three actions |

## তিনটি checkpoint

**দিন ৬:** একটি unknown কেন unknown, এবং পরের experiment কোন explanation আলাদা করবে—ব্যাখ্যা করতে পারছ? না পারলে আরও code নয়, question design অনুশীলন করো।

**দিন ১৮:** user outcome-এর durable ফল আছে? শুধু screenshot হলে slice অসম্পূর্ণ। Backend-only lab হলে UI বাদ দেওয়া scope-এ লেখা আছে কি?

**দিন ৩০:** অন্য reader artifact দেখে claim যাচাই করতে পারবেন? Report-এ “trust me” দরকার হলে traceability উন্নত করো।

## Spaced recall

একটি concept পড়ার দিন, তিন দিন পরে এবং এক সপ্তাহ পরে বই বন্ধ করে ব্যাখ্যা করো। তিন প্রশ্ন: “কী?”, “কেন ভুল হয়?”, “কী experiment?” নিজের ভুল উত্তর লিখে পরে সংশোধন করো। Progress chart-এ পড়া page-এর চেয়ে produced artifact ও corrected misconception বেশি কাজের।

**নিজে করো—Q22:** তোমার available সময় কম হলে কোন phase বাদ না দিয়ে ছোট করবে? নিজের সাত দিনের mini-plan লেখো। [নমুনা](../appendices/B-workbook.md)।

<!-- book-navigation -->

---

[← কতটা হলো: সৎ হিসাবের ভাষা](../chapters/21-fidelity.md) · [সূচি](../README.md) · [প্রতিদিনের ছোট engineering সভা →](../chapters/23-daily-loop.md)
