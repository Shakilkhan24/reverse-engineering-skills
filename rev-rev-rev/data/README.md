# চার্টের ডেটা

এখানকার সব dataset **synthetic teaching data**। কোনো বাস্তব service-এর benchmark নয়। [make_figures.py](../scripts/make_figures.py) এগুলো তৈরি করে এবং PNG/SVG export করে।

| File | Model / unit |
|---|---|
| [priority.csv](priority.csv) | heuristic score; impact × uncertainty ÷ hours |
| [latency.csv](latency.csv) | ১০০ request; milliseconds |
| [queue.csv](queue.csv) | discrete minute, job count; capacity ১০/minute |
| [retries.csv](retries.csv) | ৪০ client × ৩ retries; seconds; seed ৪২ |
| [verification.csv](verification.csv) | 0=NOT RUN, 1=PASS, 2=FAIL, 3=BLOCKED |
| [fidelity.csv](fidelity.csv) | ৫০ enumerated scenario-এর category counts |
| [practice-plan.csv](practice-plan.csv) | প্রস্তাবিত phase start ও day count |
| [summary.json](summary.json) | calculated summary ও percentile method |

CSV-তে পরিবর্তন করে বর্তমান script চালালে CSV আবার overwrite হবে, কারণ script data **generate** করে। স্থায়ী variant-এর জন্য script-এর source arrays/parameters বদলাও বা আলাদা analysis script দিয়ে CSV পড়ো। Default figures ফেরত পেতে source parameters ফিরিয়ে rebuild করো।

