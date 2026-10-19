// Site-wide navigation and the dated update log shown on the landing page.
export type Section = 'home' | 'next-frequency' | 'deck' | 'audit' | 'report';

export interface NavItem { section: Section; label: string; href: string; }

export const primaryNav: NavItem[] = [
  { section: 'next-frequency', label: 'Next-frequency', href: 'projects/next-frequency/' },
  { section: 'deck', label: 'Lab deck', href: 'projects/next-frequency/deck/' },
  { section: 'audit', label: 'Streaming audit', href: 'projects/generation-step-by-step/' },
  { section: 'report', label: 'Source report', href: 'report/' },
];

export interface Update { date: string; label: string; text: string; href: string; }

export const updates: Update[] = [
  { date: '2026-10-19', label: 'Lab deck', text: 'What we have learned so far: 15 slides plus a technical appendix, with speaker notes, PDF and PowerPoint.', href: 'projects/next-frequency/deck/' },
  { date: '2026-10-18', label: 'Sampler', text: 'Validated UniPC schedule: A1 FID-50K 13.75 → 9.46 with 46 network calls instead of 400. DCTdiff with the same solver: 8.68.', href: 'projects/next-frequency/#sampler' },
  { date: '2026-10-18', label: 'Maturity', text: 'A1 trained on from 146k to 250k steps: FID-50K 15.08 → 13.69, within 1.10× of DCTdiff, at 1.72× its training H100-hours.', href: 'projects/next-frequency/#ffhq' },
  { date: '2026-10-17', label: 'Matched run', text: 'FFHQ-64 at equal 3.34 H100-hours: A1 15.08 beats its joint control A0 at 18.49; DCTdiff 12.66.', href: 'projects/next-frequency/#ffhq' },
  { date: '2026-10-12', label: 'Audit', text: 'Streaming audit of 21 released checkpoints, with A1 placed in the same trajectory views.', href: 'projects/generation-step-by-step/' },
];
