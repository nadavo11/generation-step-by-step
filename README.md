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

The first project is based only on the completed “Generation, Step by Step”
report, copied into `public/report/` with its referenced image strips. Published
FID figures remain attributed to papers or official checkpoint descriptions;
the report's eight-sample trajectories are not new FID measurements. This report
does not contain the matched-100k STRONG result or a seeds 5/7 checkerboard
finding, so this page does not claim either.
