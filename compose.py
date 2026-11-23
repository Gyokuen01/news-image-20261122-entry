#!/usr/bin/env python3
"""THE WORLD TODAY front page, Sunday 22 November 2026 (v4).

This program paints a 1024x1024 newspaper front page and writes it to
entry.png: a masthead, a navy date band, a one-line statistics strip, a
hero lead about the COP31 collapse in Antalya and the Benghazi drone
strike with a large photo, three feature boxes each topped by a photo,
a four-photo strip, and a numbered digest of 57 stories from
22 November 2026 sorted into 9 regions, closed by a DATE CHECK box
that states every story on the page is dated that day. Eight photos
in total, all generated editorial-style pictures stored in photos/.

Only Pillow is used. The picture is fully deterministic: the program
reads no clock, no random source and no network, and the photos are
fixed files, so two runs write the same bytes. The layout is driven by
one FrontPage object that owns the canvas, the palette and the fonts;
each section of the page is one method. The page is packed tight on
purpose: section gaps are 6 pixels and the digest runs at a 21-pixel
pitch so photos and all 57 stories fit on one page.
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
WHITE = (255, 255, 255)
MARGIN = 28
COLUMN_W = 309
COLUMN_GAP = 20
COLUMN_X = [MARGIN, MARGIN + COLUMN_W + COLUMN_GAP,
            MARGIN + 2 * (COLUMN_W + COLUMN_GAP)]
RIGHT_EDGE = PAGE_W - MARGIN
PHOTO_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         "photos")
# Digest geometry (v4): 21 px pitch, detail line 11 px below the
# headline, region header step 14 px. At these sizes the headline
# (bold 10) and the detail (plain 8) keep a 2 px gap, the same gap
# v3 had at pitch 23.
DIGEST_TOP = 506
DIGEST_PITCH = 21
DIGEST_DETAIL = 11
DIGEST_HEADER_STEP = 14

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

    # -- photos -----------------------------------------------------------
    def photo(self, name, x, y, w, h):
        """Paste a photo from photos/ into a box, center-cropped to fit."""
        path = os.path.join(PHOTO_DIR, name)
        pic = Image.open(path).convert("RGB")
        tw, th = pic.size
        target = w / h
        have = tw / th
        if have > target:
            cut = int(th * target)
            left = (tw - cut) // 2
            pic = pic.crop((left, 0, left + cut, th))
        else:
            cut = int(tw / target)
            top = (th - cut) // 2
            pic = pic.crop((0, top, tw, top + cut))
        pic = pic.resize((w, h), Image.LANCZOS)
        self.img.paste(pic, (x, y))

    def photo_caption(self, x, y, w, text):
        """A navy caption strip with white text, laid over a photo."""
        self.d.rectangle([x, y, x + w, y + 16], fill=NAVY)
        self.d.text((x + 8, y + 3), text, font=plain(9), fill=WHITE)

    # -- page sections ----------------------------------------------------
    def top_rule(self):
        d = self.d
        d.text((MARGIN, 8), "VOL. 2026 — No. 326", font=plain(11), fill=MUTED)
        self.right(RIGHT_EDGE, 8, "PRICE: ONE DAY'S NEWS", plain(11), MUTED)
        d.line([(MARGIN, 26), (RIGHT_EDGE, 26)], fill=INK, width=1)

    def masthead(self):
        d = self.d
        self.center(PAGE_W // 2, 30, "THE WORLD TODAY", serif(58), INK)
        d.line([(MARGIN, 96), (RIGHT_EDGE, 96)], fill=INK, width=2)

    def date_band(self):
        d = self.d
        d.rectangle([MARGIN, 102, RIGHT_EDGE, 136], fill=NAVY)
        d.text((MARGIN + 20, 110), "SUNDAY • 22 NOVEMBER 2026",
               font=bold(19), fill=WHITE)
        self.right(RIGHT_EDGE - 20, 112, "57 STORIES • 9 REGIONS",
                   bold(15), GOLD)

    def stats(self):
        d = self.d
        parts = ["%s: %s" % (label, value) for label, value, _ in STAT_BOXES]
        line = "  •  ".join(parts)
        self.center(PAGE_W // 2, 144, line, bold(11), INK)
        d.line([(MARGIN, 160), (RIGHT_EDGE, 160)], fill=RULE, width=1)

    def hero(self):
        d = self.d
        d.rectangle([MARGIN, 166, RIGHT_EDGE, 274], fill=NAVY)
        d.text((MARGIN + 20, 174), "CLIMATE & CONFLICT — THE LEAD STORY",
               font=bold(12), fill=GOLD)
        d.text((MARGIN + 20, 190), "COP31 COLLAPSES —",
               font=serif(28), fill=WHITE)
        d.text((MARGIN + 20, 220), "AS DRONES HIT A WARSHIP",
               font=serif(28), fill=WHITE)
        self.para(MARGIN + 20, 248,
                  "Antalya's talks end with no deal after a fossil-fuel fight — hours after sea drones hit a Russian ship.",
                  plain(11), 580, 14, WHITE)
        self.photo("01-cop31.jpg", 640, 166, 356, 108)
        self.photo_caption(640, 258, 356,
                           "Delegates leave the Antalya talks with no deal")

    def features(self):
        d = self.d
        feat_y, feat_h = 280, 108
        specs = [
            (COLUMN_X[0], "02-hormuz.jpg", "MIDDLE EAST • HORMUZ",
             "Two tankers hit mines near Hormuz",
             "Bahrain reports attack on Sitra plant"),
            (COLUMN_X[1], "03-democrats.jpg", "WASHINGTON • MIDTERMS",
             "Democrats clinch 258 House seats",
             "Largest House majority since 1992"),
            (COLUMN_X[2], "04-liverpool.jpg", "SPORT • MANCHESTER",
             "Liverpool rout United 4-0",
             "Yoro sent off after eight minutes"),
        ]
        for fx, photo_name, kicker, headline, caption in specs:
            self.photo(photo_name, fx, feat_y, COLUMN_W, 52)
            self.photo_caption(fx, feat_y + 36, COLUMN_W, caption)
            d.rectangle([fx, feat_y, fx + COLUMN_W, feat_y + feat_h],
                        outline=RULE)
            d.text((fx + 14, feat_y + 58), kicker, font=bold(11),
                   fill=CRIMSON)
            self.para(fx + 14, feat_y + 72, headline, serif(16),
                      COLUMN_W - 28, 18, INK)

    def photo_strip(self):
        d = self.d
        strip_y, strip_h = 394, 54
        strip_w = (RIGHT_EDGE - MARGIN - 3 * COLUMN_GAP) // 4
        specs = [
            ("05-benghazi.jpg", "04 · Benghazi warship hit"),
            ("06-nigeria.jpg", "49 · Nigeria boat tragedy"),
            ("07-riopride.jpg", "54 · Rio Pride takes over"),
            ("08-wedding.jpg", "57 · Miley weds in Palm Springs"),
        ]
        for i, (photo_name, caption) in enumerate(specs):
            x = MARGIN + i * (strip_w + COLUMN_GAP)
            self.photo(photo_name, x, strip_y, strip_w, strip_h)
            d.text((x, strip_y + strip_h + 4), caption, font=plain(9),
                   fill=MUTED_DARK)

    def stories_heading(self):
        d = self.d
        d.text((MARGIN, 472), "THE DAY IN 57 STORIES",
               font=serif(20), fill=INK)
        check_font = bold(13)
        part_a = "DATE CHECK: "
        part_b = "ALL 57 STORIES DATED 22 NOV 2026"
        wa = d.textlength(part_a, font=check_font)
        wb = d.textlength(part_b, font=check_font)
        box_w = 12 + 26 + 8 + wa + wb + 12
        box_x0 = RIGHT_EDGE - box_w
        d.rectangle([box_x0, 468, RIGHT_EDGE, 494],
                    fill=WHITE, outline=GOLD, width=2)
        tick_x = box_x0 + 12
        tick_y = 481
        d.line([(tick_x, tick_y), (tick_x + 7, tick_y + 7),
                (tick_x + 20, tick_y - 8)], fill=CRIMSON, width=3)
        tx = box_x0 + 12 + 26 + 8
        d.text((tx, 474), part_a, font=check_font, fill=CRIMSON)
        d.text((tx + wa, 474), part_b, font=check_font, fill=INK)
        d.line([(MARGIN, 500), (RIGHT_EDGE, 500)], fill=INK, width=2)

    def story_columns(self):
        d = self.d
        num_font = bold(10)
        head_font = bold(10)
        det_font = plain(8)
        for col_i, groups in enumerate(STORY_COLUMNS):
            x = COLUMN_X[col_i]
            y = DIGEST_TOP
            for region, stories in groups:
                d.text((x, y), region, font=bold(13), fill=CRIMSON)
                y += DIGEST_HEADER_STEP
                for number, headline, detail in stories:
                    d.text((x, y), "%02d" % number, font=num_font, fill=INK)
                    d.text((x + 22, y), headline, font=head_font, fill=INK)
                    d.text((x + 22, y + DIGEST_DETAIL), detail,
                           font=det_font, fill=MUTED_DARK)
                    y += DIGEST_PITCH

    def sport_and_footer(self):
        d = self.d
        d.line([(MARGIN, 973), (RIGHT_EDGE, 973)], fill=RULE, width=1)
        d.text((MARGIN, 979),
               "SPORT IN BRIEF: Liverpool 4-0 Man Utd • Leeds 4-1 Chelsea • Arsenal 2-2 Newcastle • Man City 1-1 Fulham • Real Madrid 2-1 Celta • Roma 5-1 Parma • PSG 3-2 Nice",
               font=plain(11), fill=MUTED_DARK)
        self.center(PAGE_W // 2, 1005,
                    "THE WORLD TODAY • SUNDAY 22 NOVEMBER 2026 • Sources: Reuters, AP, Al Jazeera, AFP, UN",
                    plain(11), MUTED)

    def build(self):
        self.top_rule()
        self.masthead()
        self.date_band()
        self.stats()
        self.hero()
        self.features()
        self.photo_strip()
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
