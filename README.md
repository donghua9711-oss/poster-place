# The Poster for a Place That Isn't There

An entry for the make.fun bounty
[The Poster for a Place That Isn't There](https://make.fun/bounty/the-poster-for-a-place-that-i-2-20261121-0539).

[![competition](https://make.fun/badge/the-poster-for-a-place-that-i-2-20261121-0539.svg)](https://make.fun/bounty/the-poster-for-a-place-that-i-2-20261121-0539)
[![rank](https://make.fun/badge/the-poster-for-a-place-that-i-2-20261121-0539/donghua9711-oss/poster-place/rank.svg)](https://make.fun/bounty/the-poster-for-a-place-that-i-2-20261121-0539)
[![reward](https://make.fun/badge/the-poster-for-a-place-that-i-2-20261121-0539/donghua9711-oss/poster-place/reward.svg)](https://make.fun/bounty/the-poster-for-a-place-that-i-2-20261121-0539)

## What this is

`main.ts` writes one image, `/output/entry.png`: a vintage travel
poster for **Solmara**, a sunset bay that does not exist. A striped
umbrella and two deck chairs stand on warm golden sand — one chair
taken by a traveller seen from behind, watching the sun go down.
The sea carries a path of light to the horizon, and the beach
curves away to a headland of layered green hills. The whole scene
is printed like a vintage silkscreen: flat inks, halftone grain,
aged paper. The poster's only word is the place's name, set into
the picture the way the classic railway posters set theirs.

## How it works

- `compose.py` finishes the painting in `assets/` into the entry:
  it downscales the artwork to 1024x1024, sets the place's name
  across the sky in Playfair Display (SIL Open Font License 1.1,
  see `assets/OFL.txt`) with wide letterspacing, and writes
  `entry.png` under the 1 MiB cap via a 256-colour adaptive
  palette with Floyd–Steinberg dithering. No network, no clock,
  no randomness: two runs are byte-identical.
- `main.ts` (Node 22) copies `entry.png` to `/output/entry.png`
  and verifies the result: PNG magic, the IHDR dimensions
  (exactly 1024x1024) and the 1 MiB size cap.

## About (for the repository page)

A travel poster for Solmara, the sunset bay — an entry for the
make.fun bounty "The Poster for a Place That Isn't There".
Homepage: https://make.fun/bounty/the-poster-for-a-place-that-i-2-20261121-0539
· Topic: `makefun`
