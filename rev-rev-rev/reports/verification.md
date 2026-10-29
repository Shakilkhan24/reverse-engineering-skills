# চালানো যাচাইয়ের ফল

এই report `scripts/verify_book.py` চালিয়ে তৈরি। এটি local teaching artifact-এর ফল; বাস্তব reference product-এর fidelity report নয়।

- UTC execution: `2026-10-29T06:39:56.372137+00:00`
- Interpreter: Python `3.11.15`; SQLite `3.53.1`
- Document: ২৪ অধ্যায়, চার পরিশিষ্ট, 36 PNG + 36 SVG; প্রতিটি অধ্যায়ে অন্তত একটি visual।
- Local link checked: 319; parsed JSON code block: 20 (combined book-এ পুনরাবৃত্তিসহ)।
- HTML: 36 embedded image, alt text ও internal anchor পরীক্ষা।
- Latency dataset: mean ও nearest-rank p50/p95/p99 recomputed।
- Demo: duplicate, reopen, forbidden, payload conflict, stale update ও ack-gap result assertions checked।
- Lab: 14 tests; 0 failures; 0 errors।
- Document problems: 0।

| Test | Actual result |
|---|---|
| `test_01_persistence_after_reopen` | PASS |
| `test_02_same_key_replays_one_ticket_and_event` | PASS |
| `test_03_changed_payload_conflicts` | PASS |
| `test_04_cross_workspace_read_and_write_denied` | PASS |
| `test_05_stale_version_rejected` | PASS |
| `test_06_invalid_transition_preserves_state` | PASS |
| `test_07_precommit_fault_rolls_back_every_record` | PASS |
| `test_08_provider_ack_gap_survives_reopen` | PASS |
| `test_09_provider_failure_leaves_pending_work` | PASS |
| `test_10_overlapping_duplicate_requests` | PASS |
| `test_11_overlapping_versioned_updates` | PASS |
| `test_12_validation_boundaries` | PASS |
| `test_13_key_scope_is_actor_and_workspace` | PASS |
| `test_14_replay_returns_original_response_after_transition` | PASS |

## Artifacts

- [Machine-readable verification](verification.json)
- [Actual unittest output](test-output.txt)
- [Actual demo output](lab-results.json)

## যাচাইয়ের সীমা

HTML-এর structural integrity এবং বর্তমান build-এর Chromium desktop/mobile image, font, zoom ও navigation interaction যাচাই হয়েছে। Chart-গুলো আলাদাভাবে visual inspection করা হয়েছে। Lab-এ বাস্তব HTTP/UI/authentication, provider integration, power-loss recovery বা production throughput পরীক্ষা নেই। Crash window-তে exception injection ব্যবহার করা হয়েছে।

Original input SHA-256: `0a324676ca17bab5f84d14413e2439aa747e52476b6038e726c74c5c192a30de`
