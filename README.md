# Generation research site

Astro static site published at <https://nadavo11.github.io/generation-step-by-step/>.
It has two distinct reports:

- `/projects/generation-step-by-step/`: a streaming trajectory audit. The
  original report contributes 21 released-checkpoint strips and 17 DCTdiff/FAR
  spectral series. An A1 FFHQ-64 strip, figure, and spectral series are added
  in the same views, with their separate source labeled.
- `/projects/next-frequency/`: the A1 method, saved FFHQ-64 sample explorer and
  matched-compute metrics, plus the separate CIFAR-10 D192 matched-100k STRONG
  verdict and seeds 5/7 G2 artifact caveat.

The two experiments use different models and comparison protocols. The
CIFAR-10 exact FIDs and G2 artifact images were not supplied, so they are not
fabricated. The FFHQ-64 A1 run is marked crashed after saving its 146k
assessment; no later result is claimed.

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
