"""Check document integrity and execute the teaching lab; preserve real results."""
import hashlib
import io
import json
import math
import re
import sqlite3
import subprocess
import sys
import unittest
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT=Path(__file__).resolve().parents[1]
REPORTS=ROOT/"reports"
REPORTS.mkdir(exist_ok=True)


class DocumentParser(HTMLParser):
    def __init__(self):
        super().__init__(); self.ids=[]; self.refs=[]; self.images=[]
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        if "id" in attrs: self.ids.append(attrs["id"])
        if "href" in attrs: self.refs.append(attrs["href"])
        if tag=="img" and attrs.get("id")!="enlarged-figure": self.images.append(attrs)


class RecordingResult(unittest.TextTestResult):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs); self.cases=[]
    def addSuccess(self,test):
        super().addSuccess(test); self.cases.append({"id":test.id(),"result":"PASS"})
    def addFailure(self,test,err):
        super().addFailure(test,err); self.cases.append({"id":test.id(),"result":"FAIL"})
    def addError(self,test,err):
        super().addError(test,err); self.cases.append({"id":test.id(),"result":"ERROR"})


def main():
    problems=[]; links=0; json_blocks=0
    # Materialize the linked demo artifact before auditing document links.
    demo=subprocess.run([sys.executable,str(ROOT/"lab/run_lab.py"),"--output",str(REPORTS/"lab-results.json")],
                        cwd=ROOT,text=True,capture_output=True,check=True)
    actual=json.loads(demo.stdout)
    config=json.loads((ROOT/"book.json").read_text(encoding="utf-8"))
    assert len(config["chapters"])==24 and len(config["appendices"])==4
    # Exclude the untouched input; only new authoring and generated documents are audited.
    markdown_files=[ROOT/"README.md",ROOT/"TUTORIAL.md"]
    markdown_files+=list((ROOT/"chapters").glob("*.md"))+list((ROOT/"appendices").glob("*.md"))
    markdown_files+=list((ROOT/"templates").glob("*.md"))+[ROOT/"data/README.md"]
    for path in markdown_files:
        source=path.read_text(encoding="utf-8")
        if len(re.findall(r"^```",source,re.M))%2:
            problems.append(f"Unbalanced code fence: {path.relative_to(ROOT)}")
        for match in re.finditer(r"```json\s*\n(.*?)\n```",source,re.S):
            try: json.loads(match[1]); json_blocks+=1
            except json.JSONDecodeError as error: problems.append(f"Invalid JSON in {path.name}: {error}")
        prose=re.sub(r"```.*?```","",source,flags=re.S)
        for target in re.findall(r"!?\[[^\]]*\]\(([^\s)]+)\)",prose):
            parts=urlsplit(target)
            if parts.scheme or target.startswith("#"): continue
            resolved=(path.parent/unquote(parts.path)).resolve()
            links+=1
            # Verification report is written by this run after the checks.
            if not resolved.exists() and resolved!=REPORTS/"verification.md":
                problems.append(f"Missing link in {path.name}: {target}")
    for path in list((ROOT/"examples").glob("*.json"))+list((ROOT/"data").glob("*.json")):
        json.loads(path.read_text(encoding="utf-8"))
    manifest=json.loads((ROOT/"assets/figures/manifest.json").read_text())
    from PIL import Image
    assert len(manifest)==config["figure_count"]
    chapter_visuals={slug:len(re.findall(r'!\[[^\]]*\]\(', (ROOT/"chapters"/(slug+".md")).read_text()))
                     for slug,*_ in config["chapters"]}
    assert all(chapter_visuals.values()), "Every chapter needs at least one teaching visual"
    for figure in manifest:
        path=ROOT/"assets/figures"/(figure["file"]+".png")
        with Image.open(path) as img:
            img.verify()
        if not (path.with_suffix(".svg")).exists(): problems.append(f"Missing SVG: {path.stem}")
    import csv
    with (ROOT/"data/latency.csv").open() as stream:
        latencies=sorted(int(row["latency_ms"]) for row in csv.DictReader(stream))
    summary=json.loads((ROOT/"data/summary.json").read_text())
    assert sum(latencies)/len(latencies)==summary["latency"]["mean_ms"]==175
    for p in [50,95,99]:
        assert latencies[math.ceil(len(latencies)*p/100)-1]==summary["latency"][f"p{p}_ms"]
    parser=DocumentParser(); parser.feed((ROOT/"book.html").read_text(encoding="utf-8"))
    if len(parser.ids)!=len(set(parser.ids)): problems.append("Duplicate HTML IDs")
    for ref in parser.refs:
        if ref.startswith("#") and ref[1:] not in parser.ids: problems.append(f"Broken HTML anchor: {ref}")
    if len(parser.images)!=config["figure_count"]: problems.append(f"Expected {config['figure_count']} embedded images, got {len(parser.images)}")
    if not all(i.get("src","").startswith("data:image/") and i.get("alt") for i in parser.images):
        problems.append("HTML images must be embedded and have alt text")
    assert actual["duplicate_submission"]=={"same_id":True,"ticket_count":1}
    assert actual["reopen"]["persisted"] is True
    assert actual["cross_workspace"]["error"]=="forbidden"
    assert actual["changed_payload"]["error"]=="key_payload_mismatch"
    assert actual["stale_update"]=={"error":"version_conflict","version":2}
    assert actual["ack_gap"]=={"provider_effects":1,"pending_events":1}
    assert actual["worker_retry"]=={"provider_effects":1,"pending_events":0}
    sys.path.insert(0,str(ROOT/"lab"))
    suite=unittest.defaultTestLoader.discover(str(ROOT/"lab"),pattern="test_*.py")
    stream=io.StringIO()
    result=unittest.TextTestRunner(stream=stream,verbosity=2,resultclass=RecordingResult).run(suite)
    (REPORTS/"test-output.txt").write_text(stream.getvalue(),encoding="utf-8")
    if not result.wasSuccessful(): problems.append("Lab test suite failed; see test-output.txt")
    browser_path=REPORTS/"reader-browser-check.json"
    browser=json.loads(browser_path.read_text()) if browser_path.exists() else None
    browser_current=bool(browser and browser.get("book_sha256")==hashlib.sha256((ROOT/"book.html").read_bytes()).hexdigest() and not browser.get("errors"))
    html_scope="structural plus Chromium desktop/mobile interaction checks" if browser_current else "structural only; no current browser check"
    html_note="HTML-এর structural integrity এবং বর্তমান build-এর Chromium desktop/mobile image, font, zoom ও navigation interaction যাচাই হয়েছে।" if browser_current else "HTML-এর structural integrity যাচাই হয়েছে; এই build-এর browser check report নেই।"
    report={"executed_at_utc":datetime.now(timezone.utc).isoformat(),"python":sys.version,
            "sqlite":sqlite3.sqlite_version,"command":"python scripts/verify_book.py",
            "source_sha256":hashlib.sha256((ROOT/"INSTRUCTION.md").read_bytes()).hexdigest(),
            "chapters":24,"appendices":4,"figures":len(manifest),"chapter_visuals":chapter_visuals,"checked_local_links":links,
            "parsed_json_code_blocks":json_blocks,"lab_tests":result.testsRun,
            "test_results":result.cases,"problems":problems,
            "html_validation":html_scope,
            "limitations":["No real target comparison","No load benchmark","Fake external provider","Injected exceptions are not power-loss tests"]}
    (REPORTS/"verification.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    rows="\n".join(f"| `{case['id'].split('.')[-1]}` | {case['result']} |" for case in result.cases)
    content=f'''# চালানো যাচাইয়ের ফল

এই report `scripts/verify_book.py` চালিয়ে তৈরি। এটি local teaching artifact-এর ফল; বাস্তব reference product-এর fidelity report নয়।

- UTC execution: `{report['executed_at_utc']}`
- Interpreter: Python `{sys.version.split()[0]}`; SQLite `{sqlite3.sqlite_version}`
- Document: ২৪ অধ্যায়, চার পরিশিষ্ট, {len(manifest)} PNG + {len(manifest)} SVG; প্রতিটি অধ্যায়ে অন্তত একটি visual।
- Local link checked: {links}; parsed JSON code block: {json_blocks} (combined book-এ পুনরাবৃত্তিসহ)।
- HTML: {len(parser.images)} embedded image, alt text ও internal anchor পরীক্ষা।
- Latency dataset: mean ও nearest-rank p50/p95/p99 recomputed।
- Demo: duplicate, reopen, forbidden, payload conflict, stale update ও ack-gap result assertions checked।
- Lab: {result.testsRun} tests; {len(result.failures)} failures; {len(result.errors)} errors।
- Document problems: {len(problems)}।

| Test | Actual result |
|---|---|
{rows}

## Artifacts

- [Machine-readable verification](verification.json)
- [Actual unittest output](test-output.txt)
- [Actual demo output](lab-results.json)

## যাচাইয়ের সীমা

{html_note} Chart-গুলো আলাদাভাবে visual inspection করা হয়েছে। Lab-এ বাস্তব HTTP/UI/authentication, provider integration, power-loss recovery বা production throughput পরীক্ষা নেই। Crash window-তে exception injection ব্যবহার করা হয়েছে।

Original input SHA-256: `{report['source_sha256']}`
'''
    if problems: content+="\n## Problems\n\n"+"\n".join("- "+p for p in problems)+"\n"
    (REPORTS/"verification.md").write_text(content,encoding="utf-8")
    print(json.dumps({"tests":result.testsRun,"document_problems":problems,"local_links":links,"json_blocks":json_blocks},ensure_ascii=False))
    return 1 if problems else 0


if __name__=="__main__":
    raise SystemExit(main())
