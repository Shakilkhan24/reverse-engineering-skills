# ১২ · পরিচয় আছে, অনুমতি আছে কি

Authentication বলে তুমি কে। Authorization বলে তুমি **এই resource-এ এই কাজ** করতে পারো কি না। অফিসের ID card থাকলেই সব আলমারির চাবি পাওয়া যায় না।

## আমাদের test cast

![Alice workspace A-এর এবং Bob workspace B-এর member; Bob-এর A-এর ticket পড়ার পথ server-এ বন্ধ](../assets/figures/26-workspace-doors.png)

Bob-কে `t_A`-এর সঠিক ID দেওয়া হলো। এখন অনুমতি মিলেছে? না—ঠিকানা জানা আর দরজা খোলার অনুমতি আলাদা। Request পাঠিয়ে denial দেখবে; তারপর Alice দিয়ে আবার পড়ে নিশ্চিত হবে ticket-ও বদলায়নি।

| Actor | Membership | Resource | Intended result |
|---|---|---|---|
| alice | ws_a | ws_a/t1 read | allow |
| bob | ws_b | ws_a/t1 read | deny |
| bob | ws_b | ws_a/t1 update | deny |
| alice, membership revoked | none | ws_a/t1 read | deny |

Button লুকিয়ে রাখা presentation behavior। Server-side enforcement প্রয়োজন; request-এর client-supplied `actor_id`-কে সত্য ধরে নেওয়া যাবে না। Permission প্রতিটি প্রাসঙ্গিক request ও resource boundary-তে যাচাই করা উচিত। [OWASP authorization guidance](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html)।

## Boundary ধরে ভাবো

```text
Untrusted client input
        ↓
Authenticated server context
        ↓
Permission + resource scope
        ↓
Domain operation → persistence
```

Lab-এ actor string সরাসরি function-এ দেওয়া হয়। কারণ lab authentication শেখায় না; caller-কে trusted ধরে authorization logic দেখায়। HTTP server বানালে body থেকে ওই string নিয়ে পাশ করানো নিরাপদ implementation হবে না।

## শুধু happy path test নয়

```text
Given: bob কেবল ws_b-এর member
And: t1 ws_a-এর ticket
When: bob t1 পড়তে বা update করতে চায়
Then: request rejected
And: response-এ title/description প্রকাশিত নয়
And: ticket version ও state অপরিবর্তিত
```

Denied response এলো, কিন্তু write ইতিমধ্যে হয়ে গেছে—এমন bug ধরতে `And` অংশ দরকার। ID guessed হলেও denial চাই; ID random হওয়া authorization-এর বিকল্প নয়।

## Permission কোথায় ছড়িয়ে থাকে

| পথ | সাধারণ ভুল | কী পরীক্ষা |
|---|---|---|
| Detail endpoint | unscoped ID lookup | অন্য workspace ID |
| Search | global index result | tenant filter bypass নয়, scoped result check |
| Attachment | public download URL | revoked actor access |
| Export | worker context হারায় | export job-এর owner scope |
| WebSocket | connect-এ একবার check | revoke-এর পরে নতুন event/edit |

আগে ডাউনলোড করা তথ্য user-এর device থেকে জাদুর মতো ফিরিয়ে নেওয়া যায় না। Revocation policy-তে future server access, open connection ও local cache আলাদা করে আলোচনা করতে হয়।

## Original-এর দুর্বলতা পেলে

Observation লিখবে; replacement-এর জন্য নিরাপদ আচরণ বেছে নিলে fidelity difference-টিও লিখবে। “সঠিকভাবে clone” করার নামে sensitive data leak পুনরায় তৈরি করার প্রয়োজন নেই। তদন্তে অনুমোদিত account ও synthetic data ব্যবহার করলে ফল review করাও সহজ হয়।

**নিজে করো—Q12:** Search API tenant-scoped কিন্তু export worker global query করে। Detail API test পাস করলেও কী ঝুঁকি থাকে? [উত্তর](../appendices/B-workbook.md)।

<!-- book-navigation -->

---

[← নেটওয়ার্কের চিহ্ন কী বলে](../chapters/11-network.md) · [সূচি](../README.md) · [সিস্টেমের গল্প শোনার যন্ত্র →](../chapters/13-observability.md)
