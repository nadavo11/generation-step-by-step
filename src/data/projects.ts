import type { Project } from '../types';

// This entry is transcribed from the approved “Generation, Step by Step” report.
export const projects: Project[] = [
  {
    slug: 'generation-step-by-step',
    title: 'Generation, Step by Step',
    category: 'Image generation · checkpoint audit',
    contribution: 'An image-space audit of when structure and detail emerge in official DCTdiff and FAR samples, alongside four released streaming and coarse-to-fine models.',
    status: 'completed',
    verdict: 'DCTdiff settles from coarse to fine in pixel space. FAR’s carried prefix stays blurred; most mid- and high-frequency pixel detail is decided at its last stage.',
    motivation: 'A generator can expose intermediate states without providing a useful image preview. This audit decodes those states and measures how closely each frequency band matches the trajectory’s own final image.',
    question: 'Do successive sampling states become usable image previews, and when does each pixel-frequency band stop changing?',
    setup: 'Eight trajectories per checkpoint. The report samples all 14 public DCTdiff and 3 FAR checkpoints with official samplers, plus one ImageNet-256 checkpoint each for D-AR, FlexVAR, VAR, and DetailFlow. Luma FFT residuals are measured against each trajectory’s final sample and summarized by the median over eight samples.',
    metrics: [
      { label: 'DCTdiff checkpoints', value: '14', context: 'Official public checkpoints sampled across five datasets.' },
      { label: 'Coarsest band settles', value: '28–40%', context: 'Fraction of DCTdiff’s 100 network calls, across all 14 checkpoints.' },
      { label: 'Finest band settles', value: '70–95%', context: 'Fraction of DCTdiff’s 100 network calls; always after coarser bands.' },
    ],
    results: [
      { comparison: 'DCTdiff prediction', setting: '14 checkpoints · 100 network calls', result: 'Coarsest 28–40%; finest 70–95%', interpretation: 'Pixel frequencies settle in coarse-to-fine order without an explicit ordering constraint.' },
      { comparison: 'FAR-H stage prediction', setting: '10 generation stages', result: 'Coarsest residual 0.51 at stage 2; 0.14 at stage 4', interpretation: 'Full-image predictions improve, but stages redraw details.' },
      { comparison: 'FAR carried context', setting: 'Stage 9 of 10', result: 'Residual 0.74–0.84 in the 1/16–1/4 bands', interpretation: 'The state passed forward is a blur with VAE grid ringing, not a stable partial image.' },
    ],
    relatedMethods: [
      { comparison: 'D-AR', setting: 'Paper: 1.4B · released: XL 775M', result: 'Paper FID 2.00 · released 2.09', interpretation: 'Denoising-state previews; early states are noisy.' },
      { comparison: 'FlexVAR', setting: 'Paper: 1B, 13 stages · released: d24', result: 'Paper FID 2.08 · released 2.21 at 10 stages', interpretation: 'First scale is already recognizable; later scales revise shape and texture.' },
      { comparison: 'VAR', setting: 'Paper: 2B · released: d30', result: 'Paper FID 1.73 · released 1.97 (1.80 re-eval)', interpretation: 'Decoded next-scale previews gain identity and detail gradually.' },
      { comparison: 'NFIG', setting: 'Low-to-high frequency generation', result: 'Paper FID 2.81', interpretation: 'No public pretrained generator or tokenizer weights for a trajectory.' },
      { comparison: 'DetailFlow', setting: '128-token stream · released 16-GPT-L', result: 'Paper gFID 2.96 · released 2.96', interpretation: 'Recognizable composition after the first eight tokens; later groups refine detail.' },
    ],
    interpretation: 'The trajectories measure when a generated image becomes decided, not how good it is against real data. DCTdiff’s ordering appears in decoded pixels, whereas FAR’s frequency progression is carried in VAE-latent space and its last stage makes many visible detail decisions.',
    qualitative: [
      'DCTdiff’s predicted image develops coarse structure before fine detail. At 32² and 64², object identity is often unclear; high-resolution outputs can look smooth because high DCT coefficients are truncated.',
      'FAR stage predictions are full images, but early stages are patchy mosaics. The context actually passed between stages decodes to blur and VAE grid ringing.',
      'Among released ImageNet-256 comparators, FlexVAR and DetailFlow show recognizable subjects early; VAR starts with blurred structure; D-AR’s early denoising states are noisy.',
    ],
    caveats: [
      'Published FID-50k values are quoted from papers or official checkpoint descriptions. This eight-sample audit did not re-measure FID, and the model figures are not a controlled ranking.',
      'The settle metric compares every intermediate state with that trajectory’s own final sample. It measures when a sample is decided, not its realism or fidelity to data.',
      'DCTdiff’s ImageNet-64 label mapping was built from an unsorted training-folder listing and was not released; its label indices cannot be treated as named standard ImageNet classes.',
      'FAR’s carried context is outside the VAE decoder’s training distribution. Some decoded ringing comes from that decoder and does not directly describe what the transformer reads.',
      'NFIG is represented by its published result only because its public repository provides no pretrained generator or tokenizer checkpoint.',
    ],
    nextExperiments: [
      'Run a controlled evaluation before ranking these methods by FID; the reported figures use different models, inference settings, and evaluation details.',
      'Re-measure FID-50k for the reproduced checkpoint and sampler settings. The current report contains sample trajectories and cited FID values, not new FID estimates.',
    ],
    claims: [
      { status: 'completed', text: 'DCTdiff orders pixel frequencies without an explicit stage schedule.', evidence: 'Across 14 checkpoints, the coarsest FFT residual band settles at 28–40% of 100 network calls and the finest at 70–95%, always in band order.' },
      { status: 'completed', text: 'FAR’s carried prefix is not yet a usable partial image.', evidence: 'At stage 9 its 1/16–1/4 pixel-frequency bands retain residual 0.74–0.84; the decoded context is blurred and exhibits VAE grid ringing.' },
      { status: 'reported', text: 'The ImageNet-256 comparator figures are published results.', evidence: 'The report cites paper and official checkpoint FIDs separately. It generated eight trajectory samples per released model, without a 50k-image FID run.' },
    ],
    figures: [
      { src: 'report/img/ffhq128_mid_x0.jpg', alt: 'DCTdiff FFHQ-128 mid decoded predictions at successive diffusion calls, eight samples in rows.', caption: 'DCTdiff, FFHQ-128 mid: predicted images across 100 network calls. Coarse structure stabilizes before fine detail.' },
      { src: 'report/img/far_huge_pred.jpg', alt: 'FAR-H stage predictions, eight samples in rows across ten stages.', caption: 'FAR-H: each stage predicts a complete image; early predictions are patchy and later stages redraw detail.' },
      { src: 'report/img/far_huge_ctx.jpg', alt: 'FAR-H context passed to the next stage, decoded as images across ten stages.', caption: 'FAR-H carried context: the decoded prefix remains blurred with VAE grid ringing.' },
      { src: 'report/img/dar_xl_preview.jpg', alt: 'D-AR XL eight ImageNet-256 sample trajectories across eight denoising states.', caption: 'D-AR XL: eight denoising-state previews from the released 775M checkpoint.' },
      { src: 'report/img/flexvar_d24_preview.jpg', alt: 'FlexVAR d24 eight ImageNet-256 trajectories across 13 scales.', caption: 'FlexVAR d24: independently decoded images across the report’s 13-stage schedule.' },
      { src: 'report/img/var_d30_preview.jpg', alt: 'VAR d30 eight ImageNet-256 trajectories across ten scales.', caption: 'VAR d30: cumulative next-scale previews reveal identity and fine detail gradually.' },
      { src: 'report/img/detailflow_preview.jpg', alt: 'DetailFlow eight ImageNet-256 trajectories across 16 token groups.', caption: 'DetailFlow: successive prefixes of a 128-token sequence; the first eight tokens reveal the broad composition.' },
    ],
    sourceNote: 'Source: “Generation, Step by Step,” the completed checkpoint trajectory report. The full report contains all 17 DCTdiff/FAR strips, four released comparator strips, the checkpoint table, method notes, and spectral plots.',
  },
];
