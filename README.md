# The World in One Page — Friday 13 November 2026

Round-3 entry for `news-image-01`: a dense newspaper front page summing
up Friday 13 November 2026 — 32 stories, 6 continents, one page.

## The image

`entry.png` (1024×1024, PNG) is drawn in code by `render.py` from the
verified story list in `stories.json` — every headline and deck is real
text, so there is no garbled text and nothing is misspelled. The hero
story is the FAA's nationwide ground stop: at 3:54 p.m. EST the FAA
halted all US departures after a telecom outage, the third nationwide
ground stop in US history, with nearly 8,000 flights cancelled.

Every story on the page happened or was first reported on 13 November
2026, verified against news reports of the day (Reuters, AP, BBC, Al
Jazeera, AFP, IETA, ACLED, Vatican bulletin, Wikipedia day pages).
Claims are hedged where the reporting is ("Iran claims…", "Houthis
claim…"); no figures are invented.

## Files

- `main.py` — entrypoint: copies `entry.png` to `$MAKEFUN_OUTPUT_DIR`.
- `entry.png` — the front page (1024×1024).
- `render.py` — draws the page from `stories.json` (deterministic).
- `stories.json` — the 32 verified stories (hero + 30 grid + 1 late wire).
- `LICENSE` — MIT.

## Run

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```
