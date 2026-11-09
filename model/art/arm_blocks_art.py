"""Arms as two overlapping blocks (2026-11-09, user: replace the upper core + elbow joint pieces with two blocks that
overlap; no complex joint). Per arm:
  upper_arm  7x15x7, x 8..15 (mirrored), y 26.625..41.625 (from inside the pad to 2 px under the elbow pivot),
             z -5..2 (centred on the elbow pivot z -1.5): dark iron noise like the old upper core (under-armour)
  forearm    the gauntlet grown 3 px up: y 20.625..30.625 (2 px over the pivot), x 7.5..15.5, z -5.5..2.5, so the
             upper arm's end sits inside it 0.5 px from every side and the elbow never opens a gap (-25..90 deg)
Removes upper_core_*, elbow_joint*, elbow_arc_*; clears their texels (not shared with other nets).
Writes plan.json: clear, upper arm side/end rects + hex, forearm side rect + hex (shared by the 4 sides; left
mirrored), keeps the forearms' up/down faces (the left's down face = socket coupling).
Run in .scratch/armblock/ (reads source.json; writes plan.json for arm_blocks_apply.js). The grown forearm was undone the same day by arm_inner_art.py.
"""
import json, math, base64, io, random
from PIL import Image
s = json.load(open('source.json'))
im = Image.open(io.BytesIO(base64.b64decode(s['tex'].split(',')[1]))).convert('RGBA')
W, H = im.size
def rects(c):
    if c['box']:
        w, h, d = [math.floor(abs(c['t'][i] - c['f'][i]) + 1e-6) for i in range(3)]
        u, v = c['uvo'] or [0, 0]
        return [(u, v, 2 * (w + d), d + h)]
    return [(math.floor(min(f[0], f[2])), math.floor(min(f[1], f[3])), math.ceil(abs(f[2] - f[0])), math.ceil(abs(f[3] - f[1])))
            for f in c['faces'].values() if f]
GONE = lambda n: n.startswith('upper_core_') or n.startswith('elbow_joint') or n.startswith('elbow_arc_')
# the forearms' side rects are replaced too (their up/down rects stay)
fore = {c['n']: c for c in s['cubes'] if c['n'] in ('forearm_r', 'forearm_l')}
old_sides = [(math.floor(min(f[0], f[2])), math.floor(min(f[1], f[3])), 8, 6) for c in fore.values()
             for k, f in c['faces'].items() if k in ('north', 'south', 'east', 'west')]
keep = [c for c in s['cubes'] if not GONE(c['n']) and c['n'] not in fore]
keep_rects = [r for c in keep for r in rects(c)] + [r for c in fore.values() for k, f in c['faces'].items() if k in ('up', 'down')
                                                    for r in [(math.floor(min(f[0], f[2])), math.floor(min(f[1], f[3])), 8, 8)]]
cov = lambda rs: {(x, y) for (u, v, w, h) in rs for x in range(u, u + w) for y in range(v, v + h) if 0 <= x < W and 0 <= y < H}
kept = cov(keep_rects)
gone = cov([r for c in s['cubes'] if GONE(c['n']) for r in rects(c)] + old_sides)
clear = gone - kept
px = im.load()
for (x, y) in clear: px[x, y] = (0, 0, 0, 0)
used = [[px[x, y][3] > 0 or (x, y) in kept for x in range(W)] for y in range(H)]
def alloc(w, h):
    for v in range(H - h + 1):
        for u in range(W - w + 1):
            if all(not used[y][x] for y in range(v, v + h) for x in range(u, u + w)):
                for y in range(v, v + h):
                    for x in range(u, u + w): used[y][x] = True
                return [u, v]
    raise SystemExit(f'no room for {w}x{h}')
rng = random.Random(11)
IRON = ['2f3437'] * 6 + ['25292c'] * 3 + ['3b4246'] * 2 + ['1a1d1f'] * 2     # the old upper core's noise mix
# no 28x22 box-UV net fits the fragmented texture: per-face UV, one 7x15 rect for the 4 sides, one 7x7 for top/bottom
up_side, up_end = alloc(7, 15), alloc(7, 7)
side_net = [[rng.choice(IRON) for _ in range(7)] for _ in range(15)]
end_net = [[rng.choice(IRON) for _ in range(7)] for _ in range(7)]
S = ['22262e', '3c424c', '58606a', '757c85', '8a9097', '9fa4a9', 'cdcfcf', 'fbf8f0']
band = ['23322335', '22222225', '11111111']           # the gauntlet's bands, as painted on forearm_r
side = ['33333335'] + band * 3                       # a plain lip on top, then three bands (10 rows)
fs = alloc(8, 10)
hexs = lambda rows: ''.join(('00000000' if c is None else c + 'ff') for r in rows for c in r)
json.dump({'clear': sorted(clear), 'up_side': up_side, 'up_side_hex': hexs(side_net), 'up_end': up_end, 'up_end_hex': hexs(end_net),
           'fside': fs, 'fside_hex': hexs([[S[int(ch)] for ch in r] for r in side])}, open('plan.json', 'w'))
print('cleared', len(clear), 'upper at', up_side, up_end, 'forearm side at', fs)
