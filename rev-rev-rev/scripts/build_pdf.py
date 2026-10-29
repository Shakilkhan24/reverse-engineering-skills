"""Build the complete Bengali book as a print PDF with embedded resources.

Requires: weasyprint, lxml, fonttools, pymupdf; see requirements-pdf.txt.
Source: existing book.html; it is not modified by this export.
"""
import base64
import hashlib
import html as escape_module
import io
import json
import logging
from pathlib import Path
from urllib.parse import urlsplit, unquote
from zipfile import ZipFile, ZIP_DEFLATED

from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from lxml import html
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration
import pymupdf

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "Reverse-Engineering-Bangla.pdf"
REPORTS = ROOT / "reports"
FONTS = ROOT / "assets" / "fonts"
CONFIG = json.loads((ROOT / "book.json").read_text(encoding="utf-8"))
FIGURES_BN = str(CONFIG["figure_count"]).translate(str.maketrans("0123456789", "০১২৩৪৫৬৭৮৯"))

STYLE = """
@font-face {font-family:BookBengali;src:url('assets/fonts/NotoSansBengali-Regular.ttf');font-weight:400}
@font-face {font-family:BookBengali;src:url('assets/fonts/NotoSansBengali-Bold.ttf');font-weight:700}
@page {size:A4;margin:20mm 17mm 20mm;
 @top-left {content:'দেখা থেকে জানা';font-family:BookBengali;font-size:8pt;color:#557079}
 @top-right {content:'REVERSE ENGINEERING';font-family:sans-serif;font-size:7pt;color:#557079;letter-spacing:1px}
 @bottom-left {content:'বাংলা দৃশ্যপাঠ  ·  প্রমাণ থেকে নির্মাণ';font-family:BookBengali;font-size:7.5pt;color:#557079}
 @bottom-right {content:counter(page);font-family:BookBengali;font-size:9pt;color:#127c7a}
}
@page cover {margin:0;@top-left{content:none}@top-right{content:none}@bottom-left{content:none}@bottom-right{content:none}}
* {box-sizing:border-box}
html {font-family:BookBengali,sans-serif;color:#203b45;font-size:10.2pt;line-height:1.6}
body {margin:0}
a {color:#116f70;text-decoration:none}
p {margin:0 0 2.8mm;orphans:3;widows:3}
strong,b {font-weight:700}
h1,h2,h3,h4 {font-weight:700;line-height:1.5;break-after:avoid;orphans:3;widows:3}
h1 {font-size:23pt;color:#116f70;margin:0 0 7mm}
h2 {font-size:14.5pt;color:#1a6067;margin:7mm 0 3mm}
h3 {font-size:12pt;margin:6mm 0 3mm}
h1 {bookmark-level:1}h2 {bookmark-level:2}h3 {bookmark-level:3}h4 {bookmark-level:none}
ul,ol {padding-left:6mm;margin:2mm 0 4mm}li {margin-bottom:1.5mm}
section.chapter {break-before:page}
section[id="15-architecture"],section[id="18-four-worlds"] {font-size:10pt;line-height:1.55}
section[id="18-four-worlds"] p {margin-bottom:2mm}
section[id="18-four-worlds"] th,section[id="18-four-worlds"] td {padding-top:2mm;padding-bottom:2mm}
section[id="C-prompts"] h2 {margin-top:5mm}
section[id="C-prompts"] pre {padding:2.5mm;margin:3mm 0}
section[id="C-prompts"] li {margin-bottom:1mm}
section[id="C-prompts"] ul {margin-bottom:1mm}
.chapter>.small {font-size:9pt;letter-spacing:.3px;color:#68828a;margin-bottom:4mm}
.chapter-nav {display:none}
.table-wrap {margin:4mm 0;overflow:visible}
table {width:100%;border-collapse:collapse;table-layout:fixed;font-size:8.7pt;line-height:1.55}
th,td {padding:2.5mm 2mm;border:0.25mm solid #d2dedf;vertical-align:top;overflow-wrap:anywhere}
th {background:#e6efec;font-weight:700;color:#174e55}
thead {display:table-header-group}tr {break-inside:avoid}table p {margin:0}
pre {font-size:8pt;line-height:1.5;padding:4mm;background:#edf2f1;border-left:1mm solid #1a827d;
 white-space:pre-wrap;overflow-wrap:anywhere;tab-size:2;break-inside:avoid;margin:4mm 0}
code {font-family:'DejaVu Sans Mono',BookBengali,monospace;font-size:.88em}
pre code {font-size:1em}td code {font-size:.85em}p code {background:#edf2f1;padding:0 .7mm}
blockquote {margin:4mm 0;padding:3mm 5mm;border-left:1mm solid #d29a34;background:#faf6eb}
img {display:block;width:100%;height:auto;max-height:185mm;object-fit:contain;margin:4mm 0;break-inside:avoid}
figure {margin:4mm 0;break-inside:avoid}
.answer {padding:3.5mm 4mm;border:.25mm solid #d4e1df;border-radius:2mm;margin:3mm 0;break-inside:avoid}
.answer .answer-title {font-weight:700;color:#116f70;margin-bottom:2mm}
.answer p:last-child {margin:0}
.print-widget {padding:5mm;border:0.5mm solid #16817c;background:#f2f8f5;break-inside:avoid;margin:6mm 0}
.small {font-size:9pt;color:#5e767f}
.cover {page:cover;height:297mm;padding:25mm 22mm;background:#112e3b;color:#f1f8f3;break-after:page;position:relative}
.cover .edition {font:9pt sans-serif;letter-spacing:2pt;color:#91cbbd;margin-bottom:28mm}
.cover h1 {font-size:47pt;line-height:1.4;color:#f1f8f3;margin:0 0 7mm;bookmark-level:none}
.cover h2 {font-size:22pt;color:#9bd9c9;margin:0 0 9mm;font-weight:400;bookmark-level:none}
.cover .rule {width:29mm;height:1.5mm;background:#d8a350;margin:10mm 0}
.cover .subtitle {font-size:13pt;line-height:1.9;max-width:151mm}
.cover .counts {font-size:12pt;border-top:.3mm solid #507378;border-bottom:.3mm solid #507378;padding:5mm 0;margin-top:14mm}
.cover .foot {position:absolute;bottom:24mm;left:22mm;right:22mm;font-size:10pt;color:#b6d4d0}
.front {break-before:page}
.toc ol {list-style:none;padding:0;margin:0}
.toc li {margin:0;border-bottom:.2mm solid #dce4e1;padding:1.5mm 0;font-size:9.5pt;line-height:1.4}
.toc a::after {content:leader('.') target-counter(attr(href),page);color:#425f67}
.toc h1 {bookmark-level:1}
.resources {break-before:page}
.source-link {color:#43616b}
"""


def prepare_fonts():
    variable = FONTS / "NotoSansBengali-variable.ttf"
    if not variable.exists():
        raise FileNotFoundError("Bundled font missing: assets/fonts/NotoSansBengali-variable.ttf")
    for name,weight in [("Regular",400),("Bold",700)]:
        destination = FONTS / f"NotoSansBengali-{name}.ttf"
        if not destination.exists():
            font=TTFont(variable)
            static=instantiateVariableFont(font,{"wght":weight,"wdth":100},inplace=False)
            static.save(destination)


def resources_zip():
    folders=["chapters","appendices","lab","examples","templates","data","scripts"]
    files=[ROOT/name for name in ["README.md","INSTRUCTION.md","TUTORIAL.md","book.html","book.json",
           "requirements.txt","requirements-lock.txt","requirements-pdf.txt","requirements-visuals.txt"]]
    for folder in folders:
        files.extend(p for p in (ROOT/folder).rglob("*") if p.is_file() and "__pycache__" not in p.parts)
    files += [p for p in (ROOT/"assets").rglob("*") if p.is_file()]
    files += [ROOT/"reports"/name for name in ["lab-results.json","verification.md","verification.json","test-output.txt","reader-check.json","reader-browser-check.json","visual-stories.json"]]
    buffer=io.BytesIO()
    with ZipFile(buffer,"w",ZIP_DEFLATED) as archive:
        for file in sorted(set(files)):
            if file.exists(): archive.write(file,file.relative_to(ROOT).as_posix())
    payload=buffer.getvalue()
    (ROOT/"RelayDesk-Book-Resources.zip").write_bytes(payload)
    return payload


def compose():
    doc=html.fromstring((ROOT/"book.html").read_text(encoding="utf-8"))
    sections=doc.xpath('//section[contains(@class,"chapter")]')
    assert len(sections)==28, "Expected all 24 chapters and four appendices"
    image_map={}
    for png in (ROOT/"assets/figures").glob("*.png"):
        image_map[hashlib.sha256(png.read_bytes()).hexdigest()]=png.with_suffix(".svg").as_uri()
    images=0
    for section in sections:
        for navigation in section.xpath('.//nav[contains(@class,"chapter-nav")]'):
            navigation.getparent().remove(navigation)
        for image in section.xpath('.//img'):
            original=base64.b64decode(image.get("src").split(",",1)[1])
            image.set("src",image_map[hashlib.sha256(original).hexdigest()])
            images+=1
        for answer in section.xpath('.//details'):
            answer.tag="div"; answer.set("class","answer");answer.attrib.pop("open",None)
            summary=answer.find("summary")
            if summary is not None:
                summary.tag="div";summary.set("class","answer-title")
        for widget in section.xpath('.//div[contains(@class,"lab-widget")]'):
            static=html.fromstring('''<div class="print-widget"><h3>Latency playground · স্থির পাঠ</h3>
<p>HTML-এর interactive উদাহরণের তিনটি অবস্থা এখানে পাশাপাশি দেখানো হলো। মোট ১০০ request; মাঝারি ৫টি ২০০ ms, ধীর request ১,৫০০ ms, বাকিগুলো ১০০ ms।</p>
<table><thead><tr><th>ধীর request</th><th>Mean</th><th>p95</th><th>p99</th></tr></thead><tbody>
<tr><td>০</td><td>১০৫ ms</td><td>১০০ ms</td><td>২০০ ms</td></tr>
<tr><td>৫</td><td>১৭৫ ms</td><td>২০০ ms</td><td>১,৫০০ ms</td></tr>
<tr><td>২০</td><td>৩৮৫ ms</td><td>১,৫০০ ms</td><td>১,৫০০ ms</td></tr>
</tbody></table><p class="small">Nearest-rank percentile; synthetic teaching data। Slider-টি ব্যবহার করতে book.html খুলুন।</p></div>''')
            widget.getparent().replace(widget,static)
        for anchor in section.xpath('.//a[@href]'):
            href=anchor.get("href")
            if not href.startswith("#") and not urlsplit(href).scheme:
                anchor.set("href","#resource-pack")
                anchor.set("title","Companion resource: "+unquote(href))
                anchor.set("class","source-link")
    assert images==CONFIG["figure_count"]
    entries=[(s,t) for s,t,*_ in CONFIG["chapters"]]+CONFIG["appendices"]
    toc="".join(f'<li><a href="#{slug}">{escape_module.escape(slug.split("-")[0])} · {escape_module.escape(title)}</a></li>' for slug,title in entries)
    content="".join(html.tostring(s,encoding="unicode") for s in sections)
    return f'''<!DOCTYPE html><html lang="bn"><head><meta charset="utf-8">
<title>{escape_module.escape(CONFIG['title'])}</title><meta name="author" content="বাংলা দৃশ্যপাঠ">
<meta name="description" content="সম্পূর্ণ ২৪ অধ্যায়, চার পরিশিষ্ট ও {FIGURES_BN}টি diagram-সহ বাংলা Reverse Engineering tutorial।"></head><body>
<section class="cover" id="top"><p class="edition">THE EVIDENCE-DRIVEN BUILDER</p>
<h1>দেখা থেকে জানা</h1><h2>Reverse Engineering-এর<br>বাংলা দৃশ্যপাঠ</h2><div class="rule"></div>
<p class="subtitle">সফটওয়্যারের দৃশ্যমান চেহারা থেকে অদৃশ্য আচরণ বোঝা—গল্প, উদাহরণ, পরীক্ষা ও AI agent-এর সঙ্গে কাজের একটি ব্যবহারিক বই।</p>
<p class="counts">২৪ অধ্যায় · {FIGURES_BN} visual · চার পরিশিষ্ট<br>Python lab · JSON ও SQL · অনুশীলন ও উত্তর</p>
<p class="foot">{escape_module.escape(CONFIG['edition'])}<br>সম্পূর্ণ PDF · অক্টোবর ২০২৬</p></section>
<section class="front"><h1>এই PDF কীভাবে পড়বে</h1>
<p>এই সংস্করণে সব ২৪টি অধ্যায়, চারটি পরিশিষ্ট, {FIGURES_BN}টি ছবি, chart ও diagram, code examples এবং workbook-এর সব উত্তর রয়েছে। নতুন ২২টি দৃশ্যে বাংলা লেবেল আছে। বাংলা font PDF-এর মধ্যে সংযুক্ত।</p>
<p>দৃশ্যটি দেখে পরের ফল অনুমান করো। তারপর ছবির নিচের ছোট উদাহরণটি পড়ো। API, SQL বা design-এর বিশদ অংশ চাইলে দ্বিতীয়বার পড়ার সময় খুলতে পারো।</p>
<p>পরের সূচিতে অধ্যায়ের নাম বা পৃষ্ঠা নম্বরে চাপলে সেই অধ্যায়ে যেতে পারবে। PDF reader-এর Bookmarks panel থেকেও অধ্যায় ও উপশিরোনাম খোলা যায়।</p>
<h2>তিনটি পড়ার পথ</h2><p><strong>শুরু থেকে:</strong> ১ → ৩ → ৫ → ৬ → ৭; তারপর ১৬-এর lab।<br>
<strong>AI দিয়ে project:</strong> ১ → ৩ → ১৬ → ১৭ → ১৯ → ২১।<br>
<strong>Backend ও reliability:</strong> ৮ → ৯ → ১০ → ১২ → ১৩ → ১৪ → ২০।</p>
<h2>ছবি, interactive উদাহরণ ও code</h2><p>চার্টগুলো vector আকারে রাখা হয়েছে। HTML-এর latency slider-এর বদলে PDF-তে কয়েকটি স্থির ফল দেওয়া আছে। Workbook-এর ভাঁজ করা উত্তরগুলো PDF-তে খোলা অবস্থায় আছে।</p>
<p>পূর্ণ lab source, JSON/CSV, templates, chapter source ও build scripts <a href="#resource-pack">সংযুক্ত resource pack</a>-এ আছে। PDF reader attachment না দেখালে PDF-এর পাশের <code>RelayDesk-Book-Resources.zip</code> ব্যবহার করো।</p>
<h2>প্রমাণের পরিচয়</h2><p>Conceptual diagram, synthetic data ও executed local lab result আলাদা। কাল্পনিক RelayDesk-এর উদাহরণ বাস্তব কোনো সেবার আবিষ্কৃত অভ্যন্তরীণ বিবরণ নয়।</p></section>
<section class="front toc"><h1>অধ্যায়সূচি</h1><ol>{toc}<li><a href="#resource-pack">সংযুক্ত ব্যবহারিক উপকরণ</a></li></ol></section>
{content}
<section class="resources" id="resource-pack"><h1>সংযুক্ত ব্যবহারিক উপকরণ</h1>
<p>এই PDF-তে <code>RelayDesk-Book-Resources.zip</code> নামে একটি attachment আছে। একই ZIP PDF-এর পাশেও আলাদাভাবে দেওয়া হয়েছে। Attachment সমর্থিত PDF reader-এর Attachments panel থেকে এটি সংরক্ষণ করা যায়।</p>
<table><thead><tr><th>ফোল্ডার / ফাইল</th><th>কী পাবে</th></tr></thead><tbody>
<tr><td>chapters/, appendices/</td><td>সব সম্পাদনাযোগ্য বাংলা অধ্যায় ও পরিশিষ্ট</td></tr>
<tr><td>lab/</td><td>Service implementation, demonstration ও ১৪টি contract test</td></tr>
<tr><td>examples/, data/</td><td>JSON records, synthetic CSV, calculated summary</td></tr>
<tr><td>templates/</td><td>নিজের project-এর জন্য control notebook</td></tr>
<tr><td>assets/</td><td>PNG/SVG charts ও বাংলা font-এর license</td></tr>
<tr><td>scripts/, requirements*</td><td>বই/ছবি/PDF আবার তৈরির উপকরণ</td></tr>
<tr><td>reports/</td><td>আগে চালানো lab verification ও ফল</td></tr>
</tbody></table><p>ZIP খুলে lab চালাতে:</p><pre><code>python3 lab/run_lab.py\npython3 -m unittest discover -s lab -p 'test_*.py' -v</code></pre>
<p>Chart ও HTML rebuild করতে README-এর নির্দেশনা দেখো। PDF build-এর জন্য <code>requirements-pdf.txt</code> install করে <code>python3 scripts/build_pdf.py</code> চালানো যায়। Linux-এ Pango/Harfbuzz-এর system libraries-ও প্রয়োজন।</p>
<p class="small">সংযুক্ত code কোনো network call বা বাস্তব email পাঠায় না। এটি শিক্ষামূলক service-level lab।</p></section>
</body></html>'''


def main():
    REPORTS.mkdir(exist_ok=True)
    logger=logging.getLogger("weasyprint")
    logger.setLevel(logging.WARNING)
    handler=logging.FileHandler(REPORTS/"pdf-build.log",mode="w",encoding="utf-8")
    logger.addHandler(handler)
    prepare_fonts()
    source=compose()
    (REPORTS/"pdf-print.html").write_text(source,encoding="utf-8")
    font_config=FontConfiguration()
    document=HTML(string=source,base_url=str(ROOT)).render(
        stylesheets=[CSS(string=STYLE,base_url=str(ROOT),font_config=font_config)],font_config=font_config)
    # Capture layout geometry before PDF serialization, including image coverage.
    layout={"page_count":len(document.pages),"chapter_pages":{},"figures":0,"horizontal_overflow":[]}
    for number,page in enumerate(document.pages,1):
        for anchor in page.anchors:
            if anchor in {s for s,*_ in CONFIG["chapters"]+CONFIG["appendices"]}:
                layout["chapter_pages"].setdefault(anchor,number)
        for box in page._page_box.descendants():
            if box.element_tag=="img": layout["figures"]+=1
            if box.__class__.__name__=="TextBox" and (box.position_x<-1 or box.position_x+box.width>page.width+1):
                layout["horizontal_overflow"].append({"page":number,"text":box.text[:100]})
    assert len(layout["chapter_pages"])==28
    assert layout["figures"]==CONFIG["figure_count"]
    data=document.write_pdf()
    resource_data=resources_zip()
    pdf=pymupdf.open(stream=data,filetype="pdf")
    pdf.embfile_add("RelayDesk-Book-Resources.zip",resource_data,filename="RelayDesk-Book-Resources.zip",
                    desc="Complete editable chapters, labs, JSON/CSV, templates, charts and build scripts.")
    pdf.set_metadata({**pdf.metadata,"title":CONFIG["title"],"subject":"সম্পূর্ণ বাংলা tutorial; ২৪ অধ্যায় ও চার পরিশিষ্ট"})
    pdf.save(OUTPUT,garbage=4,deflate=True)
    layout["pdf_bytes"]=OUTPUT.stat().st_size
    layout["attachment_bytes"]=len(resource_data)
    layout["pdf_sha256"]=hashlib.sha256(OUTPUT.read_bytes()).hexdigest()
    (REPORTS/"pdf-layout.json").write_text(json.dumps(layout,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(layout,ensure_ascii=False,indent=2))


if __name__=="__main__":
    main()
