#!/usr/bin/env python3
"""Render THE WORLD TODAY front page for Sunday 22 November 2026 (v2).

A 1024x1024 newspaper front page: masthead, date band, a six-box stats
strip, a lead-story hero with three portraits, three feature boxes, and
a numbered list of 36 dated stories across 9 regions, with a DATE CHECK
box proving every story is dated 22 November 2026.

Built with Pillow only. Fully deterministic: no timestamps, no random
numbers, no network. Running this file twice produces a byte-identical
entry.png.
"""

import os

from PIL import Image, ImageDraw, ImageFont

# ------------------------------------------------------------------ canvas
W, H = 1024, 1024
CREAM = (246, 242, 233)
INK = (20, 20, 20)
NAVY = (16, 28, 64)
GOLD = (212, 175, 55)
RED = (178, 34, 34)
RED_SOFT = (205, 92, 92)
GREEN = (34, 139, 34)
GRAY = (110, 110, 105)
GRAY_DARK = (70, 70, 68)
GRAY_LINE = (180, 175, 165)
SKIN = (240, 200, 160)
MARGIN = 28
COL_W = 309
COL_GAP = 20
COL_X = [MARGIN, MARGIN + COL_W + COL_GAP, MARGIN + 2 * (COL_W + COL_GAP)]

# ------------------------------------------------------------------ fonts
FONT_DIRS = [
    "/usr/share/fonts/truetype/liberation",
    "/usr/share/fonts/truetype/dejavu",
]


def load_font(basename, size):
    """Load a TTF by basename from the known font directories."""
    for folder in FONT_DIRS:
        path = os.path.join(folder, basename)
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default(size)


def serif_bold(size):
    return load_font("LiberationSerif-Bold.ttf", size)


def sans_bold(size):
    return load_font("LiberationSans-Bold.ttf", size)


def sans(size):
    return load_font("LiberationSans-Regular.ttf", size)


# ------------------------------------------------------------------ text
def wrap(draw, text, font, max_w):
    """Word-wrap text to fit max_w pixels; return a list of lines."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def centered(draw, cx, y, text, font, fill):
    """Draw text horizontally centered on cx at y."""
    w = draw.textlength(text, font=font)
    draw.text((cx - w / 2, y), text, font=font, fill=fill)


def right_aligned(draw, x, y, text, font, fill):
    """Draw text right-aligned so it ends at x."""
    w = draw.textlength(text, font=font)
    draw.text((x - w, y), text, font=font, fill=fill)


# ------------------------------------------------------------------ stories
# (number, headline, detail), grouped by column and region.
COLUMNS = [
    [
        ("CLIMATE", [
            (1, "COP31 nears a final deal",
             "Antalya package put to nations; vote 06:00 GMT"),
            (2, "Draft drops fossil-fuel phase-out",
             "130 nations pushed for it; producers resisted"),
        ]),
        ("THE GULF", [
            (3, "Iran hits Bahrain: site ablaze",
             "IRGC missiles, drones strike; fire, no injuries"),
            (4, "Bahrain defences intercept attacks",
             "Shrapnel causes damage; no casualties reported"),
            (5, "Houthi missile at Saudi Arabia",
             "Saudi coalition says it was intercepted"),
            (6, "Trump: Iran deal 'could last 20 years'",
             "US president floats a long-term agreement"),
            (7, "Iran internet bill targets privacy",
             "Accounts to be tied to real identities"),
        ]),
        ("ISRAEL & GAZA", [
            (8, "Eisenkot tasked to form government",
             "Herzog picks ex-army chief over Netanyahu"),
            (9, "Eisenkot open to Netanyahu joining",
             "Likud invited to coalition talks on Sunday"),
            (10, "Likud sets unity-govt conditions",
             "Keep security zones; no Palestinian state"),
            (11, "Gaza aid plea from four nations",
             "150,000 tents stuck at the border, floods bite"),
            (12, "Turkey intel chief meets Hamas",
             "Talks in Istanbul as Gaza ceasefire holds"),
        ]),
    ],
    [
        ("UKRAINE WAR", [
            (13, "Sparta II hit by drones in Baltic",
             "Russian ship ablaze, drifts into Finnish waters"),
            (14, "Russian helicopter 'breaches' Finland",
             "Airspace violated near Loviisa; NATO told"),
            (15, "Russia strikes Kryvyi Rih",
             "Missiles hit Zelenskyy's hometown again"),
            (16, "Kindergarten hit in Zaporizhzhya",
             "Russian forces strike the region, Kyiv says"),
            (17, "Melania Trump seeks more ceasefires",
             "Wants Russia-Ukraine truces before Christmas"),
        ]),
        ("EUROPE", [
            (18, "France: 4th weekend of protests",
             "Cost-of-living marches across the country"),
            (19, "Lisbon: thousands march on prices",
             "Portugal protest over inflation and rents"),
            (20, "EU hunts new ECB chief",
             "Search opens as Christine Lagarde resigns"),
            (21, "Blair: rejoin EU only if UK innovates",
             "Ex-PM sets a technology test for return"),
        ]),
        ("WASHINGTON & THE UN", [
            (22, "US details $12bn Venezuela revenue",
             "State Dept report on oil and mineral income"),
            (23, "Hegseth memo limits US-Canada ties",
             "Secret memo curbs defence cooperation"),
            (24, "Killer-robot talks run to 2028 deal",
             "UN states agree to keep negotiating the ban"),
        ]),
    ],
    [
        ("AFRICA", [
            (25, "Al-Shabaab claims ambush killings",
             "Group says hundreds of Somali troops dead"),
            (26, "Kenya's last Ebola patient out",
             "Kenya's last case out; DRC toll passes 5,300"),
            (27, "Ghana unveils Heritage banknotes",
             "Nkrumah and Kofi Annan honoured on cash"),
            (28, "Tigray's new mayor vows a vote",
             "Elections promised in six months after clashes"),
        ]),
        ("AFRICA & ASIA", [
            (29, "Sahel states reopen West Africa talks",
             "Dialogue restarts with the regional bloc"),
            (30, "DRC leader signs reform law",
             "Constitutional change amid high tensions"),
            (31, "Nigeria starts building naval ships",
             "Bid to cut reliance on foreign yards"),
            (32, "India-Canada end trade talks round",
             "Sixth round of CEPA negotiations closes"),
        ]),
        ("AMERICAS & SPORT", [
            (33, "US jails Nikhil Gupta: 235 months",
             "Murder-for-hire plot sentence handed down"),
            (34, "Bolsonaro in ICU in Brazil",
             "Ex-president admitted with bowel obstruction"),
            (35, "US airlines warned of terror threat",
             "Alert ahead of Thanksgiving travel surge"),
            (36, "ATP final today: Alcaraz v Zverev",
             "Turin title decider; Zverev seeks third crown"),
        ]),
    ],
]

STATS = [
    ("COP31 VOTE", "06:00 GMT", NAVY),
    ("BAHRAIN", "0 injured", RED),
    ("GAZA TENTS", "150,000", RED),
    ("SPARTA II", "16 safe", GREEN),
    ("EBOLA TOLL", "5,300+", RED),
    ("ATP FINAL", "Turin", NAVY),
]


# ------------------------------------------------------------------ pictures
def draw_portrait(draw, cx, top, hair, tie, name, title):
    """Draw a simple cartoon leader portrait: head, hair, suit, tie."""
    draw.polygon(
        [(cx - 38, top + 110), (cx + 38, top + 110),
         (cx + 30, top + 60), (cx - 30, top + 60)],
        fill=(24, 24, 30),
    )
    draw.polygon(
        [(cx - 10, top + 60), (cx + 10, top + 60), (cx, top + 80)],
        fill=(245, 245, 245),
    )
    draw.polygon(
        [(cx - 5, top + 64), (cx + 5, top + 64),
         (cx + 4, top + 90), (cx, top + 96), (cx - 4, top + 90)],
        fill=tie,
    )
    draw.ellipse(
        [cx - 27, top, cx + 27, top + 54],
        fill=SKIN, outline=(200, 160, 120),
    )
    draw.pieslice([cx - 27, top - 4, cx + 27, top + 26], 180, 360, fill=hair)
    draw.ellipse([cx - 14, top + 24, cx - 8, top + 28], fill=INK)
    draw.ellipse([cx + 8, top + 24, cx + 14, top + 28], fill=INK)
    centered(draw, cx, top + 116, name, sans_bold(14), (255, 255, 255))
    centered(draw, cx, top + 134, title, sans(10), (180, 180, 180))


def draw_flame(draw, cx, top):
    """Draw a simple flame icon for the Bahrain feature box."""
    draw.polygon(
        [(cx, top), (cx + 26, top + 34), (cx + 12, top + 30),
         (cx + 20, top + 52), (cx, top + 44), (cx - 20, top + 52),
         (cx - 12, top + 30), (cx - 26, top + 34)],
        fill=RED,
    )
    draw.polygon(
        [(cx, top + 22), (cx + 12, top + 44), (cx, top + 52),
         (cx - 12, top + 44)],
        fill=GOLD,
    )
    draw.rectangle([cx - 30, top + 56, cx + 30, top + 62], fill=INK)


def draw_ballot(draw, cx, top):
    """Draw a simple ballot-box icon for the Israel feature box."""
    draw.rectangle([cx - 34, top + 8, cx + 34, top + 52], fill=NAVY)
    draw.rectangle([cx - 40, top, cx + 40, top + 10], fill=INK)
    draw.rectangle([cx - 10, top + 2, cx + 10, top + 8], fill=CREAM)
    draw.rectangle([cx - 22, top - 26, cx + 22, top - 4],
                   outline=RED, width=3)
    draw.line([(cx - 16, top - 15), (cx - 4, top - 6),
               (cx + 16, top - 24)], fill=RED, width=3)


def draw_tennis(draw, cx, top):
    """Draw a simple tennis-ball icon for the sport feature box."""
    draw.ellipse([cx - 30, top, cx + 30, top + 60], fill=(200, 220, 60),
                 outline=INK, width=2)
    draw.arc([cx - 30, top + 4, cx - 2, top + 56], 270, 90,
             fill=(255, 255, 255), width=4)
    draw.arc([cx + 2, top + 4, cx + 30, top + 56], 90, 270,
             fill=(255, 255, 255), width=4)


# ------------------------------------------------------------------ render
def render():
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)

    # Top meta line and rule.
    draw.text((MARGIN, 8), "VOL. 2026 — No. 326", font=sans(11), fill=GRAY)
    right_aligned(draw, W - MARGIN, 8, "PRICE: ONE DAY'S NEWS", sans(11), GRAY)
    draw.line([(MARGIN, 28), (W - MARGIN, 28)], fill=INK, width=1)

    # Masthead.
    centered(draw, W // 2, 34, "THE WORLD TODAY", serif_bold(72), INK)
    draw.line([(MARGIN, 108), (W - MARGIN, 108)], fill=INK, width=2)

    # Date band (navy).
    draw.rectangle([MARGIN, 114, W - MARGIN, 154], fill=NAVY)
    draw.text((MARGIN + 20, 124), "SUNDAY • 22 NOVEMBER 2026",
              font=sans_bold(20), fill=(255, 255, 255))
    right_aligned(draw, W - MARGIN - 20, 128, "36 STORIES • 9 REGIONS",
                  sans_bold(16), GOLD)

    # Stats strip: six boxes.
    box_w, box_gap = 155, 7
    for i, (label, value, color) in enumerate(STATS):
        bx = MARGIN + i * (box_w + box_gap)
        draw.rectangle([bx, 160, bx + box_w, 206],
                       fill=(255, 255, 255), outline=GRAY_LINE)
        centered(draw, bx + box_w // 2, 165, label, sans(11), GRAY)
        centered(draw, bx + box_w // 2, 182, value, sans_bold(20), color)
    draw.line([(MARGIN, 212), (W - MARGIN, 212)], fill=RED, width=3)

    # Hero (navy).
    draw.rectangle([MARGIN, 218, W - MARGIN, 414], fill=NAVY)
    draw.text((MARGIN + 20, 230), "CLIMATE & CONFLICT — THE LEAD STORY",
              font=sans_bold(13), fill=GOLD)
    draw.text((MARGIN + 20, 250), "COP31 NEARS A DEAL —",
              font=serif_bold(38), fill=(255, 255, 255))
    draw.text((MARGIN + 20, 292), "AS IRAN HITS BAHRAIN",
              font=serif_bold(38), fill=(255, 255, 255))
    draw.text((MARGIN + 20, 340),
              "Antalya's overtime talks put a new package to 200 nations —",
              font=sans(15), fill=(255, 255, 255))
    draw.text((MARGIN + 20, 360),
              "hours after Iranian missiles set a Bahraini plant ablaze.",
              font=sans(15), fill=(255, 255, 255))
    w1 = draw.textlength("COP31 VOTE: 06:00 GMT  •  ", font=sans_bold(12))
    draw.text((MARGIN + 20, 388), "COP31 VOTE: 06:00 GMT  •  ",
              font=sans_bold(12), fill=RED_SOFT)
    draw.text((MARGIN + 20 + w1, 388), "BAHRAIN: FIRE, NO INJURIES",
              font=sans_bold(12), fill=GOLD)

    # Three portraits on the right of the hero.
    draw_portrait(draw, 735, 238, (40, 40, 40), RED, "KURUM", "COP31 president")
    draw_portrait(draw, 835, 238, (205, 205, 205), (40, 80, 160),
                  "EISENKOT", "Israel's PM-designate")
    draw_portrait(draw, 935, 238, (245, 215, 110), RED, "TRUMP", "US President")

    # Three feature boxes.
    feat_y, feat_h = 420, 172
    for i, fx in enumerate(COL_X):
        draw.rectangle([fx, feat_y, fx + COL_W, feat_y + feat_h],
                       fill=(255, 255, 255), outline=GRAY_LINE)

    # Feature 1: Bahrain.
    fx = COL_X[0]
    draw.text((fx + 14, 430), "GULF • ATTACK", font=sans_bold(12), fill=RED)
    for j, line in enumerate(wrap(draw, "Iran's missiles hit Bahrain",
                                  serif_bold(19), COL_W - 28)):
        draw.text((fx + 14, 448 + j * 22), line, font=serif_bold(19), fill=INK)
    draw_flame(draw, fx + COL_W // 2, 496)
    for j, line in enumerate(wrap(
            draw, "An industrial site burns; defences intercept the rest.",
            sans(12), COL_W - 28)):
        draw.text((fx + 14, 566 + j * 15), line, font=sans(12), fill=GRAY_DARK)

    # Feature 2: Israel.
    fx = COL_X[1]
    draw.text((fx + 14, 430), "ISRAEL • NEW GOVERNMENT", font=sans_bold(12), fill=RED)
    for j, line in enumerate(wrap(draw, "Eisenkot tasked to govern",
                                  serif_bold(19), COL_W - 28)):
        draw.text((fx + 14, 448 + j * 22), line, font=serif_bold(19), fill=INK)
    draw_ballot(draw, fx + COL_W // 2, 512)
    for j, line in enumerate(wrap(
            draw, "Herzog picks the ex-army chief over Netanyahu.",
            sans(12), COL_W - 28)):
        draw.text((fx + 14, 566 + j * 15), line, font=sans(12), fill=GRAY_DARK)

    # Feature 3: Sport.
    fx = COL_X[2]
    draw.text((fx + 14, 430), "SPORT • TURIN", font=sans_bold(12), fill=RED)
    for j, line in enumerate(wrap(draw, "Alcaraz v Zverev for the title",
                                  serif_bold(19), COL_W - 28)):
        draw.text((fx + 14, 448 + j * 22), line, font=serif_bold(19), fill=INK)
    draw_tennis(draw, fx + COL_W // 2, 500)
    for j, line in enumerate(wrap(
            draw, "ATP Finals decider today; Zverev chases a third crown.",
            sans(12), COL_W - 28)):
        draw.text((fx + 14, 566 + j * 15), line, font=sans(12), fill=GRAY_DARK)

    # "The day in 36 stories" heading, rule, and DATE CHECK box.
    draw.text((MARGIN, 600), "THE DAY IN 36 STORIES",
              font=serif_bold(22), fill=INK)
    dc_font = sans_bold(13)
    dc_a = "DATE CHECK: "
    dc_b = "ALL 36 STORIES DATED 22 NOV 2026"
    wa = draw.textlength(dc_a, font=dc_font)
    wb = draw.textlength(dc_b, font=dc_font)
    box_w = 12 + 26 + 8 + wa + wb + 12
    box_x0 = W - MARGIN - box_w
    draw.rectangle([box_x0, 596, W - MARGIN, 626],
                   fill=(255, 255, 255), outline=GOLD, width=2)
    cx = box_x0 + 12
    cy = 611
    draw.line([(cx, cy), (cx + 7, cy + 7), (cx + 20, cy - 8)], fill=RED, width=3)
    tx = box_x0 + 12 + 26 + 8
    draw.text((tx, 604), dc_a, font=dc_font, fill=RED)
    draw.text((tx + wa, 604), dc_b, font=dc_font, fill=INK)
    draw.line([(MARGIN, 630), (W - MARGIN, 630)], fill=INK, width=2)

    # Numbered story columns.
    num_font = sans_bold(12)
    head_font = sans_bold(12)
    det_font = sans(10)
    for col_i, groups in enumerate(COLUMNS):
        x = COL_X[col_i]
        y = 640
        for region, stories in groups:
            draw.text((x, y), region, font=sans_bold(13), fill=RED)
            y += 16
            for number, headline, detail in stories:
                draw.text((x, y), "%02d" % number, font=num_font, fill=INK)
                for j, line in enumerate(wrap(draw, headline, head_font, COL_W - 22)):
                    draw.text((x + 22, y + j * 13), line, font=head_font, fill=INK)
                for j, line in enumerate(wrap(draw, detail, det_font, COL_W - 22)):
                    draw.text((x + 22, y + 11 + j * 12), line, font=det_font, fill=GRAY_DARK)
                y += 22

    # Sport strip.
    draw.line([(MARGIN, 968), (W - MARGIN, 968)], fill=GRAY_LINE, width=1)
    draw.text((MARGIN, 974),
              "SPORT IN BRIEF: Bournemouth beat Forest • France reach rugby final v South Africa • Australia beat Wales",
              font=sans(11), fill=GRAY_DARK)

    # Footer.
    centered(draw, W // 2, 1000,
             "THE WORLD TODAY • SUNDAY 22 NOVEMBER 2026 • Sources: Reuters, AP, Al Jazeera, AFP, UN",
             sans(11), GRAY)
    return img


def main():
    img = render()
    img.save("entry.png")
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
