"""Swaps one embedded image inside an existing .docx, leaving everything else
in the package untouched.

Used when the document has been edited by hand and must not be regenerated: the
figure is replaced in place rather than rebuilding the report around it.

    python replace_figure.py <document.docx> <old_image> <new_image>

The media entry to replace is found by matching the old image's bytes, and
failing that its pixel dimensions, so it still works if Word has re-encoded the
picture on save. The original document is copied to <name>.bak first.
"""

import shutil
import sys
import zipfile
from io import BytesIO
from pathlib import Path

from PIL import Image


def dimensions(blob):
    try:
        with Image.open(BytesIO(blob)) as im:
            return im.size
    except Exception:
        return None


def find_target(zf, old_blob):
    media = [n for n in zf.namelist() if n.startswith("word/media/")]
    for name in media:
        if zf.read(name) == old_blob:
            return name, "exact bytes"

    want = dimensions(old_blob)
    matches = [n for n in media if dimensions(zf.read(n)) == want] if want else []
    if len(matches) == 1:
        return matches[0], f"pixel size {want[0]}x{want[1]}"
    if len(matches) > 1:
        raise SystemExit(f"ambiguous: {len(matches)} images share size {want}; "
                         f"cannot tell which to replace")
    raise SystemExit("the old image was not found in the document")


def main():
    if len(sys.argv) != 4:
        raise SystemExit(__doc__)
    doc, old_path, new_path = (Path(a) for a in sys.argv[1:])
    old_blob = old_path.read_bytes()
    new_blob = new_path.read_bytes()

    with zipfile.ZipFile(doc) as zf:
        target, how = find_target(zf, old_blob)
        entries = [(i, zf.read(i.filename)) for i in zf.infolist()]

    backup = doc.with_suffix(doc.suffix + ".bak")
    shutil.copy2(doc, backup)

    buf = BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as out:
        for info, data in entries:
            out.writestr(info, new_blob if info.filename == target else data)
    doc.write_bytes(buf.getvalue())

    print(f"replaced {target} (matched by {how})")
    print(f"  {len(old_blob):,} bytes -> {len(new_blob):,} bytes")
    print(f"  backup at {backup.name}")


if __name__ == "__main__":
    main()
