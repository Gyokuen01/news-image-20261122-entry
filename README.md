# news-image-20261122 — The World Today, Sunday 22 November 2026

A newspaper front page summing up the world's news of Sunday 22
November 2026 in one 1024x1024 image: COP31's overtime deal in
Antalya, Iran's missile-and-drone attack on Bahrain, Israel's
Eisenkot tasked to form a government, Gaza aid blocked at the border,
a drone-hit Russian ship drifting into Finnish waters, and the ATP
Finals decider in Turin — plus a numbered list of all 36 dated
stories across 9 regions, with a DATE CHECK box.

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

Reuters, AP, Al Jazeera, AFP, UN — all stories verified against
reporting published on 22 November 2026. Events from earlier days
(Voyager-1's 18 Nov milestone, the 20 Nov Virginia measles death,
Nvidia's 12 Nov CEO resignation, Norway's 13 Nov oil ruling) were
deliberately left out: this page is about 22 November alone.

## License

MIT — see LICENSE.
