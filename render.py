#!/usr/bin/env python3
"""Render 'THE WORLD IN ONE DAY — Sunday, 22 November 2026' front page.
1024x1024 PNG, deterministic (no timestamps, fixed drawing order).
Build-machine only; the entry itself (main.ts) just copies entry.png.
Determinism: PIL writes no timestamps into the PNG, and every draw call is
in a fixed order, so two runs are byte-identical (verified by sha256).
"""
from PIL import Image, ImageDraw, ImageFont
import textwrap, os

W = H = 1024
PAPER = (248, 244, 232)
INK = (26, 26, 26)
RED = (164, 30, 34)
BLUE = (31, 78, 121)
GOLD = (180, 140, 30)
GRAY = (110, 105, 95)
LIGHT = (235, 229, 214)
SKY = (38, 52, 84)
SEA = (52, 96, 128)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

def font(path, size):
    return ImageFont.truetype(path, size)

def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def draw_lines(draw, lines, fnt, x, y, fill, leading):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y

def fit_block(draw, text, fnt_path, start_size, max_w, max_h, min_size=12):
    """Largest font size (<= start) whose wrapped text fits max_w x max_h."""
    size = start_size
    while size >= min_size:
        fnt = font(fnt_path, size)
        lines = wrap(draw, text, fnt, max_w)
        lh = int(size * 1.28)
        if len(lines) * lh <= max_h:
            return fnt, lines, lh
        size -= 1
    fnt = font(fnt_path, min_size)
    lines = wrap(draw, text, fnt, max_w)
    return fnt, lines, int(min_size * 1.28)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ---- frame ----
d.rectangle([14, 14, W-15, H-15], outline=INK, width=3)

# ---- masthead ----
f_mast = font(SERIF_B, 58)
mast = "THE WORLD IN ONE DAY"
mw = d.textlength(mast, font=f_mast)
d.text(((W-mw)/2, 30), mast, font=f_mast, fill=INK)
d.line([36, 104, W-36, 104], fill=INK, width=3)
d.line([36, 110, W-36, 110], fill=INK, width=1)

# ---- dateline bar ----
f_date = font(SANS_B, 20)
d.text((36, 122), "SUNDAY, 22 NOVEMBER 2026", font=f_date, fill=RED)
right = "FIVE STORIES  ·  ONE DAY"
rw = d.textlength(right, font=f_date)
d.text((W-36-rw, 122), right, font=f_date, fill=INK)
d.line([36, 152, W-36, 152], fill=INK, width=2)

# ================= LEAD STORY =================
# panel y 166..468
d.rectangle([36, 166, W-36, 468], outline=INK, width=2)
# lead icon box (right): night sky + bridge + blasts
ix0, iy0, ix1, iy1 = 668, 182, 972, 452
d.rectangle([ix0, iy0, ix1, iy1], fill=SKY)
# stars
for (sx, sy) in [(700, 200), (760, 230), (830, 195), (900, 225), (950, 200),
                 (720, 260), (880, 260), (800, 250), (940, 280), (690, 300)]:
    d.ellipse([sx-2, sy-2, sx+2, sy+2], fill=(255, 255, 220))
# moon
d.ellipse([900, 195, 934, 229], fill=(245, 240, 210))
# river
d.rectangle([ix0, 400, ix1, iy1], fill=(24, 38, 66))
# bridge deck + towers
d.line([ix0, 380, ix1, 380], fill=(200, 200, 200), width=6)
for tx in (720, 820, 920):
    d.line([tx, 300, tx, 400], fill=(220, 220, 220), width=8)
    d.polygon([(tx-14, 300), (tx+14, 300), (tx, 272)], fill=(220, 220, 220))
# suspension arcs
for cx0, cx1 in ((668, 720), (720, 820), (820, 920), (920, 972)):
    pts = []
    for i in range(21):
        t = i / 20
        x = cx0 + (cx1 - cx0) * t
        y = 380 - 46 * 4 * t * (1 - t)
        pts.append((x, y))
    d.line(pts, fill=(200, 200, 200), width=3)
# explosion bursts (orange starbursts over the bridge)
def burst(cx, cy, r, col):
    pts = []
    for i in range(16):
        ang = 3.14159 * i / 8
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * 0.95 ** 0 * __import__("math").cos(ang),
                    cy + rr * __import__("math").sin(ang)))
    d.polygon(pts, fill=col)
burst(770, 330, 34, (255, 170, 40))
burst(770, 330, 20, (255, 220, 90))
burst(880, 310, 26, (255, 150, 30))
burst(880, 310, 14, (255, 210, 80))
burst(700, 350, 18, (255, 150, 30))
# smoke
for (sx, sy, sr) in [(770, 300, 16), (800, 285, 12), (880, 280, 14), (905, 265, 10)]:
    d.ellipse([sx-sr, sy-sr, sx+sr, sy+sr], fill=(120, 120, 130))
burst(770, 330, 34, (255, 170, 40))
burst(880, 310, 26, (255, 150, 30))

# lead text (left column)
lx, lw = 56, 592
y = 182
f_kick = font(SANS_B, 19)
d.text((lx, y), "UKRAINE  ·  WAR IN EUROPE", font=f_kick, fill=RED)
y += 32
f_head, lines, lh = fit_block(d, "RUSSIA'S 500-WEAPON NIGHT OVER KYIV",
                              SERIF_B, 40, lw, 110)
y = draw_lines(d, lines, f_head, lx, y, INK, lh)
y += 8
body = ("Moscow fired 27 ballistic missiles, 84 cruise missiles and 404 drones "
        "at Ukraine overnight — one of the largest barrages of the war. Three "
        "bridges over the Dnipro were hit, at least nine people were killed, "
        "and Russian weapons came down in Poland. Hours later a missile strike "
        "on Kryvyi Rih, President Zelenskyy's hometown, killed two more and "
        "wounded 60.")
f_body, blines, blh = fit_block(d, body, SANS, 19, lw, 150)
draw_lines(d, blines, f_body, lx, y, INK, blh)

# ================= 2x2 GRID =================
panels = [
    # (x0, y0, kicker, headline, body, icon)
    (36, 486, "THE BALTIC SEA", "DRONE HIT SETS RUSSIAN SHIP ABLAZE",
     "The sanctioned cargo vessel Sparta II, bound for Kaliningrad, was struck "
     "by two drones in the Gulf of Finland and drifted burning into Finnish "
     "waters. Her 16 crew were evacuated. Finland says Ukraine was likely "
     "behind the attack.", "ship"),
    (520, 486, "SOUTH AMERICA", "6.9 QUAKE SHAKES PERU'S ANDES",
     "A magnitude 6.9 earthquake struck near Junín on Friday evening, shaking "
     "the capital Lima and sending residents into the streets. Peru's "
     "geophysics institute reported no damage or casualties.", "quake"),
    (36, 742, "CLIMATE  ·  COP31", "FOSSIL-FUEL FIGHT DEADLOCKS COP31",
     "Climate talks stalled as negotiators fought over fossil fuels, with the "
     "draft text dropping any phase-out language and discussions spilling into "
     "overtime.", "climate"),
    (520, 742, "EUROPE  ·  ESPIONAGE", "DENMARK EXPELS RUSSIAN DIPLOMAT OVER 'ASSASSINATION PLOT'",
     "Copenhagen accused Russian intelligence of plotting to kill "
     "Ukrainian-American rapper Kyivstoner at a concert near the capital. Two "
     "men face attempted-murder charges; Moscow denies the claim.", "denmark"),
]
PW, PH = 468, 234

def draw_ship(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=SEA)
    # hull
    d.polygon([(x0+8, y1-58), (x1-8, y1-58), (x1-26, y1-18), (x0+26, y1-18)],
              fill=(60, 60, 70))
    # containers
    d.rectangle([x0+22, y1-92, x0+52, y1-58], fill=(200, 60, 40))
    d.rectangle([x0+56, y1-92, x0+86, y1-58], fill=(40, 120, 80))
    d.rectangle([x0+90, y1-92, x0+120, y1-58], fill=(220, 170, 40))
    # bridge tower
    d.rectangle([x1-58, y1-108, x1-30, y1-58], fill=(230, 230, 230))
    # flames
    for (fx, fy, fr) in [(x0+40, y1-104, 16), (x0+75, y1-112, 20), (x0+108, y1-104, 14)]:
        burst(fx, fy, fr, (255, 170, 40))
        burst(fx, fy, fr*0.55, (255, 220, 90))
    # waves
    for wy in (y1-10, y1-4):
        d.line([(x0+4, wy), (x1-4, wy)], fill=(220, 235, 240), width=2)

def draw_quake(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(238, 228, 205))
    # mountains
    d.polygon([(x0+6, y1-10), (x0+60, y0+40), (x0+110, y1-10)], fill=(120, 100, 80))
    d.polygon([(x0+55, y1-10), (x0+115, y0+70), (x0+150, y1-10)], fill=(90, 78, 64))
    # snow caps
    d.polygon([(x0+48, y0+52), (x0+60, y0+40), (x0+72, y0+52), (x0+66, y0+58),
               (x0+60, y0+54), (x0+54, y0+58)], fill=(255, 255, 255))
    # crack
    pts = [(x0+20, y0+16), (x0+45, y0+45), (x0+30, y0+75), (x0+60, y0+105),
           (x0+45, y0+135), (x0+70, y0+165), (x0+55, y1-12)]
    d.line(pts, fill=RED, width=5)
    # seismograph line
    pts = [(x0+10, y0+150)]
    import math
    for i in range(1, 14):
        px = x0 + 10 + i * 10
        py = y0 + 150 + (18 if i % 3 == 0 else -14 if i % 3 == 1 else 6)
        pts.append((px, py))
    d.line(pts, fill=INK, width=2)

def draw_climate(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(214, 232, 222))
    cx, cy, r = (x0+x1)//2, (y0+y1)//2 - 6, 62
    d.ellipse([cx-r, cy-r, cx+r, cy+r], fill=(70, 130, 180))
    d.ellipse([cx-r+18, cy-r+22, cx-r+58, cy-r+52], fill=(90, 170, 90))
    d.ellipse([cx+8, cy+6, cx+52, cy+38], fill=(90, 170, 90))
    d.ellipse([cx-r+6, cy+r-30, cx-r+40, cy+r-8], fill=(90, 170, 90))
    # factory in front
    fx0 = x0 + 12
    d.rectangle([fx0, y1-52, fx0+52, y1-8], fill=(70, 70, 78))
    d.rectangle([fx0+56, y1-40, fx0+96, y1-8], fill=(90, 90, 98))
    d.rectangle([fx0+18, y1-84, fx0+30, y1-52], fill=(70, 70, 78))
    for (sx, sy, sr) in [(fx0+24, y1-96, 10), (fx0+36, y1-108, 13), (fx0+52, y1-120, 10)]:
        d.ellipse([sx-sr, sy-sr, sx+sr, sy+sr], fill=(150, 150, 155))
    # red X over smoke = phase-out dropped
    d.line([x1-46, y0+14, x1-16, y0+44], fill=RED, width=6)
    d.line([x1-16, y0+14, x1-46, y0+44], fill=RED, width=6)

def draw_denmark(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(232, 226, 214))
    cx, cy = (x0+x1)//2, (y0+y1)//2 - 8
    # target rings
    for rr, col in ((58, RED), (44, PAPER), (30, RED), (16, PAPER)):
        d.ellipse([cx-rr, cy-rr, cx+rr, cy+rr], outline=col, width=5)
    d.ellipse([cx-6, cy-6, cx+6, cy+6], fill=RED)
    # microphone
    mx = x0 + 26
    d.rounded_rectangle([mx, cy-52, mx+26, cy+2], radius=13, fill=(50, 50, 58))
    d.line([(mx+13, cy+2), (mx+13, cy+34)], fill=(50, 50, 58), width=5)
    d.arc([mx-8, cy+22, mx+34, cy+52], 0, 180, fill=(50, 50, 58), width=4)
    # stand base
    d.line([(mx-12, y1-14), (mx+38, y1-14)], fill=(50, 50, 58), width=4)

ICONS = {"ship": draw_ship, "quake": draw_quake,
         "climate": draw_climate, "denmark": draw_denmark}

for (px0, py0, kicker, headline, body, icon) in panels:
    px1, py1 = px0 + PW, py0 + PH
    d.rectangle([px0, py0, px1, py1], outline=INK, width=2)
    # icon box right
    ix0, iy0, ix1, iy1 = px1 - 168, py0 + 10, px1 - 10, py1 - 10
    ICONS[icon](d, ix0, iy0, ix1, iy1)
    d.rectangle([ix0, iy0, ix1, iy1], outline=INK, width=1)
    tx, tw = px0 + 16, PW - 16 - 176
    y = py0 + 14
    f_k = font(SANS_B, 15)
    d.text((tx, y), kicker, font=f_k, fill=RED)
    y += 26
    f_h, hlines, hlh = fit_block(d, headline, SERIF_B, 25, tw, 62)
    y = draw_lines(d, hlines, f_h, tx, y, INK, hlh)
    y += 6
    f_b, blines, blh = fit_block(d, body, SANS, 15, tw, 130)
    draw_lines(d, blines, f_b, tx, y, INK, blh)

# ---- footer sources ----
d.line([36, 984, W-36, 984], fill=INK, width=1)
f_src = font(SANS, 12)
src = ("Sources: Institute for the Study of War · Kyiv Independent · Reuters · "
       "CNN · USGS · AP · BBC — 22 November 2026")
sw = d.textlength(src, font=f_src)
d.text(((W-sw)/2, 990), src, font=f_src, fill=GRAY)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
img.save(out, format="PNG", optimize=True)
print("wrote", out, os.path.getsize(out), "bytes")
