# ০৯ · ডেটার মালিক, কপি ও বিদায়

নীরা প্রশ্ন করল, “Ticket কোথায়?” আরিফ বলল, “Database-এ।” কিন্তু title ছিল browser cache-এ, search index-এ, email-এ, backup-এও। একই তথ্যের অনেক জীবন আছে।

![Ticket-এর authoritative store এবং cache, search, dashboard, notification-এর সম্পর্ক](../assets/figures/05-data-map.png)

**ছবি পড়ো:** তীর মানে তথ্যের প্রবাহ; সব store সমান authority নয়। এটি candidate replacement model, original physical schema নয়।

## Conceptual model আগে

```text
User ── Membership ── Workspace ── Ticket ── Comment
                                     └──── Attachment
Ticket change ── Activity / Outbox ── Derived views
```

একজন user একাধিক workspace-এর member হতে পারেন। তাই user table-এ একটিমাত্র `workspace_id` বসানো আমাদের এই requirement পূরণ করবে না। UI-তে workspace switcher আছে বলে exact schema জানা যায় না; তবে বহু workspace membership-এর আচরণ model করা যায়।

## একটি assignment-এর তিনটি ঘড়ি

| সময় | Durable ticket | Details cache | Search projection |
|---:|---|---|---|
| t=0 | arif, v7 | arif, v7 | arif, v7 |
| t=100ms | nira, v8 | arif, v7 | arif, v7 |
| t=150ms | nira, v8 | nira, v8 | arif, v7 |
| t=1500ms | nira, v8 | nira, v8 | nira, v8 |

এটি বানানো timeline। এই সময়গুলো benchmark নয়। এখানে stale search দিয়ে database failure ঘোষণা করা ভুল; আবার search latency contract ভাঙলে “database ঠিক আছে” বলেও user impact অস্বীকার করা যাবে না।

## Delete একটি বহু-ধাপের ঘটনা

![Delete-এর পরে primary store, search, attachment ও backup-এ ticket-এর আলাদা অবস্থা](../assets/figures/23-delete-shadows.png)

Primary store-এ `deleted v10`, অথচ search-এ পুরোনো title। এবার worker দেরিতে `updated v9` পেল। Version না দেখে সেটি লিখলে ticket আবার “জীবিত” দেখাতে পারে। ছবির চারটি ঘরের জন্য আলাদা cleanup বা retention rule লাগবে।

| কপি | সম্ভাব্য প্রয়োজন | যাচাই |
|---|---|---|
| Primary record | tombstone বা hard delete | normal read-এ unavailable |
| Search | document removal | query-তে আর ফেরে না |
| Cache | invalidate বা expiry | পুরোনো response আর accessible নয় |
| Attachment | access revoke / purge policy | direct URL-এর access |
| Audit | প্রয়োজনীয় সীমিত history | sensitive payload minimization |
| Backup | retention ও restore handling | restore-এর পরে deletion পুনঃপ্রয়োগের policy |

Retention product ও প্রযোজ্য requirements অনুযায়ী ঠিক করতে হয়; এখানে নির্দিষ্ট আইন বা সময়সীমা নির্ধারণ করা হচ্ছে না। “Soft delete আছে” মানে privacy lifecycle সম্পন্ন নয়।

## Out-of-order event-এর dry run

Worker প্রথমে `ticket.updated v9` পেল, পরে দেরিতে `v8`। যদি প্রতিবার অন্ধভাবে projection overwrite করে, search পিছিয়ে যাবে। একটি design হলো per-ticket version দেখে পুরোনো update উপেক্ষা করা। তবে partial event payload হলে “বড় version পেলেই যথেষ্ট” সব সময় ঠিক নয়; snapshot event বনাম delta event-এর semantics জানতে হবে।

Delete tombstone-এর version ১০। দেরিতে version ৯-এর update এলে deleted ticket আবার জীবিত করা যাবে না। এই resurrection bug সাধারণ create/read test-এ ধরা পড়ে না।

## কোন প্রশ্ন agent-কে করবে

“এই field-এর source of truth কোনটি? কোন কপি rebuild করা যায়? কোন event হারালে data irrecoverable? Deletion হলে derived copy কীভাবে পরিষ্কার হবে?” উত্তরগুলো data ownership design-এর ভিত্তি।

**নিজে করো—Q09:** database থেকে ticket মুছে search-এ রেখে দিলে কী কী mismatch হয়? [উত্তর](../appendices/B-workbook.md)।

<!-- book-navigation -->

---

[← ব্যবসার নিয়মকে পরীক্ষাযোগ্য করা](../chapters/08-domain-rules.md) · [সূচি](../README.md) · [একই সময়ে দুজন: সময়ের ফাঁদ →](../chapters/10-time-concurrency.md)
