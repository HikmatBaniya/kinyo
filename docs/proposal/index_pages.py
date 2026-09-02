"""Reads the exported PDF and records which printed page each figure and table
caption falls on, so the List of Figures and List of Tables can carry real page
numbers.

The printed page number is taken from the running header rather than the PDF
page index, because the front matter is numbered in roman numerals and the body
restarts at 1.

Run after exporting the PDF, then rebuild the document:
    python index_pages.py
    python build_docx.py
"""

import json
import re
from pathlib import Path

import pymupdf

HERE = Path(__file__).parent
PDF = HERE.parent / "Kinyo_ProjectVI_Proposal.pdf"
OUT = HERE / "page_index.json"

CAPTION = re.compile(r"^(Figure|Table)\s+(\d+)$")


def printed_number(page):
    """The page number shown in the top-right header, as written."""
    top = page.rect.height * 0.09
    words = [w for w in page.get_text("words") if w[3] < top]
    if not words:
        return None
    words.sort(key=lambda w: -w[0])
    token = words[0][4].strip()
    return token if re.fullmatch(r"[ivxlcdm]+|\d+", token, re.I) else None


def main():
    doc = pymupdf.open(PDF)
    index = {"figures": {}, "tables": {}}
    for page in doc:
        shown = printed_number(page)
        if shown is None:
            continue
        for line in page.get_text().split("\n"):
            m = CAPTION.match(line.strip())
            if not m:
                continue
            kind, number = m.group(1), m.group(2)
            bucket = "figures" if kind == "Figure" else "tables"
            index[bucket].setdefault(number, shown)

    OUT.write_text(json.dumps(index, indent=2), encoding="utf-8")
    print(f"wrote {OUT}")
    print("  figures:", index["figures"])
    print("  tables :", index["tables"])


if __name__ == "__main__":
    main()
