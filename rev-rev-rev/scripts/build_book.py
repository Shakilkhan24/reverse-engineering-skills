"""Compile editable Markdown into one Markdown book and a portable HTML reader."""
import base64
import html
import json
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit
import markdown

ROOT = Path(__file__).resolve().parents[1]
CONFIG = json.loads((ROOT / "book.json").read_text(encoding="utf-8"))
FIGURES_BN = str(CONFIG["figure_count"]).translate(str.maketrans("0123456789", "০১২৩৪৫৬৭৮৯"))
ENTRIES = [(ROOT / "chapters" / (slug + ".md"), slug, title, group)
           for slug, title, group in CONFIG["chapters"]]
ENTRIES += [(ROOT / "appendices" / (slug + ".md"), slug, title, "পরিশিষ্ট")
            for slug, title in CONFIG["appendices"]]
ANCHORS = {path.resolve(): slug for path, slug, *_ in ENTRIES}
ANCHORS[ROOT / "README.md"] = "top"

CSS = """
:root {--paper:#faf8f2;--surface:#fffdf8;--ink:#233c46;--muted:#627077;--accent:#127b78;--line:#dce3df;--code:#102d39;--body-size:18px}
*{box-sizing:border-box}html{scroll-behavior:smooth;scroll-padding-top:90px}
body{margin:0;background:var(--paper);color:var(--ink);font:var(--body-size)/1.95 'ReaderBengali','Nirmala UI','Noto Sans Bengali','Vrinda',system-ui,sans-serif}
body.dark{--paper:#10212c;--surface:#172e39;--ink:#e4eceb;--muted:#b2c2c6;--accent:#77d6c5;--line:#38505c;--code:#0b1923}
a{color:var(--accent);text-underline-offset:4px}a:hover{text-decoration-thickness:2px}button,input{font:inherit}button{cursor:pointer}
.skip{position:fixed;left:12px;top:-70px;background:var(--surface);padding:8px;z-index:10}.skip:focus{top:10px}
:focus-visible{outline:3px solid #d18c25;outline-offset:4px}
aside{position:fixed;inset:0 auto 0 0;width:285px;overflow:auto;background:var(--surface);border-right:1px solid var(--line);padding:24px 20px;font-size:14px}
aside .brand{font-size:26px;font-weight:800;text-decoration:none;display:block}aside p{color:var(--muted);line-height:1.6}
aside input{width:100%;padding:9px;border:1px solid var(--line);border-radius:8px;background:var(--paper);color:var(--ink)}
aside ol{list-style:none;padding:0}aside li{margin:6px 0;line-height:1.6}aside a{display:block;text-decoration:none;padding:6px;border-radius:6px}aside a:hover{background:var(--paper)}
.toolbar{position:sticky;top:0;z-index:5;margin-left:285px;display:flex;align-items:center;justify-content:space-between;gap:8px;padding:10px 28px;background:var(--surface);border-bottom:1px solid var(--line);font-size:14px}
.tools{display:flex;gap:8px;flex-wrap:wrap}.tools button{color:var(--ink);background:var(--paper);border:1px solid var(--line);border-radius:8px;padding:5px 12px}
main{margin-left:285px;max-width:1290px;padding:38px clamp(20px,5vw,78px) 80px}
.hero{background:var(--code);color:#eaf4ed;border-radius:24px;padding:45px;margin:10px 0 44px;position:relative;overflow:hidden}
.hero .eyebrow{letter-spacing:3px;font:12px/2 system-ui;color:#8fd4c4}.hero h1{font-size:clamp(38px,5vw,72px);line-height:1.35;margin:10px 0}.hero h2{font-size:22px;color:#a7dfd2;font-weight:500}
.hero p{max-width:710px}.hero a{color:#9ae4d0}.chips{display:flex;gap:10px;flex-wrap:wrap;font-size:14px}.chips span{border:1px solid #5b7980;border-radius:30px;padding:4px 15px}
section.chapter{padding:28px 0 42px;border-bottom:2px solid var(--line);scroll-margin-top:75px}
.chapter>h1{font-size:clamp(29px,3vw,40px);line-height:1.55;margin:12px 0 22px;color:var(--accent)}h2{font-size:1.4em;margin-top:1.8em;line-height:1.6}h3{font-size:1.12em;margin-top:1.7em}p{margin:1em 0}
img{display:block;width:100%;height:auto;margin:25px auto;border:1px solid var(--line);border-radius:12px;background:#f6f4ef}
.figure-open{display:block;width:100%;padding:0;border:0;background:none;cursor:zoom-in;color:inherit}.figure-open img{margin:18px 0}.figure-open:hover img{border-color:var(--accent)}
dialog{width:min(1500px,96vw);max-width:96vw;height:94vh;max-height:94vh;padding:15px;border:1px solid var(--line);border-radius:14px;background:var(--surface);color:var(--ink)}dialog[open]{display:flex;flex-direction:column}dialog::backdrop{background:#10212ce0}
.viewer-tools{display:flex;align-items:center;gap:10px;flex-wrap:wrap}.viewer-tools p{flex:1;margin:0;font-size:15px}.viewer-tools button{padding:5px 12px;border:1px solid var(--line);border-radius:6px;background:var(--paper);color:var(--ink)}
.viewer-scroll{flex:1;min-height:0;overflow:auto;margin-top:12px;background:var(--paper)}.viewer-scroll img{width:100%;max-width:none;margin:0;border:0;border-radius:0}
@media print{dialog{display:none!important}}
pre{background:var(--code);color:#e2f0e9;border-radius:12px;padding:21px;overflow:auto;line-height:1.65;font-size:.83em;tab-size:4}
code{font-family:ui-monospace,Consolas,'ReaderBengali','Nirmala UI',monospace}p code,li code,td code{background:var(--line);padding:2px 5px;border-radius:4px;overflow-wrap:anywhere}
.table-wrap{overflow-x:auto;margin:23px 0;border:1px solid var(--line);border-radius:10px}table{border-collapse:collapse;width:100%;font-size:.91em;line-height:1.75}th,td{border-bottom:1px solid var(--line);padding:12px 15px;text-align:left;min-width:110px;vertical-align:top}th{background:var(--line)}tr:last-child td{border-bottom:0}
blockquote{border-left:4px solid var(--accent);margin:25px 0;padding:10px 22px;background:var(--surface)}
details{border:1px solid var(--line);background:var(--surface);border-radius:10px;padding:14px 20px;margin:12px 0}summary{cursor:pointer;font-weight:700;color:var(--accent)}
.chapter-nav{display:flex;justify-content:space-between;gap:20px;margin-top:30px;font-size:14px}.chapter-nav a{max-width:45%}
.lab-widget{padding:25px;border:2px solid var(--accent);border-radius:16px;margin:32px 0;background:var(--surface)}.lab-widget h3{margin-top:0}.lab-widget input{width:100%;accent-color:var(--accent)}
.metrics{display:grid;grid-template-columns:repeat(4,1fr);gap:10px}.metrics div{background:var(--paper);padding:12px;text-align:center;border-radius:8px}.metrics strong{display:block;font-size:23px;color:var(--accent)}
.distribution{display:flex;height:25px;border-radius:6px;overflow:hidden;margin:20px 0}.distribution span:nth-child(1){background:#137e7e}.distribution span:nth-child(2){background:#d08b19}.distribution span:nth-child(3){background:#b64848}
.small{font-size:.85em;color:var(--muted)}footer{margin-top:40px;color:var(--muted)}
@media(max-width:1050px){aside{width:235px}.toolbar,main{margin-left:235px}.toolbar>span{display:none}main{padding:25px}.hero{padding:30px}}
@media(max-width:760px){aside{position:static;width:auto;max-height:340px;border-right:0;border-bottom:1px solid var(--line)}.toolbar,main{margin-left:0}.toolbar{padding:10px 16px}main{padding:16px}.hero{padding:24px;border-radius:14px}.metrics{grid-template-columns:repeat(2,1fr)}body{--body-size:17px}.chapter>h1{font-size:29px}}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
@media print{aside,.toolbar,.chapter-nav,.skip,.lab-widget{display:none!important}main{margin:0;padding:0;max-width:none}body,body.dark{--paper:white;--surface:white;--ink:#111;--accent:#174b48;--line:#ddd;font-size:11pt;line-height:1.7}.hero{background:white;color:#111;padding:0}.hero h2{color:#333}.hero .eyebrow{color:#333}section.chapter{break-before:page;border:0}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#f1f3f2;color:#111}img,table,tr,details{break-inside:avoid}a{color:inherit}h1,h2,h3{break-after:avoid}.table-wrap{overflow:visible}}
"""

WIDGET = """
<div class="lab-widget" id="latency-playground">
<h3>নিজে সংখ্যা বদলে দেখো · latency playground</h3>
<p>মোট ১০০ request। মাঝারি ৫টি সবসময় ২০০ ms; ধীর request ১,৫০০ ms; বাকিগুলো ১০০ ms। নিচের slider বদলে mean ও nearest-rank percentile দেখো।</p>
<label for="slow-count">ধীর request সংখ্যা: <output id="slow-label">৫</output></label>
<input id="slow-count" type="range" min="0" max="20" value="5" step="1">
<div class="distribution" aria-hidden="true"><span id="fast-bar" style="width:90%"></span><span style="width:5%"></span><span id="slow-bar" style="width:5%"></span></div>
<div class="metrics" aria-live="polite"><div>Mean<strong id="mean">১৭৫ ms</strong></div><div>p50<strong id="p50">১০০ ms</strong></div><div>p95<strong id="p95">২০০ ms</strong></div><div>p99<strong id="p99">১৫০০ ms</strong></div></div>
<p class="small">সবুজ = ১০০ ms; হলুদ = ২০০ ms; লাল = ১,৫০০ ms। এটি synthetic calculator, benchmark নয়। JavaScript বন্ধ থাকলে default ৫টি slow request-এর ফল দেখা যাবে।</p>
</div>
"""

JS = """
const body = document.body;
document.querySelector('#theme').addEventListener('click', (event) => {
  const dark = body.classList.toggle('dark');
  event.currentTarget.setAttribute('aria-pressed', String(dark));
});
let size = 18;
document.querySelector('#bigger').addEventListener('click', () => {size = Math.min(25,size+1);body.style.setProperty('--body-size',size+'px');});
document.querySelector('#smaller').addEventListener('click', () => {size = Math.max(15,size-1);body.style.setProperty('--body-size',size+'px');});
document.querySelector('#print').addEventListener('click', () => window.print());
document.querySelector('#chapter-filter').addEventListener('input', event => {
 const term = event.target.value.toLocaleLowerCase();
 document.querySelectorAll('aside li').forEach(li => {li.hidden = !li.textContent.toLocaleLowerCase().includes(term);});
});
const nf = new Intl.NumberFormat('bn-BD',{maximumFractionDigits:1});
function updateLatency(){
 const slow = Number(document.querySelector('#slow-count').value), fast = 95-slow;
 const values = [...Array(fast).fill(100),...Array(5).fill(200),...Array(slow).fill(1500)];
 const mean = values.reduce((a,b)=>a+b,0)/100;
 document.querySelector('#slow-label').textContent = nf.format(slow);
 document.querySelector('#fast-bar').style.width=fast+'%';
 document.querySelector('#slow-bar').style.width=slow+'%';
 for(const [id,value] of Object.entries({mean,p50:values[49],p95:values[94],p99:values[98]})){
  document.getElementById(id).textContent=nf.format(value)+' ms';
 }
}
document.querySelector('#slow-count').addEventListener('input',updateLatency);
updateLatency();
const viewer = document.querySelector('#figure-viewer');
const enlarged = document.querySelector('#enlarged-figure');
let zoom = 100;
function setZoom(value){zoom=Math.max(100,Math.min(250,value));enlarged.style.width=zoom+'%';}
document.querySelectorAll('.chapter img').forEach(img=>{
 const button=document.createElement('button');
 button.type='button';button.className='figure-open';
 button.setAttribute('aria-label','ছবি বড় করে দেখুন: '+img.alt);
 img.parentNode.insertBefore(button,img);button.appendChild(img);
 button.addEventListener('click',()=>{enlarged.src=img.src;enlarged.alt=img.alt;setZoom(100);viewer.showModal();document.querySelector('.viewer-scroll').scrollTo(0,0);});
});
document.querySelector('#zoom-in').addEventListener('click',()=>setZoom(zoom+25));
document.querySelector('#zoom-out').addEventListener('click',()=>setZoom(zoom-25));
document.querySelector('#zoom-fit').addEventListener('click',()=>setZoom(100));
document.querySelector('#viewer-close').addEventListener('click',()=>viewer.close());
viewer.addEventListener('click',event=>{if(event.target===viewer)viewer.close();});
window.addEventListener('beforeprint',()=>{document.querySelectorAll('details').forEach(d=>{d.dataset.wasOpen=String(d.open);d.open=true;});});
window.addEventListener('afterprint',()=>{document.querySelectorAll('details').forEach(d=>{d.open=d.dataset.wasOpen==='true';});});
"""


def destination(url, source, embed=False):
    parsed = urlsplit(html.unescape(url))
    if parsed.scheme or url.startswith("#"):
        return url
    target = (source.parent / unquote(parsed.path)).resolve()
    if embed and target.suffix.lower() in {".png", ".svg", ".jpg"}:
        mime = {".png":"image/png", ".svg":"image/svg+xml", ".jpg":"image/jpeg"}[target.suffix.lower()]
        return "data:"+mime+";base64,"+base64.b64encode(target.read_bytes()).decode()
    if target in ANCHORS:
        return "#"+ANCHORS[target]
    relative = target.relative_to(ROOT).as_posix()
    return relative + ("#"+parsed.fragment if parsed.fragment else "")


def without_navigation(text):
    return text.split("<!-- book-navigation -->")[0].rstrip()+"\n"


def main():
    font_css=""
    for weight,name in [(400,"Regular"),(700,"Bold")]:
        encoded=base64.b64encode((ROOT/"assets/fonts"/f"NotoSansBengali-{name}.ttf").read_bytes()).decode()
        font_css+=f"@font-face{{font-family:ReaderBengali;font-weight:{weight};font-display:swap;src:url(data:font/ttf;base64,{encoded})}}"
    md_parts=[f'<a id="top"></a>\n\n# {CONFIG["title"]}\n\n'
              f'তোমার INSTRUCTION.md অবলম্বনে ২৪ অধ্যায়, চার পরিশিষ্ট ও {FIGURES_BN}টি visual। '
              '[মূল সূচি](README.md) · [অফলাইন interactive বই](book.html)\n\n## অধ্যায়সূচি\n']
    toc=[]; sections=[]
    for path,slug,title,group in ENTRIES:
        md_parts.append(f"- [{title}](#{slug})\n")
        toc.append(f'<li><a href="#{slug}">{html.escape(slug.split("-")[0])} · {html.escape(title)}</a></li>')
    for i,(path,slug,title,group) in enumerate(ENTRIES):
        raw=without_navigation(path.read_text(encoding="utf-8"))
        rebased=re.sub(r'(!?\[[^\]]*\]\()([^\s)]+)(\))',
                       lambda m:m[1]+destination(m[2],path)+m[3],raw)
        md_parts.append(f'\n\n---\n\n<a id="{slug}"></a>\n\n'+rebased)
        rendered=markdown.markdown(raw,extensions=["extra","sane_lists","md_in_html"])
        rendered=re.sub(r'(href|src)="([^"]+)"',
                        lambda m:m[1]+'="'+html.escape(destination(m[2],path,embed=m[1]=="src"),quote=True)+'"',rendered)
        rendered=re.sub(r'<table>(.*?)</table>',r'<div class="table-wrap"><table>\1</table></div>',rendered,flags=re.S)
        navigation=[]
        if i: navigation.append(f'<a href="#{ENTRIES[i-1][1]}">← {html.escape(ENTRIES[i-1][2])}</a>')
        if i+1<len(ENTRIES): navigation.append(f'<a href="#{ENTRIES[i+1][1]}">{html.escape(ENTRIES[i+1][2])} →</a>')
        widget=WIDGET if slug=="14-performance" else ""
        sections.append(f'<section class="chapter" id="{slug}"><p class="small">{html.escape(group)}</p>{rendered}{widget}<nav class="chapter-nav" aria-label="অধ্যায় পরিবর্তন">'+"".join(navigation)+"</nav></section>")
    (ROOT / "TUTORIAL.md").write_text("".join(md_parts),encoding="utf-8")
    page=f'''<!doctype html>
<html lang="bn"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="Reverse engineering ও AI agent collaboration-এর বাংলা visual tutorial।">
<title>{html.escape(CONFIG['title'])}</title><style>{font_css}{CSS}</style></head>
<body><a class="skip" href="#content">মূল লেখায় যান</a>
<aside aria-label="বইয়ের সূচি"><a class="brand" href="#top">দেখা থেকে জানা</a><p>একটি বাংলা দৃশ্যপাঠ<br>২৪ অধ্যায় · {FIGURES_BN} visual · হাতে-কলমে lab</p>
<label for="chapter-filter">অধ্যায় খুঁজুন</label><input id="chapter-filter" type="search" placeholder="যেমন: প্রমাণ, API, সময়">
<ol>{''.join(toc)}</ol><p>পুরো লেখায় খুঁজতে Ctrl+F / Cmd+F ব্যবহার করুন।</p><a href="README.md">Repository README</a></aside>
<div class="toolbar"><span>পড়ো · পরীক্ষা করো · নিজের ভাষায় বলো</span><div class="tools">
<button id="smaller" aria-label="অক্ষর ছোট করুন">অ−</button><button id="bigger" aria-label="অক্ষর বড় করুন">অ+</button>
<button id="theme" aria-pressed="false">রঙের মোড</button><button id="print">প্রিন্ট / PDF</button></div></div>
<main id="content"><header class="hero" id="top"><div class="eyebrow">THE EVIDENCE-DRIVEN BUILDER</div>
<h1>দেখা থেকে জানা</h1><h2>Reverse Engineering-এর বাংলা দৃশ্যপাঠ</h2>
<p>আরিফ ticket তৈরি করল। Refresh দিতেই ticket উধাও। এই ছোট ঘটনা দিয়ে শুরু—তারপর form-এর বদলানো অবস্থা, retry-এর রসিদ, পাশাপাশি চলা request আর নিজের হাতে চালানোর lab।</p>
<div class="chips"><span>২৪ অধ্যায়</span><span>{FIGURES_BN} visual</span><span>১৪ contract test</span><span>চার পরিশিষ্ট</span></div>
<p>{html.escape(CONFIG['edition'])}। ছবিতে চাপলে বড় করে দেখা যাবে। আগে দৃশ্যটি দেখো, পরের ফল অনুমান করো, তারপর নিচের ব্যাখ্যা পড়ো।</p>
<p><a href="#01-surface-system">শুরু থেকে পড়ুন →</a> · <a href="#16-vertical-lab">সরাসরি lab →</a></p>
<p class="small" style="color:#b7d2d2">ছবি ও বাংলা font এই file-এ embedded; পড়তে internet দরকার নেই। Code/CSV link খুলতে repository সঙ্গে রাখুন। ছবির উৎস conceptual, synthetic বা executed lab result হিসেবে চিহ্নিত।</p></header>
{''.join(sections)}<footer>প্রধান উৎস: INSTRUCTION.md। এই বই একটি learning artifact; real target-এর universal equivalence বা production readiness-এর দাবি নয়।</footer></main>
<dialog id="figure-viewer" aria-labelledby="viewer-title"><div class="viewer-tools"><p id="viewer-title">ছবি বড় করে দেখুন · বড় হলে scroll করুন</p><button id="zoom-out" aria-label="ছবি ছোট করুন">−</button><button id="zoom-in" aria-label="ছবি বড় করুন">+</button><button id="zoom-fit">মানানসই</button><button id="viewer-close" autofocus>বন্ধ করুন · Esc</button></div><div class="viewer-scroll"><img id="enlarged-figure" alt=""></div></dialog>
<script>{JS}</script></body></html>'''
    (ROOT / "book.html").write_text(page,encoding="utf-8")
    print(f"Built {len(ENTRIES)} sections into TUTORIAL.md and standalone book.html.")


if __name__ == "__main__":
    main()
