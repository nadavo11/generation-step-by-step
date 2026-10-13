export type EvidenceStatus = 'completed' | 'ongoing' | 'reported' | 'proposed';

export interface Metric {
  label: string;
  value: string;
  context: string;
}

export interface ResultRow {
  comparison: string;
  setting: string;
  result: string;
  interpretation?: string;
}

export interface Claim {
  text: string;
  evidence: string;
  status: EvidenceStatus;
}

export interface FigureData {
  src: string;
  alt: string;
  caption: string;
  credit?: string;
}

export interface Project {
  slug: string;
  title: string;
  category: string;
  contribution: string;
  status: EvidenceStatus;
  verdict: string;
  motivation: string;
  question: string;
  setup: string;
  metrics: Metric[];
  results: ResultRow[];
  relatedMethods: ResultRow[];
  interpretation: string;
  qualitative: string[];
  caveats: string[];
  nextExperiments: string[];
  claims: Claim[];
  figures: FigureData[];
  sourceNote: string;
}
