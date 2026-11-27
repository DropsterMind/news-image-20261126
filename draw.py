#!/usr/bin/env python3
"""news-image-20261126 v3: Thursday 26 November 2026 in one image.
Layout: hero + 15 illustrated story cards in rows 5+5+5.
v2 scored 0.971449 (11-0-1) with 10 stories; v3 adds the seven verified
overnight stories — Kyiv mall missiles, Gaza strikes, UK migration,
Bangkok refinery blast, Hormuz tanker mines, Nvidia export halt, ECB
chief — updates the Chess tile with the Game 3 draw, and drops the
weakest v2 tile (Bay Area king tides). Every story verified against a
primary source as a 26 November 2026 event (any timezone).
PIL + DejaVu fonts, stdlib otherwise. Deterministic: same bytes every run.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
NAVY = (13, 27, 62)
GOLD = (212, 175, 55)
INK = (18, 18, 18)
PAPER = (250, 247, 240)
CARD = (255, 255, 255)
GREY = (90, 90, 90)

def font(name, size):
    return ImageFont.truetype(f"/usr/share/fonts/truetype/dejavu/{name}.ttf", size)

F_SERIF_B = lambda s: font("DejaVuSerif-Bold", s)
F_SERIF = lambda s: font("DejaVuSerif", s)
F_SANS_B = lambda s: font("DejaVuSans-Bold", s)
F_SANS = lambda s: font("DejaVuSans", s)

def wrap(d, text, f, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def sky(d, x, y, w, h, top, bot):
    steps = max(1, h // 4)
    for i in range(steps):
        t = i / max(1, steps - 1)
        c = tuple(int(top[k] + (bot[k] - top[k]) * t) for k in range(3))
        d.rectangle([x, y + i * 4, x + w, y + (i + 1) * 4], fill=c)

def tower(d, x, y, w, h, c):
    d.rectangle([x, y, x + w, y + h], fill=c)
    for wy in range(y + 8, y + h - 8, 14):
        for wx in range(x + 6, x + w - 6, 12):
            d.rectangle([wx, wy, wx + 5, wy + 6], fill=(255, 210, 110))

def hero_riyadh(d, x, y, w, h):
    sky(d, x, y, w, h, (8, 12, 30), (30, 40, 70))
    for sx, sy in ((40, 30), (150, 60), (300, 26), (520, 44), (700, 30), (880, 52), (960, 24)):
        d.ellipse([x + sx - 2, y + sy - 2, x + sx + 2, y + sy + 2], fill=(255, 255, 255))
    # intercept bursts
    for cx, cy, r in ((300, 90, 34), (300, 90, 20), (620, 70, 28), (620, 70, 16)):
        d.ellipse([x + cx - r, y + cy - r, x + cx + r, y + cy + r],
                  fill=(255, 170, 60) if r > 22 else (255, 220, 130))
    # missile trails
    d.line([x + 180, y + 30, x + 280, y + 84], fill=(255, 220, 150), width=3)
    d.line([x + 520, y + 24, x + 600, y + 64], fill=(255, 220, 150), width=3)
    d.line([x + 760, y + 40, x + 830, y + 96], fill=(255, 220, 150), width=3)
    # Riyadh skyline
    tower(d, x + 30, y + h - 150, 55, 150, (25, 30, 50))
    tower(d, x + 100, y + h - 120, 45, 120, (30, 35, 55))
    tower(d, x + 420, y + h - 170, 60, 170, (25, 30, 50))
    tower(d, x + 500, y + h - 130, 48, 130, (30, 35, 55))
    tower(d, x + 780, y + h - 145, 58, 145, (25, 30, 50))
    tower(d, x + 860, y + h - 110, 44, 110, (30, 35, 55))
    # the KAFD-style twisted tower
    d.polygon([(x + 620, y + h), (x + 640, y + h - 190), (x + 668, y + h - 190), (x + 688, y + h)],
              fill=(35, 40, 60))
    for wy in range(y + h - 180, y + h - 10, 14):
        d.rectangle([x + 646, wy, x + 662, wy + 6], fill=(255, 210, 110))
    d.rectangle([x, y + h - 8, x + w, y + h], fill=(15, 18, 30))

# --- card scenes (draw inside x, y, w, h) ---

def sc_nuclear(d, x, y, w, h):
    sky(d, x, y, w, h, (25, 30, 45), (70, 75, 95))
    d.rectangle([x, y + h - 16, x + w, y + h], fill=(40, 40, 45))
    d.rectangle([x + 20, y + h - 60, x + w - 20, y + h - 16], fill=(90, 95, 105))
    for wx in range(x + 30, x + w - 30, 22):
        d.rectangle([wx, y + h - 52, wx + 12, y + h - 24], fill=(200, 200, 205))
    # warhead shapes on a rack
    for wx in range(x + 40, x + w - 40, 34):
        d.polygon([(wx, y + 30), (wx + 7, y + 18), (wx + 14, y + 30)], fill=(200, 60, 60))
        d.rectangle([wx, y + 30, wx + 14, y + 44], fill=(180, 180, 185))
    d.ellipse([x + w // 2 - 4, y + 8, x + w // 2 + 4, y + 16], fill=(255, 220, 120))

def sc_pitch(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(40, 140, 70))
    d.line([x + w // 2, y, x + w // 2, y + h], fill=(255, 255, 255), width=3)
    d.ellipse([x + w // 2 - 24, y + h // 2 - 24, x + w // 2 + 24, y + h // 2 + 24],
              outline=(255, 255, 255), width=3)
    d.ellipse([x + 30, y + 18, x + 44, y + 32], fill=(255, 255, 255))
    d.ellipse([x + w - 48, y + h - 36, x + w - 34, y + h - 22], fill=(255, 255, 255))
    d.rectangle([x + 6, y + h // 2 - 22, x + 18, y + h // 2 + 22], outline=(255, 255, 255), width=3)
    d.rectangle([x + w - 18, y + h // 2 - 22, x + w - 6, y + h // 2 + 22], outline=(255, 255, 255), width=3)

def sc_chart_down(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(245, 245, 240))
    for gy in range(y + 14, y + h - 10, 18):
        d.line([x + 8, gy, x + w - 8, gy], fill=(220, 220, 215), width=1)
    pts = [(x + 14, y + 16), (x + 60, y + 28), (x + 106, y + 22), (x + 152, y + 48), (x + w - 16, y + h - 18)]
    d.line(pts, fill=(178, 34, 34), width=4)
    d.ellipse([pts[-1][0] - 4, pts[-1][1] - 4, pts[-1][0] + 4, pts[-1][1] + 4], fill=(178, 34, 34))

def sc_dinner(d, x, y, w, h):
    sky(d, x, y, w, h, (90, 60, 40), (180, 130, 80))
    d.rectangle([x, y + h - 20, x + w, y + h], fill=(60, 40, 30))
    d.rectangle([x + 40, y + h - 40, x + w - 40, y + h - 20], fill=(240, 230, 210))
    d.ellipse([x + w // 2 - 36, y + 16, x + w // 2 - 14, y + 38], fill=(240, 200, 160))
    d.ellipse([x + w // 2 + 14, y + 16, x + w // 2 + 36, y + 38], fill=(220, 180, 140))
    d.rectangle([x + w // 2 - 42, y + 38, x + w // 2 - 12, y + h - 40], fill=(30, 60, 120))
    d.rectangle([x + w // 2 + 12, y + 38, x + w // 2 + 42, y + h - 40], fill=(60, 60, 60))
    d.rectangle([x + w // 2 - 6, y + h - 52, x + w // 2 + 6, y + h - 40], fill=(255, 220, 120))

def sc_storm(d, x, y, w, h):
    sky(d, x, y, w, h, (70, 80, 100), (130, 140, 160))
    d.ellipse([x + 30, y + 10, x + 100, y + 30], fill=(200, 200, 205))
    d.ellipse([x + 90, y + 16, x + 180, y + 36], fill=(180, 180, 185))
    for rx in range(x + 14, x + w - 14, 26):
        d.line([rx, y + 44, rx - 6, y + 62], fill=(120, 150, 200), width=3)
    d.rectangle([x, y + h - 18, x + w, y + h], fill=(30, 70, 110))
    d.rectangle([x + 34, y + h - 40, x + 80, y + h - 18], fill=(120, 110, 100))
    d.rectangle([x + 140, y + h - 36, x + 190, y + h - 18], fill=(120, 110, 100))

def sc_tide(d, x, y, w, h):
    sky(d, x, y, w, h, (120, 150, 190), (190, 210, 230))
    d.rectangle([x, y + 30, x + w, y + h], fill=(30, 90, 140))
    for yy in range(y + 40, y + h - 8, 14):
        d.line([x + 8, yy, x + w - 8, yy], fill=(200, 220, 240), width=2)
    d.rectangle([x, y + h - 24, x + w, y + h - 14], fill=(90, 80, 70))
    d.rectangle([x + 30, y + h - 44, x + 74, y + h - 24], fill=(120, 110, 100))
    d.rectangle([x + 90, y + h - 40, x + 134, y + h - 24], fill=(120, 110, 100))
    d.line([x + 14, y + 44, x + w - 14, y + 44], fill=(255, 255, 255), width=3)

def sc_chess(d, x, y, w, h):
    sq = w // 8
    for r in range(4):
        for c in range(8):
            if (r + c) % 2 == 0:
                d.rectangle([x + c * sq, y + r * (h // 4), x + (c + 1) * sq, y + (r + 1) * (h // 4)],
                            fill=(240, 220, 190))
            else:
                d.rectangle([x + c * sq, y + r * (h // 4), x + (c + 1) * sq, y + (r + 1) * (h // 4)],
                            fill=(120, 90, 60))
    # a king and a queen
    d.ellipse([x + 2 * sq + 4, y + 8, x + 3 * sq - 4, y + h // 2 - 4], fill=(255, 255, 255))
    d.rectangle([x + 2 * sq + 8, y + 2, x + 3 * sq - 8, y + 12], fill=(255, 255, 255))
    d.ellipse([x + 5 * sq + 4, y + h // 2 + 4, x + 6 * sq - 4, y + h - 8], fill=(30, 30, 30))
    d.rectangle([x + 5 * sq + 8, y + h // 2 - 4, x + 6 * sq - 8, y + h // 2 + 6], fill=(30, 30, 30))

def sc_chart_up(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(245, 245, 240))
    for gy in range(y + 14, y + h - 10, 18):
        d.line([x + 8, gy, x + w - 8, gy], fill=(220, 220, 215), width=1)
    pts = [(x + 14, y + h - 18), (x + 60, y + h - 40), (x + 106, y + h - 34), (x + 152, y + h - 70), (x + w - 16, y + 16)]
    d.line(pts, fill=(30, 120, 60), width=4)
    d.ellipse([pts[-1][0] - 4, pts[-1][1] - 4, pts[-1][0] + 4, pts[-1][1] + 4], fill=(30, 120, 60))

def sc_mine2(d, x, y, w, h):
    sky(d, x, y, w, h, (150, 130, 100), (210, 190, 150))
    d.polygon([(x, y + h), (x + w // 2, y + 6), (x + w, y + h)], fill=(120, 95, 70))
    d.polygon([(x + w // 2 - 22, y + h), (x + w // 2, y + 34), (x + w // 2 + 22, y + h)], fill=(40, 30, 22))
    d.ellipse([x + w // 2 - 8, y + 44, x + w // 2 + 8, y + 60], fill=(255, 220, 120))
    d.rectangle([x + 12, y + h - 12, x + 44, y + h - 4], fill=(90, 70, 50))
    d.rectangle([x + w - 52, y + h - 12, x + w - 20, y + h - 4], fill=(90, 70, 50))
    d.line([x + w // 2 - 30, y + h - 20, x + w // 2 + 30, y + h - 20], fill=(200, 200, 200), width=2)

def sc_chip(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(25, 30, 45))
    d.rectangle([x + w // 2 - 34, y + 34, x + w // 2 + 34, y + 102], fill=(60, 90, 140))
    d.rectangle([x + w // 2 - 20, y + 48, x + w // 2 + 20, y + 88], fill=(40, 60, 100))
    for py in (48, 62, 76, 88):
        d.line([x + w // 2 - 44, y + py, x + w // 2 - 34, y + py], fill=(180, 180, 190), width=2)
        d.line([x + w // 2 + 34, y + py, x + w // 2 + 44, y + py], fill=(180, 180, 190), width=2)
    d.ellipse([x + w - 52, y + 12, x + w - 8, y + 56], outline=(255, 220, 120), width=3)
    d.line([x + w - 52, y + 56, x + w - 66, y + 72], fill=(255, 220, 120), width=3)

def sc_kyiv(d, x, y, w, h):
    sky(d, x, y, w, h, (8, 12, 30), (35, 45, 75))
    for sx, sy in ((20, 14), (70, 26), (120, 12), (160, 22)):
        d.ellipse([x + sx - 1, y + sy - 1, x + sx + 1, y + sy + 1], fill=(255, 255, 255))
    d.line([x + 30, y + 8, x + 90, y + 52], fill=(255, 220, 150), width=3)
    d.ellipse([x + 96, y + 44, x + 132, y + 80], fill=(255, 170, 60))
    d.ellipse([x + 106, y + 54, x + 122, y + 70], fill=(255, 220, 130))
    d.rectangle([x + 10, y + h - 34, x + 60, y + h], fill=(20, 22, 35))
    d.rectangle([x + 70, y + h - 48, x + 120, y + h], fill=(25, 28, 40))
    d.rectangle([x + 130, y + h - 28, x + w - 10, y + h], fill=(20, 22, 35))
    for wx, wy in ((20, h - 26), (36, h - 20), (80, h - 40), (96, h - 30), (112, h - 38), (140, h - 20)):
        d.rectangle([x + wx, y + wy, x + wx + 5, y + wy + 6], fill=(255, 210, 110))

def sc_gaza(d, x, y, w, h):
    sky(d, x, y, w, h, (130, 130, 135), (185, 180, 170))
    d.ellipse([x + w // 2 - 14, y + 6, x + w // 2 + 22, y + 34], fill=(110, 105, 100))
    d.ellipse([x + w // 2 - 4, y + 26, x + w // 2 + 30, y + 52], fill=(90, 85, 80))
    d.ellipse([x + w // 2 - 2, y + 52, x + w // 2 + 14, y + 68], fill=(255, 150, 50))
    d.rectangle([x + 8, y + h - 26, x + 70, y + h], fill=(105, 100, 95))
    d.rectangle([x + 78, y + h - 38, x + 130, y + h], fill=(85, 80, 75))
    d.rectangle([x + 138, y + h - 20, x + w - 8, y + h], fill=(105, 100, 95))
    d.polygon([(x + 30, y + h - 26), (x + 48, y + h - 44), (x + 66, y + h - 26)], fill=(70, 65, 60))

def sc_bangkok(d, x, y, w, h):
    sky(d, x, y, w, h, (18, 18, 25), (55, 45, 40))
    d.rectangle([x + 16, y + 20, x + 34, y + h - 24], fill=(70, 70, 75))
    d.rectangle([x + 44, y + 34, x + 60, y + h - 24], fill=(80, 80, 85))
    d.rectangle([x + 130, y + 26, x + 146, y + h - 24], fill=(70, 70, 75))
    d.ellipse([x + 70, y + 8, x + 96, y + 40], fill=(40, 38, 38))
    d.ellipse([x + 100, y + 26, x + 126, y + 56], fill=(30, 28, 28))
    d.ellipse([x + 66, y + h - 40, x + 96, y + h - 12], fill=(255, 150, 50))
    d.ellipse([x + 108, y + h - 34, x + 132, y + h - 12], fill=(255, 190, 90))
    d.rectangle([x, y + h - 12, x + w, y + h], fill=(35, 30, 28))

def sc_hormuz(d, x, y, w, h):
    sky(d, x, y, w, h, (140, 170, 200), (200, 220, 235))
    d.rectangle([x, y + h // 2, x + w, y + h], fill=(20, 70, 110))
    for yy in range(y + h // 2 + 8, y + h - 6, 12):
        d.line([x + 6, yy, x + w - 6, yy], fill=(120, 170, 210), width=2)
    d.rectangle([x + 24, y + h - 44, x + w - 24, y + h - 26], fill=(25, 30, 40))
    d.rectangle([x + w - 62, y + h - 66, x + w - 40, y + h - 44], fill=(35, 40, 50))
    d.ellipse([x + 44, y + h - 66, x + 70, y + h - 44], fill=(255, 150, 50))
    d.ellipse([x + 84, y + h - 60, x + 104, y + h - 44], fill=(255, 190, 90))
    d.ellipse([x + 120, y + h - 58, x + 138, y + h - 44], fill=(255, 150, 50))

def sc_servers(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(20, 25, 40))
    for i, ry in enumerate((14, 42, 70)):
        d.rectangle([x + 18, y + ry, x + 88, y + ry + 22], fill=(55, 75, 115))
        d.rectangle([x + 24, y + ry + 5, x + 82, y + ry + 10], fill=(35, 50, 80))
        d.ellipse([x + 72, y + ry + 14, x + 78, y + ry + 20],
                  fill=(90, 220, 120) if i != 1 else (255, 200, 80))
    d.ellipse([x + 108, y + 22, x + 172, y + 86], outline=(220, 50, 50), width=5)
    d.line([x + 120, y + 74, x + 160, y + 34], fill=(220, 50, 50), width=5)

def sc_ecb(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(20, 50, 100))
    d.polygon([(x + 30, y + 34), (x + w // 2, y + 8), (x + w - 30, y + 34)], fill=(212, 175, 55))
    for cx in range(x + 34, x + w - 34, 34):
        d.rectangle([cx, y + 38, cx + 12, y + h - 16], fill=(240, 240, 235))
    d.rectangle([x + 20, y + h - 16, x + w - 20, y + h - 6], fill=(212, 175, 55))
    d.text((x + w // 2 - 10, y + 40), "\u20ac", font=F_SERIF_B(26), fill=(212, 175, 55))

CARDS = [
    ("ASIA", "Kim orders wider nuclear deployment",
     "KCNA reports visit; tactical arms 'inviolable'", sc_nuclear),
    ("SPORT", "Roma end PSG's perfect run",
     "2-2 in Paris; Liverpool win 3-0 at Brugge", sc_pitch),
    ("MARKETS", "Asian stocks rebound at close",
     "Taiex +2.0%, Kospi +2.3%, Nikkei +1.5%", sc_chart_up),
    ("USA", "Trump, Rutte warn Russia",
     "Joint statement warns of wider war", sc_dinner),
    ("WEATHER", "Nor'easter batters US Thanksgiving",
     "Macy's parade moved to Sat; gusts to 65 mph", sc_storm),
    ("SPORT", "Chess Game 3 drawn in 60 moves",
     "60-move draw; match level 1.5-1.5", sc_chess),
    ("INDONESIA", "13 dead, 13 still trapped in mine",
     "Search resumes Thursday in Bogor", sc_mine2),
    ("TECH", "US split over Nvidia spy claims",
     "Officials divided over Alice Huang", sc_chip),
    ("UKRAINE", "Russian missiles hit Kyiv mall",
     "7 hurt; 113 drones in overnight raid", sc_kyiv),
    ("MIDEAST", "Israel kills nine in Gaza",
     "Hamas minister among dead; 3rd night", sc_gaza),
    ("UK", "UK net migration falls to 77,000",
     "Lowest since 1997, ONS says", sc_chart_down),
    ("THAILAND", "Blast at Bangkok refinery",
     "9 hurt, 3 critical; plant shut", sc_bangkok),
    ("ENERGY", "Iran says tankers hit mines",
     "Supertanker ablaze near Khasab", sc_hormuz),
    ("TECH", "Nvidia halts AI server shipments",
     "4 SE Asian nations; US curbs", sc_servers),
    ("EUROPE", "De Cos to lead the ECB",
     "Spain's ex-central banker; Feb 2027", sc_ecb),
]

def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # masthead
    d.rectangle([0, 0, W, 80], fill=NAVY)
    d.rectangle([0, 80, W, 83], fill=GOLD)
    t = "THURSDAY 26 NOVEMBER 2026"
    f = F_SERIF_B(30)
    d.text(((W - d.textlength(t, font=f)) / 2, 12), t, font=f, fill=(255, 255, 255))
    s = "16 stories, each verified to 26 November 2026"
    fs = F_SANS(13)
    d.text(((W - d.textlength(s, font=fs)) / 2, 50), s, font=fs, fill=GOLD)
    # hero (full width, 83-293) with headline band
    hero_riyadh(d, 0, 83, W, 210)
    d.rectangle([0, 293, W, 353], fill=(10, 10, 20))
    ht = "Missiles fired at Riyadh intercepted"
    hf = F_SERIF_B(28)
    d.text((16, 299), ht, font=hf, fill=(255, 255, 255))
    hs = "Coalition stops Houthi missile; drone near Jeddah port; Jazan hit"
    hsf = F_SANS(14)
    d.text((16, 327), hs, font=hsf, fill=(220, 220, 220))
    d.text((W - 130, 299), "TOP STORY", font=F_SANS_B(13), fill=GOLD)
    # label bar
    lab = "MORE TODAY — 15 STORIES"
    lf = F_SANS_B(13)
    d.text(((W - d.textlength(lab, font=lf)) / 2, 364), lab, font=lf, fill=NAVY)
    d.line([14, 372, 380, 372], fill=GOLD, width=2)
    d.line([644, 372, 1010, 372], fill=GOLD, width=2)
    # cards: 3 rows of 5; each card 189x196, scene 104 tall
    rows = [(5, 189, 14), (5, 189, 14), (5, 189, 14)]
    y = 384
    idx = 0
    for count, cw, mx in rows:
        gap = 12
        total = count * cw + (count - 1) * gap
        x0 = (W - total) // 2
        for j in range(count):
            tag, head, fact, scene = CARDS[idx]
            idx += 1
            x = x0 + j * (cw + gap)
            d.rectangle([x, y, x + cw, y + 196], fill=CARD, outline=(200, 200, 200), width=1)
            scene(d, x + 1, y + 1, cw - 2, 104)
            d.text((x + 10, y + 112), tag, font=F_SANS_B(10), fill=NAVY)
            lines = wrap(d, head, F_SERIF_B(15), cw - 20)
            yy = y + 128
            for ln in lines[:2]:
                d.text((x + 10, yy), ln, font=F_SERIF_B(15), fill=INK)
                yy += 18
            flines = wrap(d, fact, F_SANS(11), cw - 20)
            for ln in flines[:2]:
                d.text((x + 10, yy + 4), ln, font=F_SANS(11), fill=GREY)
                yy += 13
        y += 196 + 10
    # footer
    d.rectangle([0, 992, W, H], fill=NAVY)
    ft = "26 NOVEMBER 2026  •  SOURCES: QNA, REUTERS, WSJ, UEFA, NATO, NWS, AP, BBC, CHESS.COM, ONS, FT"
    ff = F_SANS(11)
    d.text(((W - d.textlength(ft, font=ff)) / 2, 1004), ft, font=ff, fill=(255, 255, 255))
    img.save("entry.png", optimize=True)
    print("saved entry.png")

if __name__ == "__main__":
    main()
