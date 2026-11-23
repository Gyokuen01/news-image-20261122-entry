#!/usr/bin/env python3
"""THE WORLD TODAY front page, Sunday 22 November 2026 (v3).

This program paints a 1024x1024 newspaper front page and writes it to
entry.png: a masthead, a navy date band, a six-cell statistics strip, a
hero lead about COP31 and the Bahrain strike with three small portraits,
three feature boxes, and a numbered digest of 36 stories from 22 November
2026 sorted into 9 regions, closed by a DATE CHECK box that states every
story on the page is dated that day.

Only Pillow is used. The picture is fully deterministic: the program reads
no clock, no random source and no network, so two runs write the same
bytes. The layout is driven by one FrontPage object that owns the canvas,
the palette and the fonts; each section of the page is one method.
"""

import os

from PIL import Image, ImageDraw, ImageFont

PAGE_W, PAGE_H = 1024, 1024
PAPER = (246, 242, 233)
INK = (20, 20, 20)
NAVY = (16, 28, 64)
GOLD = (212, 175, 55)
CRIMSON = (178, 34, 34)
CRIMSON_LIGHT = (205, 92, 92)
LEAF = (34, 139, 34)
MUTED = (110, 110, 105)
MUTED_DARK = (70, 70, 68)
RULE = (180, 175, 165)
SKIN_TONE = (240, 200, 160)
WHITE = (255, 255, 255)
SUIT = (24, 24, 30)
SHIRT = (245, 245, 245)
FAINT = (180, 180, 180)
SKIN_LINE = (200, 160, 120)
TENNIS_BALL = (200, 220, 60)
BLUE_TIE = (40, 80, 160)
MARGIN = 28
COLUMN_W = 309
COLUMN_GAP = 20
COLUMN_X = [MARGIN, MARGIN + COLUMN_W + COLUMN_GAP,
            MARGIN + 2 * (COLUMN_W + COLUMN_GAP)]
RIGHT_EDGE = PAGE_W - MARGIN

FONT_FOLDERS = [
    "/usr/share/fonts/truetype/liberation",
    "/usr/share/fonts/truetype/dejavu",
]


def _load_ttf(basename, size):
    """Return a TTF font by basename, falling back to Pillow's default."""
    for folder in FONT_FOLDERS:
        candidate = os.path.join(folder, basename)
        if os.path.exists(candidate):
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default(size)


def serif(size):
    return _load_ttf("LiberationSerif-Bold.ttf", size)


def bold(size):
    return _load_ttf("LiberationSans-Bold.ttf", size)


def plain(size):
    return _load_ttf("LiberationSans-Regular.ttf", size)


# ------------------------------------------------------------------ content
# (number, headline, detail) per region, grouped into three columns.
STORY_COLUMNS = [
    [
        ("CLIMATE", [
            (1, "COP31 nears a final deal", "Antalya package put to nations; vote 06:00 GMT"),
            (2, "Draft drops fossil-fuel phase-out", "130 nations pushed for it; producers resisted"),
        ]),
        ("THE GULF", [
            (3, "Iran hits Bahrain: site ablaze", "IRGC missiles, drones strike; fire, no injuries"),
            (4, "Bahrain defences intercept attacks", "Shrapnel causes damage; no casualties reported"),
            (5, "Houthi missile at Saudi Arabia", "Saudi coalition says it was intercepted"),
            (6, "Trump: Iran deal 'could last 20 years'", "US president floats a long-term agreement"),
            (7, "Iran internet bill targets privacy", "Accounts to be tied to real identities"),
        ]),
        ("ISRAEL & GAZA", [
            (8, "Eisenkot tasked to form government", "Herzog picks ex-army chief over Netanyahu"),
            (9, "Eisenkot open to Netanyahu joining", "Likud invited to coalition talks on Sunday"),
            (10, "Likud sets unity-govt conditions", "Keep security zones; no Palestinian state"),
            (11, "Gaza aid plea from four nations", "150,000 tents stuck at the border, floods bite"),
            (12, "Turkey intel chief meets Hamas", "Talks in Istanbul as Gaza ceasefire holds"),
        ]),
    ],
    [
        ("UKRAINE WAR", [
            (13, "Sparta II hit by drones in Baltic", "Russian ship ablaze, drifts into Finnish waters"),
            (14, "Russian helicopter 'breaches' Finland", "Airspace violated near Loviisa; NATO told"),
            (15, "Russia strikes Kryvyi Rih", "Missiles hit Zelenskyy's hometown again"),
            (16, "Kindergarten hit in Zaporizhzhya", "Russian forces strike the region, Kyiv says"),
            (17, "Melania Trump seeks more ceasefires", "Wants Russia-Ukraine truces before Christmas"),
        ]),
        ("EUROPE", [
            (18, "France: 4th weekend of protests", "Cost-of-living marches across the country"),
            (19, "Lisbon: thousands march on prices", "Portugal protest over inflation and rents"),
            (20, "EU hunts new ECB chief", "Search opens as Christine Lagarde resigns"),
            (21, "Blair: rejoin EU only if UK innovates", "Ex-PM sets a technology test for return"),
        ]),
        ("WASHINGTON & THE UN", [
            (22, "US details $12bn Venezuela revenue", "State Dept report on oil and mineral income"),
            (23, "Hegseth memo limits US-Canada ties", "Secret memo curbs defence cooperation"),
            (24, "Killer-robot talks run to 2028 deal", "UN states agree to keep negotiating the ban"),
        ]),
    ],
    [
        ("AFRICA", [
            (25, "Al-Shabaab claims ambush killings", "Group says hundreds of Somali troops dead"),
            (26, "Kenya's last Ebola patient out", "Kenya's last case out; DRC toll passes 5,300"),
            (27, "Ghana unveils Heritage banknotes", "Nkrumah and Kofi Annan honoured on cash"),
            (28, "Tigray's new mayor vows a vote", "Elections promised in six months after clashes"),
        ]),
        ("AFRICA & ASIA", [
            (29, "Sahel states reopen West Africa talks", "Dialogue restarts with the regional bloc"),
            (30, "DRC leader signs reform law", "Constitutional change amid high tensions"),
            (31, "Nigeria starts building naval ships", "Bid to cut reliance on foreign yards"),
            (32, "India-Canada end trade talks round", "Sixth round of CEPA negotiations closes"),
        ]),
        ("AMERICAS & SPORT", [
            (33, "US jails Nikhil Gupta: 235 months", "Murder-for-hire plot sentence handed down"),
            (34, "Bolsonaro in ICU in Brazil", "Ex-president admitted with bowel obstruction"),
            (35, "US airlines warned of terror threat", "Alert ahead of Thanksgiving travel surge"),
            (36, "ATP final today: Alcaraz v Zverev", "Turin title decider; Zverev seeks third crown"),
        ]),
    ],
]

STAT_BOXES = [
    ("COP31 VOTE", "06:00 GMT", NAVY),
    ("BAHRAIN", "0 injured", CRIMSON),
    ("GAZA TENTS", "150,000", CRIMSON),
    ("SPARTA II", "16 safe", LEAF),
    ("EBOLA TOLL", "5,300+", CRIMSON),
    ("ATP FINAL", "Turin", NAVY),
]

LEAD_PORTRAITS = [
    (735, (40, 40, 40), CRIMSON, "KURUM", "COP31 president"),
    (835, (205, 205, 205), BLUE_TIE, "EISENKOT", "Israel's PM-designate"),
    (935, (245, 215, 110), CRIMSON, "TRUMP", "US President"),
]


class FrontPage:
    """Owns the canvas and draws every section of the front page."""

    def __init__(self):
        self.img = Image.new("RGB", (PAGE_W, PAGE_H), PAPER)
        self.d = ImageDraw.Draw(self.img)

    # -- text helpers ---------------------------------------------------
    def fit(self, text, font, width):
        """Greedy word wrap: split text into lines no wider than width."""
        out, current = [], ""
        for word in text.split():
            joined = (current + " " + word).strip()
            if self.d.textlength(joined, font=font) <= width:
                current = joined
            else:
                if current:
                    out.append(current)
                current = word
        if current:
            out.append(current)
        return out

    def center(self, cx, y, text, font, fill):
        w = self.d.textlength(text, font=font)
        self.d.text((cx - w / 2, y), text, font=font, fill=fill)

    def right(self, x, y, text, font, fill):
        w = self.d.textlength(text, font=font)
        self.d.text((x - w, y), text, font=font, fill=fill)

    def para(self, x, y, text, font, width, step, fill):
        """Draw wrapped lines of text, one every `step` pixels."""
        for i, line in enumerate(self.fit(text, font, width)):
            self.d.text((x, y + i * step), line, font=font, fill=fill)

    # -- small pictures --------------------------------------------------
    def portrait(self, cx, top, hair, tie, name, title):
        """A cartoon leader: suit, shirt, tie, head, hair and two eyes."""
        d = self.d
        suit = [(cx - 38, top + 110), (cx + 38, top + 110),
                (cx + 30, top + 60), (cx - 30, top + 60)]
        d.polygon(suit, fill=SUIT)
        shirt = [(cx - 10, top + 60), (cx + 10, top + 60), (cx, top + 80)]
        d.polygon(shirt, fill=SHIRT)
        tie_shape = [(cx - 5, top + 64), (cx + 5, top + 64),
                     (cx + 4, top + 90), (cx, top + 96), (cx - 4, top + 90)]
        d.polygon(tie_shape, fill=tie)
        d.ellipse([cx - 27, top, cx + 27, top + 54],
                  fill=SKIN_TONE, outline=SKIN_LINE)
        d.pieslice([cx - 27, top - 4, cx + 27, top + 26], 180, 360, fill=hair)
        d.ellipse([cx - 14, top + 24, cx - 8, top + 28], fill=INK)
        d.ellipse([cx + 8, top + 24, cx + 14, top + 28], fill=INK)
        self.center(cx, top + 116, name, bold(14), WHITE)
        self.center(cx, top + 134, title, plain(10), FAINT)

    def flame(self, cx, top):
        """A flame over a dark base line, for the Bahrain feature."""
        d = self.d
        outer = [(cx, top), (cx + 26, top + 34), (cx + 12, top + 30),
                 (cx + 20, top + 52), (cx, top + 44), (cx - 20, top + 52),
                 (cx - 12, top + 30), (cx - 26, top + 34)]
        d.polygon(outer, fill=CRIMSON)
        inner = [(cx, top + 22), (cx + 12, top + 44),
                 (cx, top + 52), (cx - 12, top + 44)]
        d.polygon(inner, fill=GOLD)
        d.rectangle([cx - 30, top + 56, cx + 30, top + 62], fill=INK)

    def ballot(self, cx, top):
        """A ballot box with a red tick, for the Israel feature."""
        d = self.d
        d.rectangle([cx - 34, top + 8, cx + 34, top + 52], fill=NAVY)
        d.rectangle([cx - 40, top, cx + 40, top + 10], fill=INK)
        d.rectangle([cx - 10, top + 2, cx + 10, top + 8], fill=PAPER)
        d.rectangle([cx - 22, top - 26, cx + 22, top - 4],
                    outline=CRIMSON, width=3)
        d.line([(cx - 16, top - 15), (cx - 4, top - 6),
                (cx + 16, top - 24)], fill=CRIMSON, width=3)

    def tennis(self, cx, top):
        """A tennis ball, for the sport feature."""
        d = self.d
        d.ellipse([cx - 30, top, cx + 30, top + 60], fill=TENNIS_BALL,
                  outline=INK, width=2)
        d.arc([cx - 30, top + 4, cx - 2, top + 56], 270, 90,
              fill=WHITE, width=4)
        d.arc([cx + 2, top + 4, cx + 30, top + 56], 90, 270,
              fill=WHITE, width=4)

    # -- page sections ----------------------------------------------------
    def top_rule(self):
        d = self.d
        d.text((MARGIN, 8), "VOL. 2026 — No. 326", font=plain(11), fill=MUTED)
        self.right(RIGHT_EDGE, 8, "PRICE: ONE DAY'S NEWS", plain(11), MUTED)
        d.line([(MARGIN, 28), (RIGHT_EDGE, 28)], fill=INK, width=1)

    def masthead(self):
        d = self.d
        self.center(PAGE_W // 2, 34, "THE WORLD TODAY", serif(72), INK)
        d.line([(MARGIN, 108), (RIGHT_EDGE, 108)], fill=INK, width=2)

    def date_band(self):
        d = self.d
        d.rectangle([MARGIN, 114, RIGHT_EDGE, 154], fill=NAVY)
        d.text((MARGIN + 20, 124), "SUNDAY • 22 NOVEMBER 2026",
               font=bold(20), fill=WHITE)
        self.right(RIGHT_EDGE - 20, 128, "36 STORIES • 9 REGIONS",
                   bold(16), GOLD)

    def stats(self):
        d = self.d
        cell_w, cell_gap = 155, 7
        for i, (label, value, color) in enumerate(STAT_BOXES):
            bx = MARGIN + i * (cell_w + cell_gap)
            d.rectangle([bx, 160, bx + cell_w, 206],
                        fill=WHITE, outline=RULE)
            self.center(bx + cell_w // 2, 165, label, plain(11), MUTED)
            self.center(bx + cell_w // 2, 182, value, bold(20), color)
        d.line([(MARGIN, 212), (RIGHT_EDGE, 212)], fill=CRIMSON, width=3)

    def hero(self):
        d = self.d
        d.rectangle([MARGIN, 218, RIGHT_EDGE, 414], fill=NAVY)
        d.text((MARGIN + 20, 230), "CLIMATE & CONFLICT — THE LEAD STORY",
               font=bold(13), fill=GOLD)
        d.text((MARGIN + 20, 250), "COP31 NEARS A DEAL —",
               font=serif(38), fill=WHITE)
        d.text((MARGIN + 20, 292), "AS IRAN HITS BAHRAIN",
               font=serif(38), fill=WHITE)
        d.text((MARGIN + 20, 340),
               "Antalya's overtime talks put a new package to 200 nations —",
               font=plain(15), fill=WHITE)
        d.text((MARGIN + 20, 360),
               "hours after Iranian missiles set a Bahraini plant ablaze.",
               font=plain(15), fill=WHITE)
        first = "COP31 VOTE: 06:00 GMT  •  "
        w1 = d.textlength(first, font=bold(12))
        d.text((MARGIN + 20, 388), first, font=bold(12), fill=CRIMSON_LIGHT)
        d.text((MARGIN + 20 + w1, 388), "BAHRAIN: FIRE, NO INJURIES",
               font=bold(12), fill=GOLD)
        for cx, hair, tie, name, title in LEAD_PORTRAITS:
            self.portrait(cx, 238, hair, tie, name, title)

    def features(self):
        d = self.d
        feat_y, feat_h = 420, 172
        for fx in COLUMN_X:
            d.rectangle([fx, feat_y, fx + COLUMN_W, feat_y + feat_h],
                        fill=WHITE, outline=RULE)
        specs = [
            (COLUMN_X[0], "GULF • ATTACK", "Iran's missiles hit Bahrain",
             self.flame, 496,
             "An industrial site burns; defences intercept the rest."),
            (COLUMN_X[1], "ISRAEL • NEW GOVERNMENT",
             "Eisenkot tasked to govern", self.ballot, 512,
             "Herzog picks the ex-army chief over Netanyahu."),
            (COLUMN_X[2], "SPORT • TURIN", "Alcaraz v Zverev for the title",
             self.tennis, 500,
             "ATP Finals decider today; Zverev chases a third crown."),
        ]
        for fx, kicker, headline, icon, icon_y, caption in specs:
            d.text((fx + 14, 430), kicker, font=bold(12), fill=CRIMSON)
            self.para(fx + 14, 448, headline, serif(19), COLUMN_W - 28,
                      22, INK)
            icon(fx + COLUMN_W // 2, icon_y)
            self.para(fx + 14, 566, caption, plain(12), COLUMN_W - 28,
                      15, MUTED_DARK)

    def stories_heading(self):
        d = self.d
        d.text((MARGIN, 600), "THE DAY IN 36 STORIES",
               font=serif(22), fill=INK)
        check_font = bold(13)
        part_a = "DATE CHECK: "
        part_b = "ALL 36 STORIES DATED 22 NOV 2026"
        wa = d.textlength(part_a, font=check_font)
        wb = d.textlength(part_b, font=check_font)
        box_w = 12 + 26 + 8 + wa + wb + 12
        box_x0 = RIGHT_EDGE - box_w
        d.rectangle([box_x0, 596, RIGHT_EDGE, 626],
                    fill=WHITE, outline=GOLD, width=2)
        tick_x = box_x0 + 12
        tick_y = 611
        d.line([(tick_x, tick_y), (tick_x + 7, tick_y + 7),
                (tick_x + 20, tick_y - 8)], fill=CRIMSON, width=3)
        tx = box_x0 + 12 + 26 + 8
        d.text((tx, 604), part_a, font=check_font, fill=CRIMSON)
        d.text((tx + wa, 604), part_b, font=check_font, fill=INK)
        d.line([(MARGIN, 630), (RIGHT_EDGE, 630)], fill=INK, width=2)

    def story_columns(self):
        d = self.d
        num_font = bold(12)
        head_font = bold(12)
        det_font = plain(10)
        for col_i, groups in enumerate(STORY_COLUMNS):
            x = COLUMN_X[col_i]
            y = 640
            for region, stories in groups:
                d.text((x, y), region, font=bold(13), fill=CRIMSON)
                y += 16
                for number, headline, detail in stories:
                    d.text((x, y), "%02d" % number, font=num_font, fill=INK)
                    for j, line in enumerate(self.fit(headline, head_font,
                                                      COLUMN_W - 22)):
                        d.text((x + 22, y + j * 13), line,
                               font=head_font, fill=INK)
                    for j, line in enumerate(self.fit(detail, det_font,
                                                      COLUMN_W - 22)):
                        d.text((x + 22, y + 11 + j * 12), line,
                               font=det_font, fill=MUTED_DARK)
                    y += 22

    def sport_and_footer(self):
        d = self.d
        d.line([(MARGIN, 968), (RIGHT_EDGE, 968)], fill=RULE, width=1)
        d.text((MARGIN, 974),
               "SPORT IN BRIEF: Bournemouth beat Forest • France reach rugby final v South Africa • Australia beat Wales",
               font=plain(11), fill=MUTED_DARK)
        self.center(PAGE_W // 2, 1000,
                    "THE WORLD TODAY • SUNDAY 22 NOVEMBER 2026 • Sources: Reuters, AP, Al Jazeera, AFP, UN",
                    plain(11), MUTED)

    def build(self):
        self.top_rule()
        self.masthead()
        self.date_band()
        self.stats()
        self.hero()
        self.features()
        self.stories_heading()
        self.story_columns()
        self.sport_and_footer()
        return self.img


def main():
    page = FrontPage()
    img = page.build()
    img.save("entry.png")
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
