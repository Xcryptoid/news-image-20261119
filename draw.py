#!/usr/bin/env python3
"""Draw 'THE WORLD TODAY' - a newspaper front page summing up the world
news of Thursday 19 November 2026. Output: entry.png, 1024x1024."""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BG = (247, 243, 234)      # newsprint off-white
INK = (18, 18, 18)
RED = (178, 34, 34)
GREY = (90, 90, 88)
RULE = (60, 60, 60)
BLUE = (28, 68, 128)
GOLD = (198, 142, 32)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
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
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, fnt, x, y, fill, spacing=4, align="left", box_w=None):
    """Draw lines of text; returns y just below the last line."""
    for ln in lines:
        if align == "center":
            lx = x + (box_w - draw.textlength(ln, font=fnt)) / 2
        else:
            lx = x
        draw.text((lx, y), ln, font=fnt, fill=fill)
        y += fnt.size + spacing
    return y


def hline(draw, x0, x1, y, fill=RULE, width=2):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


# ---------------------------------------------------------------- lead art
def lead_art(draw, x, y, w, h):
    """Shenzhen skyline at dusk with the three flags above three leaders."""
    sky = (38, 52, 96)
    draw.rectangle([x, y, x + w, y + h], fill=sky)
    # dusk gradient bands
    for i in range(5):
        yy = y + i * h // 5
        draw.rectangle([x, yy, x + w, yy + h // 5],
                       fill=(38 + i * 6, 52 + i * 5, 96 - i * 8))
    # sun
    draw.ellipse([x + w - 78, y + 14, x + w - 38, y + 54], fill=(240, 180, 60))
    # skyline silhouettes
    import random
    rnd = random.Random(7)
    bx = x + 6
    while bx < x + w - 10:
        bw = rnd.randint(26, 52)
        bh = rnd.randint(38, h - 78)
        draw.rectangle([bx, y + h - 34 - bh, bx + bw, y + h - 34],
                       fill=(16, 22, 44))
        for wy in range(y + h - 30 - bh, y + h - 40, 12):
            for wx in range(bx + 4, bx + bw - 4, 10):
                if rnd.random() < 0.55:
                    draw.rectangle([wx, wy, wx + 4, wy + 5],
                                   fill=(250, 210, 110))
        bx += bw + 4
    # ground
    draw.rectangle([x, y + h - 34, x + w, y + h], fill=(24, 26, 30))
    # three flag poles with recognisable flags: US, China, Russia
    fx = x + 26
    # US: red/white stripes + blue canton
    draw.line([(fx, y + 10), (fx, y + h - 34)], fill=(220, 220, 220), width=3)
    for s in range(4):
        draw.rectangle([fx, y + 10 + s * 4, fx + 34, y + 14 + s * 4],
                       fill=(178, 34, 34) if s % 2 == 0 else (255, 255, 255))
    draw.rectangle([fx, y + 10, fx + 15, y + 18], fill=(28, 48, 110))
    fx += 52
    # China: red field, small yellow stars
    draw.line([(fx, y + 10), (fx, y + h - 34)], fill=(220, 220, 220), width=3)
    draw.rectangle([fx, y + 10, fx + 34, y + 26], fill=(222, 32, 32))
    draw.ellipse([fx + 4, y + 13, fx + 10, y + 19], fill=(255, 220, 60))
    draw.ellipse([fx + 14, y + 12, fx + 18, y + 16], fill=(255, 220, 60))
    draw.ellipse([fx + 22, y + 15, fx + 26, y + 19], fill=(255, 220, 60))
    fx += 52
    # Russia: white-blue-red horizontal tricolour
    draw.line([(fx, y + 10), (fx, y + h - 34)], fill=(220, 220, 220), width=3)
    draw.rectangle([fx, y + 10, fx + 34, y + 15], fill=(255, 255, 255))
    draw.rectangle([fx, y + 15, fx + 34, y + 21], fill=(40, 90, 180))
    draw.rectangle([fx, y + 21, fx + 34, y + 26], fill=(200, 30, 30))
    # three leaders: simple suited figures
    px = x + w - 150
    for suit in [(64, 64, 72), (96, 96, 104), (48, 72, 110)]:
        draw.ellipse([px + 8, y + h - 96, px + 32, y + h - 72], fill=(214, 182, 150))
        draw.polygon([(px, y + h - 72), (px + 40, y + h - 72),
                      (px + 46, y + h - 34), (px - 6, y + h - 34)], fill=suit)
        draw.polygon([(px + 14, y + h - 72), (px + 26, y + h - 72),
                      (px + 20, y + h - 48)], fill=(240, 240, 240))
        px += 48


# ---------------------------------------------------------------- panel art
def art_icj(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(222, 226, 232))
    # courthouse: pediment + columns
    draw.polygon([(x + 8, y + 26), (x + w // 2, y + 6), (x + w - 8, y + 26)],
                 fill=(120, 110, 96))
    for cx in range(x + 22, x + w - 20, 30):
        draw.rectangle([cx, y + 30, cx + 12, y + h - 14], fill=(245, 242, 235))
    draw.rectangle([x + 10, y + h - 14, x + w - 10, y + h - 8], fill=(120, 110, 96))
    # scales of justice
    cx, cy = x + w // 2, y + h // 2 + 8
    draw.line([(cx, cy - 26), (cx, cy + 16)], fill=(60, 52, 40), width=3)
    draw.line([(cx - 26, cy - 20), (cx + 26, cy - 20)], fill=(60, 52, 40), width=3)
    draw.line([(cx - 26, cy - 20), (cx - 34, cy - 2)], fill=(60, 52, 40), width=2)
    draw.line([(cx - 26, cy - 20), (cx - 18, cy - 2)], fill=(60, 52, 40), width=2)
    draw.line([(cx + 26, cy - 20), (cx + 18, cy - 2)], fill=(60, 52, 40), width=2)
    draw.line([(cx + 26, cy - 20), (cx + 34, cy - 2)], fill=(60, 52, 40), width=2)
    draw.ellipse([cx - 38, cy - 4, cx - 14, cy + 6], fill=(198, 142, 32))
    draw.ellipse([cx + 14, cy - 4, cx + 38, cy + 6], fill=(198, 142, 32))


def art_bridge(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(168, 196, 222))
    # sea
    draw.rectangle([x, y + h - 26, x + w, y + h], fill=(52, 96, 150))
    # bridge deck, broken in the middle
    draw.rectangle([x + 4, y + 44, x + w // 2 - 14, y + 52], fill=(70, 70, 74))
    draw.rectangle([x + w // 2 + 14, y + 44, x + w - 4, y + 52], fill=(70, 70, 74))
    # arch + pylons
    draw.arc([x + 8, y + 8, x + w - 8, y + 66], 180, 360, fill=(70, 70, 74), width=4)
    draw.rectangle([x + 16, y + 20, x + 22, y + 46], fill=(70, 70, 74))
    draw.rectangle([x + w - 22, y + 20, x + w - 16, y + 46], fill=(70, 70, 74))
    # explosion at the break
    cx, cy = x + w // 2, y + 34
    for r, col in [(26, (255, 140, 40)), (18, (255, 190, 60)), (10, (255, 240, 150))]:
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
    draw.rectangle([x + w // 2 - 2, y + 52, x + w // 2 + 2, y + h - 26],
                   fill=(90, 90, 90))


def art_tower(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(232, 214, 176))
    # Riyadh tower: tall slab with stepped top
    tx = x + w // 2 - 26
    draw.rectangle([tx, y + 18, tx + 52, y + h - 8], fill=(90, 110, 140))
    draw.rectangle([tx - 6, y + 12, tx + 58, y + 20], fill=(70, 88, 116))
    for wy in range(y + 24, y + h - 12, 10):
        for wx in (tx + 6, tx + 24, tx + 42):
            draw.rectangle([wx, wy, wx + 6, wy + 5], fill=(200, 220, 240))
    # smoke + flame at the top
    draw.ellipse([tx + 8, y - 2, tx + 30, y + 16], fill=(90, 90, 90))
    draw.ellipse([tx + 26, y - 8, tx + 46, y + 8], fill=(120, 120, 120))
    draw.polygon([(tx + 18, y + 12), (tx + 26, y - 2), (tx + 34, y + 12)],
                 fill=(255, 120, 30))
    # small buildings
    draw.rectangle([x + 6, y + h - 34, x + 40, y + h - 8], fill=(120, 110, 96))
    draw.rectangle([x + w - 40, y + h - 28, x + w - 6, y + h - 8], fill=(120, 110, 96))


def art_tank(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(226, 208, 170))
    # dunes
    draw.polygon([(x, y + h - 22), (x + w // 3, y + h - 40),
                  (x + 2 * w // 3, y + h - 18), (x + w, y + h - 34),
                  (x + w, y + h), (x, y + h)], fill=(198, 172, 120))
    # tank
    tx, ty = x + w // 2 - 52, y + h - 58
    draw.rectangle([tx, ty + 18, tx + 104, ty + 38], fill=(74, 84, 52))
    draw.rectangle([tx + 22, ty, tx + 66, ty + 20], fill=(88, 98, 62))
    draw.line([(tx + 60, ty + 8), (tx + 100, ty + 2)], fill=(60, 68, 42), width=6)
    for wx in range(tx + 4, tx + 100, 14):
        draw.ellipse([wx, ty + 38, wx + 12, ty + 48], fill=(50, 56, 36))
    # ceasefire line
    draw.line([(x + 6, y + h - 62), (x + w - 6, y + h - 62)],
              fill=(178, 34, 34), width=2)
    draw.text((x + 8, y + h - 78), "CEASEFIRE LINE", font=font(SANS_B, 11),
              fill=(178, 34, 34))


def art_ipo(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(222, 234, 222))
    # bar chart rising
    bars = [18, 30, 26, 44, 58, 74]
    bw = (w - 24) // len(bars)
    for i, bh in enumerate(bars):
        bx = x + 12 + i * bw
        draw.rectangle([bx, y + h - 12 - bh, bx + bw - 6, y + h - 12],
                       fill=(28, 68, 128) if i < 5 else (198, 142, 32))
    # arrow
    pts = [(x + 14, y + h - 34), (x + w // 2, y + h - 66), (x + w - 18, y + 16)]
    draw.line(pts, fill=(178, 34, 34), width=5, joint="curve")
    draw.polygon([(x + w - 18, y + 10), (x + w - 18, y + 30),
                  (x + w - 2, y + 16)], fill=(178, 34, 34))
    draw.text((x + 10, y + 6), "$81 BILLION", font=font(SANS_B, 20), fill=(28, 68, 128))


def art_cyclone(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(196, 214, 232))
    # spiral
    cx, cy = x + w // 2, y + h // 2
    for a in range(0, 720, 6):
        r = 4 + a * 0.075
        px = cx + r * math.cos(math.radians(a))
        py = cy + r * math.sin(math.radians(a)) * 0.85
        col = (255, 255, 255) if a % 60 < 30 else (120, 150, 190)
        draw.ellipse([px - 3, py - 3, px + 3, py + 3], fill=col)
    # coastline at bottom
    draw.polygon([(x, y + h), (x, y + h - 16), (x + w // 3, y + h - 26),
                  (x + 2 * w // 3, y + h - 12), (x + w, y + h - 22),
                  (x + w, y + h)], fill=(120, 150, 110))
    draw.text((x + 8, y + 6), "90-100 km/h", font=font(SANS_B, 16), fill=(28, 68, 128))


# ---------------------------------------------------------------- page build
def build():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    M = 28  # margin

    # ---- masthead
    title_f = font(SERIF_B, 74)
    title = "THE WORLD TODAY"
    tw = d.textlength(title, font=title_f)
    d.text(((W - tw) / 2, 18), title, font=title_f, fill=INK)
    hline(d, M, W - M, 108, width=3)
    date_f = font(SANS_B, 26)
    date = "THURSDAY, 19 NOVEMBER 2026"
    dw = d.textlength(date, font=date_f)
    d.text(((W - dw) / 2, 118), date, font=date_f, fill=RED)
    hline(d, M, W - M, 156, width=2)

    # ---- lead story
    ly = 168
    lead_h = 268
    d.text((M, ly), "LEAD", font=font(SANS_B, 15), fill=RED)
    h_f = font(SERIF_B, 33)
    headline = "TRUMP, XI AND PUTIN MEET IN SHENZHEN"
    hl = wrap(d, headline, h_f, 610)
    y = ly + 20
    y = draw_lines(d, hl, h_f, M, y, INK, spacing=2)
    sub_f = font(SANS, 19)
    sub = ("First-ever three-way summit on the APEC sidelines: a joint "
           "declaration pledging dialogue on nuclear risks and stable "
           "energy flows.")
    sl = wrap(d, sub, sub_f, 590)
    y = draw_lines(d, sl, sub_f, M, y + 4, GREY, spacing=3)
    # lead art on the right
    ax, ay, aw, ah = 660, ly, W - M - 660, lead_h - 8
    lead_art(d, ax, ay, aw, ah)
    d.rectangle([ax, ay, ax + aw, ay + ah], outline=INK, width=2)
    d.text((ax + 8, ay + ah - 26), "SHENZHEN, CHINA", font=font(SANS_B, 14),
           fill=(255, 255, 255))
    hline(d, M, W - M, ly + lead_h + 6, width=2)

    # ---- 3x2 grid of panels
    gy = ly + lead_h + 18
    gw = (W - 2 * M - 2 * 16) // 3
    gh = 232
    panels = [
        ("WORLD COURT: MYANMAR GUILTY OF GENOCIDE",
         "ICJ rules 9-6 that Myanmar committed genocide against the "
         "Rohingya in 2017; about 10,000 killed.",
         art_icj, "THE HAGUE"),
        ("UKRAINE HITS CRIMEA BRIDGE AGAIN",
         "Third strike in a week on the Kerch Bridge; rail traffic halted.",
         art_bridge, "KERCH STRAIT"),
        ("HOUTHI STRIKE HITS RIYADH TOWER",
         "Attack damages the tower housing Saudi Arabia's sovereign "
         "wealth fund, the PIF.",
         art_tower, "RIYADH"),
        ("ISRAELI TANKS PUSH INTO CENTRAL GAZA",
         "Armour crosses the ceasefire line near Nuseirat despite the truce.",
         art_tank, "GAZA"),
        ("ANTHROPIC IPO SETS RECORD",
         "About $81 billion raised at $83 a share; trading starts today.",
         art_ipo, "NEW YORK"),
        ("CYCLONE AKVAN NEARS INDIA'S EAST COAST",
         "Landfall due Friday on the Andhra Pradesh-Odisha coast; "
         "winds 90-100 km/h.",
         art_cyclone, "BAY OF BENGAL"),
    ]
    for i, (head, sub, art, tag) in enumerate(panels):
        row, col = divmod(i, 3)
        px = M + col * (gw + 16)
        py = gy + row * (gh + 14)
        # art strip on top
        ah2 = 96
        art(d, px, py, gw, ah2)
        d.rectangle([px, py, px + gw, py + ah2], outline=INK, width=1)
        tag_f = font(SANS_B, 12)
        tw2 = d.textlength(tag, font=tag_f)
        d.rectangle([px + 3, py + ah2 - 21, px + 9 + tw2, py + ah2 - 3],
                    fill=(18, 18, 18))
        d.text((px + 6, py + ah2 - 20), tag, font=tag_f,
               fill=(255, 255, 255))
        ty = py + ah2 + 8
        hf = font(SANS_B, 19)
        hl2 = wrap(d, head, hf, gw - 4)
        ty = draw_lines(d, hl2[:2], hf, px + 2, ty, INK, spacing=1)
        sf = font(SANS, 15)
        sl2 = wrap(d, sub, sf, gw - 4)
        draw_lines(d, sl2[:3], sf, px + 2, ty + 2, GREY, spacing=2)

    # ---- footer
    fy = gy + 2 * gh + 14 + 8
    hline(d, M, W - M, fy, width=2)
    foot = "19 NOVEMBER 2026  —  THE WORLD IN ONE IMAGE"
    ff = font(SANS_B, 18)
    fw = d.textlength(foot, font=ff)
    d.text(((W - fw) / 2, fy + 10), foot, font=ff, fill=INK)

    return img


if __name__ == "__main__":
    img = build()
    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)
