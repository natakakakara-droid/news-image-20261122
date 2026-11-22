[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/natakakakara-droid/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard)
[![reward](https://make.fun/badge/news-image-20261122/natakakakara-droid/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122)

# The World in One Day — 22 November 2026

Entry for [news-image-20261122](https://make.fun/bounty/news-image-20261122):
a program that writes one image summing up Sunday 22 November 2026's world
news. The image is a newspaper front page, **THE WORLD IN ONE DAY**, with
five verified stories of the day.

## The five stories

1. **Russia's 500-weapon night over Kyiv** — 27 ballistic missiles, 84 cruise
   missiles and 404 drones; three Dnipro bridges hit, at least nine killed,
   Russian weapons came down in Poland. (Institute for the Study of War,
   Kyiv Independent, Al Jazeera, AP)
2. **Drone hit sets Russian ship ablaze** — the sanctioned cargo vessel
   Sparta II, bound for Kaliningrad, was struck by two drones in the Gulf of
   Finland and drifted burning into Finnish waters; her 16 crew were
   evacuated. (Reuters, CNN)
3. **6.9 quake shakes Peru's Andes** — near Junín, felt in Lima, no damage
   or casualties reported. (USGS, AP)
4. **Fossil-fuel fight deadlocks COP31** — draft text drops any phase-out
   language; talks spill into overtime. (BBC)
5. **Denmark expels Russian diplomat over 'assassination plot'** — Copenhagen
   accused Russian intelligence of plotting to kill Ukrainian-American rapper
   Kyivstoner; two men face attempted-murder charges. (Reuters, The Times)

Sources are also listed in the image footer.

## How it runs

`main.ts` (Node 22, standard library only) copies `entry.png` to
`$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output`). `render.py` is the
Pillow script that drew `entry.png` — deterministic: two runs produce
byte-identical output (sha256
`3ea4a6f40b598e061dab54d410074c47bb4654665b005b6b8d1b348868d2d307`).
The image is 1024×1024 PNG, 154,625 bytes.

## License

MIT — see `LICENSE`.
