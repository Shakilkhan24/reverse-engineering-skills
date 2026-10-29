# ০২ · অজানা রিপোজিটরিতে প্রথম অভিযান

নীরা আরিফকে একটি repository দিল। “প্রথম আধঘণ্টায় কিছু বানাবে না; কী আছে বোঝো।” আরিফের AI ইতিমধ্যে `NewSuperTicketEngineFinalV2` নামের পরিকল্পনা করছিল। নীরা বলল, “নামের মধ্যে Final থাকলে investigation শেষ হয় না।”

## প্রথম ৩০ মিনিটের অভিযান

![Repository-র পাঁচটি file বা folder এবং প্রত্যেকটিতে খোঁজার নির্দিষ্ট প্রশ্ন](../assets/figures/16-repository-map.png)

ধরো, `TicketForm` সঠিক payload পাঠাচ্ছে। Handler-ও চলছে। কিন্তু `TicketService` শুধু একটি memory array-তে item যোগ করে। এখন refresh bug-এর জন্য sidebar rewrite করতে হবে? পথ ধরে পড়লে কাজটি service-এর persistence অংশে এসে ছোট হয়ে যায়।

| সময় | কাজ | হাতে আসবে |
|---|---|---|
| ০–৫ মিনিট | instructions, README, git status | নিয়ম ও existing changes |
| ৫–১২ মিনিট | package/config/test structure | কীভাবে build ও run হয় |
| ১২–২০ মিনিট | একটি workflow-এর call path | UI → handler → service → store |
| ২০–৩০ মিনিট | ছোট baseline check | command, result, known failure |

এটি অনুশীলনের সময়বণ্টন, সব repository-এর deadline নয়। বড় project-এ একই প্রশ্নের উত্তর পেতে বেশি সময় লাগবে।

```bash
pwd
git status --short
rg --files -g 'AGENTS.md' -g 'README*' -g 'package.json' -g 'pyproject.toml'
rg -n 'createTicket|create_ticket|TicketService' src tests
```

শেষ command-এর directory নিজের repository অনুযায়ী বদলাবে। এখানে `rg` কেবল text খোঁজে; matching symbol দেখেই runtime call প্রমাণ হয় না। Call site, route registration ও tests মিলিয়ে দেখতে হবে। `.env`-এর secret value report-এ কপি না করে প্রয়োজনীয় configuration **নাম** লিখবে।

## একটি request-এর পায়ের ছাপ

```text
TicketForm.onSubmit
  → POST /tickets
  → route handler
  → TicketService.create
  → repository.insert
  → response mapper
```

এটি একটি candidate call chain। প্রতিটি arrow-এর পাশে file path বা runtime evidence যোগ করো। Source-এ function আছে কিন্তু route-এ ব্যবহার হয় না—এমন code-কে active behavior বললে ভুল model তৈরি হবে।

## Tool নির্বাচন: প্রশ্ন আগে

| তোমার প্রশ্ন | উপযোগী evidence source | কী জানা যাবে না |
|---|---|---|
| Browser কী request পাঠায়? | DevTools network capture | অদেখা server internals |
| Permission check কোথায়? | authorized source + execution | unexecuted branch ঠিক কি না |
| Packaged app-এ কী আছে? | উপযুক্ত artifact inspection | সব remote backend rule |
| Refresh-এ কী থাকে? | controlled UI/API observation | backup recovery guarantee |

REA বা অন্য tool-এর নাম বড় হলেই তার capability অসীম হয় না। Tool unavailable হলে “source inspect করা যায়নি” লিখে browser evidence নিয়ে এগোনো যায়। Tool চালানো ও প্রশ্নের উত্তর পাওয়া একই ঘটনা নয়।

## Baseline খাতা

```json
{
  "target": "local teaching checkout",
  "command": "python3 -m unittest discover -s tests",
  "execution_status": "NOT_RUN",
  "reason": "example record; replace after actual execution",
  "existing_changes": "inspect before editing",
  "next_action": "locate test entry point"
}
```

`NOT_RUN` ইচ্ছাকৃত। বানানো output দিয়ে baseline পূরণ করলে পরের improvement-এর হিসাবও বানানো হয়ে যায়। Test fail করলে আগে দেখো failure আগেই ছিল কি না। নতুন code-কে সব দোষ দেওয়া বা সব পুরোনো failure উপেক্ষা করা—দুটিই diagnosis নষ্ট করে।

**নিজে করো—Q02:** code-এ একটি `TicketService` পেয়েছ। Agent দ্বিতীয় service বানাতে চায়। সিদ্ধান্ত নেওয়ার আগে কোন তিনটি তথ্য চাইবে? [উত্তর](../appendices/B-workbook.md)।

<!-- book-navigation -->

---

[← চেহারার নিচে যে সিস্টেম](../chapters/01-surface-system.md) · [সূচি](../README.md) · [প্রমাণের খাতা ও অনুমানের সীমানা →](../chapters/03-evidence.md)
