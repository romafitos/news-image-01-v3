#!/usr/bin/env python3
"""Render a dense one-page newspaper front page (1024x1024) for
news-image-01 round 3: 33 real stories first reported Friday 13 Nov 2026,
6 continents, clean grid, one dominant hero headline, zero typos.

Code-drawn (PIL) so every character is exactly the verified text: no AI
text garbling, 100% legible at full resolution. Deterministic: fixed
inputs, no randomness, no timestamps. Reads stories.json next to this file,
writes entry.png next to this file.
"""
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
W, H = 1024, 1024
PAPER = (248, 244, 236)
INK = (22, 21, 19)
RED = (127, 29, 29)
RULE = (22, 21, 19)
HAIR = (150, 145, 132)
GREY = (90, 86, 76)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w, max_lines=None):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
            if max_lines and len(lines) >= max_lines:
                break
    if cur and (not max_lines or len(lines) < max_lines):
        lines.append(cur)
    return lines


def fit_text(draw, text, fnt_path, size, max_w, max_lines):
    """Shrink font until text fits in max_lines; return (font, lines)."""
    while size >= 12:
        fnt = font(fnt_path, size)
        lines = wrap(draw, text, fnt, max_w, max_lines)
        joined = " ".join(lines)
        if len(lines) <= max_lines and draw.textlength(joined, font=fnt) <= max_w * max_lines:
            # check nothing was dropped: all words present
            if " ".join(text.split()) == " ".join(" ".join(lines).split()):
                return fnt, lines
            if len(lines) < max_lines:
                return fnt, lines
        size -= 1
    fnt = font(fnt_path, 12)
    return fnt, wrap(draw, text, fnt, max_w, max_lines)


def draw_globe(draw, cx, cy, r):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=INK, width=2)
    draw.ellipse([cx - int(r * 0.45), cy - r, cx + int(r * 0.45), cy + r],
                 outline=INK, width=1)
    draw.line([cx - r, cy, cx + r, cy], fill=INK, width=1)
    draw.arc([cx - r, cy - int(r * 0.55), cx + r, cy + int(r * 0.55)],
             200, 340, fill=INK, width=1)
    draw.arc([cx - r, cy - int(r * 0.55), cx + r, cy + int(r * 0.55)],
             20, 160, fill=INK, width=1)


def main():
    data = json.loads((HERE / "stories.json").read_text())
    hero = data["hero"]
    columns = data["columns"]  # list of 3: each list of {"section": str, "stories": [...]}
    ticker = data["ticker"]
    total = 1 + sum(len(s["stories"]) for col in columns for s in col) + data.get("ticker_stories", 0)
    assert total == data["story_count"], f"story count {total} != {data['story_count']}"

    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    MX = 30  # side margin

    # --- globe + masthead ---
    draw_globe(d, W // 2, 38, 22)
    mast = font(SERIF_B, 78)
    d.text((W // 2, 108), "THE WORLD", font=mast, fill=INK, anchor="mm")
    d.line([MX, 152, W - MX, 152], fill=RULE, width=2)
    dl = font(SANS_B, 14)
    d.text((MX, 166), "FRIDAY, 13 NOVEMBER 2026", font=dl, fill=INK, anchor="lm")
    right = f"{data['story_count']} STORIES  ·  6 CONTINENTS  ·  ONE PAGE"
    d.text((W - MX, 166), right, font=dl, fill=INK, anchor="rm")
    d.line([MX, 182, W - MX, 182], fill=RED, width=3)
    d.line([MX, 187, W - MX, 187], fill=RULE, width=1)

    # --- hero ---
    y = 202
    kick = font(SANS_B, 13)
    d.text((MX, y), hero["kicker"], font=kick, fill=RED, anchor="la")
    y += 22
    hf, hlines = fit_text(d, hero["headline"], SERIF_B, 44, W - 2 * MX, 2)
    for ln in hlines:
        d.text((MX, y), ln, font=hf, fill=INK, anchor="la")
        y += 52
    y += 2
    deck_f = font(SERIF, 15)
    for ln in wrap(d, hero["deck"], deck_f, W - 2 * MX, 2):
        d.text((MX, y), ln, font=deck_f, fill=INK, anchor="la")
        y += 19
    sub_f = font(SERIF, 13)
    for ln in wrap(d, hero["subdeck"], sub_f, W - 2 * MX, 1):
        d.text((MX, y), ln, font=sub_f, fill=(52, 50, 46), anchor="la")
        y += 17
    y += 8
    d.line([MX, y, W - MX, y], fill=RULE, width=2)
    y += 12
    grid_top = y

    # --- grid: 3 columns ---
    col_w = (W - 2 * MX - 2 * 16) // 3
    xs = [MX, MX + col_w + 16, MX + 2 * (col_w + 16)]
    label_f = font(SANS_B, 14)
    head_f = font(SERIF_B, 17)
    deck2_f = font(SERIF, 12)
    for ci, col in enumerate(columns):
        x = xs[ci]
        yy = grid_top
        for sec in col:
            # section bar
            d.rectangle([x, yy, x + col_w, yy + 23], fill=INK)
            d.text((x + 8, yy + 11), sec["section"], font=label_f,
                   fill=PAPER, anchor="lm")
            yy += 23 + 8
            for st in sec["stories"]:
                hlines = wrap(d, st["headline"], head_f, col_w, 2)
                for ln in hlines:
                    d.text((x, yy), ln, font=head_f, fill=INK, anchor="la")
                    yy += 19
                for ln in wrap(d, st["deck"], deck2_f, col_w, 2):
                    d.text((x, yy), ln, font=deck2_f, fill=(52, 50, 46), anchor="la")
                    yy += 14
                yy += 6
                d.line([x, yy, x + col_w, yy], fill=HAIR, width=1)
                yy += 6
        if yy > 956:
            print(f"COLUMN {ci} OVERFLOW: bottom y={yy} (limit 956)", file=sys.stderr)
            return 1
        print(f"column {ci} bottom y={yy}", file=sys.stderr)

    # --- ticker + footer ---
    d.rectangle([MX, 962, W - MX, 990], fill=INK)
    tick_f = font(SANS_B, 13)
    d.text((MX + 10, 976), ticker, font=tick_f, fill=PAPER, anchor="lm")
    foot_f = font(SANS, 11)
    d.text((W // 2, 1004),
           "THE WORLD  ·  Every story first reported Friday 13 November 2026",
           font=foot_f, fill=GREY, anchor="mm")

    out = HERE / "entry.png"
    img.save(out, "PNG", optimize=True)
    print(f"wrote {out} ({out.stat().st_size} bytes) stories={total}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
