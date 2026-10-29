# ০১ · চেহারার নিচে যে সিস্টেম

রাত ২টা ১৭। আরিফ AI-কে বলল, “এই support app-টা বানাও।” একটু পর sidebar, ticket list, search—সব হাজির। সে আনন্দে চা আনতে গেল। ফিরে এসে refresh দিল। Ticket উধাও। চা গরম, database ঠান্ডা—কারণ database-ই ছিল না!

নীরা বলল, “তোমার বাটন একটি ছবি বদলেছে। আমরা চেয়েছিলাম একটি নির্ভরযোগ্য ঘটনা ঘটুক।” এই বইয়ে তাদের সঙ্গে আমরা **RelayDesk** নামের কাল্পনিক support system তৈরি করার যুক্তি শিখব। আরিফের ভুলগুলো তোমার অনুশীলনের সুযোগ। এখানে কোনো বাস্তব RelayDesk সেবার গোপন তথ্য আবিষ্কারের দাবি নেই।

## দৃশ্য ১: একই স্ক্রিন, আলাদা সত্য

![দুটি একই ticket list; refresh-এর পরে A খালি, B-তে t_101 রয়ে গেছে](../assets/figures/15-refresh-reveal.png)

ওপরের দুই screen-এ তফাত নেই। নিচে Refresh-এর ফল দেখা যাচ্ছে। অ্যাপ A-তে ticket উধাও; B-তে নতুন read-এ সেটি পাওয়া গেছে। প্রথম screenshot থেকে এই পার্থক্যটি ধরতে পারতে?

এবার নিজের app-এ একই খেলা: একটি item তৈরি করো, তার ID লিখে রাখো, তারপর page আবার খোলো। “দেখাচ্ছে” থেকে “ফিরে পাওয়া যাচ্ছে”—দুটি ছোট কিন্তু আলাদা observation হলো।

| ঘটনা | সংস্করণ A | সংস্করণ B | কী পরীক্ষা করবে |
|---|---|---|---|
| Create চাপলে ticket দেখা যায় | browser memory-তে object | server-confirmed record | নতুন session-এ পড়া |
| আরেক workspace-এর ID দেওয়া | সব record ফেরত | permission যাচাই | অন্য test actor দিয়ে read |
| response হারিয়ে retry | নতুন ticket | একই logical operation replay | count ও ID তুলনা |
| email provider বন্ধ | save-ও ব্যর্থ | ticket থাকে, delivery pending | আলাদা failure injection |

এই টেবিলের B আমাদের সম্ভাব্য design; original-এর আবিষ্কৃত আচরণ নয়। কোনো ছোট prototype-এ A-ও যথার্থ হতে পারে, যদি scope-এ persistence না থাকে। ভুলটি হলো scope না বলে “সব complete” ঘোষণা করা।

![দৃশ্যমান UI থেকে data ও recovery পর্যন্ত আচরণের স্তর](../assets/figures/01-system-layers.png)

**ছবি পড়ো:** ওপরের স্তর দেখা সহজ; নিচের স্তরের জন্য আলাদা প্রশ্ন প্রয়োজন। বাক্সের আকার complexity-এর শতাংশ বোঝায় না। কোনো সর্বজনীন “৫% UI, ৯৫% backend” মাপ এখানে নেই।

## Reverse engineering বলতে এখানে কী বোঝাচ্ছি

একটি অজানা সফটওয়্যারের **পর্যবেক্ষণযোগ্য নিয়ম** বুঝে একটি পরীক্ষাযোগ্য model তৈরি করা। তারপর সেই model অনুযায়ী replacement বানানো হলো reconstruction। Source analysis, browser observation, protocol inspection ও binary analysis প্রমাণের ভিন্ন পথ; সব কাজেই সব পথ দরকার হয় না।

এই বইয়ের কেন্দ্র product behavior এবং AI-assisted reconstruction। Assembly, exploit development বা firmware decompilation-এর পূর্ণ কোর্স এটি নয়। ওই পথে গেলেও “প্রমাণ কোথায়?” প্রশ্নটি কাজে লাগবে।

**Behavioral equivalence** মানে নির্দিষ্ট input, state ও condition-এ দরকারি output সমতুল্য। Original PostgreSQL ব্যবহার করেছে কি না অজানা হলেও replacement SQLite দিয়ে একটি ছোট শিক্ষামূলক contract পূরণ করতে পারে। একই technology ব্যবহার করলেই একই আচরণ হবে, এমন নিশ্চয়তাও নেই।

## নিজের fidelity চুক্তি বানাও

ধরা যাক, তোমার লক্ষ্য শুধু ticket তৈরি ও পড়া। তাহলে লিখতে পারো:

```text
Included: create, list, refresh persistence, workspace isolation
Visual target: layout ও readable states
Excluded: real email, billing, mobile offline sync
Critical gate: অন্য workspace-এর ticket প্রকাশ পাবে না
Evidence boundary: অনুমোদিত demo accounts এবং local repository
```

এবার এই scope ধরে চারটি check চালাবে: create, list, reload এবং অন্য workspace দিয়ে read। Email পাঠানোর কাজটি এই iteration-এ নেই।

## ক্ষুদ্র dry run

১. একটি ticket তৈরি করলে UI-তে `t_101` এলো। লিখলে: “এই session-এ item দৃশ্যমান।”  
২. Refresh-এর পরও item আছে। লিখলে: “এই reload-এ state টিকে আছে।”  
৩. Browser storage মুছে অন্য অনুমোদিত session-এ একই ID এলো। Server persistence-এর পক্ষে evidence আরও শক্ত হলো।  
৪. তবু “database engine PostgreSQL” বলা গেল না। Observable ফল দিয়ে অদৃশ্য implementation-এর সব পথ আলাদা করা যায় না।

**নিজে করো—Q01:** success toast দেখেছ। “ডেটা স্থায়ী হয়েছে” দাবিটি যাচাই করতে পরের দুটি পরীক্ষা কী হবে? [উত্তর পরে দেখো](../appendices/B-workbook.md)।

<!-- book-navigation -->

---

[সূচি](../README.md) · [অজানা রিপোজিটরিতে প্রথম অভিযান →](../chapters/02-reconnaissance.md)
