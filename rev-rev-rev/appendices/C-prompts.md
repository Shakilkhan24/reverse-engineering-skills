# পরিশিষ্ট C · সরাসরি ব্যবহারযোগ্য agent prompts

`<...>` অংশ নিজের project অনুযায়ী পূরণ করো। কোনো prompt tool permission বা project access স্বয়ংক্রিয়ভাবে দেয় না; বাস্তব অনুমোদিত scope মানতে হবে। Agent-এর কাজ review করার দায়িত্ব ফল ও evidence দিয়ে পালন করবে।

## ১. Repository-তে প্রথম প্রবেশ

```text
লক্ষ্য: <journey> বোঝা ও প্রয়োজনীয় পরিবর্তনের ভিত্তি তৈরি।
আগে project instructions, git status, README, existing tests ও entry points পড়ো।
একটি request-এর UI/handler/service/store call path file reference-সহ দেখাও।
Baseline check চালিয়ে exact command ও result লেখো।
Existing changes সংরক্ষণ করো। Rewrite-এর আগে প্রমাণিত defect ও কারণ দাও।
Deliverable: current behavior, unknowns, smallest coherent next slice।
```

## ২. Observation-কে evidence-এ রূপ দাও

```text
এই artifacts পর্যালোচনা করো: <paths>।
প্রতিটি finding-এ ID, question, context, method, observation ও limitation দাও।
OBSERVED / DERIVED / INFERRED / ASSUMED / UNKNOWN / CONTRADICTED আলাদা করো।
যে architecture এসব artifacts থেকে জানা যায় না, তা বানিয়ে পূরণ করবে না।
প্রতিটি high-impact unknown-এর জন্য একটি discriminating experiment প্রস্তাব করো।
```

## ৩. Screenshot থেকে behavior specification

```text
Target journey: <journey>। Evidence: <captures>।
Loaded screen ছাড়াও loading, empty, validation, permission, conflict,
timeout এবং recovery state inventory করো।
চার ধরনের state আলাদা করো: local UI, server, cache, derived।
Keyboard ও narrow viewport-এর acceptance criteria দাও।
Missing evidence-কে unknown রাখো; নতুন product choice আলাদা label করো।
```

## ৪. Vertical slice implement করো

```text
Outcome: <একটি নির্দিষ্ট user outcome>।
Source contract: <spec path>; evidence: <IDs>।
Existing architecture অনুসরণ করে validation, authorization, domain rule,
persistence ও প্রয়োজনীয় error/recovery path implement করো।
Mock বনাম real integration স্পষ্ট রাখো।
Relevant happy, boundary, forbidden এবং failure cases চালাও।
Deliverable: changed files, actual test results, unresolved gaps।
```

## ৫. Concurrency ও retry review

```text
এই operation review করো: <operation>।
Logical operation identity, dedupe scope, payload mismatch, retention,
in-flight duplicate এবং stale-version policy নির্ধারণ করো।
Check-then-write race আছে কি দেখো।
DB commit, event record, external send ও acknowledgement-এর failure windows আঁকো।
কমপক্ষে একটি overlapping request test ও একটি ack-gap test চালাও।
যে guarantee provider বা database-এর ওপর নির্ভর করে তা স্পষ্ট লেখো।
```

## ৬. Differential review

```text
Reference evidence: <paths/version>। Replacement: <build>।
Equivalent actor, data, initial state ও timing দিয়ে <scenarios> তুলনা করো।
Normalization rule আগে লেখো; semantic field বাদ দিও না।
প্রতিটি mismatch-এ expected, actual, reproduction, severity ও evidence দাও।
Suspected cause এবং confirmed cause আলাদা রাখো।
Fix-এর পরে relevant regression চালিয়ে discrepancy status update করো।
```

## ৭. Agent-এর অতিরিক্ত দাবি সংশোধন

```text
তোমার আগের completion report-টি requirement ধরে audit করো।
কোন tests বাস্তবে execute হয়েছে, কোন command ও environment-এ?
যে result শুধু expected, তাকে NOT RUN হিসেবে চিহ্নিত করো।
Original সম্পর্কে evidence-বিহীন claim-কে inference/unknown-এ সংশোধন করো।
Pass rate-এর denominator এবং critical failed scenario আলাদা দাও।
তারপর সর্বোচ্চ মূল্যবান পরের তিনটি কাজ নির্ধারণ করো।
```

## ৮. Context handoff

```text
পরের session-এর জন্য concise handoff লেখো:
১. Agreed scope ও current outcome
২. Evidence-backed findings এবং accepted decisions
৩. Changed files ও actual verification result paths
৪. Failed/blocked/unverified items এবং কারণ
৫. Next three actions, dependencies ও definition of done
Chat-এর অনুমানকে repository fact হিসেবে লিখবে না।
```

## Prompt review-এর ছোট checklist

- Outcome কি দেখা/মাপা যায়?
- Existing evidence কোথায় পড়তে হবে বলা আছে?
- Done হওয়ার condition আছে?
- Error/recovery requirement প্রাসঙ্গিক হলে অন্তর্ভুক্ত?
- Agent কী report করবে নির্দিষ্ট?

প্রতিটি task-এ আটটি prompt একসঙ্গে পাঠানোর প্রয়োজন নেই। যে uncertainty বা কাজ সামনে, তার জন্য যথাযথ নির্দেশটি ব্যবহার করো।

<!-- book-navigation -->

---

[← অনুশীলন, উত্তর ও capstone rubric](../appendices/B-workbook.md) · [সূচি](../README.md) · [উৎস, সীমা ও মূল লেখার মানচিত্র →](../appendices/D-sources.md)
