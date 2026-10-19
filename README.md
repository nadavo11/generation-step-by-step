# Generation research site

Astro static site published at <https://nadavo11.github.io/generation-step-by-step/>.

| Page | What |
|---|---|
| `/` | Landing page: the two projects as cards and a dated update log (`src/data/site.ts`) |
| `/projects/next-frequency/` | Our A1 method: FFHQ-64 results against DCTdiff (R0) and the joint control (A0), the UniPC sampler, the 146k stage explorer, CIFAR-10, limits and next experiments |
| `/projects/next-frequency/deck/` | Lab deck of 19 Oct 2026: slide viewer with speaker notes, PDF / PPTX / one-slide summary downloads |
| `/projects/generation-step-by-step/` | Streaming trajectory audit of 21 released checkpoints, with A1 in the same views |
| `/report/` | The archived original audit report |

Header navigation and the footer site map come from `src/data/site.ts` and
`src/layouts/Base.astro`; the next-frequency pages share a breadcrumb and tab bar
(`src/components/ProjectTabs.astro`).

The two projects use different models and comparison protocols. Next-frequency
numbers are as of 19 Oct 2026 and come from the campaign’s result files in
`learned-spectral-basis/reports/dct_causal/`; the deck’s `PROVENANCE.md` lists
the file behind each figure.

## Adding a deck

Build the deck and its viewer images in `learned-spectral-basis/reports/shai_deck`
(`src/build_deck.js`, then `src/build_page.py build page`), then run

```bash
python scripts/import_deck.py /path/to/learned-spectral-basis/reports/shai_deck
```

It copies slides, PDF, PPTX and figures into `public/decks/<id>/` and writes
`src/data/deck-<date>.json` (titles, kickers, speaker notes) for `DeckViewer`.

## Local development

```bash
source ~/.nvm/nvm.sh
nvm use 24
npm install
npm run dev
```

Open <http://127.0.0.1:4321/generation-step-by-step/>. Run `npm run build`
to type-check and generate the static site in `dist/`. The GitHub Pages
workflow deploys pushes to `main` in `nadavo11/generation-step-by-step`.

## Provenance

The original audit is archived in `public/report/`; its raw display data is
`public/report/catalog.json` and `public/report/measurements.json`. The saved
FFHQ-64 A1 source sheet, final grids, hashes, run IDs, and metric values are in
`public/ours/ffhq64-a1-d256/` and its `source.json`.

Run `python scripts/build_ours_trajectory.py` to reconstruct the two display
montages and `spectral.json` from `stages-146k.png`. The script only rearranges
pixels for the montages. Spectral residuals use the original audit's luma FFT
bands, lower median of eight samples, and 0.1 settle rule, measured from the
saved 8-bit PNG. The A1 stage viewer crops that source sheet in the browser;
its smooth 4× option is display interpolation, not generated super-resolution.

The streaming report's comparison scrubber reads the saved A1, DCTdiff, and
FAR strips. Its slider uses each run's own fraction of sampling work and
shows the last saved frame reached, with blank panels before the first frame.
The panels differ in dataset, resolution, and total compute. The A1 report's
channel diagram uses the documented 6/12/18/18 grouping, and its frequency
heatmap reads the derived `spectral.json` values. Playback in both views
starts only when clicked.

The streaming PSNR instrument reads `public/streaming/psnr.json`. Regenerate it
with `python scripts/build_streaming_psnr.py --results /path/to/prior_intermediates/results`.
It converts the archived public-run median RGB RMSE arrays to PSNR and measures
the four A1 stages from the native 64px saved PNG. Source SHA-256 hashes travel
with each row. The graph groups runs by dataset and native resolution; its horizontal coordinate
is each run's fraction of calls/stages, **not elapsed seconds**. The archive has
only total batch wall time for DCTdiff/FAR and no per-stage wall times, so these
curves do not establish a latency ranking or cross-dataset streaming superiority.
The interactive view groups by both dataset and native pixel size, defaults to
A1 alone on FFHQ-64, and links the highlighted curve to one saved preview and
its own final image. The image is a visual example; the plotted value is the
lower-median RMSE converted to PSNR over eight samples.
