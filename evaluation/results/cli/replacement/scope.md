# Local CLI reconstruction scope

Target: `../reference.py`, SHA-256 `ee8071e68c18a9b37e027f624991ad63f8505bc49c30824becbbc4535c6a07ba`.
Owner: this single evaluation agent. Profile: minimal. The user authorizes source reading and local execution with synthetic data, plus implementation and checks entirely inside this directory.

Deliver a Python standard-library-only CLI invoked as `python3 replacement.py --db PATH {put,list,remove} [key] [value]`. No network, deployment, UI, service, dependency installation, or library modifications. The artifact is local source plus run instructions.

Available: Python 3.12.3, sqlite3, shell, full reference source, executable reference, reconstruction state helper. Not required: REA, browser, network, deployment. No pre-existing replacement or project records were present.

## Contract and evidence

Evidence E-001 retains all source in `reconstruction/artifacts/reference-source.txt`; E-002 retains eight reference probe results in `reconstruction/artifacts/discovery.json`. The structured ledger holds six requirements R-001 through R-006, design D-001, and seven scenarios S-001 through S-007.

- Parser: required `--db`; required action from `put`, `list`, `remove`; optional key and value. Use default argparse behavior, including help, abbreviation, invalid-option handling, and positional limitations. Program name naturally follows the invoked file name.
- Storage: connect with sqlite3 defaults, then `create table if not exists items (key text primary key, value text not null)`. This precedes semantic validation. Parser failures occur before connecting. Keep SQL parameter binding and transaction boundaries.
- Put: reject missing/empty key or absent value with stdout `{"error": "key and value required"}` and exit 2. Empty value is valid. Query current value: different value gives `{"error": "key conflict"}` and exit 3; identical insertion succeeds. Insert-or-ignore and commit. Return key/value JSON and newline.
- List: query `key,value` in SQLite key order, encode as an array of key/value objects with default json.dumps formatting. Optional positional key/value are ignored.
- Remove: reject missing/empty key with stdout `{"error": "key required"}` and exit 2. Delete exact key, commit, return boolean `removed`. Optional value is ignored.
- Use default JSON ASCII escaping and whitespace; preserve all exact strings, including whitespace and empty values. New processes must see committed state. Existing compatible SQLite files must work with both programs.
- Unhandled SQLite errors remain unhandled: compare exit code, stdout, and terminal exception type/message. Traceback source paths, stack structure, and line numbers reflect different implementations and are not compatibility targets.

## Acceptance and limits

Use identical Python, locale, and fixtures. Differential checks compare stdout, stderr, exit status, file existence, schema, and ordered logical database rows. Normalize only argparse's invoked basename; SQLite error scenarios additionally compare terminal exceptions rather than implementation stack frames. Record raw outputs before normalization. Do not normalize JSON, ordering, meaningful messages, or state differences.

Stop when all seven enumerated scenarios pass, evidence records validate, and the finite helper gate passes. These counts describe tested scenarios, not exhaustive equivalence. Concurrent interleavings, crash recovery, lock timing, arbitrary damaged/pre-existing schemas, OS/Python-version parity, and performance benchmarks remain outside the claim. No additional external action is needed.

On resume, read `reconstruction/state.json`, verify target and replacement SHA-256, review latest results and this scope, then run `python3 check_compatibility.py` followed by the helper validation/report/gate commands in README.md. A code/target/contract change requires fresh runs; prior logs are retained.
