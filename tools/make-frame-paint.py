"""Builds the frame's painted textures, one per dye and build (run after python3 tools/export-frame.py):

    uv run --with pillow python3 tools/make-frame-paint.py [--scope armour|helmet|frame] [outdir]

The frame's paint (design sec. 4d, frame step 7): right-clicking a suit with a dye paints it (PowerSuitEntity.paintWith).
As on the big suit (tools/make-paint-textures.py, whose dye ramps this reuses) painting is a palette swap: the iron
armour is drawn in the eight steel shades (model/art/frame_iron_art.py), and on the painted texels each shade becomes
the same step of the dye's ramp, so every dye keeps the plates' shading and wear marks.

Which texels take paint, by --scope (each includes the one before; the user picked helmet, the default, on 2026-11-14,
from in-game mockups .scratch/paint7/sheet.png: as on the big suit, armour and the helmet's shell; frame read busy, its
grain speckled in a colour):
  armour  the iron pieces (the ar_* cubes: breastplate, waist, hip block, arm pieces with their pauldrons, leg pieces)
  helmet  + the helmet's shell (ar_helmet, its gear layer ar_hx_layer: only their steel; the brow, visor and gear
          stay as they are)
  frame   + the bare frame's members (fr_* cubes: their own four greys W / V / U / G and the grain beside them, each
          mapped to the steel step nearest in lightness)
Slate, leather, copper, brass, glass, the engine and the tools never take paint. Texels are found through each cube's
faces, so the layout follows the model.
Output: textures/entity/paint/power_frame(_slim)_<dye>.png (PowerSuitModel picks one by the suit's paint and build).
"""
import argparse
import importlib.util
import json
import math
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
TEX = ROOT / 'src/main/resources/assets/power_suits/textures/entity'
BUILDS = {'power_frame': ROOT / 'model/power_frame.bbmodel', 'power_frame_slim': ROOT / 'model/power_frame_slim.bbmodel'}
HELMET = {'ar_helmet', 'ar_hx_layer'}
SCOPES = ('armour', 'helmet', 'frame')

spec = importlib.util.spec_from_file_location('paint', ROOT / 'tools/make-paint-textures.py')
paint = importlib.util.module_from_spec(spec)
spec.loader.exec_module(paint)
H = paint.H


def lightness(rgb):
    return paint.to_lch(rgb)[0]


STEEL_L = [lightness(H(c)) for c in paint.STEEL]


def nearest_step(rgb):
    """The steel step nearest in lightness (the frame's own greys onto the paint ramp)."""
    L = lightness(rgb)
    return min(range(len(STEEL_L)), key=lambda i: abs(STEEL_L[i] - L))


def painted(name, scope):
    if name in HELMET:
        return SCOPES.index(scope) >= 1
    if name.startswith('ar_'):
        return True
    return name.startswith('fr_') and scope == 'frame'


def texels(model, img, scope):
    """{texel: kind} for every painted cube's faces: 'steel' (armour, helmet) or 'member' (the frame's)."""
    sx, sy = img.width / model['resolution']['width'], img.height / model['resolution']['height']
    out = {}
    for e in model['elements']:
        if not painted(e['name'], scope):
            continue
        kind = 'member' if e['name'].startswith('fr_') else 'steel'
        for f in e['faces'].values():
            if f.get('texture') is None:
                continue
            u1, v1, u2, v2 = f['uv']
            for x in range(math.floor(min(u1, u2) * sx), math.ceil(max(u1, u2) * sx)):
                for y in range(math.floor(min(v1, v2) * sy), math.ceil(max(v1, v2) * sy)):
                    out[(x, y)] = kind
    return out


def members():
    """The frame members' greys (frame_model.py's W / V / U / G and the grain bar() puts beside them)."""
    # frame_model.py builds when imported: read its palette from the source instead
    src = (ROOT / 'model/art/frame_model.py').read_text()
    cols = set()
    for letter in 'WVUG':
        i = src.index(f"'{letter}': (0x")
        cols.add(tuple(int(v, 16) for v in src[i + 6:src.index(')', i)].split(', ')))
    return cols


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--scope', choices=SCOPES, default='helmet')
    ap.add_argument('outdir', nargs='?', default=str(TEX / 'paint'))
    args = ap.parse_args()
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    step = {H(c): i for i, c in enumerate(paint.STEEL)}
    member_greys = members()
    ramps = {dye: paint.FIXED.get(dye) or paint.ramp(main, rng) for dye, (main, rng) in paint.DYES.items()}
    for build, bbmodel in BUILDS.items():
        src = Image.open(TEX / f'{build}.png').convert('RGBA')
        sp = src.load()
        swap = {}
        for xy, kind in texels(json.load(open(bbmodel)), src, args.scope).items():
            x, y = xy
            if not (0 <= x < src.width and 0 <= y < src.height) or not sp[xy][3]:
                continue
            rgb = sp[xy][:3]
            if rgb in step:
                swap[xy] = step[rgb]
            elif kind == 'member' and min(sum(abs(a - b) for a, b in zip(rgb, g)) for g in member_greys) <= 24:
                swap[xy] = nearest_step(rgb)   # a member grey or its grain (a few steps off it)
        if len(swap) < 500:
            raise SystemExit(f'only {len(swap)} paintable texels in {build}: is it the frame texture?')
        print(build, args.scope, len(swap), 'paintable texels')
        for dye, r in ramps.items():
            im = src.copy()
            px = im.load()
            for xy, i in swap.items():
                px[xy] = H(r[i]) + (255,)
            im.save(outdir / f'{build}_{dye}.png')


if __name__ == '__main__':
    main()
