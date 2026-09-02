# Kinyo — Project-VI Proposal

`Kinyo_ProjectVI_Proposal.docx` is the deliverable. `Kinyo_ProjectVI_Proposal.pdf`
is a rendered copy for checking. Both are generated — edit the sources under
`proposal/`, never the `.docx` directly, or your changes are lost on the next build.

## Regenerating

```bash
cd proposal
python build_docx.py            # content.py + figures/ -> ../Kinyo_ProjectVI_Proposal.docx
```

Then open the document in Word and press `Ctrl+A`, `F9` to update the table of
contents, or run the same update from PowerShell:

```powershell
$w = New-Object -ComObject Word.Application
$d = $w.Documents.Open("<abs path>\Kinyo_ProjectVI_Proposal.docx")
$d.Fields.Update(); foreach ($t in $d.TablesOfContents) { $t.Update() }
$d.Save(); $d.Close(0); $w.Quit()
```

## Layout

| Path | Purpose |
| --- | --- |
| `proposal/content.py` | All prose, tables, references and metadata |
| `proposal/build_docx.py` | APA 7th edition formatting and document assembly |
| `proposal/diagrams/*.mmd` | Mermaid sources (Figure 2 only) |
| `proposal/diagrams/gen_*.py` | SVG generators for Figures 1, 5, 6, 7 |
| `proposal/diagrams/fig3_flowchart.html`, `fig4_usecase.html` | Hand-authored SVG for Figures 3 and 4 |
| `proposal/figures/*.png` | Rendered figures embedded in the document |
| `proposal/render_html.js` | Puppeteer HTML/SVG → PNG renderer |
| `proposal/trim_figures.py` | Crops white margins from rendered figures |

Mermaid is used only for the architecture diagram. The other six figures are
authored as SVG because Mermaid's layout spacing makes the text illegible once a
diagram is scaled down to the 6.1 in text width of an A4 page.

### Rebuilding a figure

```bash
cd proposal
python diagrams/gen_erd.py                                    # regenerate the SVG
node render_html.js diagrams/fig7_erd.html figures/fig7_erd.png 1670 2
python trim_figures.py                                        # crop white margins
python build_docx.py
```

Figure 2 is the exception:

```bash
npx -y @mermaid-js/mermaid-cli@11 -i diagrams/fig2_architecture.mmd \
  -o figures/fig2_architecture.png -c mermaid-config.json -b white -s 3
```

## Before submitting

Replace every placeholder in square brackets in `proposal/content.py` (`META`):

- [ ] `college` and `college_address`
- [ ] `students` — names and roll numbers
- [ ] `supervisor`
- [ ] `city` and `month_year`
- [ ] `repo_backend` and `repo_frontend` — the checklist requires live repository links
- [ ] `MONTHS` — replace `M1`–`M6` with the real month names, and check the shaded
      cells in `TIMELINE` match your actual schedule

Then:

- [ ] Rebuild, update the table of contents, and fill the page numbers in the
      List of Figures and List of Tables (they are left blank deliberately —
      they cannot be known until the TOC is updated).
- [ ] Verify every reference URL and year still resolves. The reference list was
      written from the official documentation of each system, but publication
      years for living documentation should be checked against what you actually
      accessed.
- [ ] Delete the italic instruction line under the Table of Contents heading.

## Formatting implemented

Times New Roman 12 pt throughout; double spacing with 0 pt paragraph spacing;
A4 portrait with 1 in margins; flush-left ragged-right text; 0.5 in first-line
indent; page numbers top right, lower-case roman in the front matter and
restarting at 1 in arabic from Chapter 1; APA heading levels 1–3 distinguished
by position and emphasis at 12 pt; tables with horizontal rules only, table
number bold above and italic title below; figure number bold above and italic
title below it with the image beneath; reference list alphabetical with a 0.5 in
hanging indent and italicised titles of larger works.

Chapter lengths in the current build: Chapter 1, 4 pages; Chapter 2, 8 pages;
Chapter 3, 15 pages; Chapter 4, 4 pages; Chapter 5, 3 pages — all above the
minimums in the template.
