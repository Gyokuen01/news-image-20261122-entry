# news-image-20261122 — The World Today, Sunday 22 November 2026

A newspaper front page summing up the world's news of Sunday 22
November 2026 in one 1024x1024 image: COP31's collapse in Antalya,
sea drones striking a Russian warship at Benghazi, two tankers hit by
mines off Hormuz, Democrats clinching 258 House seats, and Liverpool
routing Manchester United 4-0 — plus a numbered list of all 57 dated
stories across 9 regions, with a DATE CHECK box.

v4 changes vs v3: 8 photos added — a large COP31 photo in the hero,
one photo topping each of the three feature boxes (Hormuz tankers,
Democrats 258 seats, Liverpool 4-0), and a four-photo strip (Benghazi
warship, Nigeria boat tragedy, Rio Pride, Miley's Palm Springs
wedding), each photo captioned and linked to its digest story number.
The photos are generated editorial-style pictures in photos/, pasted
in by compose.py. The page is packed tighter to fit them: masthead,
date band and stats strip slimmed, digest at a 21 px pitch with 11 px
detail offset, section gaps of 6 px. Still all 57 stories, 9 regions,
same lead, same DATE CHECK box.

v3 changes vs v2: 57 stories (was 36) in a denser digest — smaller
digest type (bold 11 / plain 9), a slimmer hero without portraits and
text-only feature boxes to make room; the lead is now the COP31
collapse (verified against CNN and Le Monde reporting of 22 Nov),
with the Benghazi drone strike as the second lead; stats strip,
features and sport line all refreshed to the 22 Nov outcomes. Same
masthead, date band and DATE CHECK box.

v2 changes vs v1: the story list is regrouped into 9 visible regions
(was 3 headers claiming 7); the heading now reads "THE DAY IN 36
STORIES" (was "32 MORE STORIES" over a 36-item list); a gold DATE
CHECK box states all 36 stories are dated 22 Nov 2026; story 26's
detail now names both Kenya and the DRC toll. Same 36 verified
stories, same lead — nothing added, nothing dropped.

## How it is built

`compose.py` (Pillow only, no network, fully deterministic) draws the
front page and writes `entry.png`. `main.ts` (Node 22, stdlib only)
copies that exact image to the grader's output directory on every run.

## Reproduce

```sh
python3 compose.py            # writes entry.png (1024x1024, < 1 MiB)
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## Sources

Reuters, AP, CNN, Le Monde, Al Jazeera, AFP, UN — all stories verified against
reporting published on 22 November 2026. Events from earlier days
(Voyager-1's 18 Nov milestone, the 20 Nov Virginia measles death,
Nvidia's 12 Nov CEO resignation, Norway's 13 Nov oil ruling) were
deliberately left out: this page is about 22 November alone.

## License

MIT — see LICENSE.
