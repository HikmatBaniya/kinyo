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

# A caption is the figure number followed by its exact title. Matching on the
# number alone also catches body sentences such as "Figure 7 decomposes ...".
CAPTIONS = {f"Figure {n} {title}": ("figures", str(n))
            for n, (title, _f, _w) in C.FIGURES.items()}
CAPTIONS.update({f"Table {n} {title}": ("tables", str(n))
                 for n, title in C.TABLE_TITLES.items()})


def printed_number(page):
    """The page number as written in the running footer."""
    floor = page.rect.height * 0.88
    words = [w for w in page.get_text("words") if w[1] > floor]
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
            hit = CAPTIONS.get(line.strip())
            if hit:
                bucket, number = hit
                index[bucket].setdefault(number, shown)

    OUT.write_text(json.dumps(index, indent=2), encoding="utf-8")
    print(f"wrote {OUT}")
    print("  figures:", index["figures"])
    print("  tables :", index["tables"])


if __name__ == "__main__":
    main()
