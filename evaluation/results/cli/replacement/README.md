# Compatible local key/value CLI

Python 3 with its standard-library `sqlite3` module is sufficient. From this directory:

```bash
python3 replacement.py --db example.sqlite put greeting hello
python3 replacement.py --db example.sqlite list
python3 replacement.py --db example.sqlite remove greeting
python3 replacement.py --help
```

`put` repeats successfully for an identical value. A different value for an existing key returns `{"error": "key conflict"}` and exits 3. Missing operands return JSON errors and exit 2; argparse errors use stderr. Successful commands exit 0. Data persists in an ordinary SQLite file compatible with the reference.

Run the retained differential checks while `../reference.py` and the suite helper remain available:

```bash
python3 check_compatibility.py
python3 /mnt/c/Users/User/OneDrive/Desktop/REVRS_SKLS/skills/reconstruct-orchestrate/scripts/project_state.py validate reconstruction/state.json
python3 /mnt/c/Users/User/OneDrive/Desktop/REVRS_SKLS/skills/reconstruct-orchestrate/scripts/project_state.py report reconstruction/state.json
python3 /mnt/c/Users/User/OneDrive/Desktop/REVRS_SKLS/skills/reconstruct-orchestrate/scripts/project_state.py gate reconstruction/state.json
```

The application has no dependency on the suite helper. The check runner records fresh fixtures and append-only run artifacts under this directory. It rejects a changed reference digest until investigation and contracts are updated. If the skills directory moves, update `HELPER` in the runner before rerunning it. Read `scope.md` and `reconstruction/state.json` before resuming work.

`evaluation-result.md` describes the actual results and compatibility limits. Raw comparisons and the captured source live under `reconstruction/artifacts/`.
