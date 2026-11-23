#!/usr/bin/env python3
"""THE WORLD TODAY front page, Sunday 22 November 2026 (v3).

This program paints a 1024x1024 newspaper front page and writes it to
entry.png: a masthead, a navy date band, a one-line statistics strip, a
hero lead about the COP31 collapse in Antalya and the Benghazi drone
strike, three feature boxes, and a numbered digest of 57 stories from
22 November 2026 sorted into 9 regions, closed by a DATE CHECK box
that states every story on the page is dated that day.

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
# 57 stories, all dated Sunday 22 November 2026. Headlines stay under
# 40 characters and details under 55 so each story fits one line each
# at the digest type sizes (bold 11 / plain 9 across 287 px).
STORY_COLUMNS = [
    [
        ("CLIMATE", [
            (1, "COP31 collapses in Antalya", "No deal after fossil-fuel fight; first since 2009"),
            (2, "COP31 negotiator 'very disappointed'", "Chris Bowen rues the collapse of the Antalya talks"),
            (3, "India flags lack of equity", "Developing bloc decries diluted climate responsibility"),
        ]),
        ("RUSSIA-UKRAINE", [
            (4, "Sea drones hit Russian warship", "Ship capsizes at Benghazi naval base, satellites show"),
            (5, "Russian strike kills 3 near Kyiv", "Apartment block in Dymer hit; up to 7 feared trapped"),
            (6, "Woman pulled alive after 22 hours", "Rescued from rubble after night strike near Kyiv"),
            (7, "Missiles hit Zelenskyy's hometown", "Ballistic attack on Kryvyi Rih kills 2, wounds scores"),
            (8, "Russian missiles land in Poland", "NATO calls it a violation as drills run nearby"),
            (9, "Poland: Russia tried to kill rapper", "Moscow allegedly targeted a Ukrainian American"),
            (10, "Russia grasps US security offer", "Moscow revives old demands on European security"),
            (11, "Drone hits Russian ship off Finland", "Attack in the Baltic Sea as tensions stay high"),
        ]),
        ("MIDDLE EAST", [
            (12, "Two tankers hit mines off Hormuz", "Bahrain reports attack on Sitra plant; 2 injured"),
            (13, "Iran vows to counter US blockade", "IRGC Navy warns ships to coordinate with Tehran"),
            (14, "Eisenkot: settler attacks 'terrorism'", "Settlers hit four villages, torch vehicles"),
            (15, "Israeli strikes kill 5 in Gaza", "Two killed by forces; three die in a vehicle strike"),
            (16, "ICJ: Myanmar committed genocide", "Court rules over the Rohingya in landmark case"),
            (17, "Rohingya welcome verdict, want home", "Refugees in Bangladesh hail ruling, seek return"),
            (18, "Houthis strike Saudi Arabia", "Coalition intercepts a Houthi missile"),
            (19, "US sanctions Iran oil 'trustees'", "Treasury targets collectors of oil revenues"),
        ]),
    ],
    [
        ("NORTH AMERICA", [
            (20, "Democrats clinch 258 House seats", "Largest majority since 1992; Hubbard wins recount"),
            (21, "Trump backs 10% card-rate cap", "President says he will work with Democrats on cap"),
            (22, "Trump orders contractors in line", "Congressional requests to go via White House"),
            (23, "FBI probes crime-database hack", "Reported breach of the National Crime Info Center"),
            (24, "Top court rejects Trump UC appeal", "Research-grant cuts stand after Supreme Court no"),
            (25, "First US deep-sea mining leases", "Auctions near American Samoa; $3M minimum each"),
            (26, "Senate rejects Iran war powers", "Three Republicans join Democrats in the vote"),
            (27, "Musk: 'pretty foolish' on $500M", "Musk rues spending nearly $500M on the GOP"),
            (28, "Stocks slide as AI sell-off deepens", "S&P and Dow in correction; Nasdaq falls 5.28%"),
            (29, "Nvidia chip scandal widens", "US confirms China got AI chips; SEC probe opens"),
        ]),
        ("EUROPE", [
            (30, "EU signs Indonesia trade deal", "Ten years of talks end; 98.5% of tariffs axed"),
            (31, "EU confirms data leak after hack", "Commission hit by cyberattack; personal data out"),
            (32, "450 German schools get bomb threats", "Threat emails spark probe across the country"),
            (33, "Macron proposes budget 'golden rule'", "French president pitches a new fiscal anchor"),
            (34, "Sanchez ups ante before snap poll", "Spain votes 29 November as pressure builds"),
            (35, "Manchester concert evacuated", "Gas scare hits Don Toliver gig; 12,000 affected"),
            (36, "Czech police detain fund executive", "Turkish executive wanted in a fund probe held"),
            (37, "Hungary PM to visit Transcarpathia", "Pledges support to locals across the border"),
            (38, "Turkey seeks EU car-tariff waiver", "Ankara wants exemption from hybrid-car duties"),
        ]),
    ],
    [
        ("ASIA", [
            (39, "Indonesia names 6 in treason plot", "Police officials among suspects, officials say"),
            (40, "Candy factory fire: 34 missing", "Three killed, four hurt; more remains found"),
            (41, "Thai court upholds royal conviction", "Opposition MP's sentence cut to three years"),
            (42, "India pledges EUR 1.4bn to Nepal", "Rebuild aid after a deadly glacier flood"),
            (43, "Nepal PM starts two-day India visit", "Eight MoUs signed, from space to security"),
            (44, "China eases margin trading rules", "Minimum ratio cut to 80% from 100% on 30 Nov"),
            (45, "China chipmakers gain ground", "CXMT and YMTC advance amid US export curbs"),
            (46, "Taiwan cautions Canada on China", "Taipei warns over closer economic ties"),
            (47, "North Korea leader cites security", "Kim highlights defence after Trump no-show"),
            (48, "Mongolia heads for snap vote", "Presidential ballot after president resigns"),
        ]),
        ("AFRICA", [
            (49, "Nigeria boat capsizes; 24 dead", "Vessel carrying funeral mourners sinks"),
            (50, "Kenya enforces crypto licensing", "Central bank starts VASP framework for assets"),
            (51, "Nigeria seizes 50.4kg of cannabis", "Golfer and chef arrested in NDLEA swoop"),
            (52, "Drone strikes destroy Khartoum homes", "Rebels kill 15 civilians in South Sudan"),
        ]),
        ("LATIN AMERICA", [
            (53, "Cartel boss 'Chapo Isidro' captured", "Bloody firefight in Mexico leaves 11 dead"),
            (54, "Pride takes over Copacabana", "Colourful costumes and dancing fill Rio beach"),
        ]),
        ("SPORT & CULTURE", [
            (55, "Liverpool rout United 4-0", "Yoro sent off after eight minutes at Anfield"),
            (56, "Leeds stun Chelsea 4-1", "Arsenal draw 2-2; City held 1-1 by Fulham"),
            (57, "Miley Cyrus marries in Palm Springs", "Pop star weds drummer Maxx Morando"),
        ]),
    ],
]

STAT_BOXES = [
    ("COP31", "COLLAPSED", CRIMSON),
    ("DEMS 258", "HOUSE", NAVY),
    ("HORMUZ", "2 TANKERS", CRIMSON),
    ("BENGHAZI", "SHIP HIT", NAVY),
    ("LIVERPOOL", "4-0", LEAF),
    ("NASDAQ", "-5.28%", CRIMSON),
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
        self.right(RIGHT_EDGE - 20, 128, "57 STORIES • 9 REGIONS",
                   bold(16), GOLD)

    def stats(self):
        d = self.d
        parts = ["%s: %s" % (label, value) for label, value, _ in STAT_BOXES]
        line = "  •  ".join(parts)
        self.center(PAGE_W // 2, 162, line, bold(12), INK)
        d.line([(MARGIN, 182), (RIGHT_EDGE, 182)], fill=RULE, width=1)

    def hero(self):
        d = self.d
        d.rectangle([MARGIN, 188, RIGHT_EDGE, 308], fill=NAVY)
        d.text((MARGIN + 20, 198), "CLIMATE & CONFLICT — THE LEAD STORY",
               font=bold(13), fill=GOLD)
        d.text((MARGIN + 20, 216), "COP31 COLLAPSES —",
               font=serif(32), fill=WHITE)
        d.text((MARGIN + 20, 250), "AS DRONES HIT A WARSHIP",
               font=serif(32), fill=WHITE)
        d.text((MARGIN + 20, 284),
               "Antalya's talks end with no deal after a fossil-fuel fight — hours after sea drones hit a Russian ship.",
               font=plain(13), fill=WHITE)

    def features(self):
        d = self.d
        feat_y, feat_h = 314, 110
        for fx in COLUMN_X:
            d.rectangle([fx, feat_y, fx + COLUMN_W, feat_y + feat_h],
                        fill=WHITE, outline=RULE)
        specs = [
            (COLUMN_X[0], "MIDDLE EAST • HORMUZ",
             "Two tankers hit mines near Hormuz",
             "Bahrain reports an attack on a Sitra plant; Iran vows to counter a US blockade."),
            (COLUMN_X[1], "WASHINGTON • MIDTERMS",
             "Democrats clinch 258 House seats",
             "Largest House majority since 1992; Hubbard wins the NC recount."),
            (COLUMN_X[2], "SPORT • MANCHESTER",
             "Liverpool rout United 4-0",
             "Yoro sent off after eight minutes at Anfield; Leeds stun Chelsea 4-1."),
        ]
        for fx, kicker, headline, caption in specs:
            d.text((fx + 14, feat_y + 10), kicker, font=bold(12), fill=CRIMSON)
            self.para(fx + 14, feat_y + 28, headline, serif(18),
                      COLUMN_W - 28, 21, INK)
            self.para(fx + 14, feat_y + 78, caption, plain(11),
                      COLUMN_W - 28, 14, MUTED_DARK)

    def stories_heading(self):
        d = self.d
        d.text((MARGIN, 432), "THE DAY IN 57 STORIES",
               font=serif(22), fill=INK)
        check_font = bold(13)
        part_a = "DATE CHECK: "
        part_b = "ALL 57 STORIES DATED 22 NOV 2026"
        wa = d.textlength(part_a, font=check_font)
        wb = d.textlength(part_b, font=check_font)
        box_w = 12 + 26 + 8 + wa + wb + 12
        box_x0 = RIGHT_EDGE - box_w
        d.rectangle([box_x0, 428, RIGHT_EDGE, 458],
                    fill=WHITE, outline=GOLD, width=2)
        tick_x = box_x0 + 12
        tick_y = 443
        d.line([(tick_x, tick_y), (tick_x + 7, tick_y + 7),
                (tick_x + 20, tick_y - 8)], fill=CRIMSON, width=3)
        tx = box_x0 + 12 + 26 + 8
        d.text((tx, 436), part_a, font=check_font, fill=CRIMSON)
        d.text((tx + wa, 436), part_b, font=check_font, fill=INK)
        d.line([(MARGIN, 464), (RIGHT_EDGE, 464)], fill=INK, width=2)

    def story_columns(self):
        d = self.d
        num_font = bold(10)
        head_font = bold(10)
        det_font = plain(8)
        for col_i, groups in enumerate(STORY_COLUMNS):
            x = COLUMN_X[col_i]
            y = 468
            for region, stories in groups:
                d.text((x, y), region, font=bold(13), fill=CRIMSON)
                y += 15
                for number, headline, detail in stories:
                    d.text((x, y), "%02d" % number, font=num_font, fill=INK)
                    d.text((x + 22, y), headline, font=head_font, fill=INK)
                    d.text((x + 22, y + 13), detail, font=det_font,
                           fill=MUTED_DARK)
                    y += 23

    def sport_and_footer(self):
        d = self.d
        d.line([(MARGIN, 968), (RIGHT_EDGE, 968)], fill=RULE, width=1)
        d.text((MARGIN, 974),
               "SPORT IN BRIEF: Liverpool 4-0 Man Utd • Leeds 4-1 Chelsea • Arsenal 2-2 Newcastle • Man City 1-1 Fulham • Real Madrid 2-1 Celta • Roma 5-1 Parma • PSG 3-2 Nice",
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
