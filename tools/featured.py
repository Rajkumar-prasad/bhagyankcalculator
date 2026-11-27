"""Featured images for blog posts (1200x630 JPG), drawn from the post title in the site's navy-and-gold style.

Used by build.py: make_featured(post, out_path). Works for English, Hindi and Marathi titles (Poppins covers Devanagari;
Pillow needs raqm for correct Hindi/Marathi shaping - check.py warns if it is missing).
"""
import random
import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, features

FONTS = Path(__file__).resolve().parent / "fonts"
W, H = 1200, 630
NAVY_TOP, NAVY_BOTTOM = (20, 17, 48), (43, 35, 87)
GOLD, CREAM, MUTED = (240, 185, 65), (240, 233, 220), (185, 176, 156)
LANG_TAG = {"en": "NUMEROLOGY GUIDE", "hi": "अंक ज्योतिष गाइड", "mr": "अंकशास्त्र मार्गदर्शक"}
BY = {"en": "By Ananya Sharma", "hi": "लेखिका: अनन्या शर्मा", "mr": "लेखिका: अनन्या शर्मा"}


def _font(weight, size):
    layout = ImageFont.Layout.RAQM if features.check("raqm") else ImageFont.Layout.BASIC
    return ImageFont.truetype(str(FONTS / f"Poppins-{weight}.ttf"), size, layout_engine=layout)


def _wrap(draw, text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if draw.textlength(test, font=font) <= max_w or not cur:
            cur = test
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


_NUM_WORDS = r"(?:bhagyank|mulank|moolank|namank|number|no\.|भाग्यांक|मूलांक|नामांक|अंक|नंबर|क्रमांक)"


def _numbers(text):
    """Numbers the post is about: digits right after (or before) a number word, e.g.
    'मूलांक 5 भाग्यांक 8' -> ['5', '8'], 'missing number 8' -> ['8'], '5 नंबर' -> ['5'].
    A count like '5 उदाहरणे' or '3 examples' is ignored."""
    after = re.findall(_NUM_WORDS + r"\s*([1-9])(?![\d.,])", text, flags=re.I)
    before = re.findall(r"(?<![\d.,])([1-9])\s*" + _NUM_WORDS, text, flags=re.I)
    seen = []
    for n in after + before:
        if n not in seen:
            seen.append(n)
    return seen[:2]


def make_featured(post, out_path):
    title = post["h1"]
    lang = post.get("lang", "en")
    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)
    for y in range(H):  # vertical gradient
        t = y / H
        d.line([(0, y), (W, y)], fill=tuple(int(a + (b - a) * t) for a, b in zip(NAVY_TOP, NAVY_BOTTOM)))
    rnd = random.Random(post["slug"])  # same post -> same stars, so the file does not change between builds
    for _ in range(70):
        x, y, r = rnd.randint(0, W), rnd.randint(0, H), rnd.choice([1, 1, 1, 2])
        c = rnd.randint(90, 170)
        d.ellipse([x, y, x + r, y + r], fill=(c, c, min(255, c + 40)))

    # right-hand badge: the number(s) the post is about, or a star
    nums = _numbers(title)
    cx, cy, R = 1010, 300, 118
    d.ellipse([cx - R, cy - R, cx + R, cy + R], outline=GOLD, width=6, fill=(56, 46, 98))
    if nums:
        label = " + ".join(nums)
        f = _font("Bold", 150 if len(nums) == 1 else 92)
        d.text((cx, cy - 6), label, font=f, fill=GOLD, anchor="mm")
    else:
        s = 70
        pts = [(cx, cy - s), (cx + s * .26, cy - s * .26), (cx + s, cy), (cx + s * .26, cy + s * .26),
               (cx, cy + s), (cx - s * .26, cy + s * .26), (cx - s, cy), (cx - s * .26, cy - s * .26)]
        d.polygon(pts, fill=GOLD)

    # tag pill
    tag = LANG_TAG.get(lang, LANG_TAG["en"])
    ft = _font("Medium", 24)
    tw = d.textlength(tag, font=ft)
    d.rounded_rectangle([70, 64, 70 + tw + 44, 112], radius=24, outline=GOLD, width=2, fill=(52, 43, 70))
    d.text((92, 88), tag, font=ft, fill=GOLD, anchor="lm")

    # title, auto-fitted to at most 4 lines in the left 780px
    max_w, size = 780, 66
    while True:
        f = _font("Bold", size)
        lines = _wrap(d, title, f, max_w)
        line_h = int(size * (1.45 if lang != "en" else 1.25))
        if len(lines) <= 4 or size <= 38:
            break
        size -= 4
    lines = lines[:4]
    top = 150 + max(0, (4 - len(lines)) * line_h // 2) // 2
    for i, line in enumerate(lines):
        d.text((70, top + i * line_h), line, font=f, fill=CREAM)

    # footer: brand + author
    d.line([(70, 530), (W - 70, 530)], fill=(70, 62, 120), width=2)
    d.ellipse([70, 552, 110, 592], fill=GOLD)
    d.polygon([(90, 558), (94, 568), (104, 572), (94, 576), (90, 586), (86, 576), (76, 572), (86, 568)], fill=NAVY_TOP)
    d.text((124, 572), "bhagyank-calculator.online", font=_font("Medium", 28), fill=CREAM, anchor="lm")
    d.text((W - 70, 572), BY.get(lang, BY["en"]), font=_font("Medium", 24), fill=MUTED, anchor="rm")

    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    img.save(out_path, "JPEG", quality=84, optimize=True, progressive=True)
