"""Legs as machine + armour, like the arms (2026-11-10, user: give the thighs the treatment of the arms, an actual leg
with the armour on top, so armour sets can swap later). The iron blocks stay as they are (the iron set: thigh_r in
iron_thigh_r, shin_r in iron_shin_r); a machine leg goes inside them, built like the arm (upper arm 7x15x6 over an
inner forearm 6x8x5 reaching 2 px over the elbow):
  upper_leg_r  7x13x6, x 2..9, y 12.625..25.625 (knee pivot to inside the belt), z -3..3, in frame_thigh_r (right_leg)
  lower_leg_r  6x15x5, x 2.5..8.5, y -0.375..14.625 (ground to 2 px over the knee, inside the upper leg), z -2.5..2.5,
               inflate -0.05 (its bottom would share the iron shin's ground plane), in frame_shin_r (right_shin)
No faces share a plane: the upper leg sits 1.1 px inside the thigh armour (inflate 0.1) and 0.1 inside its ends, the
lower leg 0.5 px inside the upper leg. The lower leg replaces knee_r: its row 2 is the 1 px band between the iron pieces.
Painted in the arms' cable recipe (arm_cables_art.py, draft D: rubber cables in dark channels, brass clamps, the clamps
under the armour so the knee band keeps its look). The left leg mirrors the right (same texels, u flipped).
Run in .scratch/legs/ (source3.json = live texture + cubes); writes plan3.json for leg_frame_apply.js.
"""
import json, math, base64, io
from PIL import Image
s = json.loads(open('source3.json').read())
im = Image.open(io.BytesIO(base64.b64decode(s['tex'].split(',')[1]))).convert('RGBA')
W, H = im.size
def rects(c):
    if c['box']:
        w, h, d = [math.floor(abs(c['t'][i] - c['f'][i]) + 1e-6) for i in range(3)]
        u, v = c['uvo'] or [0, 0]
        return [(u, v, 2 * (w + d), d + h)]
    return [(math.floor(min(f[0], f[2])), math.floor(min(f[1], f[3])), math.ceil(abs(f[2] - f[0])), math.ceil(abs(f[3] - f[1])))
            for f in c['faces'].values() if f]
gone = [c for c in s['cubes'] if c['n'] in ('knee_r', 'knee_l')]
keep = [c for c in s['cubes'] if c not in gone]
cov = lambda cs: {(x, y) for c in cs for (u, v, w, h) in rects(c) for x in range(u, u + w) for y in range(v, v + h) if 0 <= x < W and 0 <= y < H}
kept = cov(keep)
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
P = {'.': '1a1d1f', 'r': '5b6167', 'k': '34383c', 'R': '474c51', 'K': '25292c', 'b': '6b4a24', 'B': '9c6b32', 'y': 'c99a4e'}
def cables(pattern, rows, clamps, ring_from=1):                # arm_cables_art.py
    w = len(pattern)
    ring = pattern.replace('r', 'R').replace('k', 'K')
    return [('y' + 'B' * (w - 2) + 'b') if r in clamps else (ring if (r - ring_from) % 4 == 3 else pattern) for r in range(rows)]
F = {
    'ul_north': cables('.rk.rk.', 13, {3, 9}), 'ul_south': cables('.rk.rk.', 13, {3, 9}),
    'ul_east': cables('rk..rk', 13, {3, 9}), 'ul_west': cables('rk..rk', 13, {3, 9}),
    'ul_up': ['.......', '.rk.rk.', '.KK.KK.', '.rk.rk.', '.KK.KK.', '.......'],
    'ul_down': ['.......', '.rk.rk.', '.KK.KK.', '.rk.rk.', '.KK.KK.', '.......'],
    # rows 0-2 sit inside the upper leg / show at the knee (row 2), the clamps hide under the iron shin
    'll_north': cables('rk..rk', 15, {6, 11}), 'll_south': cables('rk..rk', 15, {6, 11}),
    'll_east': cables('rk.rk', 15, {6, 11}), 'll_west': cables('rk.rk', 15, {6, 11}),
    'll_up': ['......', 'rk..rk', 'KK..KK', 'rk..rk', '......'],
    'll_down': ['......', 'rk..rk', 'KK..KK', 'rk..rk', '......']}
plan = {'clear': clear, 'rects': {}, 'hex': {}}
for k, rows in F.items():
    plan['rects'][k] = alloc(len(rows[0]), len(rows))
    plan['hex'][k] = ''.join(''.join(P[ch] + 'ff' for ch in r) for r in rows)
json.dump(plan, open('plan3.json', 'w'))
print('cleared', len(clear), 'texels;', plan['rects'])
