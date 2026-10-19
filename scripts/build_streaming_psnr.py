"""Derive native-resolution PSNR trajectories from the archived audit metrics.

Usage: python scripts/build_streaming_psnr.py --results /path/to/prior_intermediates/results
The public checkpoint JSONs contain median per-sample RGB RMSE in [0,1],
measured against each trajectory's own final image before display resizing.
The A1 row is measured from its saved 8-bit, native 64px PNG stage sheet.
"""

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SHEET = ROOT / 'public/ours/ffhq64-a1-d256/stages-146k.png'
OUTPUT = ROOT / 'public/streaming/psnr.json'
RUNS = [
    'cifar10_small', 'cifar10_mid', 'cifar10_mid_deep',
    'celeba64_small_ddim', 'celeba64_small_DPMSolver',
    'imgnet64_small', 'imgnet64_mid', 'imgnet64_mid_deep',
    'ffhq128_small', 'ffhq128_mid', 'ffhq128_mid_deep',
    'ffhq256_mid', 'ffhq512_mid', 'afhq512_mid',
    'far_base', 'far_large', 'far_huge',
    'dar_xl', 'flexvar_d24', 'var_d30', 'detailflow',
]
DATASETS = {'cifar10': 'CIFAR-10', 'celeba': 'CelebA', 'celeba64': 'CelebA', 'imgnet64': 'ImageNet',
            'ffhq128': 'FFHQ', 'ffhq256': 'FFHQ', 'ffhq512': 'FFHQ', 'afhq512': 'AFHQ'}


def psnr(rmse):
    return None if rmse == 0 else -20 * np.log10(rmse)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--results', type=Path, required=True)
    args = parser.parse_args()
    rows = []
    for key in RUNS:
        path = args.results / f'{key}.json'
        source = path.read_bytes()
        record = json.loads(source)
        method = record['method']
        view = 'x0' if method == 'DCTdiff' else 'pred' if method == 'FAR' else None
        metric = record['metrics'][view] if view else record['metrics']
        rmse = metric['rmse']
        assert metric['stat'] == 'median over samples'
        assert len(rmse) == (100 if method == 'DCTdiff' else 10 if method == 'FAR' else len(record['steps']))
        dataset = DATASETS.get(record['dataset'], 'ImageNet' if 'ImageNet' in record['dataset'] else record['dataset'])
        label = key.replace('_', ' ')
        if method == 'DCTdiff':
            label = key.split('_', 1)[1].replace('_', ' ')
        elif method == 'FAR':
            label = key.split('_')[1].upper()[0]
        else:
            label = record['model'].split('-', 1)[-1]
        rows.append({
            'key': key, 'method': method, 'label': label,
            'dataset': dataset, 'resolution': record['resolution'],
            'view': 'predicted RGB image' if method in ('DCTdiff', 'FAR') else 'decoded preview',
            'steps': len(rmse), 'progress': [(i + 1) / len(rmse) for i in range(len(rmse))],
            'psnr': [psnr(value) for value in rmse],
            'rmse': rmse, 'total_batch_seconds': record.get('sec_traj_batch'),
            'source_sha256': hashlib.sha256(source).hexdigest(),
        })

    sheet = np.asarray(Image.open(SHEET).convert('RGB'), dtype=np.float64) / 255
    assert sheet.shape == (256, 512, 3)
    stages = np.stack([[sheet[g*64:(g+1)*64, n*64:(n+1)*64] for g in range(4)] for n in range(8)])
    per_sample = np.sqrt(np.mean((stages - stages[:, -1:, ...]) ** 2, axis=(2, 3, 4)))
    # torch.median over eight samples chooses the lower median (4th sorted).
    rmse = np.partition(per_sample, 3, axis=0)[3].tolist()
    rows.append({
        'key': 'ours_a1_ffhq64', 'method': 'Ours A1', 'label': 'A1 D256',
        'dataset': 'FFHQ', 'resolution': 64, 'view': 'cumulative decoded prefix',
        'steps': 4, 'progress': [0.25, 0.5, 0.75, 1.0],
        'psnr': [psnr(value) for value in rmse], 'rmse': rmse,
        'total_batch_seconds': None,
        'source_sha256': hashlib.sha256(SHEET.read_bytes()).hexdigest(),
    })
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps({
        'definition': 'PSNR = -20 log10(median per-sample RGB RMSE), range [0,1], reference = same trajectory final image',
        'checkpoint_source': 'Archived prior_intermediates/results/*.json, native resolution before display resizing',
        'ours_source': 'Saved 8-bit 64px stages-146k.png; JPEG not used for measurement',
        'progress_note': 'Fraction of saved network calls or stages, not elapsed seconds. DCTdiff last predicted x0 is before the separate solver final output.',
        'runs': rows,
    }, separators=(',', ':')) + '\n')
    print(f'Wrote {OUTPUT}: {len(rows)} trajectories')


if __name__ == '__main__':
    main()
