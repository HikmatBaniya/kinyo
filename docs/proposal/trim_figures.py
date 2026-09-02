"""Trims uniform white margins from the rendered figures, leaving a small pad."""
from pathlib import Path
from PIL import Image, ImageChops

PAD = 24

for f in sorted(Path("figures").glob("*.png")):
    im = Image.open(f).convert("RGB")
    bg = Image.new("RGB", im.size, (255, 255, 255))
    bbox = ImageChops.difference(im, bg).getbbox()
    if not bbox:
        continue
    l, t, r, b = bbox
    box = (max(l - PAD, 0), max(t - PAD, 0),
           min(r + PAD, im.width), min(b + PAD, im.height))
    out = im.crop(box)
    out.save(f)
    print(f"{f.name}: {im.size} -> {out.size}  aspect {out.height / out.width:.2f}")
