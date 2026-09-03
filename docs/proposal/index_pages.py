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

import content as C

HERE = Path(__file__).parent
PDF = HERE.parent / "Kinyo_ProjectVI_Proposal.pdf"
OUT = HERE / "page_index.json"

# With the number on its own line above the figure, a caption is a line that is
# exactly "Figure N" or "Table N"; body prose never takes that form.
CAPTION = re.compile(r"^(Figure|Table)\s+(\d+)$")

def printed_number(page):
    """The page number as written in the running header."""
    ceiling = page.rect.height * 0.12
    words = [w for w in page.get_text("words") if w[3] < ceiling]
    for w in words:
        token = w[4].strip()
        if re.fullmatch(r"[ivxlcdm]+|\d+", token, re.I):
            return token
    return None


def main():
    doc = pymupdf.open(PDF)
    index = {"figures": {}, "tables": {}}
    for page in doc:
        shown = printed_number(page)
        if shown is None:
            continue
        for line in page.get_text().splitlines():
            m = CAPTION.match(line.strip())
            if m:
                bucket = "figures" if m.group(1) == "Figure" else "tables"
                index[bucket].setdefault(m.group(2), shown)

    OUT.write_text(json.dumps(index, indent=2), encoding="utf-8")
    print(f"wrote {OUT}")
    print("  figures:", index["figures"])
    print("  tables :", index["tables"])


if __name__ == "__main__":
    main()
