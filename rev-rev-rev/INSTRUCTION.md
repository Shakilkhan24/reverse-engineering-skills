# THE REVERSE ENGINEERING MASTERY HANDBOOK
## অদৃশ্য Software System-কে বুঝতে শেখা: Observation থেকে Production-Grade Reconstruction পর্যন্ত

**একটি গল্প, একটি Engineering দর্শন, একটি Investigation Playbook এবং AI যুগের Software Builder-এর জন্য পূর্ণাঙ্গ শিক্ষাযাত্রা**

---

## প্রস্তাবনা: যে Software-কে তুমি দেখছ, সেটাই কি আসল Software?

রাত ২টা ১৭ মিনিট।

আরিফ তার কম্পিউটারের সামনে বসে আছে। স্ক্রিনে একটি Customer Support SaaS application খোলা। দেখতে আধুনিক, পরিষ্কার, সুন্দর। বাম দিকে sidebar, মাঝখানে ticket list, ডান দিকে conversation panel। উপরে search bar, নিচে comment box, পাশে assignment dropdown।

সে অনেকক্ষণ ধরে application-টি পর্যবেক্ষণ করছে।

তার মাথায় একটি চিন্তা এসেছে:

“আমি চাইলে এই application-এর মতো একটি application তৈরি করতে পারি। UI দেখব, screenshot নেব, AI coding agent-কে দেব, তারপর বলব—পুরো application-টি clone করো।”

সে একটি শক্তিশালী AI Agent খুলল।

Prompt লিখল:

> Reconstruct this application. Make it look and behave exactly like the original. Use modern architecture and production-ready code.

কয়েক মিনিট পর Agent তাকে একটি সুন্দর application দেখাল।

Sidebar আছে। Ticket list আছে। Search আছে। Assignment dropdown আছে। Button-গুলো কাজ করছে বলেও মনে হচ্ছে।

আরিফ খুশি।

কিন্তু পরের দিন যখন সে একটু গভীরভাবে পরীক্ষা করতে শুরু করল, তখন সমস্যাগুলো একে একে বেরিয়ে এল।

- Page refresh দিলে ticket হারিয়ে যায়।
- একজন user অন্য workspace-এর ticket দেখতে পারে।
- একই button দুবার চাপলে duplicate ticket তৈরি হয়।
- Notification failure হলে পুরো operation-এর অবস্থা অস্পষ্ট হয়ে যায়।
- Search result পুরোনো data দেখায়।
- API error-এর format অসামঞ্জস্যপূর্ণ।
- Application-টি দেখতে original-এর মতো হলেও keyboard navigation কাজ করে না।
- Database migration চালালে পুরোনো data নষ্ট হয়।
- AI Agent দাবি করেছে যে সব feature complete, কিন্তু বাস্তবে অনেক feature শুধু mock data দিয়ে তৈরি।

আরিফ তখন বুঝতে পারল, সে একটি application-এর **চেহারা পুনর্নির্মাণ করেছে, কিন্তু তার আচরণ পুনর্নির্মাণ করেনি।**

ঠিক তখনই তার mentor নীরা তাকে একটি প্রশ্ন করল।

“তুমি কি জানো, original application-এর একটি ticket তৈরি হওয়ার পর থেকে সেটি user-এর কাছে দৃশ্যমান হওয়া পর্যন্ত কী কী ঘটে?”

আরিফ বলল, “API call হয়, database-এ save হয়, তারপর UI update হয়।”

নীরা হাসল।

“এটাই সমস্যা। তুমি একটি সম্ভাব্য গল্প বলেছ। কিন্তু তুমি কি সেটি পর্যবেক্ষণ করেছ? Database-এর ভেতরে কী ঘটে তুমি জানো? Notification synchronous, নাকি asynchronous? Search indexing সঙ্গে সঙ্গে হয়, নাকি কিছু সময় পরে? User-এর permission কোথায় যাচাই হয়? Request timeout হলে ticket তৈরি হয়েছিল কি না, তুমি কীভাবে জানবে? একই request পুনরায় এলে কী হবে?”

আরিফ চুপ করে রইল।

নীরা এবার বলল:

**“Reverse Engineering হলো অজানা system সম্পর্কে বিশ্বাস তৈরি করার প্রক্রিয়া—কিন্তু সেই বিশ্বাসকে evidence দিয়ে পরীক্ষা করতে হয়।”**

এই মুহূর্ত থেকেই আরিফের আসল যাত্রা শুরু হলো।

এই বইয়ের উদ্দেশ্যও ঠিক এখান থেকেই শুরু।

---

# অধ্যায় ১: Reverse Engineering-এর প্রথম সত্য—Surface আর System এক জিনিস নয়

একটি Software Product-কে একটি iceberg হিসেবে কল্পনা করো।

সমুদ্রের ওপরে যতটুকু দেখা যায়, সেটি হলো product-এর visible surface। কিন্তু সেই surface-এর নিচে থাকে আরও অনেক layer।

একটি button-এর পেছনে থাকতে পারে:

- UI state management
- Input validation
- Authentication
- Authorization
- API contract
- Business rules
- Database transaction
- Event publication
- Background worker
- Notification provider
- Search index
- Cache invalidation
- Error recovery
- Logging and tracing

একটি button দেখতে যতটা ছোট, তার পেছনের system ততটা ছোট নাও হতে পারে।

তবে এখানে একটি গুরুত্বপূর্ণ সতর্কতা আছে।

Iceberg analogy-তে কখনো কখনো বলা হয়, visible অংশ মাত্র ৫%, আর বাকি ৯৫% লুকানো। এটি একটি শিক্ষামূলক metaphor, সর্বজনীনভাবে মাপা কোনো engineering statistic নয়। বাস্তবে প্রতিটি application-এর জটিলতা আলাদা।

মূল শিক্ষা হলো: **যা দেখা যায়, তা দিয়ে পুরো system-এর পরিধি নির্ধারণ করা যায় না।**

## ১.১ একই button, দুটি সম্পূর্ণ ভিন্ন system

ধরা যাক, দুটি application-এ `Create Ticket` button আছে।

প্রথম application-এ:

1. Button চাপলে একটি object তৈরি হয়।
2. Object-টি frontend memory-তে থাকে।
3. UI-তে ticket দেখানো হয়।
4. Refresh দিলে ticket হারিয়ে যায়।

দ্বিতীয় application-এ:

1. Button চাপলে input validate হয়।
2. Server user identity যাচাই করে।
3. Workspace authorization পরীক্ষা করে।
4. Domain rules প্রয়োগ হয়।
5. Database-এ transaction সম্পন্ন হয়।
6. Activity event সংরক্ষণ বা publish করা হয়।
7. Notification job queue-তে যেতে পারে।
8. Search index পরে update হতে পারে।
9. UI server-confirmed state দেখায়।
10. Failure হলে উপযুক্ত recovery path সক্রিয় হয়।

দুটি application দেখতে একই রকম হতে পারে। কিন্তু তাদের reliability, security, persistence এবং failure behavior এক নয়।

এখানে আরেকটি গভীর বিষয় আছে।

দ্বিতীয় application-টি যদি database হিসেবে PostgreSQL ব্যবহার করে, আর তোমার reconstruction যদি MySQL ব্যবহার করে, তাতেই reconstruction ব্যর্থ হয়ে যায় না। যদি তোমার লক্ষ্য হয় observable behavior এবং domain semantics পুনর্নির্মাণ করা, তাহলে database engine-এর অভিন্নতা সব সময় প্রয়োজনীয় নয়।

অর্থাৎ, **ভেতরের implementation একই হওয়া এবং বাইরের আচরণ সমতুল্য হওয়া দুটি আলাদা বিষয়।**

## ১.২ কোন জিনিসগুলো আসলে পুনর্নির্মাণ করতে হবে?

প্রথমে একটি Product Fidelity Matrix তৈরি করো।

| Dimension | কী জানতে হবে? |
|---|---|
| UI and Interaction | Screen, state, navigation, validation কেমন? |
| Feature Completeness | Critical user journey-গুলো কাজ করে কি? |
| Domain Semantics | Business rules এবং state transitions কী? |
| API Compatibility | Request, response, error contract কী? |
| Data and Persistence | Data কোথায়, কীভাবে, কতক্ষণ থাকে? |
| Authorization | কে কোন resource ব্যবহার করতে পারে? |
| Concurrency | একাধিক operation একসঙ্গে এলে কী হয়? |
| Asynchronous Processing | Queue, retries, scheduling কীভাবে আচরণ করে? |
| Integrations | Email, payment, storage বা external service কীভাবে যুক্ত? |
| Observability | Failure খুঁজে বের করার জন্য কী telemetry দরকার? |
| Performance | Latency, throughput, resource usage কতটা গুরুত্বপূর্ণ? |
| Resilience | Timeout, outage, duplicate request হলে কী হয়? |
| Deployment | Build, migration, release, rollback কীভাবে হয়? |
| Accessibility | Keyboard, focus, screen reader, responsive behavior কী? |
| Maintainability | Code পরিবর্তন ও পরীক্ষা করা কতটা সহজ? |

প্রতিটি dimension-এর জন্য পাঁচটি প্রশ্ন করো:

1. কী জানা আছে?
2. কী সরাসরি পর্যবেক্ষণ করা হয়েছে?
3. কী অনুমান করা হচ্ছে?
4. কী এখনও অজানা?
5. কোন evidence দিয়ে বিষয়টি যাচাই করা যাবে?

এই প্রশ্নগুলো তোমার investigation-এর compass।

## ১.৩ একজন Expert কীভাবে চিন্তা করে?

একজন Beginner দেখে:

“এই button-এর রং নীল।”

একজন Intermediate Developer ভাবে:

“এই button একটি API call করছে।”

একজন Senior Engineer প্রশ্ন করে:

“Request failure হলে কী হবে? User permission কোথায় যাচাই হচ্ছে? Retry করলে duplicate operation হবে কি? State কোথায় authoritative? UI কীভাবে server state-এর সঙ্গে synchronize হচ্ছে?”

একজন Reconstruction Engineer আরও এক ধাপ এগিয়ে যায়:

“এই প্রশ্নগুলোর কোনটির উত্তর আমার কাছে evidence দিয়ে আছে? কোনটি শুধু অনুমান? কোন পরীক্ষা করলে সবচেয়ে কম সময়ে সবচেয়ে বেশি uncertainty দূর হবে?”

এটাই প্রথম বড় পরিবর্তন।

তুমি শুধু software তৈরি করতে শিখছ না। তুমি **software সম্পর্কে নির্ভরযোগ্য জ্ঞান তৈরি করতে শিখছ।**

---

# অধ্যায় ২: প্রথম Investigation—Code লেখার আগে System-কে চিনতে শেখা

পরদিন নীরা আরিফকে কোনো code লিখতে দিল না।

বরং তাকে একটি existing repository দিল।

নির্দেশনা ছিল:

“আগামী ৩০ মিনিটে তুমি আমাকে বলবে, এই project-এ কী আছে, কী নেই, কী চলছে, এবং কী পরিবর্তন করলে সবচেয়ে বেশি ঝুঁকি তৈরি হতে পারে।”

আরিফ প্রথমে সরাসরি code generation শুরু করতে চেয়েছিল। কিন্তু নীরা তাকে থামিয়ে দিল।

“একটি অজানা repository-তে ঢুকে প্রথমেই সবকিছু rewrite করা মানে অন্ধকার ঘরে দেয়াল ভাঙা।”

## ২.১ Workspace Reconnaissance

প্রথম কাজ হলো existing environment সম্পর্কে ধারণা নেওয়া।

দেখতে হবে:

- Project instructions
- README এবং architecture documents
- Repository structure
- Language ও framework
- Package manager
- Runtime configuration
- Build এবং test scripts
- Existing tests
- Deployment manifests
- Infrastructure configuration
- Environment variables-এর names ও configuration structure
- Available browser, shell, API testing এবং source-analysis tools
- Existing implementation এবং known defects

উদাহরণ:

```text
relaydesk/
├── src/
│   ├── frontend/
│   ├── api/
│   ├── domain/
│   ├── workers/
│   └── integrations/
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── infra/
├── migrations/
├── docs/
└── reconstruction/
```

এই structure একটি illustrative example। কোনো বাস্তব project-এ folder-গুলো ভিন্ন হতে পারে।

এখানে গুরুত্বপূর্ণ বিষয় হলো folder-এর নাম মুখস্থ করা নয়। বরং প্রত্যেক অংশের responsibility এবং dependency বুঝতে চেষ্টা করা।

যেমন:

- `frontend/` কি সরাসরি API call করে?
- `domain/` কি business rules ধারণ করে?
- `workers/` কি background processing করে?
- `integrations/` কি external providers-এর সঙ্গে কথা বলে?
- `migrations/` কি database schema পরিবর্তন করে?
- `tests/` কি critical behavior যাচাই করে, নাকি শুধু code coverage বাড়ায়?

## ২.২ Existing Code-এর প্রতি শ্রদ্ধা

AI coding agent অনেক সময় নতুন করে code লিখতে ভালোবাসে। কিন্তু reconstruction project-এ পুরোনো code-এর মধ্যেই মূল্যবান evidence থাকতে পারে।

ধরা যাক, repository-তে একটি `TicketService` আছে।

Agent যদি সেটি না পড়ে নতুন `TicketManager`, `TicketEngine`, `TicketHandlerV2` তৈরি করে, তাহলে একই business logic-এর একাধিক সংস্করণ তৈরি হতে পারে।

এর ফলে:

- Validation আলাদা হয়ে যায়।
- Permission rules অসামঞ্জস্যপূর্ণ হয়।
- Tests ভুল implementation-কে cover করতে পারে।
- নতুন feature পুরোনো workflow ভেঙে দিতে পারে।

সুতরাং পরিবর্তনের আগে প্রশ্ন করো:

1. Existing component কি কাজ করছে?
2. তার contract কী?
3. তার test coverage কেমন?
4. কোন defect প্রমাণিত?
5. নতুন abstraction সত্যিই প্রয়োজন কি?

**Reconstruction মানেই Rewrite নয়।**

## ২.৩ Investigation Tool নির্বাচন

যদি Reverse Engineer Anything (REA) বা অনুরূপ কোনো tool উপলব্ধ থাকে, তাহলে প্রথমে তার actual capability, input requirements এবং output limitations বুঝতে হবে।

Tool-এর নাম দেখে ধরে নেওয়া যাবে না যে সেটি সব API, সব database, সব hidden logic অথবা পুরো backend আবিষ্কার করতে পারে।

প্রতিটি tool call-এর আগে একটি নির্দিষ্ট প্রশ্ন থাকা উচিত।

উদাহরণ:

- প্রশ্ন: Client কোন request পাঠায়?
- সম্ভাব্য tool: Authorized browser network inspection।
- প্রশ্ন: Local binary-তে কোন libraries আছে?
- সম্ভাব্য tool: Static binary analysis।
- প্রশ্ন: API error contract কী?
- সম্ভাব্য tool: Controlled API tests।
- প্রশ্ন: Existing code-এর কোন branch permission check করে?
- সম্ভাব্য tool: Source search এবং call-graph analysis।

যদি একটি tool-এর প্রয়োজনীয় capability না থাকে, তাহলে সেটি স্পষ্টভাবে লিখতে হবে।

Tool unavailable মানে কাজটি করা হয়েছে এমন দাবি করা নয়।

---

# অধ্যায় ৩: Evidence-এর বিজ্ঞান—Observation, Inference এবং Assumption

আরিফ এবার RelayDesk-এর ticket assignment workflow তদন্ত করতে শুরু করল।

সে দেখল, ticket assign করার পর screen-এ নতুন assignee-এর নাম দেখা যাচ্ছে।

সে বলল:

“তাহলে assignment database-এ save হয়ে গেছে।”

নীরা সঙ্গে সঙ্গে বলল:

“না। তুমি শুধু দেখেছ যে UI-তে নাম পরিবর্তন হয়েছে। Database persistence তুমি এখনও প্রমাণ করোনি।”

এই একটি পার্থক্যই reconstruction-এর মান বদলে দেয়।

## ৩.১ Evidence-এর ছয়টি শ্রেণি

### OBSERVED — সরাসরি দেখা হয়েছে

উদাহরণ:

একটি authorized test account দিয়ে ticket assign করার পর UI-তে assignee-এর নাম পরিবর্তিত হয়েছে।

এটি একটি observation।

কিন্তু এই observation শুধু নির্দিষ্ট account, version, environment এবং test condition সম্পর্কে তথ্য দেয়।

### DERIVED — পর্যবেক্ষণ থেকে হিসাব করে পাওয়া

উদাহরণ:

দশটি controlled request-এর response বিশ্লেষণ করে দেখা গেল, আটটি request একই error schema ব্যবহার করেছে।

এটি observed data থেকে derived ফলাফল।

### INFERRED — প্রমাণসমর্থিত ব্যাখ্যা

উদাহরণ:

দুটি workspace-এর user দিয়ে পরীক্ষা করার পর দেখা গেল, অন্য workspace-এর ticket access করতে গেলে request reject হয়।

এ থেকে ধারণা করা যায়, কোনো authorization rule কার্যকর আছে।

তবে কোন middleware, database policy অথবা service layer সেই check করছে, তা আলাদা evidence ছাড়া নিশ্চিত নয়।

### ASSUMED — সাময়িকভাবে ধরে নেওয়া হয়েছে

উদাহরণ:

Original database engine অজানা, তাই replacement-এর জন্য PostgreSQL নির্বাচন করা হয়েছে।

এটি একটি engineering assumption বা design decision হতে পারে। কিন্তু original system PostgreSQL ব্যবহার করে—এমন evidence নয়।

### UNKNOWN — এখনও অজানা

উদাহরণ:

Original application-এর internal notification queue কোন technology ব্যবহার করে, তা public observation থেকে নির্ধারণ করা যাচ্ছে না।

এই unknown লিখে রাখা উচিত।

### CONTRADICTED — শক্তিশালী evidence-এ আগের দাবি ভুল প্রমাণিত

প্রথমে মনে হয়েছিল ticket update-এর সঙ্গে search index সঙ্গে সঙ্গে update হয়।

পরে controlled test-এ দেখা গেল, কয়েক সেকেন্ড পরে search result পরিবর্তিত হচ্ছে।

তখন আগের hypothesis সংশোধন করতে হবে।

## ৩.২ Evidence Ledger তৈরি করা

প্রতিটি গুরুত্বপূর্ণ finding একটি stable identifier পাবে।

উদাহরণ:

| Field | Example |
|---|---|
| Evidence ID | E-017 |
| Question | Assignment কি refresh-এর পরও থাকে? |
| Observation | Refresh-এর পর নতুন assignee দেখা গেছে |
| Method | Authorized UI interaction |
| Context | RelayDesk test environment, version X |
| Classification | OBSERVED |
| Confidence | এই নির্দিষ্ট test-এর ফল সম্পর্কে উচ্চ |
| Limitation | একাধিক user ও concurrent update পরীক্ষা হয়নি |
| Related Requirement | REQ-ASSIGN-02 |
| Next Action | Concurrent assignment পরীক্ষা |

Confidence কোনো জাদুকরী সংখ্যা নয়। ৯০% confidence লিখলেই evidence শক্তিশালী হয়ে যায় না। Confidence-এর ভিত্তি হতে হবে experiment quality, sample coverage এবং alternative explanations।

## ৩.৩ Unknowns Register

একটি আলাদা register-এ লিখতে হবে কোন বিষয়গুলো এখনও অমীমাংসিত।

প্রতিটি unknown-এর সঙ্গে থাকবে:

- প্রশ্নটি কী?
- কেন গুরুত্বপূর্ণ?
- কোন subsystem প্রভাবিত?
- বর্তমান evidence কী?
- সম্ভাব্য ব্যাখ্যাগুলো কী?
- ভুল হলে কী ক্ষতি হতে পারে?
- কোন experiment প্রয়োজন?
- কোন access দরকার?
- পরবর্তী পদক্ষেপ কী?

উদাহরণ:

`U-008: Duplicate ticket submission-এর ক্ষেত্রে original system idempotency enforce করে কি না—অজানা।`

এটি গুরুত্বপূর্ণ, কারণ timeout-এর পরে retry করলে duplicate ticket তৈরি হতে পারে।

পরবর্তী action হতে পারে controlled test environment-এ repeated submission পরীক্ষা করা।

কিন্তু যদি original-এর access সীমিত থাকে এবং নির্ভরযোগ্য সিদ্ধান্ত নেওয়া সম্ভব না হয়, তাহলে unknown-টি লিখে রাখতে হবে। Replacement-এ robust idempotency implement করা যেতে পারে, তবে সেটিকে original-এর verified behavior বলা যাবে না।

## ৩.৪ Traceability Chain

সবচেয়ে গুরুত্বপূর্ণ সম্পর্কটি হলো:

**Evidence → Requirement → Design Decision → Implementation → Test → Result**

ধরা যাক:

- Evidence: Unauthorized user ticket update করতে পারে না।
- Requirement: User অবশ্যই সংশ্লিষ্ট workspace-এ authorized হতে হবে।
- Design Decision: Server-side authorization enforce করা হবে।
- Implementation: Domain operation-এর আগে permission check।
- Test: অন্য workspace-এর user দিয়ে update attempt।
- Result: Request reject হয়েছে।

এভাবে প্রতিটি গুরুত্বপূর্ণ requirement-এর পেছনে কারণ, code এবং verification থাকবে।

এটাই একটি reconstruction project-এর Control Plane।

---

# অধ্যায় ৪: Product Inventory—পুরো System-কে মানচিত্রে রূপান্তর

আরিফ এবার বলল:

“আমি কি এখন feature list তৈরি করতে পারি?”

নীরা বলল:

“Feature list তৈরি করো, কিন্তু শুধু feature-এর নাম লিখে থেমো না। প্রতিটি feature-এর behavior, dependency এবং failure path খুঁজে বের করো।”

## ৪.১ Feature Inventory

RelayDesk-এর inventory-তে থাকতে পারে:

- Login এবং session management
- Organization management
- Workspace membership
- Ticket creation
- Ticket assignment
- Comments
- Attachments
- Search
- Notifications
- Activity history
- Integrations
- Reports
- User preferences
- Data export
- Audit history

প্রতিটি feature-এর জন্য একটি structured record:

```text
Feature: Assign Ticket

Entry Point:
  Ticket details panel

Actors:
  Authorized workspace member

Preconditions:
  Ticket exists
  User has assignment permission
  Assignee belongs to the permitted workspace

Inputs:
  Ticket identifier
  Assignee identifier

Expected Outcome:
  Ticket ownership changes according to the domain rules

Possible Side Effects:
  Activity event
  Notification
  Search/index update, if applicable

Failure Conditions:
  Unauthorized access
  Invalid assignee
  Stale update
  Persistence failure

Verification:
  Happy path
  Invalid input
  Unauthorized actor
  Concurrent assignment
  Reload after success
```

এটি illustrative specification। বাস্তব target-এ প্রতিটি behavior evidence দিয়ে প্রতিষ্ঠা করতে হবে।

## ৪.২ Dependency Graph

একটি feature-এর dependency graph তৈরি করো।

উদাহরণ:

`Assign Ticket`

→ Identity  
→ Workspace Authorization  
→ Ticket Lookup  
→ Assignee Validation  
→ Domain Rules  
→ Persistence  
→ Activity History  
→ Notification  
→ Search Index  
→ UI Update

এখানে সব operation একই transaction-এ সম্পন্ন হবে, এমন নয়।

কোনটি synchronous, কোনটি asynchronous, কোনটি optional side effect—তা আলাদা করে চিহ্নিত করতে হবে।

যেমন, ticket save হওয়া একটি critical operation হতে পারে। Notification পাঠানো failure হলে ticket creation rollback করা উচিত কি না, তা business contract এবং system design-এর ওপর নির্ভর করে।

সব side effect-কে একটি বিশাল synchronous transaction-এর মধ্যে ঢুকিয়ে দেওয়া সমাধান নয়।

## ৪.৩ Product Graph বনাম Page List

একটি page list বলে:

- Dashboard
- Tickets
- Settings
- Reports

একটি dependency graph বলে:

- Dashboard-এর data কোথা থেকে আসে?
- Ticket count কোন filters ব্যবহার করে?
- User permission বদলালে dashboard কীভাবে বদলায়?
- Ticket delete হলে report-এর aggregate update হয় কি?
- Search index stale হলে কোন screen প্রভাবিত হয়?
- Background worker failure হলে কোন user journey অসম্পূর্ণ থাকে?

এই দ্বিতীয় ধরনের প্রশ্নই reconstruction-কে গভীর করে।

---

# অধ্যায় ৫: Scientific Investigation—প্রশ্ন থেকে পরীক্ষায়

একদিন নীরা আরিফকে একটি ছোট assignment দিল।

“আমরা জানতে চাই, RelayDesk-এ ticket creation request timeout হলে client আবার request পাঠালে duplicate ticket তৈরি হয় কি না।”

আরিফ সঙ্গে সঙ্গে বলল:

“আমরা API-তে idempotency key যোগ করে দিলেই হবে।”

নীরা বলল:

“সেটি একটি সম্ভাব্য implementation। কিন্তু প্রথমে original-এর আচরণ সম্পর্কে প্রশ্নটির উত্তর খোঁজো।”

এই পার্থক্যটি অত্যন্ত গুরুত্বপূর্ণ।

একটি সমস্যার ভালো solution এবং original-এর আচরণ সম্পর্কে সত্য জানা—দুটি আলাদা কাজ।

## ৫.১ Investigation Loop

একটি কার্যকর loop:

**Question → Hypothesis → Experiment → Observation → Interpretation → Confidence Update → Next Action**

### ধাপ ১: Question

Repeated submission কি duplicate ticket তৈরি করে?

### ধাপ ২: Hypothesis

- H1: প্রতিটি request নতুন ticket তৈরি করে।
- H2: একই logical request একবারই কার্যকর হয়।
- H3: Behavior request metadata বা endpoint-এর ওপর নির্ভর করে।
- H4: ফলাফল race condition বা timing-এর কারণে পরিবর্তিত হতে পারে।

### ধাপ ৩: Experiment

শুধু authorized test environment-এ একই input দিয়ে controlled submission করো।

সম্ভব হলে request identifier, response, resulting ticket state এবং timing record করো।

### ধাপ ৪: Observation

ধরা যাক, দুটি request পাঠানোর পর একটি ticket দেখা গেল।

### ধাপ ৫: Interpretation

এতে idempotency-এর সম্ভাবনা দেখা যায়। কিন্তু অন্য ব্যাখ্যাও থাকতে পারে:

- Client দ্বিতীয় request পাঠায়নি।
- Server duplicate request deduplicate করেছে।
- UI একটি ticket দেখাচ্ছে, কিন্তু backend-এ দুটি record হয়েছে।
- Test timing এমন ছিল যে race condition প্রকাশ পায়নি।

### ধাপ ৬: Confidence Update

বর্তমান evidence একটি hypothesis-কে সমর্থন করছে, কিন্তু সব সম্ভাবনা বাতিল করেনি।

### ধাপ ৭: Next Experiment

যেখানে অনুমোদিত, সেখানে request trace এবং persisted state তুলনা করো। Sequential retry-এর পাশাপাশি concurrency পরীক্ষা করার প্রয়োজন আছে কি না বিবেচনা করো।

## ৫.২ Information Gain

সব experiment সমান মূল্যবান নয়।

ধরা যাক, তোমার হাতে দুই ঘণ্টা আছে।

একটি কাজ হলো button hover animation-এর exact timing বোঝা।

আরেকটি কাজ হলো duplicate submission-এর কারণে billing বা ticket creation দুবার হয় কি না পরীক্ষা করা।

দ্বিতীয় কাজটি অধিক গুরুত্বপূর্ণ হতে পারে, কারণ ভুল হলে data integrity বা business operation প্রভাবিত হবে।

একটি heuristic ব্যবহার করা যায়:

`Priority ≈ Impact × Uncertainty × Consequence × Information Gain ÷ Effort`

এটি কোনো universal mathematical law নয়। এটি সিদ্ধান্ত নেওয়ার একটি সহায়ক model।

এখানে:

- Impact: বিষয়টি user বা business-এর কতটা ক্ষতি করতে পারে?
- Uncertainty: আমরা কতটা কম জানি?
- Consequence: ভুল সিদ্ধান্তের ফল কতটা গুরুতর?
- Information Gain: একটি experiment কতগুলো competing hypothesis আলাদা করতে পারবে?
- Effort: experiment করতে কত সময় ও resources লাগবে?

**সেরা পরবর্তী কাজটি সব সময় সবচেয়ে বড় কাজ নয়; অনেক সময় সেটি সবচেয়ে ছোট কিন্তু সবচেয়ে বেশি uncertainty দূর করতে সক্ষম experiment।**

---

# অধ্যায় ৬: UI Reverse Engineering—Screenshot থেকে State Machine

আরিফ এবার UI-কে আরও ভালোভাবে পর্যবেক্ষণ করতে শুরু করল।

আগে সে শুধু loaded page-এর screenshot নিত।

এখন সে প্রশ্ন করে:

- Loading-এর সময় কী দেখা যায়?
- Empty state আছে কি?
- Invalid input দিলে কী হয়?
- Network failure হলে কী হয়?
- User permission না থাকলে button কীভাবে আচরণ করে?
- Request চলার সময় button disable হয় কি?
- Browser refresh দিলে কী হয়?
- একই সময়ে অন্য user data update করলে কী হয়?
- Keyboard দিয়ে পুরো workflow সম্পন্ন করা যায় কি?

## ৬.১ একটি Button-এর সম্পূর্ণ জীবন

ধরা যাক, `Assign Ticket` button আছে।

এর state হতে পারে:

1. Idle
2. Validating
3. Submitting
4. Success
5. Validation Error
6. Permission Error
7. Network Error
8. Conflict
9. Retrying

State transition diagram:

```text
Idle
  |
  v
Validating
  |
  +---- Invalid Input ----> Validation Error
  |
  v
Submitting
  |
  +---- Success ----------> Success
  |
  +---- Unauthorized -----> Permission Error
  |
  +---- Conflict ---------> Conflict
  |
  +---- Timeout ----------> Network Error
```

এটি একটি illustrative model। Actual application-এ state এবং transition আলাদা হতে পারে।

এখন ভাবো, user `Submitting` অবস্থায় button দুবার চাপলে কী হবে?

- দ্বিতীয় click ignore হবে?
- দ্বিতীয় request পাঠানো হবে?
- UI optimistic update করবে?
- Server একই operation deduplicate করবে?

এই প্রশ্নগুলো UI design এবং backend semantics-কে একসঙ্গে যুক্ত করে।

## ৬.২ চার ধরনের State আলাদা করো

### Local UI State

Dropdown খোলা কি না, modal visible কি না।

### Persisted Server State

Ticket-এর প্রকৃত status, assignee, description।

### Cached State

Browser বা client library-তে রাখা আগের response।

### Derived State

Ticket count, filtered list, computed badge, aggregated report।

এই state-গুলোকে এক মনে করলে synchronization bug তৈরি হয়।

যেমন, ticket update সফল হয়েছে, কিন্তু cache invalidate হয়নি। তখন details panel নতুন data দেখাতে পারে, কিন্তু list পুরোনো data দেখায়।

## ৬.৩ Visual Fidelity-এর সঠিক ব্যবহার

Visual comparison গুরুত্বপূর্ণ, কিন্তু সেটিকে context-সহ করতে হবে।

তুলনা করার সময় নির্ধারণ করো:

- Viewport size
- Browser version
- Font availability
- UI state
- Test data
- Loading completion
- Relevant user permissions

তারপর spacing, typography, layout, menus, dialogs, focus state, responsive behavior তুলনা করো।

Pixel-perfect screenshot useful, কিন্তু একই screenshot-এর পেছনে ভিন্ন business logic থাকতে পারে।

**UI fidelity এবং behavioral fidelity আলাদাভাবে যাচাই করো।**

---

# অধ্যায় ৭: API Reverse Engineering—Request দেখলেই Contract জানা যায় না

একটি application-এর API হলো তার observable communication contract-এর গুরুত্বপূর্ণ অংশ।

কিন্তু browser network panel-এ একটি request দেখা মানেই পুরো API catalog আবিষ্কার হয়ে গেছে—এমন নয়।

## ৭.১ API Contract-এর উপাদান

একটি API investigation-এ দেখো:

- HTTP method
- Path
- Headers
- Authentication context
- Request schema
- Response schema
- Status codes
- Error formats
- Validation behavior
- Pagination
- Sorting
- Filtering
- Rate-limit behavior
- Idempotency
- Conditional requests
- File upload/download
- WebSocket বা Server-Sent Events, যেখানে প্রাসঙ্গিক
- Webhook behavior, যেখানে প্রাসঙ্গিক

উদাহরণ হিসেবে একটি hypothetical contract:

```http
POST /api/tickets
Content-Type: application/json
```

```json
{
  "title": "Login failure",
  "description": "Users cannot sign in",
  "workspace_id": "ws_demo"
}
```

সম্ভাব্য response:

```json
{
  "id": "ticket_demo",
  "title": "Login failure",
  "status": "open"
}
```

এই payload এবং path শিক্ষামূলক উদাহরণ। এগুলোকে কোনো real target-এর discovered contract হিসেবে গণ্য করা যাবে না।

## ৭.২ HTTP 200 মানেই Success নয়

ধরা যাক, request-এর response status `200 OK`।

তবুও কয়েকটি প্রশ্ন বাকি:

- Response body কি প্রত্যাশিত schema অনুসরণ করছে?
- Operation বাস্তবে সম্পন্ন হয়েছে?
- Data persisted হয়েছে?
- Response কি stale cache থেকে এসেছে?
- Business rule অনুযায়ী operation বৈধ ছিল?
- Asynchronous processing এখনও বাকি?
- Error কি response body-তে encode করা হয়েছে?

অর্থাৎ, status code একটি গুরুত্বপূর্ণ signal, কিন্তু পুরো operation-এর proof নয়।

## ৭.৩ Error Contract

একটি robust API investigation-এ negative cases-ও দেখতে হবে।

উদাহরণ:

- Invalid input
- Missing required field
- Unauthorized user
- Forbidden resource
- Nonexistent entity
- Duplicate operation
- Conflict
- Rate limit
- Dependency failure
- Timeout

সব error-এর জন্য একই generic response ব্যবহার করলে compatibility এবং debugging দুই-ই ক্ষতিগ্রস্ত হতে পারে।

তবে original-এর error behavior অনিরাপদ বা অসংগত হলে সেটি অন্ধভাবে কপি করাও উচিত নয়। Scope অনুযায়ী compatibility এবং security-এর মধ্যে সচেতন সিদ্ধান্ত নিতে হবে।

## ৭.৪ API Contract Test

একটি test শুধু happy path যাচাই করবে না।

এটি পরীক্ষা করতে পারে:

1. Required field অনুপস্থিত হলে কী হয়?
2. Unknown field গ্রহণ করা হয়, নাকি reject করা হয়?
3. Unauthorized request কীভাবে handle হয়?
4. Pagination-এর শেষ page কেমন?
5. Sorting deterministic কি?
6. Retry করলে operation পুনরাবৃত্ত হয় কি?
7. Error response-এর structure স্থিতিশীল কি?

যে behavior contract-এর অংশ, সেটিকে executable test-এ রূপান্তর করো।

---

# অধ্যায় ৮: Business Logic—Software-এর নিয়মগুলো আবিষ্কার করা

একটি application শুধু CRUD operation-এর সমষ্টি নয়।

Business logic নির্ধারণ করে কোন operation বৈধ, কোন state থেকে কোন state-এ যাওয়া যাবে, কোন actor কী করতে পারবে, এবং কোন side effect ঘটবে।

ধরা যাক, RelayDesk ticket-এর status হতে পারে:

`Open → In Progress → Resolved → Closed`

এটি কেবল একটি illustrative state machine।

বাস্তব target-এ status, transition এবং permission আলাদাভাবে তদন্ত করতে হবে।

## ৮.১ State Transition

প্রশ্ন করো:

- Closed ticket আবার Open করা যায়?
- Resolved ticket-এ নতুন comment দিলে status পরিবর্তিত হয়?
- User ticket delete করলে activity history থাকে?
- Assignment change হলে পুরোনো assignee-এর notification যায়?
- একই status বারবার set করলে duplicate activity event তৈরি হয়?

প্রতিটি উত্তর একটি business rule হতে পারে।

## ৮.২ Invariant

Invariant হলো এমন শর্ত, যা system-এর নির্দিষ্ট অবস্থায় সত্য থাকতে হবে।

উদাহরণ:

- Ticket অবশ্যই একটি valid workspace-এর অন্তর্গত হবে।
- Assignee সংশ্লিষ্ট authorization rules পূরণ করবে।
- Deleted record আর সাধারণ active query-তে ফিরে আসবে না, যদি সেটি contract হয়।
- একটি logical operation-এর duplicate retry যেন অনিচ্ছাকৃত duplicate side effect তৈরি না করে।

কোন invariant বাস্তবে প্রযোজ্য, তা evidence ও product requirements থেকে নির্ধারণ করতে হবে।

## ৮.৩ Decision Table

Assignment-এর একটি hypothetical decision table:

| Ticket valid? | User authorized? | Assignee valid? | Expected decision |
|---|---|---|---|
| Yes | Yes | Yes | Allow |
| No | Yes | Yes | Reject |
| Yes | No | Yes | Reject |
| Yes | Yes | No | Reject |

এটি একটি সহজ উদাহরণ। বাস্তব system-এ role, workspace membership, ticket state, ownership এবং policy আরও জটিল হতে পারে।

Decision table business logic-কে স্পষ্ট করে। একই সঙ্গে test case তৈরির ভিত্তিও দেয়।

**ভালো reconstruction-এর জন্য business rules-কে implicit code-এর ভেতরে লুকিয়ে না রেখে explicit specification-এ রূপান্তর করো।**

---

# অধ্যায় ৯: Data Model—কোন Data কোথায় থাকে, এবং কেন?

একটি software product-এর Data Model তার আচরণকে গভীরভাবে প্রভাবিত করে।

RelayDesk-এর সম্ভাব্য conceptual entities:

- Organization
- Workspace
- User
- Membership
- Ticket
- Comment
- Attachment
- Activity Event
- Notification
- Search Document

এটি একটি candidate model, original database schema-এর দাবি নয়।

## ৯.১ Entity Relationship

ধরা যাক:

- একটি Organization-এর একাধিক Workspace থাকতে পারে।
- একটি Workspace-এর একাধিক User Membership থাকতে পারে।
- একটি Ticket একটি Workspace-এর অন্তর্গত।
- একটি Ticket-এর একাধিক Comment থাকতে পারে।
- Ticket update হলে Activity Event তৈরি হতে পারে।
- Notification Ticket-এর lifecycle-এর সঙ্গে সম্পর্কিত হতে পারে।

এখানে relationship এবং ownership-এর নিয়ম গুরুত্বপূর্ণ।

একটি Ticket-এর `workspace_id` পরিবর্তন করা যাবে কি? User-এর membership revoke হলে তার আগের ticket access থাকবে কি? Deleted ticket-এর comment কীভাবে handle হবে?

এগুলো শুধু schema design-এর প্রশ্ন নয়। এগুলো domain semantics-এর অংশ।

## ৯.২ Authoritative Data বনাম Derived Data

সব data store সমান কর্তৃত্বপূর্ণ নয়।

উদাহরণ:

- Database-এ ticket-এর বর্তমান state authoritative হতে পারে।
- Search index ticket-এর searchable representation।
- Cache সাময়িক copy।
- Dashboard count derived aggregate।
- Notification queue pending work-এর representation হতে পারে।

যদি search index stale হয়, তাহলে database-এ ticket update ব্যর্থ হয়েছে—এমন সিদ্ধান্তে পৌঁছানো যাবে না।

আবার database update সফল হয়েছে বলেই search index সঙ্গে সঙ্গে updated থাকবে—এটিও ধরে নেওয়া যাবে না।

## ৯.৩ Deletion-এর গভীরতা

একটি ticket delete করলে কী হবে?

সম্ভাব্য আচরণ:

- Ticket record soft-delete করা
- Ticket permanently delete করা
- Comments delete করা
- Attachments-এর access revoke করা
- Search index থেকে remove করা
- Notification history রেখে দেওয়া
- Audit history সংরক্ষণ করা

কোনটি প্রযোজ্য, তা product requirements, evidence এবং legal retention obligations-এর ওপর নির্ভর করে।

এখানে একটি গুরুত্বপূর্ণ শিক্ষা:

**Data lifecycle শুধু create, read, update, delete নয়; এটি ownership, retention, consistency, recovery এবং historical semantics-এর সমষ্টি।**

## ৯.৪ Physical Database Schema আবিষ্কার করা সব সময় প্রয়োজন নয়

তুমি conceptual model পুনর্গঠন করতে পারো, এমনকি original database engine অজানা থাকলেও।

যদি তোমার কাছে শুধু observable behavior থাকে, তাহলে তুমি compatibility-এর জন্য প্রয়োজনীয় constraints এবং relationships নির্ধারণ করতে পারো।

কিন্তু original system-এর physical schema সম্পর্কে দাবি করতে হলে source, authorized schema access বা সমমানের শক্তিশালী evidence দরকার।

---

# অধ্যায় ১০: Concurrency, Queues এবং সময়ের অদৃশ্য সমস্যা

এবার আরিফ এমন একটি bug পেল, যা শুধু একটি user দিয়ে পরীক্ষা করলে ধরা পড়ে না।

দুটি user একই ticket প্রায় একই সময়ে edit করল।

User A status পরিবর্তন করল।

User B description পরিবর্তন করল।

দুটি update-এর ফলাফল কী হবে?

এখানে একাধিক সম্ভাবনা আছে।

- Last-write-wins
- Optimistic concurrency control
- Version conflict
- Field-level merge
- Application-specific conflict resolution

কোনটি সঠিক, তা product contract-এর ওপর নির্ভর করে।

## ১০.১ Race Condition

একটি Race Condition ঘটে যখন concurrent operation-এর timing বা ordering ফলাফলকে প্রভাবিত করে।

উদাহরণ:

1. User A পুরোনো ticket state পড়ে।
2. User B ticket update করে।
3. User A তার পুরোনো state-এর ওপর ভিত্তি করে update পাঠায়।
4. B-এর পরিবর্তন হারিয়ে যেতে পারে।

একটি সম্ভাব্য সমাধান হলো version-based optimistic locking:

- Client version `v1` পড়ে।
- Update request-এ expected version পাঠায়।
- Server দেখে current version এখনও `v1` কি না।
- Version বদলে গেলে conflict ফেরত দেয়।

এটি একটি design example, original-এর implementation সম্পর্কে দাবি নয়।

## ১০.২ Asynchronous Processing

Ticket creation-এর পরে একটি system হয়তো:

1. Ticket persist করে।
2. Activity event তৈরি করে।
3. Notification job schedule করে।
4. Search index update করে।
5. Client-কে response দেয়।

সব কাজ একই সময় সম্পন্ন হওয়া বাধ্যতামূলক নয়।

একটি queue-তে job গেলে worker সেটি পরে process করতে পারে।

এতে latency কমতে পারে, কিন্তু নতুন complexity তৈরি হয়:

- Job delay
- Duplicate delivery
- Retry
- Dead-letter handling
- Out-of-order processing
- Cancellation
- Poison message
- Partial failure
- Recovery

## ১০.৩ Exactly Once-এর মোহ

Distributed system-এ “একবারই কাজ হবে” কথাটি অনেক সময় অতিরিক্ত সরলীকরণ।

একটি message একাধিকবার deliver হতে পারে। Worker crash হওয়ার আগে external provider-এ side effect ঘটতে পারে, কিন্তু acknowledgement সংরক্ষিত নাও হতে পারে।

তাই বাস্তব design-এ প্রায়ই প্রয়োজন হয়:

- Idempotent handler
- Unique operation identifier
- Durable event recording
- Retry policy
- Deduplication
- Reconciliation
- Monitoring

উদাহরণ:

Notification worker একই event দুবার পেলে একই user-কে দুবার email পাঠাবে কি?

যদি business contract duplicate email নিষিদ্ধ করে, তাহলে event identity এবং delivery state-এর ওপর ভিত্তি করে duplicate side effect প্রতিরোধ করতে হবে।

## ১০.৪ Outbox Pattern-এর ধারণা

ধরা যাক, database-এ ticket save হলো, কিন্তু event publish করার আগেই process crash করল।

তখন ticket আছে, কিন্তু notification event হারিয়ে যেতে পারে।

একটি সম্ভাব্য design হলো Transactional Outbox Pattern:

একই database transaction-এ:

- Ticket update
- Outbox event record

সংরক্ষণ করা হয়।

পরে worker outbox থেকে event publish করে।

এই pattern কিছু failure window কমাতে সাহায্য করে, তবে consumer-side idempotency এবং operational monitoring এখনও প্রয়োজন হতে পারে।

মূল শিক্ষা হলো: asynchronous architecture বেছে নেওয়া মানে শুধু queue যোগ করা নয়। Data consistency, retries, ordering এবং recovery-ও design করতে হয়।

---

# অধ্যায় ১১: Networking ও Infrastructure—Fingerprint থেকে Architecture বানিও না

একটি public application-এর response header-এ কোনো server technology-এর নাম দেখা গেল।

আরিফ সিদ্ধান্ত নিল:

“Original system অবশ্যই ওই technology দিয়েই তৈরি।”

নীরা বলল:

“একটি fingerprint অনেক সময় একটি সম্ভাবনা দেখায়, পুরো architecture নয়।”

একটি response header reverse proxy, gateway বা edge layer থেকে আসতে পারে। Origin server অন্য technology ব্যবহার করতে পারে। একটি application একাধিক service এবং provider ব্যবহার করতে পারে।

## ১১.১ Network Investigation-এর স্তর

প্রাসঙ্গিক ক্ষেত্রে অনুসন্ধান করা যায়:

- DNS behavior
- TLS behavior
- HTTP protocol
- Request/response headers
- Redirects
- Proxy এবং gateway behavior
- Connection reuse
- Streaming
- Timeouts
- Rate limits
- Client-side networking
- Authorized infrastructure configuration

কিন্তু প্রতিটি পর্যবেক্ষণের সীমা আছে।

উদাহরণস্বরূপ, একটি IP address দেখে পুরো internal topology নির্ধারণ করা যায় না।

একটি HTTP response দেখে নিশ্চিত হওয়া যায় না যে backend monolith, microservices, serverless অথবা event-driven architecture ব্যবহার করে।

## ১১.২ Replacement Architecture কীভাবে বেছে নেবে?

Original architecture অজানা হলে replacement-এর architecture প্রয়োজনীয়তার ভিত্তিতে নির্ধারণ করো।

### Modular Monolith

উপযুক্ত হতে পারে যখন:

- Team ছোট
- Domain boundaries স্পষ্ট
- Independent deployment-এর প্রয়োজন সীমিত
- Operational simplicity গুরুত্বপূর্ণ

### Microservices

উপযুক্ত হতে পারে যখন:

- Independent scaling দরকার
- আলাদা service ownership প্রয়োজন
- Deployment cadence আলাদা
- Failure isolation-এর নির্দিষ্ট প্রয়োজন আছে

### Event-Driven Architecture

উপযুক্ত হতে পারে যখন:

- Asynchronous processing গুরুত্বপূর্ণ
- Event consumers আলাদা করা প্রয়োজন
- Throughput ও decoupling দরকার
- Eventual consistency গ্রহণযোগ্য

কোনো architecture নিজে থেকেই superior নয়।

**Original-এর অজানা architecture নকল করার চেয়ে প্রয়োজনীয় behavior পূরণ করে এমন architecture নির্বাচন করা অধিক যুক্তিযুক্ত।**

---

# অধ্যায় ১২: Security ও Privacy—একটি Clone-ও নিরাপদ হতে হবে

একটি reconstruction project-এ security কখনো শুধু শেষে যোগ করা feature হতে পারে না।

বিশেষত multi-tenant application-এ authorization failure পুরো system-এর trust নষ্ট করতে পারে।

## ১২.১ Authentication বনাম Authorization

Authentication প্রশ্ন করে:

“তুমি কে?”

Authorization প্রশ্ন করে:

“তুমি এই resource-এ এই operation করার অনুমতি রাখো কি?”

একজন user login করতে পারলেই সে সব workspace-এর ticket দেখতে পারবে না।

ধরা যাক:

- User A Workspace A-এর member।
- User B Workspace B-এর member।
- User A অন্য workspace-এর ticket ID জানে।

UI-তে ticket link লুকিয়ে রাখা যথেষ্ট নয়।

Server-কে request-এর actor, resource এবং requested operation যাচাই করতে হবে।

## ১২.২ Object-Level Authorization

প্রতিটি sensitive operation-এর জন্য দেখতে হবে:

- Actor কে?
- Resource কোন workspace-এর?
- Actor-এর permission কী?
- Resource-এর বর্তমান state কী?
- Requested transition অনুমোদিত কি?

এটি শুধু frontend-এর কাজ নয়।

## ১২.৩ Threat Modeling

একটি threat model-এ বিবেচনা করা যায়:

- Unauthorized resource access
- Privilege escalation
- Session theft
- Input injection
- Insecure file access
- Sensitive data exposure
- Weak secret management
- Unsafe third-party integration
- Audit gaps
- Excessive permissions

Threat modeling-এর উদ্দেশ্য ভয় তৈরি করা নয়। বরং কোথায় trust boundary আছে, কী কী ভুল হতে পারে, এবং কোন control তা প্রতিরোধ করবে—তা স্পষ্ট করা।

## ১২.৪ Original-এ Vulnerability থাকলে?

ধরা যাক, authorized testing-এ original system-এর একটি দুর্বল permission behavior দেখা গেল।

এখানে দুটি প্রশ্ন আলাদা:

1. Compatibility-এর জন্য observable behavior বোঝা দরকার কি?
2. Replacement-এ সেই দুর্বলতা রাখা উচিত কি?

দ্বিতীয় প্রশ্নের উত্তর সাধারণত security এবং product requirements-এর ভিত্তিতে নিতে হবে। Insecure behavior অন্ধভাবে copy করা উচিত নয়।

এছাড়া investigation-এর সময় access controls bypass, অন্য user-এর private data সংগ্রহ, secret extraction অথবা অনুমোদনহীন destructive testing করা যাবে না।

---

# অধ্যায় ১৩: Observability—System-এর ভেতরে কী ঘটছে, তা কীভাবে জানবে?

একটি production system শুধু কাজ করলেই যথেষ্ট নয়। সমস্যা হলে সেটি নির্ণয় করার ক্ষমতাও থাকতে হবে।

এখানে Observability গুরুত্বপূর্ণ।

ধরা যাক, RelayDesk-এ ticket creation হঠাৎ ধীর হয়ে গেছে।

একজন user শুধু বলছে:

“Save button চাপলে অনেক সময় লাগছে।”

কিন্তু সমস্যাটি কোথায়?

- Browser rendering?
- Network latency?
- API gateway?
- Application code?
- Database query?
- Lock contention?
- External dependency?
- Queue backlog?

Telemetry ছাড়া এগুলো অনুমান করেই চলতে হবে।

## ১৩.১ তিনটি গুরুত্বপূর্ণ Signal

### Logs

একটি নির্দিষ্ট event বা error সম্পর্কে বিস্তারিত তথ্য।

উদাহরণ:

```text
event=ticket_creation_failed
request_id=req_demo
reason=dependency_timeout
```

এটি illustrative log। বাস্তবে sensitive data redaction এবং structured logging policy দরকার।

### Metrics

System-এর পরিমাণগত আচরণ।

যেমন:

- Request rate
- Error rate
- Latency distribution
- Queue depth
- Worker throughput
- Database connection usage

### Distributed Traces

একটি request বিভিন্ন component-এর মধ্য দিয়ে কীভাবে প্রবাহিত হয়েছে, তার trace।

উদাহরণ:

`API Request → Authorization → Database → Event Publication → Notification Worker`

Trace দেখাতে পারে কোন span বেশি সময় নিচ্ছে, যদি tracing instrumentation সঠিকভাবে configured থাকে।

## ১৩.২ Correlation এবং Privacy

Request ID বা trace ID ব্যবহার করে related events যুক্ত করা যায়।

কিন্তু logs-এ password, access token, secret, অথবা অপ্রয়োজনীয় sensitive data রাখা উচিত নয়।

Observability-এর সঙ্গে retention, access control, redaction এবং cost management-ও যুক্ত।

## ১৩.৩ SLI, SLO এবং Alerting

একটি Service-Level Indicator (SLI) হলো পরিমাপযোগ্য service behavior।

একটি Service-Level Objective (SLO) হলো সেই behavior-এর জন্য নির্ধারিত লক্ষ্য।

উদাহরণস্বরূপ, কোনো API-এর latency target নির্ধারণ করা যেতে পারে। কিন্তু সেই target অবশ্যই application-এর প্রয়োজন, user expectation এবং বাস্তব capacity-এর সঙ্গে সামঞ্জস্যপূর্ণ হতে হবে।

Original-এর internal metrics inaccessible হলে সেগুলো recover হয়েছে বলে দাবি করা যাবে না।

বরং replacement-এর জন্য উপযুক্ত observability design তৈরি করতে হবে।

---

# অধ্যায় ১৪: Performance ও Resilience—দ্রুত হওয়া আর নির্ভরযোগ্য হওয়া এক নয়

একটি application local machine-এ খুব দ্রুত চলতে পারে, কিন্তু production workload-এ ব্যর্থ হতে পারে।

তাই Performance Engineering-এ শুধু একটি request-এর সময় মাপা যথেষ্ট নয়।

বিবেচনা করতে হবে:

- Latency distribution
- Throughput
- Concurrency
- Resource utilization
- Queue backlog
- Database contention
- Dependency latency
- Error rate
- Recovery time
- Cost per operation

## ১৪.১ Average Latency-এর ফাঁদ

ধরা যাক, একশটি request-এর বেশিরভাগ দ্রুত সম্পন্ন হয়েছে, কিন্তু কিছু request অত্যন্ত ধীর।

Average latency গ্রহণযোগ্য দেখালেও tail latency user experience খারাপ করতে পারে।

তাই প্রয়োজন অনুযায়ী percentile metrics, যেমন p95 বা p99, পর্যবেক্ষণ করা যেতে পারে।

এগুলো measurement-এর উদাহরণ, কোনো universal target নয়।

## ১৪.২ Load Test-এর সীমা

Load test করতে হলে workload, dataset, concurrency এবং environment তুলনাযোগ্য হওয়া দরকার।

Original এবং replacement আলাদা hardware, network এবং deployment environment-এ চললে সরাসরি latency comparison বিভ্রান্তিকর হতে পারে।

যা মাপা হয়েছে, সেটি report করো। যা মাপা হয়নি, তা অনুমান করে পূরণ করো না।

## ১৪.৩ Resilience-এর গুরুত্বপূর্ণ প্রশ্ন

- Database unavailable হলে কী হবে?
- External email provider fail করলে কী হবে?
- Queue backlog বাড়লে কী হবে?
- Worker crash করলে pending work কীভাবে recover হবে?
- Deployment-এর পরে migration ব্যর্থ হলে কী হবে?
- Cache unavailable হলে system degraded mode-এ চলতে পারবে?
- Backup restore সত্যিই কাজ করে কি?

Resilience হলো শুধু retry যোগ করা নয়। Retry নিজেই duplicate side effect বা overload তৈরি করতে পারে।

তাই timeout, backoff, retry budget, circuit breaking, idempotency এবং recovery strategy একসঙ্গে বিবেচনা করতে হবে।

---

# অধ্যায় ১৫: Architecture—প্রথমে প্রয়োজন, তারপর Technology

আরিফ এবার পুরো RelayDesk-এর architecture design করতে চাইল।

সে বলল:

“আমরা microservices, Kubernetes, event bus, Redis, PostgreSQL এবং distributed tracing ব্যবহার করব। তাহলেই production-grade হবে।”

নীরা বলল:

“Technology-এর তালিকা architecture নয়।”

একটি architecture ব্যাখ্যা করে:

- System-এর responsibility কী?
- Component-গুলোর boundary কোথায়?
- Data ownership কার?
- Communication কীভাবে হয়?
- Consistency requirement কী?
- Failure isolation কীভাবে হয়?
- Deployment কীভাবে হয়?
- Security boundary কোথায়?
- Trade-off কেন গ্রহণ করা হয়েছে?

## ১৫.১ Architecture Decision Record

প্রতিটি গুরুত্বপূর্ণ decision-এর জন্য একটি ছোট ADR তৈরি করা যায়।

```text
Decision:
  Ticket workflow-এর জন্য modular monolith ব্যবহার করা হবে।

Context:
  Team ছোট এবং domain boundaries স্পষ্ট।

Alternatives:
  Microservices
  Serverless decomposition

Reasons:
  Operational simplicity
  Easier local development
  Fewer distributed consistency problems

Trade-offs:
  Independent scaling সীমিত হতে পারে।

Evidence:
  Current workload requirements এবং team constraints।

Status:
  Proposed / Accepted / Superseded
```

এটি একটি illustrative decision।

প্রকৃত সিদ্ধান্ত project context অনুযায়ী নিতে হবে।

## ১৫.২ Architecture যেন Evidence-এর সঙ্গে সামঞ্জস্যপূর্ণ হয়

যদি feature-এর contract জানা থাকে, তাহলে architecture সেই contract পূরণ করতে পারে।

যদি original internal architecture অজানা থাকে, তাহলে replacement-এর architecture আলাদা হতে পারে।

যদি কোনো feature-এর behavior অজানা থাকে, তাহলে হয়:

- আরও evidence সংগ্রহ করতে হবে,
- minimal compatible behavior implement করতে হবে,
- uncertainty-সহ একটি robust design নিতে হবে,
- feature defer করতে হবে,
- অথবা প্রয়োজনীয় access চাইতে হবে।

অজানা বিষয় নিয়ে অসীম গবেষণা যেমন ভুল, তেমনি evidence ছাড়াই architecture বানিয়ে সেটিকে discovered fact বলা আরও বড় ভুল।

---

# অধ্যায় ১৬: Implementation—একবারে পুরো Application নয়

AI coding agent-কে একবারে পুরো application বানাতে বললে কী হতে পারে?

সে হয়তো শত শত file তৈরি করবে। কিছু screen কাজ করবে, কিছু API mock হবে, কিছু validation বাদ যাবে, আর কিছু integration-এর জায়গায় placeholder থাকবে।

Code দেখতে বিশাল হতে পারে। কিন্তু complexity-এর পরিমাণ এবং implementation-এর correctness এক জিনিস নয়।

নীরা আরিফকে একটি নিয়ম দিল:

**Vertical Slice দিয়ে কাজ করো।**

## ১৬.১ Vertical Slice কী?

ধরা যাক, তুমি `Create Ticket` feature তৈরি করছ।

একটি সম্পূর্ণ vertical slice-এ প্রয়োজন অনুযায়ী থাকবে:

1. UI input
2. Client validation
3. API request
4. Server-side validation
5. Authorization
6. Domain rules
7. Persistence
8. Error handling
9. Relevant side effects
10. Automated tests
11. Reload verification

অর্থাৎ, feature-টি frontend থেকে backend পর্যন্ত সম্পূর্ণ একটি user outcome সরবরাহ করবে।

এটি শুধু frontend screen নয়, আবার শুধু backend endpoint-ও নয়।

## ১৬.২ Slice-by-Slice Development

একটি সম্ভাব্য sequence:

1. Application shell এবং navigation
2. Identity এবং authorization
3. Core domain model
4. Primary workflow
5. Persistence এবং data integrity
6. Error states এবং edge cases
7. Background jobs এবং integrations
8. Real-time behavior, যেখানে প্রয়োজন
9. Observability
10. Production hardening

তবে এই sequence product-specific। Dependency অনুযায়ী বদলাতে হবে।

## ১৬.৩ প্রতি Slice-এর Workflow

প্রতিটি slice-এর জন্য:

- Existing code পর্যালোচনা করো।
- Requirement এবং contract নিশ্চিত করো।
- Smallest coherent implementation তৈরি করো।
- Automated tests লেখো।
- Application চালিয়ে বাস্তব behavior দেখো।
- Evidence-এর সঙ্গে তুলনা করো।
- Discrepancy খুঁজে বের করো।
- Root cause সংশোধন করো।
- Regression test যোগ করো।
- Evidence এবং specification update করো।

এভাবে development একটি feedback loop-এ পরিণত হয়।

## ১৬.৪ Mock-এর সঠিক ব্যবহার

Mock data test-এর জন্য উপকারী।

কিন্তু production feature-এর জায়গায় mock বসিয়ে সেটিকে complete বলা যাবে না।

উদাহরণ:

- Test fixture: গ্রহণযোগ্য, যদি সেটি স্পষ্টভাবে test-only হয়।
- Local prototype: গ্রহণযোগ্য, যদি limitation documented থাকে।
- Production search feature, যা hardcoded array থেকে result দেয়: বাস্তব search implementation-এর বিকল্প নয়।

**Code উপস্থিত থাকা, feature implemented হওয়া এবং feature verified হওয়া—তিনটি আলাদা status।**

---

# অধ্যায় ১৭: Differential Verification—দুটি System-কে একই প্রশ্ন করো

আরিফ এবার একটি working replacement তৈরি করেছে।

কিন্তু নীরা বলল:

“এখনও তোমার কাজ শেষ হয়নি। তুমি শুধু জানো তোমার code চলছে। তুমি এখনও জানো না, এটি প্রয়োজনীয় behavior সঠিকভাবে পুনর্নির্মাণ করেছে কি না।”

এখানে আসে Differential Verification।

## ১৭.১ Basic Method

1. একটি নির্দিষ্ট behavior নির্বাচন করো।
2. Original-এর evidence সংগ্রহ করো।
3. Equivalent test input প্রস্তুত করো।
4. Replacement-এ একই condition তৈরি করো।
5. Outcome তুলনা করো।
6. Difference record করো।
7. Root cause খুঁজে বের করো।
8. Fix করো।
9. Regression test যোগ করো।

সব original system-এর বিরুদ্ধে automated comparison করা সম্ভব নয়। কখনো manual observation, documented contract বা captured artifact-এর ভিত্তিতে verification করতে হবে।

যা সম্ভব নয়, সেটিকে explicit limitation হিসেবে report করো।

## ১৭.২ Test Matrix

| Dimension | Example |
|---|---|
| Visual | একই viewport-এ layout comparison |
| Behavioral | Create ticket workflow |
| Contract | Request/response schema |
| Data | Reload-এর পর persisted state |
| Security | Cross-workspace access rejection |
| Concurrency | Simultaneous updates |
| Temporal | Delayed notification |
| Failure | Dependency timeout |
| Performance | Defined workload-এর latency |
| Operations | Trace এবং error diagnosis |

## ১৭.৩ Difference Record

একটি discrepancy record এমন হতে পারে:

```text
Difference ID:
  D-014

Expected:
  Assignment-এর পর ticket details এবং list একই assignee দেখাবে।

Actual:
  Details panel নতুন assignee দেখায়,
  কিন্তু list পুরোনো assignee দেখায়।

Evidence:
  Test run T-021

Severity:
  Medium

Root Cause:
  List cache invalidation অনুপস্থিত।

Affected Requirement:
  REQ-ASSIGN-03

Fix:
  Successful update-এর পর সংশ্লিষ্ট cache invalidate করা।

Regression Test:
  Assignment → list refresh → assignee verification

Status:
  Open / Fixed / Verified
```

এটি illustrative example।

এভাবে প্রতিটি discrepancy actionable engineering task-এ পরিণত হয়।

## ১৭.৪ Test পাস করলেও কী অজানা থাকে?

ধরা যাক, একটি endpoint-এর দশটি test পাস করেছে।

তাতে প্রমাণ হয় না যে:

- সব possible input সঠিক।
- সব concurrency scenario সঠিক।
- সব permission boundary নিরাপদ।
- সব failure mode handle হয়।
- পুরো original system-এর সঙ্গে equivalence প্রতিষ্ঠিত হয়েছে।

একটি test suite শুধু তার defined conditions-এর ফলাফল প্রতিষ্ঠা করে।

তাই test coverage-এর denominator স্পষ্ট হওয়া জরুরি।

---

# অধ্যায় ১৮: চারটি বাস্তবধর্মী Scenario—একই দর্শনের ভিন্ন প্রয়োগ

এখন পর্যন্ত আমরা RelayDesk-কে কেন্দ্র করে আলোচনা করেছি। কিন্তু reverse engineering-এর এই methodology শুধু Customer Support SaaS-এর জন্য নয়।

এটি E-commerce, Collaborative Editor, AI Agent Platform এবং আরও অনেক ধরনের system-এ প্রয়োগ করা যায়।

নিচে চারটি বিস্তারিত scenario দেওয়া হলো।

---

## Scenario 1: E-commerce Platform—একটি Order Button-এর পেছনের পুরো System

ধরা যাক, তুমি একটি জনপ্রিয় E-commerce application পুনর্নির্মাণ করতে চাও।

তুমি product page, cart, checkout, payment screen এবং order history দেখতে পাচ্ছ।

প্রথমে কাজটি সহজ মনে হয়:

- Product list
- Cart
- Checkout
- Payment
- Order confirmation

কিন্তু একটি `Place Order` button-এর পেছনে থাকতে পারে অনেকগুলো stateful operation।

### ধাপ ১: Product Inventory

প্রথমে product inventory তৈরি করো:

- Product details
- Pricing
- Discounts
- Inventory
- Cart
- Checkout
- Payment
- Order lifecycle
- Shipping
- Refund
- Cancellation
- Notifications

### ধাপ ২: Domain Rules

প্রশ্ন করো:

- Cart-এর price কখন authoritative হয়?
- Checkout-এর সময় stock reserve করা হয়?
- Payment failure হলে inventory release হয়?
- একই order request পুনরায় এলে কী হয়?
- Refund আংশিক হতে পারে?
- Order cancel করার শেষ সময় কখন?
- Coupon কি একাধিকবার ব্যবহার করা যায়?

এগুলো অনুমান করে লিখবে না। Available evidence, documentation এবং authorized test environment থেকে প্রয়োজনীয় আচরণ নির্ধারণ করবে।

### ধাপ ৩: State Machine

একটি illustrative order lifecycle:

`Created → Payment Pending → Confirmed → Fulfillment → Shipped → Delivered`

Failure path:

`Payment Pending → Payment Failed`

অথবা:

`Confirmed → Cancellation Requested → Cancelled`

Actual lifecycle product-specific।

### ধাপ ৪: Failure Scenario

একজন user `Place Order` চাপল।

Payment provider charge সম্পন্ন করল, কিন্তু application response পাওয়ার আগেই network timeout হলো।

User আবার button চাপল।

এখন কী হতে পারে?

- দ্বিতীয় order তৈরি হতে পারে।
- দ্বিতীয় payment attempt হতে পারে।
- প্রথম payment সফল হলেও UI failure দেখাতে পারে।
- Reconciliation না থাকলে order এবং payment state অসামঞ্জস্যপূর্ণ হতে পারে।

এই scenario-তে প্রয়োজন হতে পারে:

- Idempotency
- Durable payment references
- Explicit order/payment state
- Retry policy
- Webhook processing
- Reconciliation jobs
- Audit trail

তবে কোনটি original-এ ব্যবহৃত হয়, তা আলাদা evidence-এর বিষয়।

### ধাপ ৫: Verification

শুধু order confirmation page দেখলেই কাজ শেষ নয়।

পরীক্ষা করো:

1. Successful checkout
2. Insufficient inventory
3. Payment decline
4. Timeout after payment attempt
5. Duplicate submission
6. Delayed payment webhook
7. Cancellation
8. Refund
9. Concurrent inventory reservation
10. Recovery after partial failure

### Expert Insight

E-commerce reconstruction-এর বড় challenge হলো UI নয়; **money, inventory এবং order state-এর consistency**।

একটি সুন্দর checkout page কোনো payment lifecycle-এর correctness প্রমাণ করে না।

---

## Scenario 2: Collaborative Editor—একই Document-এ একাধিক User

এবার একটি collaborative document editor কল্পনা করো।

দুইজন user একই document খুলে লিখছে। একজন paragraph edit করছে, অন্যজন title পরিবর্তন করছে।

দুজনের screen-এ একই document থাকা মানেই তাদের data synchronization সঠিক—এমন নয়।

### ধাপ ১: Observable Behavior

দেখো:

- Document load কীভাবে হয়?
- Changes সঙ্গে সঙ্গে দেখা যায়?
- Offline থাকলে কী হয়?
- User reconnect করলে কী হয়?
- একই text একসঙ্গে edit করলে কী হয়?
- Version history আছে?
- Undo/redo কীভাবে কাজ করে?
- Permission revoke হলে open document-এর কী হয়?

### ধাপ ২: Candidate State Model

একটি document-এর থাকতে পারে:

- Current content
- Revision identifier
- Editor identity
- Local unsaved changes
- Server-confirmed changes
- Pending synchronization
- Historical revisions

এগুলো একটি conceptual model। Actual architecture আলাদা হতে পারে।

### ধাপ ৩: Concurrency

User A এবং User B একই paragraph edit করল।

সম্ভাব্য approaches:

- Operational Transformation (OT)
- Conflict-free Replicated Data Types (CRDTs)
- Version-based conflict detection
- Server-authoritative serialization
- Product-specific merge rules

কোন approach original ব্যবহার করে, তা শুধু UI দেখে নির্ধারণ করা যায় না।

কিন্তু replacement-এর জন্য প্রয়োজনীয় observable behavior থেকে design requirement তৈরি করা যায়।

### ধাপ ৪: Experiment

একটি controlled test:

1. দুটি authorized test session দিয়ে একই document খোলো।
2. দুজনের local state record করো।
3. Network delay-এর মধ্যে আলাদা edit করো।
4. উভয় session reconnect করো।
5. Final content তুলনা করো।
6. Refresh-এর পর persistence যাচাই করো।
7. Revision history এবং conflict indication পরীক্ষা করো, যদি সেগুলো product scope-এর অংশ হয়।

### ধাপ ৫: Security

একজন user-এর edit permission revoke হলে:

- নতুন edit request reject হয়?
- Existing WebSocket connection কীভাবে handle হয়?
- Client local changes রাখতে পারে?
- User কি document-এর পুরোনো content এখনও দেখতে পারে?

এগুলো authorization এবং real-time synchronization-এর সংযোগস্থল।

### Expert Insight

Collaborative Editor-এ screenshot হলো প্রায় অর্থহীনভাবে অসম্পূর্ণ evidence, যদি তুমি concurrent state, ordering, offline behavior এবং conflict resolution না বোঝো।

---

## Scenario 3: AI Agent Platform—Chatbot-এর চেয়ে অনেক বেশি কিছু

ধরা যাক, তুমি একটি AI Agent Platform পুনর্নির্মাণ করছ।

UI-তে একটি chat window আছে। User prompt লিখে। Agent উত্তর দেয়। প্রয়োজনে tool ব্যবহার করে।

কিন্তু এখানে system-এর behavior শুধু language generation দিয়ে নির্ধারিত হয় না।

### ধাপ ১: System Inventory

প্রাসঙ্গিক component হতে পারে:

- Frontend
- Conversation API
- Session management
- Model gateway
- Prompt construction
- Tool registry
- Tool execution environment
- Retrieval system
- Memory store
- Background tasks
- Usage accounting
- Rate limiting
- Audit logs
- Streaming
- Cancellation
- Error handling

সব component প্রতিটি AI product-এ থাকবে না।

### ধাপ ২: Tool Calling

ধরা যাক, Agent একটি tool call করল।

সম্ভাব্য workflow:

1. User request আসে।
2. Application model input তৈরি করে।
3. Model response দেয়।
4. Response-এ tool call থাকতে পারে।
5. Application tool permissions যাচাই করে।
6. Tool execute হয়।
7. Tool result model context-এ ফিরে যায়।
8. Model final response তৈরি করে।

Tool execution-এর permission এবং validation গুরুত্বপূর্ণ।

Model কোনো tool call করতে চেয়েছে বলেই সেটি execute করা নিরাপদ বা অনুমোদিত—এমন নয়।

### ধাপ ৩: Streaming

প্রশ্ন করো:

- Response token-by-token stream হয়?
- Client disconnect করলে generation cancel হয়?
- Tool call চলার সময় UI কী দেখায়?
- Stream মাঝপথে ব্যর্থ হলে কী হয়?
- Retry করলে duplicate tool execution হতে পারে?
- Usage accounting কীভাবে হয়?

### ধাপ ৪: Nondeterminism

একই prompt দুইবার দিলে model-এর উত্তর ভিন্ন হতে পারে।

তাই deterministic application behavior এবং nondeterministic model output আলাদা করে পরীক্ষা করতে হবে।

যেখানে exact text match উপযুক্ত নয়, সেখানে task-specific acceptance criteria দরকার হতে পারে:

- Tool call সঠিক ছিল কি?
- Permission enforcement হয়েছে কি?
- Required information উপস্থিত?
- Output schema valid?
- Unsafe side effect আটকানো হয়েছে?
- Response-এর latency গ্রহণযোগ্য?

### ধাপ ৫: Retrieval এবং Memory

যদি AI system retrieval ব্যবহার করে, তাহলে দেখো:

- Source document কীভাবে নির্বাচন হয়?
- Access permissions retrieval-এ enforce হয়?
- Stale index কীভাবে handle হয়?
- Source references দেখানো হয়?
- User-specific memory অন্য user-এর context-এ leak করতে পারে কি?

### ধাপ ৬: Verification

একটি test matrix হতে পারে:

- Normal response
- Tool call
- Invalid tool arguments
- Tool failure
- Timeout
- Cancellation
- Retrieval miss
- Unauthorized data request
- Model gateway outage
- Duplicate action attempt
- Streaming interruption
- Usage-limit exhaustion

### Expert Insight

AI Agent reconstruction-এর মূল challenge শুধু prompt নকল করা নয়। **Model behavior, orchestration, tool permissions, state management, retrieval এবং side effects—সব মিলিয়ে observable contract তৈরি হয়।**

---

## Scenario 4: Mobile Application—Offline State এবং Device Lifecycle

এবার একটি mobile application কল্পনা করো, যেখানে user notes তৈরি করতে পারে।

UI-তে note editor এবং save button আছে।

কিন্তু mobile application-এ একটি গুরুত্বপূর্ণ বিষয় হলো, user-এর network, app lifecycle এবং local state সব সময় স্থিতিশীল নয়।

### ধাপ ১: Investigation Questions

- Note কি offline-এ তৈরি করা যায়?
- Local save হয়, নাকি শুধু server save?
- App background-এ গেলে unsaved data থাকে?
- Device restart-এর পর note থাকে?
- Reconnect করলে synchronization কীভাবে হয়?
- একই note অন্য device থেকে edit করলে কী হয়?
- Session expire হলে pending changes কীভাবে handle হয়?

### ধাপ ২: State Layers

একটি note-এর state হতে পারে:

- Local draft
- Locally persisted content
- Pending upload
- Server-confirmed content
- Conflict state
- Deleted state

এগুলো আলাদা করে model না করলে data loss হতে পারে।

### ধাপ ৩: Failure Experiment

1. Online অবস্থায় note edit করো।
2. Network disconnect করো।
3. নতুন content save করো।
4. App background-এ পাঠাও।
5. App আবার খোলো।
6. Network restore করো।
7. Sync completion যাচাই করো।
8. অন্য device-এর state-এর সঙ্গে তুলনা করো।

### ধাপ ৪: Security এবং Lifecycle

Session expire হলে local draft-এর কী হবে?

User logout করলে sensitive local data থাকবে কি?

Application reinstall করলে কোন data হারাবে?

Permission revoke হলে offline cached content-এর access কীভাবে handle হবে?

### Expert Insight

Mobile reconstruction-এ network request-এর পাশাপাশি local persistence, lifecycle transitions এবং recovery semantics-ও investigate করতে হয়।

---

# অধ্যায় ১৯: Multi-Agent Engineering—একাধিক AI Agent ব্যবহার করেও কীভাবে নিয়ন্ত্রণ বজায় রাখবে

আরিফ এবার ভাবল, “আমি যদি দশটি AI Agent চালাই, তাহলে কাজ দশ গুণ দ্রুত হবে।”

নীরা বলল:

“Parallelism তখনই লাভজনক, যখন কাজগুলো স্বাধীন, evidence shared এবং integration controlled।”

একাধিক Agent ব্যবহার করলে তারা একই feature investigate করতে পারে, পরস্পরবিরোধী architecture প্রস্তাব করতে পারে, একই file edit করতে পারে, অথবা অজানা তথ্য আত্মবিশ্বাসের সঙ্গে বানিয়ে দিতে পারে।

তাই একটি Multi-Agent Workflow প্রয়োজন।

## ১৯.১ Agent-এর দায়িত্ব ভাগ করা

একটি reconstruction project-এ workstream হতে পারে:

- Product Behavior Investigator
- Frontend and State-Machine Investigator
- API and Protocol Investigator
- Data and Domain Investigator
- Distributed-Systems Investigator
- Infrastructure Investigator
- Security Reviewer
- Observability Engineer
- Differential-Test Engineer
- Integration Lead

সব project-এ এতগুলো Agent প্রয়োজন হবে না। ছোট project-এ কয়েকটি workstream একসঙ্গে পরিচালনা করা যায়।

## ১৯.২ প্রতিটি Agent-এর Contract

প্রতিটি Agent-কে দিতে হবে:

- নির্দিষ্ট প্রশ্ন
- Scope
- Available evidence
- Permitted tools
- Expected deliverable
- Definition of Done
- Explicit limitations

Finding-এর standard format:

```text
Question:
Evidence:
Conclusion:
Confidence:
Limitations:
Open Questions:
Recommended Action:
```

এতে Agent-এর output অন্য Agent যাচাই করতে পারে।

## ১৯.৩ Integration Lead-এর কাজ

Integration Lead-এর দায়িত্ব:

- Contradictory findings reconcile করা
- Shared specification maintain করা
- Duplicate investigation কমানো
- Dependency অনুযায়ী task sequence নির্ধারণ
- API contract consistency নিশ্চিত করা
- Architecture decision review করা
- Generated code পরীক্ষা করা
- Regression tests চালানো

## ১৯.৪ AI Coding-এর সবচেয়ে বড় বিপদ

AI Agent অনেক সময় plausible implementation তৈরি করে, কিন্তু তার নিজের implementation-কে বাস্তবে verify করে না।

তাই প্রতিটি গুরুত্বপূর্ণ task-এর সঙ্গে থাকতে হবে:

1. Expected behavior
2. Acceptance criteria
3. Test command
4. Actual test result
5. Remaining limitations

যদি Agent বলে “সব tests pass”, তাহলে কোন tests, কোন environment-এ, সত্যিই execute হয়েছে কি না, তা জানতে হবে।

যদি test run করা না যায়, status হবে `IMPLEMENTED, UNVERIFIED` অথবা উপযুক্ত blocker status—`VERIFIED` নয়।

## ১৯.৫ Prompt-এর সঙ্গে Shared Memory

একটি বিশাল system prompt-এর ওপর সব দায়িত্ব চাপিয়ে দেওয়া উচিত নয়।

বরং project artifacts-কে source of truth করো:

- Scope
- Evidence Ledger
- Unknowns Register
- Behavioral Specification
- API Contracts
- Architecture Decisions
- Verification Matrix
- Fidelity Report

Agent context হারালেও persistent artifacts থেকে কাজের অবস্থা পুনরুদ্ধার করা যায়।

এখানেই Prompt Engineering, Context Engineering, Repository Design এবং Verification একসঙ্গে কাজ করে।

---

# অধ্যায় ২০: Production Readiness—Application চলছে মানেই Ready নয়

আরিফ এবার সব feature complete ঘোষণা করতে চাইল।

নীরা তাকে একটি শেষ প্রশ্ন করল:

“Database backup থেকে restore করে দেখেছ?”

আরিফ বলল, “Backup configuration আছে।”

নীরা বলল, “আমি restore test-এর কথা জিজ্ঞেস করেছি।”

এই পার্থক্যটি Production Engineering-এর কেন্দ্রীয় বিষয়।

Configuration থাকা আর কার্যকরভাবে কাজ করা এক নয়।

## ২০.১ Production Readiness Checklist

প্রয়োজন অনুযায়ী পরীক্ষা করো:

### Build and Delivery

- Reproducible build
- Dependency management
- Artifact versioning
- Automated tests
- CI/CD
- Controlled release
- Rollback strategy

### Security

- Secret management
- Least privilege
- Dependency scanning
- Input validation
- Authorization testing
- Sensitive data redaction

### Data

- Migration safety
- Backup policy
- Restore testing
- Retention
- Deletion
- Data export
- Recovery procedures

### Operations

- Health checks
- Structured logs
- Metrics
- Distributed traces
- Alerts
- Dashboards
- Incident runbooks
- Capacity planning
- Cost controls

### Reliability

- Timeout policy
- Retry policy
- Dependency failure handling
- Queue monitoring
- Recovery testing
- Deployment rollback
- Disaster recovery planning

সব application-এ একই level-এর infrastructure প্রয়োজন নয়। Scope এবং risk অনুযায়ী নির্বাচন করতে হবে।

## ২০.২ Deployment-এর সময় কী কী ভুল হতে পারে?

- Migration সফল, কিন্তু পুরোনো code নতুন schema handle করতে পারে না।
- নতুন version deploy হয়েছে, কিন্তু background worker পুরোনো version-এ চলছে।
- Secret rotate করা হয়েছে, কিন্তু একটি service পুরোনো credential ব্যবহার করছে।
- Queue backlog deployment-এর পরে বেড়ে যাচ্ছে।
- Rollback করা হয়েছে, কিন্তু schema backward-compatible নয়।
- Health check green, কিন্তু মূল business operation ব্যর্থ।

Production readiness মানে শুধু infrastructure status green নয়। গুরুত্বপূর্ণ user journey-গুলো বাস্তবে কাজ করছে কি না, সেটিও জানতে হবে।

---

# অধ্যায় ২১: Fidelity Report—কখন বলবে, কাজটি সত্যিই সম্পন্ন?

একটি reconstruction project-এর শেষ পর্যায়ে সবচেয়ে বিপজ্জনক বাক্য হতে পারে:

“সবকিছু complete।”

কারণ এই বাক্যটি অনেক সময় কোনো নির্দিষ্ট evidence ছাড়া বলা হয়।

তার বদলে প্রতিটি subsystem-এর status আলাদা করে report করো।

## ২১.১ ছয়টি Status

### VERIFIED

নির্দিষ্ট claim তার defined test পাস করেছে।

### PARTIALLY VERIFIED

কিছু condition যাচাই হয়েছে, কিন্তু পুরো requirement নয়।

### IMPLEMENTED, UNVERIFIED

Code আছে, কিন্তু পর্যাপ্ত verification নেই।

### ASSUMED

Implementation একটি unconfirmed assumption-এর ওপর নির্ভর করছে।

### BLOCKED

Access, dependency বা environment limitation-এর কারণে কাজ বা verification আটকে আছে।

### NOT IMPLEMENTED

Feature এখনও implement করা হয়নি বা agreed scope-এর বাইরে রয়েছে।

## ২১.২ Example Report

ধরা যাক, RelayDesk-এর ৫০টি acceptance scenario নির্ধারণ করা হয়েছে।

- ৪২টি পাস করেছে।
- ৩টি fail করেছে।
- ২টি execute করা যায়নি।
- ৩টি এখনও implement করা হয়নি।

তাহলে সঠিক report হবে:

“৫০টি enumerated acceptance scenario-এর মধ্যে ৪২টি pass করেছে; ৩টি fail, ২টি blocked এবং ৩টি not implemented।”

এখানে pass rate ৮৪%। কিন্তু এই সংখ্যাটি শুধু ওই defined scenario set-এর জন্য অর্থপূর্ণ।

যদি ৩টি critical security test fail করে এবং ১০টি cosmetic test pass করে, তাহলে শুধু aggregate percentage দেখে release decision নেওয়া যাবে না।

Criticality এবং risk আলাদাভাবে বিবেচনা করতে হবে।

## ২১.৩ Stopping Rule

কখন investigation থামাবে?

যখন:

- Agreed scope যথেষ্টভাবে covered।
- Critical user journeys-এর acceptance criteria পূরণ হয়েছে।
- High-risk security ও data invariants যাচাই করা হয়েছে।
- Required operational controls পরীক্ষা করা হয়েছে।
- Remaining discrepancies স্পষ্টভাবে documented।
- Blocked items-এর কারণ জানা।
- Further work-এর expected value তার cost-এর তুলনায় গ্রহণযোগ্য নয়, অথবা access limitation বাস্তব।

কিন্তু কোনো unknown অমীমাংসিত থাকলে সেটিকে “সমাধান হয়েছে” বলা যাবে না।

**একটি disciplined engineer শুধু completion ঘোষণা করে না; completion-এর শর্তগুলো কেন পূরণ হয়েছে, সেটিও দেখায়।**

---

# অধ্যায় ২২: ৩০ দিনের Reverse Engineering Practice Plan

এই জ্ঞানকে বাস্তবে রূপ দিতে একটি ৩০ দিনের practice plan অনুসরণ করা যায়।

এটি একটি প্রস্তাবিত learning schedule; তোমার project scope অনুযায়ী পরিবর্তন করা যাবে।

## দিন ১–৩: Observation এবং Scope

- একটি ছোট, অনুমোদিত target নির্বাচন করো।
- Scope এবং access boundaries লিখে ফেলো।
- UI routes এবং major workflows map করো।
- Feature inventory তৈরি করো।
- Existing repository থাকলে baseline inspect করো।

**Deliverable:** Project Scope এবং Feature Inventory।

## দিন ৪–৬: Evidence এবং Unknowns

- Evidence classification শিখো।
- Evidence Ledger তৈরি করো।
- Unknowns Register তৈরি করো।
- প্রতিটি high-impact unknown-এর জন্য একটি experiment design করো।
- আগের findings-এর limitations লিখো।

**Deliverable:** Evidence Ledger এবং Unknowns Register।

## দিন ৭–১০: UI এবং API

- গুরুত্বপূর্ণ UI state map করো।
- Authorized request/response evidence সংগ্রহ করো।
- API catalog তৈরি করো।
- Error behavior এবং validation পরীক্ষা করো।
- Critical workflows-এর acceptance criteria লিখো।

**Deliverable:** Behavioral Specification এবং API Contracts।

## দিন ১১–১৪: Domain এবং Data

- Candidate domain model তৈরি করো।
- State transitions লিখো।
- Invariants এবং decision tables তৈরি করো।
- Data lifecycle map করো।
- Concurrency ও persistence-এর প্রধান unknowns চিহ্নিত করো।

**Deliverable:** Data and State Model।

## দিন ১৫–১৮: Architecture এবং Implementation

- Architecture alternatives তুলনা করো।
- Decision records তৈরি করো।
- একটি complete vertical slice implement করো।
- Automated tests লেখো।
- Real persistence এবং mock boundary স্পষ্ট করো।

**Deliverable:** প্রথম verified end-to-end workflow।

## দিন ১৯–২২: Differential Verification

- Original evidence-এর সঙ্গে replacement তুলনা করো।
- API, UI, data এবং error behavior পরীক্ষা করো।
- Discrepancy Register তৈরি করো।
- High-impact mismatch ঠিক করো।
- Regression tests যোগ করো।

**Deliverable:** Verification Matrix এবং updated gap backlog।

## দিন ২৩–২৬: Reliability এবং Security

- Permission boundary পরীক্ষা করো।
- Duplicate requests এবং concurrent updates পরীক্ষা করো।
- Failure এবং recovery scenarios চালাও।
- Logging, metrics এবং tracing যাচাই করো।
- Backup এবং restore strategy পরীক্ষা করো।

**Deliverable:** Security এবং Reliability test report।

## দিন ২৭–৩০: Production এবং Fidelity

- Deployment pipeline পরীক্ষা করো।
- Critical workflows-এর release criteria নির্ধারণ করো।
- Remaining assumptions এবং blockers document করো।
- Fidelity Report তৈরি করো।
- পরবর্তী তিনটি highest-value engineering task নির্বাচন করো।

**Deliverable:** Evidence-backed release assessment।

এই পরিকল্পনার লক্ষ্য ৩০ দিনে সব ধরনের software reverse engineering শিখে ফেলা নয়। লক্ষ্য হলো একটি repeatable workflow শেখা, যেটিকে পরবর্তী project-এ আরও গভীর করা যায়।

---

# অধ্যায় ২৩: একজন Expert-এর Daily Operating Loop

প্রতিদিন কাজ শুরু করার আগে নিজেকে পাঁচটি প্রশ্ন করো।

### ১. আমি এখন কী জানি?

Evidence-backed findings এবং verified requirements দেখো।

### ২. কী গুরুত্বপূর্ণ বিষয় এখনও অজানা?

Unknowns Register থেকে high-impact items বের করো।

### ৩. সবচেয়ে মূল্যবান পরবর্তী পদক্ষেপ কী?

আরও evidence সংগ্রহ, experiment, implementation, অথবা verification—কোনটি এখন প্রয়োজন?

### ৪. আমার কাজ কীভাবে যাচাই হবে?

Acceptance criteria, automated test এবং expected outcome নির্ধারণ করো।

### ৫. কাজ শেষে কী update হবে?

Evidence Ledger, Specification, Architecture Decision, Verification Matrix অথবা Fidelity Report—যেটি প্রাসঙ্গিক, সেটি update করো।

এতে কাজের ধারাবাহিকতা বজায় থাকে।

## Weekly Review

সপ্তাহে অন্তত একবার পর্যালোচনা করো:

- কোন critical journey এখনও incomplete?
- কোন feature hardcoded fixture-এর ওপর নির্ভর করছে?
- কোন assumption architecture-কে প্রভাবিত করছে?
- কোন test অনুপস্থিত?
- কোন discrepancy বারবার ফিরে আসছে?
- কোন tool call নতুন evidence দিচ্ছে না?
- কোন workstream duplicate investigation করছে?
- কোন operational risk এখনও untested?
- কোন blocker external access-এর ওপর নির্ভর করছে?

এই review তোমাকে শুধু বেশি code লিখতে নয়, বরং সঠিক কাজ করতে সাহায্য করবে।

---

# অধ্যায় ২৪: ২৫টি Expert Heuristic—যেগুলো মাথায় রাখবে

১. Screenshot একটি observation, specification নয়।

২. HTTP response একটি evidence source, পুরো backend-এর বিবরণ নয়।

৩. UI update মানেই persistence নিশ্চিত নয়।

৪. API response success মানেই সব side effect সম্পন্ন নয়।

৫. একটি successful test global equivalence প্রমাণ করে না।

৬. Inaccessible internal architecture সম্পর্কে অনুমানকে fact হিসেবে লিখবে না।

৭. Existing code rewrite করার আগে তার behavior এবং tests বোঝো।

৮. প্রতিটি high-impact requirement-এর traceability থাকা উচিত।

৯. Unknowns Register বাদ দেবে না।

১০. Tool ব্যবহার করার আগে নির্দিষ্ট প্রশ্ন ঠিক করো।

১১. একই experiment পুনরাবৃত্তি করো তখনই, যখন নতুন তথ্য পাওয়ার যুক্তিসংগত কারণ আছে।

১২. Duplicate requests এবং retry behavior পরীক্ষা করো।

১৩. Concurrency-কে শুধু happy-path testing দিয়ে যাচাই করা যায় না।

১৪. Authorization frontend-এর ওপর ছেড়ে দেবে না।

১৫. Data lifecycle-এ deletion, retention এবং derived data অন্তর্ভুক্ত করো।

১৬. Mock-কে production implementation হিসেবে উপস্থাপন করবে না।

১৭. Vertical slice দিয়ে end-to-end behavior তৈরি করো।

১৮. Failing test-কে দুর্বল করে সবুজ dashboard তৈরি করবে না।

১৯. Architecture trend দেখে নয়, requirement দেখে নির্বাচন করো।

২০. Observability-কে production system-এর অংশ হিসেবে design করো।

২১. Performance comparison-এর workload এবং environment স্পষ্ট করো।

২২. Multi-Agent workflow-এ common evidence format ব্যবহার করো।

২৩. Agent-এর confidence-এর বদলে তার evidence এবং test result যাচাই করো।

২৪. Fidelity percentage-এর denominator সব সময় স্পষ্ট করো।

২৫. Unknown থাকলে সেটিকে unknown হিসেবেই report করো।

---

# উপসংহার: Reverse Engineer নয়, Evidence-Driven System Builder হও

রাত ২টা ১৭ মিনিটের সেই ঘটনার কয়েক সপ্তাহ পর আরিফ আবার তার কম্পিউটারের সামনে বসে আছে।

RelayDesk-এর নতুন সংস্করণটি এখন আগের চেয়ে অনেক বেশি সুসংগঠিত।

সে আর শুধু screenshot দেখে code লেখে না।

প্রথমে scope নির্ধারণ করে। তারপর evidence সংগ্রহ করে। Feature inventory তৈরি করে। Unknowns Register-এ uncertainty লিখে রাখে। Critical workflow-এর state machine এবং API contract তৈরি করে। তারপর একটি vertical slice implement করে।

প্রতিটি গুরুত্বপূর্ণ requirement-এর জন্য test আছে।

প্রতিটি বড় discrepancy-এর জন্য একটি record আছে।

যে subsystem যথেষ্ট verify করা হয়নি, সেটিকে complete বলা হচ্ছে না।

যে architecture original-এর source থেকে জানা যায়নি, সেটিকে reconstructed fact বলা হচ্ছে না।

যে tool ব্যবহার করা সম্ভব হয়নি, সেটি ব্যবহৃত হয়েছে বলে দাবি করা হচ্ছে না।

আরিফ এখনো সব জানে না।

কিন্তু তার একটি বড় পরিবর্তন হয়েছে।

আগে সে অজানা বিষয়গুলো দ্রুত পূরণ করে ফেলত—কখনো নিজের ধারণা দিয়ে, কখনো AI-এর তৈরি plausible explanation দিয়ে।

এখন সে অজানাকে একটি engineering object হিসেবে দেখে।

সে জানে, কোন unknown গুরুত্বপূর্ণ, কোনটি investigate করা সম্ভব, কোনটি implementation decision দিয়ে সামলানো যায়, এবং কোনটি report-এ limitation হিসেবে রাখতে হবে।

একদিন নীরা তাকে জিজ্ঞেস করল:

“তুমি কি এখন মনে করো যে যেকোনো application শতভাগ clone করতে পারবে?”

আরিফ কিছুক্ষণ চিন্তা করে উত্তর দিল:

“না। কারণ সব internal detail সব সময় observable নয়। সব behavior finite test suite দিয়ে প্রমাণ করা যায় না। Original-এর কিছু implementation detail অপ্রাপ্য থাকতে পারে। আবার কিছু behavior পুনর্নির্মাণের জন্য একই internal technology প্রয়োজনও নাও হতে পারে।”

নীরা বলল, “তাহলে তুমি কী শিখেছ?”

আরিফ উত্তর দিল:

“আমি শিখেছি, software reconstruction মানে কল্পনা দিয়ে অজানা জায়গা পূরণ করা নয়। বরং evidence দিয়ে অজানার সীমানা ছোট করা। যেখানে evidence নেই, সেখানে uncertainty স্পষ্ট রাখা। তারপর এমন implementation তৈরি করা, যার behavior পরীক্ষা করা যায়, যার failure বোঝা যায়, এবং যার limitation নিয়ে সৎভাবে কথা বলা যায়।”

নীরা এবার হাসল।

কারণ আরিফ এখন শুধু code generation করতে শিখছে না। সে engineering judgment তৈরি করছে।

## শেষবারের মতো মনে রাখবে

**Reverse Engineering-এর প্রকৃত শক্তি তুমি কতগুলো hidden technology-এর নাম জানো, তার মধ্যে নেই। শক্তি হলো—তুমি কীভাবে একটি প্রশ্ন তৈরি করো, কোন evidence বিশ্বাস করো, কীভাবে competing hypothesis আলাদা করো, কীভাবে একটি system-এর behavior model করো, এবং কীভাবে তোমার implementation-এর correctness প্রমাণ করো।**

AI যুগে code তৈরি করা আগের চেয়ে সহজ হচ্ছে। কিন্তু একটি বড় codebase তৈরি করতে পারা আর একটি জটিল system সঠিকভাবে পুনর্নির্মাণ করতে পারা এক জিনিস নয়।

AI Agent তোমার হয়ে অনেক code লিখতে পারে। Browser automation অনেক interaction পর্যবেক্ষণ করতে পারে। Static analysis কিছু implementation detail প্রকাশ করতে পারে। API tests অনেক contract যাচাই করতে পারে। Distributed tracing failure-এর কারণ বুঝতে সাহায্য করতে পারে।

কিন্তু এই সব capability-কে একটি coherent engineering process-এ যুক্ত করার দায়িত্ব তোমার।

সেই process-এর কেন্দ্র হলো:

**Observe → Investigate → Specify → Implement → Verify → Measure → Improve**

এটি একবার সম্পন্ন করার checklist নয়। এটি একটি continuous learning loop।

প্রতিটি project তোমাকে নতুন কিছু শেখাবে। প্রতিটি discrepancy নতুন প্রশ্ন তৈরি করবে। প্রতিটি failure তোমার model উন্নত করার সুযোগ দেবে। প্রতিটি verified requirement তোমার অনিশ্চয়তার একটি অংশ কমাবে।

আর সবচেয়ে গুরুত্বপূর্ণ বিষয়টি হলো—তুমি কখনো নিজের knowledge-এর সীমা লুকাবে না।

কারণ একজন সত্যিকারের expert-এর শক্তি সব উত্তর জানা নয়।

**তার শক্তি হলো, কোন উত্তরটি সত্যিই জানা, কোনটি evidence-সমর্থিত inference, কোনটি এখনও hypothesis, এবং কোনটি অজানা—এই চারটির পার্থক্য নির্ভুলভাবে বুঝতে পারা।**

এটাই একটি screenshot clone থেকে production-capable reconstruction-এর যাত্রা।

এটাই AI-assisted coding থেকে evidence-driven engineering-এর যাত্রা।

এবং এটাই Reverse Engineering-কে একটি tool ব্যবহার করার দক্ষতা থেকে একটি গভীর, পুনর্ব্যবহারযোগ্য engineering discipline-এ রূপান্তরিত করে।

---

## পরিশিষ্ট A: Project শুরু করার জন্য Master Checklist

যে কোনো নতুন reconstruction project-এ নিচের checklist-টি ব্যবহার করতে পারো।

### Scope and Access

- [ ] Target এবং desired outcome স্পষ্ট।
- [ ] Authorized access এবং investigation boundaries নির্ধারিত।
- [ ] Existing repository এবং artifacts inspect করা হয়েছে।
- [ ] Available tools এবং limitations জানা আছে।

### Evidence and Discovery

- [ ] Feature inventory তৈরি হয়েছে।
- [ ] Critical user journeys map করা হয়েছে।
- [ ] Evidence Ledger তৈরি হয়েছে।
- [ ] Unknowns Register তৈরি হয়েছে।
- [ ] গুরুত্বপূর্ণ dependency graph তৈরি হয়েছে।
- [ ] Hypothesis এবং observation আলাদা রাখা হয়েছে।

### Specification

- [ ] Critical API contracts লেখা হয়েছে।
- [ ] Domain rules এবং invariants স্পষ্ট।
- [ ] State transitions document করা হয়েছে।
- [ ] Data lifecycle এবং ownership model করা হয়েছে।
- [ ] Security boundaries নির্ধারিত।
- [ ] Acceptance criteria testable।

### Implementation

- [ ] Existing code এবং architecture review করা হয়েছে।
- [ ] Vertical slice দিয়ে implementation করা হচ্ছে।
- [ ] Mock এবং real integration আলাদা।
- [ ] Error handling আছে।
- [ ] Persistence এবং reload behavior যাচাই করা হয়েছে।
- [ ] Regression tests যোগ করা হচ্ছে।

### Verification

- [ ] Critical happy paths পরীক্ষা করা হয়েছে।
- [ ] Negative এবং boundary cases পরীক্ষা করা হয়েছে।
- [ ] Authorization পরীক্ষা করা হয়েছে।
- [ ] Duplicate requests এবং concurrency পরীক্ষা করা হয়েছে, যেখানে প্রাসঙ্গিক।
- [ ] Failure recovery পরীক্ষা করা হয়েছে।
- [ ] Visual ও behavioral discrepancies record করা হয়েছে।
- [ ] Test results সত্যিকার execution-এর ভিত্তিতে report করা হয়েছে।

### Production

- [ ] Reproducible build।
- [ ] Safe migration strategy।
- [ ] Secret এবং permission management।
- [ ] Logs, metrics, traces।
- [ ] Alerting এবং incident response।
- [ ] Backup এবং restore verification।
- [ ] Deployment rollback।
- [ ] Capacity এবং cost controls।

### Completion

- [ ] Fidelity Report তৈরি।
- [ ] Verified এবং unverified behavior আলাদা।
- [ ] Blocked এবং assumed items document করা হয়েছে।
- [ ] Remaining critical risks স্পষ্ট।
- [ ] Next three highest-value actions নির্ধারিত।

---

## পরিশিষ্ট B: একটি ছোট Reconstruction Project-এর Document Structure

```text
reconstruction/
├── 00-project-scope.md
├── 01-feature-inventory.md
├── 02-evidence-ledger.md
├── 03-unknowns-register.md
├── 04-behavioral-specification.md
├── 05-api-contracts.md
├── 06-data-and-state-model.md
├── 07-architecture-decisions.md
├── 08-verification-matrix.md
├── 09-fidelity-report.md
├── discrepancies/
│   ├── D-001.md
│   └── D-002.md
├── experiments/
│   ├── EXP-001.md
│   └── EXP-002.md
└── reports/
    └── milestone-review.md
```

এই structure একটি প্রস্তাবিত template। Existing repository-তে equivalent artifacts থাকলে অকারণে duplicate তৈরি করবে না।

---

## পরিশিষ্ট C: AI Coding Agent-এর জন্য সংক্ষিপ্ত Execution Prompt

নিচের prompt-টি কোনো বাস্তব project-এর জন্য অভিযোজিত করা যায়।

> **Role:** Act as an evidence-driven Principal Reconstruction Engineer.
>
> **Objective:** Reconstruct the target's required observable behavior within the authorized scope. Do not confuse visual similarity with behavioral equivalence.
>
> **Before implementation:** Inspect the repository, project instructions, existing tests, available tools, and existing evidence. Create or update the project scope, feature inventory, evidence ledger, unknowns register, behavioral specification, architecture decisions, verification matrix, and fidelity report.
>
> **During investigation:** Separate observed facts, derived findings, inferences, assumptions, unknowns, and contradicted claims. Design controlled experiments for high-impact uncertainties. Never invent discovered endpoints, database schemas, infrastructure, or test results.
>
> **During implementation:** Work in complete vertical slices. Reuse existing architecture when appropriate. Define acceptance criteria, implement the required behavior, add tests, run the application, compare against available evidence, fix discrepancies, and add regression tests.
>
> **During verification:** Test relevant happy paths, negative cases, authorization, persistence, concurrency, asynchronous processing, and failure recovery. Report exactly which tests ran and passed.
>
> **During production hardening:** Address security, observability, migrations, deployment, backups, rollback, performance, and recovery according to the actual project requirements.
>
> **At every milestone:** Update the evidence ledger, unknowns register, discrepancy backlog, and fidelity report. Distinguish VERIFIED, PARTIALLY VERIFIED, IMPLEMENTED BUT UNVERIFIED, ASSUMED, BLOCKED, and NOT IMPLEMENTED.
>
> **Completion rule:** Do not claim universal equivalence. Report the defined scope, verified behavior, known mismatches, unresolved unknowns, blockers, and the next three highest-value actions.
>
> **Operating principle:** Investigate deliberately. Implement incrementally. Verify relentlessly. Report honestly.

---

**এই Handbook-এর চূড়ান্ত শিক্ষা:** তুমি যখন পরবর্তীবার কোনো application দেখে AI Agent-কে বলবে “এটি clone করো”, তখন যেন সেটিই তোমার পুরো instruction না হয়। সেটি হবে শুধু project-এর নাম। আসল কাজ হবে evidence সংগ্রহ, behavior বোঝা, requirements তৈরি, implementation এবং verification-এর সম্পূর্ণ engineering process।