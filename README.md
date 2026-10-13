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

Each project's content must come from its approved research report. Record
completed, reported, and ongoing results separately. Put only accessible,
report-referenced figures in `public/` and describe their provenance in the
project's `sourceNote`.

The first project combines two clearly labeled sources: the completed
“Generation, Step by Step” checkpoint report in `public/report/`, and the
researcher's redesign brief. The brief supplies the matched-100k A0/A1 STRONG
verdict, approximately 5% relative FID cost, and the single-token G2
checkerboard caveat in seeds 5 and 7. Exact A0/A1 FIDs and G2 images were not
supplied, so the site does not show them. Published FIDs in the checkpoint
audit remain attributed to papers or official checkpoint descriptions; its
eight-sample trajectories are not new FID measurements.
