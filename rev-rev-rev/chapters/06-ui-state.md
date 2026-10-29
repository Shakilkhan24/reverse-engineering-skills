# ০৬ · একটি বাটনের আট রকম জীবন

আরিফ একটি সবুজ toast বানিয়েছে: “Saved!” Request তখনও যাচ্ছে। নীরা বলল, “তোমার toast ভবিষ্যৎ বলতে পারে। আমাদের server পারে না।”

## Submit-এর state machine

![এক form-এর লেখা, loading, validation error, confirmed, outcome unknown ও conflict অবস্থার ছয়টি UI mockup](../assets/figures/20-ui-contact-sheet.png)

তুমি user হলে ৩ নম্বরে title লিখতে। ৪ নম্বরে ticket খুলতে। কিন্তু ৫ নম্বরে আবার নতুন ticket বানানোর আগে আগেরটির ফল খুঁজতে। এই ছোট UI পার্থক্যের পেছনেই নিচের state machine।

**একবার নিজে বলো:** ৫ নম্বর screen থেকে input মুছে দিলে কী হারাবে? উত্তরটি শুধু text নয়—pending operation-এর সঙ্গে user-এর সম্পর্কও হারাতে পারে।

![Idle, validating, submitting, success, conflict এবং outcome unknown অবস্থার সম্পর্ক](../assets/figures/04-ui-state.png)

**ছবি পড়ো:** response পাওয়া এবং operation হওয়া আলাদা ঘটনা। Timeout-এর পরে এখানে `outcome_unknown` আছে। Server commit করেছে কি না জানা না থাকলে “ব্যর্থ” বলে নতুন operation তৈরি করানো duplicate ঘটাতে পারে।

| বর্তমান state | ঘটনা | পরের state | UI কী বলবে |
|---|---|---|---|
| idle | Submit | validating | input পরীক্ষা |
| validating | empty title | validation_error | field-এর কাছে কারণ |
| validating | valid | submitting | কাজ চলছে |
| submitting | confirmed response | success | server-confirmed ফল |
| submitting | stale version | conflict | নতুন state পড়ে সিদ্ধান্ত |
| submitting | response timeout | outcome_unknown | “ফল যাচাই করা হচ্ছে” |
| outcome_unknown | safe replay confirms | success | আগের operation-এর ফল |
| outcome_unknown | still unresolved | outcome_unknown | request reference ও recovery |

UI disabled করলেই duplicate-এর সব উৎস বন্ধ হয় না। Browser retry, app reconnect বা অন্য client একই operation পাঠাতে পারে। Server contract-এর প্রয়োজন এখানেই।

## চার ধরনের state-এর ছোট নাটক

```json
{
  "local_ui": {"menu_open": true},
  "server": {"assignee": "nira", "version": 8},
  "client_cache": {"assignee": "arif", "version": 7},
  "derived": {"assigned_to_nira_count": 12}
}
```

Menu খোলা local UI state। Assignee-এর durable truth server-এর। Cache পুরোনো হলে list ভুল দেখাতে পারে। Count কোন projection থেকে এসেছে, তা জানা না থাকলে ১২ ঠিক কি না বলা যাবে না। “সব state reset করে দাও” সমাধানে unsaved draft-ও হারাতে পারে।

## Optimistic update-এর dry run

১. Server version ৭; assignee আরিফ।  
২. Client নীরাকে নির্বাচন করে; UI সাময়িকভাবে নীরা দেখায়।  
৩. Server conflict দেয়, কারণ অন্য actor version ৮ করেছে।  
৪. Client নিজের pending change আলাদা রাখে, current state আনে এবং conflict দেখায়।  
৫. User নতুন state দেখে পুনরায় প্রয়োগ করবেন কি না ঠিক করেন।

Blind rollback-ও বিপজ্জনক: এই সময়ে অন্য successful update এসে থাকলে পুরো পুরোনো object বসিয়ে সেটি মুছে দিতে পারো। Mutation identity ও version মিলিয়ে cache update করা প্রয়োজন।

## Visual comparison-কে পুনরাবৃত্তিযোগ্য করো

একই viewport, font, browser, data, role, locale এবং loading state ব্যবহার করো। Random avatar ও চলমান clock screenshot diff-এ noise তৈরি করে। Normalize করতে পারো, কিন্তু actual error message বা permission-dependent button বাদ দেবে না।

Mouse বাদ দিয়ে Tab, Enter, Space ও Escape দিয়ে journey চালাও। Keyboard দিয়ে কার্যকারিতা পাওয়া accessibility-এর একটি মৌলিক দাবি; শুধু tab order পরীক্ষা পূর্ণ accessibility audit নয়। [W3C keyboard guidance](https://www.w3.org/WAI/WCAG22/Understanding/keyboard.html)।

বাংলা UI-তে দীর্ঘ label, mixed বাংলা–English ID, সংখ্যা, narrow screen ও ২০০% zoom পরীক্ষা করো। `Save` সুন্দর দেখালেও “পরিবর্তন সংরক্ষণ করুন” button থেকে বেরিয়ে যেতে পারে।

**নিজে করো—Q06:** timeout-এর পর input মুছে “Failed” দেখানো কেন ক্ষতিকর হতে পারে? [উত্তর](../appendices/B-workbook.md)।

<!-- book-navigation -->

---

[← গোয়েন্দার মতো পরীক্ষা সাজাও](../chapters/05-experiments.md) · [সূচি](../README.md) · [API-এর প্রতিশ্রুতি পড়তে শেখা →](../chapters/07-api-contract.md)
