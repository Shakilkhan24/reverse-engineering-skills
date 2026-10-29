# ১৭ · দুই সিস্টেমের মুখোমুখি পরীক্ষা

“আমার code চলছে”—একটি claim। “Reference-এর agreed behavior-এর সঙ্গে মেলে”—আরেকটি। দ্বিতীয়টির জন্য প্রথমটির বাইরে comparison দরকার।

## একই প্রশ্ন, তুলনাযোগ্য condition

| বিষয় | Reference | Replacement |
|---|---|---|
| Actor | permitted member A | equivalent permission fixture |
| Initial state | open ticket, version X | corresponding open ticket |
| Input | valid assignment | semantically same assignment |
| Observe | response, reload, list, history | একই observable surfaces |
| Timing | known wait condition | equivalent wait condition |

Literal ID আলাদা হতে পারে। তাই `t_ref_99` ও `t_local_17` mapping করে compare করো। কিন্তু workspace ID বা assignee identity নির্বিচারে মুছে দিলে permission mismatch লুকিয়ে যাবে।

## Oracle কী

যার সঙ্গে actual ফল তুলনা করছ, সেটিই test oracle। এটি verified reference observation, agreed specification বা invariant হতে পারে। Generated implementation-এর response নিজেই snapshot করে “এটাই expected” বললে ভুল behavior-ও স্থায়ী test হয়ে যায়।

```python
# শিক্ষামূলক normalization; পূর্ণ comparison framework নয়
def comparable(ticket):
    return {
        "title": ticket["title"],
        "status": ticket["status"],
        "workspace": ticket["workspace"]
    }
```

এই function version বাদ দিয়েছে। Version contract যাচাইয়ের test-এ এটি যথেষ্ট নয়। Normalization কী বাদ দিল এবং কেন—review-এ তা স্পষ্ট থাকতে হবে।

![Feature ও verification dimension-এর synthetic heatmap](../assets/figures/12-verification.png)

**ছবি পড়ো:** Create-এর happy path pass হওয়া recovery test-এর `NOT RUN` ঘরকে সবুজ করে না। Chart-এর ফল কাল্পনিক; বাস্তবে চালানো lab test-এর ফল [verification report](../reports/verification.md)-এ আলাদা থাকবে।

## একটি discrepancy-র জীবন

![সংশোধনের আগে list-এ আরিফ এবং details-এ নীরা; সংশোধনের পরে দুটিতেই নীরা](../assets/figures/30-cache-before-after.png)

বাঁয়ের ছবিতে API response বদলানো ছাড়াও bug হতে পারে: details নতুন state নিয়েছে, list পুরোনো cache দেখাচ্ছে। Fix করার পরে ডানের ছবি পেয়েছ—এবার reload-ও দাও। দুই check মিলে সাময়িক UI patch ও স্থায়ী ফল আলাদা করতে সাহায্য করবে।

```text
D-014
Expected: assignment-এর পরে details ও list একই assignee দেখায়
Actual: details=nira, list=arif
Reproduce: fixture v7 → assign → return to list
Evidence: screenshot pair + response + cache inspection
Suspected cause: list cache stale
Confirmed cause: successful mutation path list key invalidate করে না
Fix: সংশ্লিষ্ট cache update/invalidate
Regression: assign → list → reload → assert same assignee
Status: fixed; rerun না হওয়া পর্যন্ত verified নয়
```

`suspected` ও `confirmed` cause আলাদা রাখলে investigation সৎ থাকে। Cache invalidate করার পরে symptom সরে গেলেও root cause-এর সব ব্যাখ্যা স্বয়ংক্রিয়ভাবে প্রমাণিত হয় না; relevant execution path পরীক্ষা করো।

## Comparison-এর আরও তিন ধরনের পরীক্ষা

**Boundary:** title ১২০ বনাম ১২১ code point।  
**Metamorphic:** একই valid create retry করলে ticket count না বাড়া; exact random ID জানা লাগে না।  
**Failure:** external provider বন্ধ হলেও committed ticket থাকা এবং কাজ pending থাকা।

কোনো captured reference আর live reference একই build নয়? Result-এ version mismatch limitation লেখো। Nondeterministic model output হলে exact string equality-এর বদলে task-specific rubric লাগবে; orchestration permission-এর মতো deterministic boundary তবু exact test করা যায়।

**নিজে করো—Q17:** সব timestamp বাদ দিলে কখন test সহজ হয় এবং কখন bug চাপা পড়ে? [উত্তর](../appendices/B-workbook.md)।

<!-- book-navigation -->

---

[← একটি সম্পূর্ণ slice ও চলমান lab](../chapters/16-vertical-lab.md) · [সূচি](../README.md) · [দোকান, সম্পাদক, AI ও অফলাইন জীবন →](../chapters/18-four-worlds.md)
