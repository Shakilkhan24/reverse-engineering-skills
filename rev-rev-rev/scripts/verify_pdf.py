"""Validate exported PDF completeness, fonts, navigation and resource attachment."""
import hashlib
import io
import json
from pathlib import Path
from zipfile import ZipFile
import pymupdf

ROOT=Path(__file__).resolve().parents[1]


def main():
    path=ROOT/"Reverse-Engineering-Bangla.pdf"
    pdf=pymupdf.open(path)
    layout=json.loads((ROOT/"reports/pdf-layout.json").read_text(encoding="utf-8"))
    config=json.loads((ROOT/"book.json").read_text(encoding="utf-8"))
    assert len(pdf)==layout["page_count"]
    assert len(layout["chapter_pages"])==28
    assert layout["figures"]==config["figure_count"]
    assert not layout["horizontal_overflow"]
    assert layout["pdf_sha256"]==hashlib.sha256(path.read_bytes()).hexdigest()
    resources=(ROOT/"RelayDesk-Book-Resources.zip").read_bytes()
    assert pdf.embfile_names()==["RelayDesk-Book-Resources.zip"]
    assert pdf.embfile_get(0)==resources
    with ZipFile(io.BytesIO(resources)) as archive:
        assert archive.testzip() is None
        names=archive.namelist()
        for required in ["book.html","INSTRUCTION.md","lab/relaydesk.py","lab/test_relaydesk.py",
                         "examples/api-contract.json","assets/fonts/OFL.txt","scripts/build_pdf.py"]:
            assert required in names,required
    toc=pdf.get_toc()
    top_bookmarks=[row for row in toc if row[0]==1]
    bookmark_pages={row[2] for row in top_bookmarks}
    assert all(page in bookmark_pages for page in layout["chapter_pages"].values())
    destinations=pdf.resolve_names()
    for slug,page_number in layout["chapter_pages"].items():
        assert destinations[slug]["page"]==page_number-1
    fonts={};links=0;empty=[];bounds=[];replacement=0;combined=[]
    for index,page in enumerate(pdf):
        text=page.get_text()
        combined.append(text)
        replacement+=text.count("\ufffd")
        if len(text.strip())<20: empty.append(index+1)
        for link in page.get_links():
            if link["kind"] in {pymupdf.LINK_GOTO,pymupdf.LINK_NAMED}:
                assert 0<=link["page"]<len(pdf)
                if "nameddest" in link: assert link["nameddest"] in destinations
                links+=1
        for font in page.get_fonts():
            fonts[font[0]]=font[3]
        for block in page.get_text("dict")["blocks"]:
            if block["type"]!=0: continue
            for line in block["lines"]:
                for span in line["spans"]:
                    x0,y0,x1,y1=span["bbox"]
                    if x0<-1 or y0<-1 or x1>page.rect.width+1 or y1>page.rect.height+1:
                        bounds.append({"page":index+1,"text":span["text"][:80]})
    bengali=[(xref,name) for xref,name in fonts.items() if "BookBengali" in name]
    assert len(bengali)>=2
    assert all(len(pdf.extract_font(xref)[3])>0 for xref,_ in bengali)
    assert not empty
    assert not bounds
    assert replacement==0
    assert links>=29
    all_text="\n".join(combined)
    for number in range(1,25):
        assert f"Q{number:02d}" in all_text
    report={"pdf":path.name,"pages":len(pdf),"chapters_and_appendices":28,"figures":layout["figures"],
            "bookmarks":len(toc),"internal_links":links,"embedded_bengali_fonts":[name for _,name in bengali],
            "attachment_files":len(names),"empty_pages":empty,"out_of_page_text":bounds,
            "replacement_characters":replacement,"workbook_questions":"Q01–Q24 found",
            "pdf_sha256":layout["pdf_sha256"],"bytes":path.stat().st_size,
            "visual_review":"All-page overview plus full-size cover, TOC, table/code and workbook samples"}
    (ROOT/"reports/pdf-verification.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(report,ensure_ascii=False,indent=2))


if __name__=="__main__":
    main()
