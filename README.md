# Research project site

Astro static site for research project pages. The landing page lists subjects;
each subject uses the reusable route in `src/pages/projects/[slug].astro` and
content in `src/data/projects.ts`.

Published site: <https://nadavo11.github.io/generation-step-by-step/>.
The GitHub Pages workflow builds and deploys on pushes to `main` in the separate
`nadavo11/generation-step-by-step` website repository.

## Local development

```bash
source ~/.nvm/nvm.sh
nvm use 24
cd site
npm install
npm run dev
```

Open <http://127.0.0.1:4321/generation-step-by-step/>. Run `npm run build` to type-check and build the
static site into `dist/`.

## Evidence rule

Each project's content must come from approved research evidence. Record
completed, reported, and ongoing results separately. Keep figure provenance
alongside published assets in `public/`.

The first project combines three clearly labeled sources: the completed
“Generation, Step by Step” checkpoint report in `public/report/`; the separate
CIFAR-10 D192 matched-100k experiment; and the FFHQ-64 D256 W&B runs. The
CIFAR-10 experiment supplies the A0/A1 STRONG verdict, approximately 5%
relative FID cost, and the single-token G2 checkerboard caveat in seeds 5 and
7. Its exact FIDs and G2 images are not shown. The FFHQ-64 source manifest is
in `public/ours/ffhq64-a1-d256/source.json`. Published FIDs in the checkpoint
audit remain attributed to papers or official checkpoint descriptions; its
eight-sample trajectories are not new FID measurements.

The project's interactive audit instruments reuse the archived report's exact
measurement arrays (`public/report/measurements.json`) and its 21 trajectory
strips (`public/report/catalog.json`, with images under `public/report/img/`).
The 17 DCTdiff/FAR entries drive the settle chart and residual curves; all 21
sampled runs are available in the trajectory viewer. These archived artifacts
are contextual evidence for streaming behavior, separate from the A0/A1 result.

The A1 stage viewer crops the original 8-column × 4-row FFHQ-64 stage sheet in
the browser. “Smooth 4×” uses browser canvas interpolation to display each
64 × 64 sample at 256 × 256; it is not a generated super-resolution result.
