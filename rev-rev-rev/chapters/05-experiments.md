# ০৫ · গোয়েন্দার মতো পরীক্ষা সাজাও

আরিফ দুবার click করল, একটি ticket দেখল। “Server deduplicate করে!” নীরা browser network panel খুলল। দ্বিতীয় request-ই যায়নি। গোয়েন্দা একটি সন্দেহভাজনকে না দেখেই নির্দোষ ঘোষণা করেছিল।

## প্রশ্নকে hypothesis-এ ভাঙো

![দুই click-এর একটি ঘটনায় এক request, অন্য ঘটনায় দুই request; দুটিতেই list-এ একটি ticket](../assets/figures/19-two-clicks.png)

দুইবার click করে একটি card দেখলে ছবির A ও B—দুটিই সম্ভব। Network log খুলে request গুনলেই তাদের আলাদা করা শুরু হয়। এরপর persisted ID ও count দেখবে; list-ও duplicate লুকিয়ে রাখতে পারে।

প্রশ্ন: একই submission আবার এলে কী হয়?

| Hypothesis | কী ব্যাখ্যা করে | আলাদা করার পরীক্ষা |
|---|---|---|
| H1: client দ্বিতীয় click আটকায় | একটি visible ticket | actual request count |
| H2: server একই operation replay করে | দুই request, এক record | same key + payload |
| H3: UI duplicate লুকায় | list-এ একটি item | authorized API count/IDs |
| H4: কেবল sequential retry নিরাপদ | ধীরে retry-এ এক record | overlapping requests |

“আরও screenshot” সব hypothesis আলাদা করবে না। কী মাপলে ব্যাখ্যাগুলো আলাদা ফল predict করে, সেই observation খোঁজো।

## EXP-001: শুকনো মহড়া

নিচের ফল **কল্পিত expected result**, real capture নয়।

| ধাপ | Actor | Key | Title | H2 হলে response | মোট ticket |
|---|---|---|---|---|---:|
| ১ | alice | k1 | Login failure | t1 | ১ |
| ২ | alice | k1 | Login failure | t1 replay | ১ |
| ৩ | alice | k2 | Login failure | t2 | ২ |
| ৪ | alice | k1 | Changed title | conflict | ২ |

Control: একই workspace, actor, application version। Variable: key; চতুর্থ ধাপে payload mismatch আলাদা subcase। Observe: request সংখ্যা, response ID, persisted count, outbox count। Reset: প্রতিটি independent run-এর আগে নতুন fixture। পূর্ণ card: [experiment.json](../examples/experiment.json)।

## কোন পরীক্ষা আগে করবে

![পাঁচটি কাল্পনিক investigation-এর effort ও priority তুলনা](../assets/figures/03-experiment-priority.png)

**ছবি পড়ো:** toy score = impact × uncertainty ÷ effort। Impact ১–৫, uncertainty ০–১, effort ঘণ্টায়। এটি সিদ্ধান্ত-সহায়ক অনুমান, পরিসংখ্যানগত probability বা universal law নয়। Tenant leak-এর মতো critical boundary score কম হলেও release gate থাকতে পারে।

মূল লেখায় impact, uncertainty, consequence ও information gain-সহ সমৃদ্ধ heuristic আছে। কাজে impact ও consequence একই অর্থে ব্যবহার করলে double-counting হয়। তাই এই চার্টে ছোট model নিয়েছি; বেশি factor নিলে প্রত্যেকটির পৃথক অর্থ লিখতে হবে।

## গভীরে যাও: information gain-এর অর্থ

ধরো, H1 ও H2 দুটিই বর্তমান screenshot-এর সঙ্গে মিলে যায়। নতুন screenshot দুটির জন্যই একই রকম হবে; তাই আলাদা করার ক্ষমতা কম। Network request count H1-এর ক্ষেত্রে ১ এবং H2-এর ক্ষেত্রে ২ predict করলে পরীক্ষাটি বেশি তথ্যবহুল।

Formal probability model থাকলে entropy দিয়ে uncertainty মাপা যায়। এখানে probability distribution নেই; তাই “information gain ৮৭%” বানাচ্ছি না। **Competing explanation বাদ দেওয়ার ক্ষমতা** হিসেবে ধারণাটি ব্যবহার করছি।

## Experiment নষ্ট হওয়ার চারটি পথ

- একই সঙ্গে role, payload ও environment বদলালে ফলের কারণ আলাদা করা কঠিন।
- প্রথম run-এর data পরের run-এ থাকলে duplicate policy ভুল বোঝা যায়।
- UI cache-কে durable store মনে করলে wrong oracle হয়।
- একটি timeout-কে server failure ধরে নিলে ইতিমধ্যে committed operation চোখ এড়িয়ে যায়।

**নিজে করো—Q05:** search stale। Cache delay ও asynchronous index—এই দুই explanation আলাদা করতে কী evidence চাইবে? শুধু delay দিয়ে কী বলতে পারবে না? [উত্তর](../appendices/B-workbook.md)।

<!-- book-navigation -->

---

[← পাতার তালিকা থেকে আচরণের মানচিত্র](../chapters/04-product-map.md) · [সূচি](../README.md) · [একটি বাটনের আট রকম জীবন →](../chapters/06-ui-state.md)
