"""Run and retain differential CLI checks using only the Python standard library."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import platform
import sqlite3
import subprocess
import sys
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent
REFERENCE = ROOT.parent / 'reference.py'
CANDIDATE = ROOT / 'replacement.py'
RECORDS = ROOT / 'reconstruction'
STATE = RECORDS / 'state.json'
HELPER = Path('/mnt/c/Users/User/OneDrive/Desktop/REVRS_SKLS/skills/reconstruct-orchestrate/scripts/project_state.py')
STAMP = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
FIXTURES = ROOT / 'fixtures' / STAMP
FIXTURES.mkdir(parents=True)
ENV = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONIOENCODING='utf-8', LC_ALL='C.UTF-8', COLUMNS='80')


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save_state(state):
    temporary = STATE.with_suffix('.tmp')
    temporary.write_text(json.dumps(state, indent=2) + '\n')
    temporary.replace(STATE)


def snapshot(path):
    if not path.exists():
        return {'exists': False}
    if path.is_dir():
        return {'exists': True, 'kind': 'directory'}
    result = {'exists': True, 'kind': 'file'}
    try:
        with sqlite3.connect('file:' + quote(str(path)) + '?mode=ro', uri=True) as connection:
            result['schema'] = connection.execute('select type,name,tbl_name,sql from sqlite_master order by type,name').fetchall()
            if any(row[1] == 'items' for row in result['schema']):
                result['rows'] = connection.execute('select * from items order by 1').fetchall()
    except sqlite3.Error as error:
        result['error'] = type(error).__name__ + ': ' + str(error)
    return result


class Scenario:
    def __init__(self, sid):
        self.sid = sid
        self.steps = []
        self.errors = []
        self.directory = FIXTURES / sid
        self.directory.mkdir()
        # Matching argv[0] basenames give identical argparse help line wrapping.
        # These symlinks only read their targets; all output stays in fixtures/.
        self.programs = []
        for label, target in [('reference', REFERENCE), ('replacement', CANDIDATE)]:
            program = self.directory / label / 'keyvalue.py'
            program.parent.mkdir()
            program.symlink_to(target)
            self.programs.append(program)

    def paths(self, name='database'):
        return [self.directory / 'reference' / (name + '.sqlite'), self.directory / 'replacement' / (name + '.sqlite')]

    def invoke(self, program, args, db):
        actual = [arg.replace('<DB>', str(db)) for arg in args]
        command = [sys.executable, str(program), *actual]
        process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=ENV, cwd=ROOT, timeout=15)
        return {'command': command, 'returncode': process.returncode, 'stdout': process.stdout.decode('utf-8'), 'stderr': process.stderr.decode('utf-8'), 'state': snapshot(db)}

    def pair(self, args, name='database', exception=False, right_reference=False):
        dbs = self.paths(name)
        left = self.invoke(self.programs[0], args, dbs[0])
        right = self.invoke(self.programs[0] if right_reference else self.programs[1], args, dbs[1])
        comparable = ['returncode', 'stdout', 'state']
        mismatches = [field for field in comparable if left[field] != right[field]]
        if exception:
            # Preserve full stderr in the artifact; compare stable terminal diagnostics.
            lerr = left['stderr'].splitlines()[-1:] if left['stderr'] else []
            rerr = right['stderr'].splitlines()[-1:] if right['stderr'] else []
            if lerr != rerr:
                mismatches.append('terminal exception')
            if left['returncode'] != 1 or not lerr or not lerr[0].startswith('sqlite3.'):
                mismatches.append('expected uncaught SQLite exception')
        elif left['stderr'] != right['stderr']:
            mismatches.append('stderr')
        self.steps.append({'args': args, 'reference': left, 'replacement': right, 'exception_comparison': exception, 'mismatches': mismatches})
        if mismatches:
            self.errors.append({'step': len(self.steps), 'args': args, 'fields': mismatches})


def parser_cases(s):
    cases = [[], ['--help'], ['-h'], ['--db', '<DB>'], ['list'], ['--db'],
             ['--db', '<DB>', 'bogus'], ['--db', '<DB>', 'list', 'a', 'b', 'c'],
             ['--db', '<DB>', 'list', '--unknown'], ['--d', '<DB>', 'list'],
             ['--db=<DB>', 'list'], ['list', '--db', '<DB>'],
             ['put', '--db', '<DB>', 'k', 'v'], ['--db', '<DB>', '--', 'put', '-key', '-value'],
             ['--db', '<DB>', 'put', 'k', '--'], ['--db', '<DB>', 'put', '-1', '-2'],
             ['--db', '<DB>', 'PUT'], ['--db', '<DB>', 'list', 'unused', 'ignored']]
    for index, args in enumerate(cases):
        s.pair(args, name='case-' + str(index))


def initialization(s):
    for index, args in enumerate([['list'], ['put'], ['put', 'key'], ['put', '', 'v'], ['remove'], ['remove', '']]):
        s.pair(['--db', '<DB>', *args], name='fresh-' + str(index))
    s.pair(['--db', '<DB>', 'invalid-action'], name='parser-failure')


def puts(s):
    cases = [['put'], ['put', 'a'], ['put', '', 'value'], ['put', 'a', ''], ['put', 'a', ''],
             ['put', 'a', 'changed'], ['list'], ['put', 'b', ' spaced '], ['put', '日本語', 'বাংলা 😀'],
             ['put', 'quote"\nkey', 'line1\nline2\t\\end'], ['put', "x'); DROP TABLE items; --", 'safe'],
             ['put', ' ', '\x01'], ['list']]
    for args in cases:
        s.pair(['--db', '<DB>', *args])
    s.pair(['--db', ':memory:', 'put', 'volatile', 'yes'], name='memory')
    s.pair(['--db', ':memory:', 'list'], name='memory')


def listing(s):
    for key in ['z', 'A', 'a', '10', '2', 'é', '日本', ' ', 'B']:
        s.pair(['--db', '<DB>', 'put', key, 'value-' + key])
    for operands in [[], ['ignored'], ['ignored', 'also ignored']]:
        s.pair(['--db', '<DB>', 'list', *operands])


def removes(s):
    cases = [['remove'], ['remove', ''], ['remove', 'missing'], ['put', 'a', 'value'], ['put', '日本', '値'],
             ['remove', 'a', 'unused value'], ['remove', 'a'], ['list'], ['remove', '日本'], ['list']]
    for args in cases:
        s.pair(['--db', '<DB>', *args])


def failures(s):
    for path in s.paths('corrupt'):
        path.write_bytes(b'this is not a sqlite database\x00\xff')
    s.pair(['--db', '<DB>', 'list'], name='corrupt', exception=True)
    # Parent directory is deliberately absent, under the isolated fixtures directory.
    s.pair(['--db', '<DB>/missing.sqlite', 'list'], name='missing-parent', exception=True)
    for path in s.paths('directory'):
        path.mkdir()
    s.pair(['--db', '<DB>', 'list'], name='directory', exception=True)
    for path in s.paths('schema'):
        with sqlite3.connect(path) as connection:
            connection.execute('create table items (other text)')
            connection.execute('insert into items values (?)', ('retained',))
    s.pair(['--db', '<DB>', 'list'], name='schema', exception=True)
    # This unusual but readable existing schema exposes SQLite value types unchanged.
    for path in s.paths('integer'):
        with sqlite3.connect(path) as connection:
            connection.execute('create table items (key text primary key, value integer)')
            connection.execute('insert into items values (?, ?)', ('number', 7))
    s.pair(['--db', '<DB>', 'list'], name='integer')
    s.pair(['--db', '<DB>', 'put', 'number', '7'], name='integer')


def interoperability(s):
    steps = [('replacement', ['put', 'shared', 'first']), ('reference', ['list']),
             ('reference', ['put', 'second', 'next']), ('replacement', ['list']),
             ('replacement', ['put', 'shared', 'other']), ('reference', ['list']),
             ('reference', ['remove', 'shared']), ('replacement', ['list']),
             ('replacement', ['remove', 'second']), ('reference', ['list'])]
    for program, args in steps:
        s.pair(['--db', '<DB>', *args], right_reference=program == 'reference')


state = json.loads(STATE.read_text())
target_version = 'sha256:' + digest(REFERENCE)
if state['project']['target_version'] != target_version:
    raise SystemExit('Reference digest changed: reinvestigate and update the contract before testing.')
revision = 'sha256:' + digest(CANDIDATE)
state['project']['replacement_revision'] = revision
for requirement in state['requirements']:
    requirement['status'] = 'IMPLEMENTED, UNVERIFIED'
state['checkpoint'] = {'summary': 'Replacement implemented; differential checks are running.', 'next_action': 'Complete checks, inspect actual results, and run the finite readiness gate.', 'blockers': []}
save_state(state)
checks = [('S-001', parser_cases), ('S-002', initialization), ('S-003', puts), ('S-004', listing),
          ('S-005', removes), ('S-006', failures), ('S-007', interoperability)]
results = {}
for sid, check in checks:
    fingerprint = subprocess.check_output([sys.executable, str(HELPER), 'fingerprint', str(STATE), sid], text=True).strip()
    executed_at = datetime.datetime.now(datetime.timezone.utc).isoformat()
    scenario = Scenario(sid)
    try:
        check(scenario)
    except Exception as error:
        scenario.errors.append({'harness_error': type(error).__name__ + ': ' + str(error)})
    result = 'FAIL' if scenario.errors else 'PASS'
    artifact = RECORDS / 'artifacts' / (STAMP + '-' + sid + '.json')
    artifact.write_text(json.dumps({'scenario': sid, 'target_version': target_version, 'replacement_revision': revision,
                                   'contract_sha256': fingerprint, 'executed_at': executed_at, 'harness_sha256': digest(Path(__file__)),
                                   'helper_sha256': digest(HELPER), 'fixture_root': str(scenario.directory),
                                   'result': result, 'steps': scenario.steps, 'errors': scenario.errors}, indent=2) + '\n')
    state['runs'].append({'id': 'T-' + STAMP + '-' + sid, 'scenario': sid, 'target_version': target_version,
                          'replacement_revision': revision, 'contract_sha256': fingerprint, 'executed_at': executed_at,
                          'command': 'python3 check_compatibility.py (scenario ' + sid + ')',
                          'environment': platform.platform() + '; Python ' + platform.python_version() + '; SQLite ' + sqlite3.sqlite_version + '; C.UTF-8; shared basename keyvalue.py; standard-library subprocess and file fixtures',
                          'result': result, 'comparison': 'equivalent', 'artifact': {'path': artifact.relative_to(RECORDS).as_posix(), 'sha256': digest(artifact)}})
    results[sid] = {'result': result, 'comparisons': len(scenario.steps), 'errors': scenario.errors}
    save_state(state)
    print(sid, result, str(len(scenario.steps)) + ' paired invocations', flush=True)
for requirement in state['requirements']:
    requirement['status'] = 'VERIFIED' if all(results[sid]['result'] == 'PASS' for sid in requirement['scenarios']) else 'PARTIALLY VERIFIED'
passed = sum(item['result'] == 'PASS' for item in results.values())
summary = {'scenarios_passed': passed, 'scenarios_total': len(checks), 'paired_invocations': sum(item['comparisons'] for item in results.values()), 'results': results}
(RECORDS / 'artifacts' / (STAMP + '-summary.json')).write_text(json.dumps(summary, indent=2) + '\n')
state['checkpoint'] = {'summary': str(passed) + '/7 differential scenarios pass; ' + str(summary['paired_invocations']) + ' paired CLI comparisons retained with raw outputs and state snapshots.', 'next_action': 'Run helper validate/report/gate and review evaluation-result.md; no required implementation work remains if all pass.', 'blockers': [] if passed == len(checks) else ['Resolve failing compatibility scenarios; inspect latest artifacts.']}
save_state(state)
print(json.dumps(summary, indent=2))
raise SystemExit(0 if passed == len(checks) else 1)
