"""Import a lab deck built in learned-spectral-basis/reports/shai_deck into the site.

Copies the slide images (rendered by that repo's src/build_page.py), the PDF / PPTX / one-slide summary, and a few
figures into public/decks/<id>/, and writes src/data/deck-<date>.json with each slide's kicker, title and speaker
notes (read from the deck's own .pptx by build_page.py).

  python scripts/import_deck.py /path/to/learned-spectral-basis/reports/shai_deck
"""
import json
import re
import shutil
import sys
from pathlib import Path

DECK_ID, DATE = 'next-frequency-2026-10-19', '2026-10-19'


def main(src):
    src = Path(src)
    site = Path(__file__).resolve().parents[1]
    dst = site / 'public' / 'decks' / DECK_ID
    (dst / 'slides').mkdir(parents=True, exist_ok=True)
    (dst / 'figures').mkdir(exist_ok=True)
    for f in sorted((src / 'page' / 'slides').glob('*.jpg')):
        shutil.copy(f, dst / 'slides' / f.name)
    files = {'pdf': 'frequency_ar_shai_deck.pdf', 'pptx': 'frequency_ar_shai_deck.pptx', 'summary': 'executive_summary.pdf'}
    for name in files.values():
        shutil.copy(src / 'build' / name, dst / name)
    for name in ('frontier_abc.png', 'unipc_pareto.png', 'cifar_fid_vs_h100.png'):
        shutil.copy(src / 'figures' / 'plots' / name, dst / 'figures' / name)
    for k in range(4):   # worst-of-5k UniPC sample, cumulative G0 .. G0-G3 (the G3 tail artifact)
        shutil.copy(src / 'figures' / 'samples' / f'fail_0_g{k}.png', dst / 'figures' / f'tail-failure-g{k}.png')

    page = (src / 'page' / 'index.html').read_text()
    slides = json.loads(re.search(r'const SLIDES = (\[.*?\]);\n', page, re.S).group(1))
    for s in slides:
        s['img'] = f'decks/{DECK_ID}/' + s['img']
        if s['title'] == 'Technical appendix':
            s['kicker'] = 'APPENDIX'
    meta = {
        'id': DECK_ID, 'date': DATE,
        'title': 'Frequency-autoregressive image generation: what have we learned?',
        'occasion': 'Lab discussion with Prof. Shai Avidan',
        'mainSlides': 15,
        'files': {k: {'path': f'decks/{DECK_ID}/{v}', 'bytes': (dst / v).stat().st_size} for k, v in files.items()},
        'slides': slides,
    }
    out = site / 'src' / 'data' / f'deck-{DATE}.json'
    out.write_text(json.dumps(meta, ensure_ascii=False, indent=1) + '\n')
    print(out, len(slides), 'slides', {k: v['bytes'] for k, v in meta['files'].items()})


if __name__ == '__main__':
    main(sys.argv[1])
