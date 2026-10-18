"""Rearrange the saved A1 stage sheet and measure its displayed pixels.

The input has four cumulative stages in rows and eight samples in columns.
The output strip has eight samples in rows and four stages in columns, matching
the streaming report viewer. Tiles are copied without interpolation. Spectral
residuals use the same luma FFT bands and lower median as the original audit.
"""

import json
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "public/ours/ffhq64-a1-d256"
SOURCE = OUT / "stages-146k.png"
EDGES = (0.0, 0.0625, 0.125, 0.25, 0.5, 10.0)


def main() -> None:
    image = Image.open(SOURCE).convert("RGB")
    if image.size != (512, 256):
        raise ValueError(f"Expected 8×4 64-pixel stage sheet, got {image.size}")

    strip = Image.new("RGB", (256, 512))
    gallery = Image.new("RGB", (512, 256))
    stages = np.empty((8, 4, 64, 64, 3), dtype=np.float64)
    for sample in range(8):
        for stage in range(4):
            tile = image.crop((sample * 64, stage * 64, (sample + 1) * 64, (stage + 1) * 64))
            strip.paste(tile, (stage * 64, sample * 64))
            gallery.paste(tile, (((sample % 2) * 4 + stage) * 64, (sample // 2) * 64))
            stages[sample, stage] = np.asarray(tile, dtype=np.float64) / 255.0
    strip.save(OUT / "trajectory-146k.png")
    gallery.save(OUT / "gallery-146k.png")

    luma = np.einsum("nshwc,c->nshw", stages, (0.299, 0.587, 0.114))
    final = luma[:, -1]
    difference = np.fft.fft2(luma - final[:, None])
    final_fft = np.fft.fft2(final)
    f = np.fft.fftfreq(64)
    radius = np.hypot(f[:, None], f[None, :]) / 0.5
    bands = []
    commits = []
    for lower, upper in zip(EDGES[:-1], EDGES[1:]):
        mask = (radius >= lower) & (radius < upper) & (radius > 0)
        numerator = (np.abs(difference[:, :, mask]) ** 2).sum(axis=-1)
        denominator = (np.abs(final_fft[:, mask]) ** 2).sum(axis=-1)[:, None]
        per_sample = numerator / np.maximum(denominator, 1e-12)
        values = np.partition(per_sample, 3, axis=0)[3].tolist()
        bands.append(values)
        last_bad = max((index for index, value in enumerate(values) if value >= 0.1), default=-1)
        commits.append(None if last_bad == 3 else (last_bad + 2) / 4)

    view = {"bands": bands}
    run = {
        "key": "ours_a1_ffhq64",
        "label": "Ours A1 · FFHQ-64",
        "method": "Ours · A1",
        "prog": [0.25, 0.5, 0.75, 1.0],
        "views": {"guess": view, "state": view},
        "commits": {"guess": commits, "state": commits},
        "source": "Saved 146k PNG stage sheet; 8 samples; cumulative decoded prefix G0–G3",
    }
    (OUT / "spectral.json").write_text(json.dumps(run, indent=2) + "\n")


if __name__ == "__main__":
    main()
