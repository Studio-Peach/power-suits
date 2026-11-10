"""Legs straight into the belt (2026-11-10, user: Minecraft mobs have no hip axle; the legs connect directly to the
waist / belt). Removes hip_axle + hip_axle_top (and their texels) and grows each thigh up to the belt: thigh_r
y 12.625..25.625 (13 tall, was 11; inflate 0.1), its top 0.2 inside the hip plates (y 25.525..28.525). Swinging, the
thigh's top corners stay inside the plate (they're 5.14 px from the hip axis: under the plate's top 28.525 and its
z +-5.5); its outer 3 px (past the plate's x 7.25) rise beside it.
Repaints the thigh's four sides 13 rows tall in the same recipe (legs_solid_art.py side()); top and bottom kept.
Run in .scratch/legs/ (source2.json = live texture + cubes); writes plan2.json for hip_join_apply.js.
"""
import json, math, base64, io, random, re
from PIL import Image
s = json.loads(open('source2.json').read())
im = Image.open(io.BytesIO(base64.b64decode(s['tex'].split(',')[1]))).convert('RGBA')
W, H = im.size
cubes = {c['n']: c for c in s['cubes']}
def rects(c, only=None):
    if c['box']:
        w, h, d = [math.floor(abs(c['t'][i] - c['f'][i]) + 1e-6) for i in range(3)]
        u, v = c['uvo'] or [0, 0]
        return [(u, v, 2 * (w + d), d + h)]
    return [(math.floor(min(f[0], f[2])), math.floor(min(f[1], f[3])), math.ceil(abs(f[2] - f[0])), math.ceil(abs(f[3] - f[1])))
            for k, f in c['faces'].items() if f and (only is None or k in only)]
SIDES = ('north', 'south', 'east', 'west')
gone = [(cubes['hip_axle'], None), (cubes['hip_axle_top'], None), (cubes['thigh_r'], SIDES), (cubes['thigh_l'], SIDES)]
cov = lambda pairs: {(x, y) for c, only in pairs for (u, v, w, h) in rects(c, only) for x in range(u, u + w) for y in range(v, v + h) if 0 <= x < W and 0 <= y < H}
kept_pairs = [(c, None) for c in s['cubes'] if c['n'] not in ('hip_axle', 'hip_axle_top', 'thigh_r', 'thigh_l')]
kept_pairs += [(cubes['thigh_r'], ('up', 'down')), (cubes['thigh_l'], ('up', 'down'))]
kept = cov(kept_pairs)
clear = sorted(cov(gone) - kept)
px = im.load()
for (x, y) in clear: px[x, y] = (0, 0, 0, 0)
used = [[px[x, y][3] > 0 or (x, y) in kept for x in range(W)] for y in range(H)]
def alloc(w, h):
    for v in range(H - h + 1):
        for u in range(W - w + 1):
            if all(not used[y][x] for y in range(max(0, v - 1), min(H, v + h + 1)) for x in range(max(0, u - 1), min(W, u + w + 1))):
                for y in range(v, v + h):
                    for x in range(u, u + w): used[y][x] = True
                return [u, v, w, h]
    raise SystemExit(f'no room for {w}x{h}')
S = ['22262e', '3c424c', '58606a', '757c85', '8a9097', '9fa4a9', 'cdcfcf', 'fbf8f0']
rng = random.Random(11)
def side(w, h):                                                # legs_solid_art.py's recipe
    rows = []
    for y in range(h):
        row = []
        for x in range(w):
            if y == 0: c = 5 if x == 0 else 6
            elif y == h - 1: c = 2
            elif x == 0: c = 5
            elif x == 1: c = 4
            elif x == w - 1: c = 1
            elif x == w - 2: c = 2
            else: c = 3
            row.append(S[c])
        rows.append(row)
    for _ in range(max(1, w * h // 40)):
        x, y = rng.randrange(2, w - 2), rng.randrange(2, h - 3)
        rows[y][x] = S[4]
    rows[1][1] = S[7]
    return rows
F = {'thigh_north': side(9, 13), 'thigh_south': side(9, 13), 'thigh_east': side(8, 13), 'thigh_west': side(8, 13)}
plan = {'clear': clear, 'rects': {}, 'hex': {}}
for k, rows in F.items():
    plan['rects'][k] = alloc(len(rows[0]), len(rows))
    plan['hex'][k] = ''.join(''.join(c + 'ff' for c in r) for r in rows)
json.dump(plan, open('plan2.json', 'w'))
print('cleared', len(clear), 'texels;', plan['rects'])
