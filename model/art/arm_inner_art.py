"""Gauntlet back to its old size + an inner forearm block (2026-11-09, user: instead of extending the forearm, put
another block inside to be the forearm; the current one stays a gauntlet the size it was).
  forearm_r/l        back to 8x7x8 (y 20.625..27.625) with its old side faces (texels restored from source.json,
                     the snapshot before the two-block arms)
  forearm_inner_r/l  6x8x5 dark iron, x 8.5..14.5 (mirrored), y 22.625..30.625 (from inside the gauntlet to 2 px over
                     the elbow pivot), z -4..1 (centred on the pivot z -1.5): inside the upper arm (7x6) by 0.5 px on
                     every side, so the elbow is the upper arm over the inner forearm and no faces share a plane
Writes inner_plan.json: restore {rect: hex}, clear (the 8x10 grown-forearm rect), inner side/end rects + hex.
Run in .scratch/armblock/ (reads source.json + source2.json; writes inner_plan.json for arm_inner_apply.js).
"""
import json, math, base64, io, random
from PIL import Image
def load(p):
    s = json.load(open(p)); s = json.loads(s) if isinstance(s, str) else s
    return s, Image.open(io.BytesIO(base64.b64decode(s['tex'].split(',')[1]))).convert('RGBA')
old, old_im = load('source.json')
cur, im = load('source2.json')
W, H = im.size
of = {c['n']: c for c in old['cubes'] if c['n'] in ('forearm_r', 'forearm_l')}
restore = {}
for c in of.values():
    for k in ('north', 'south', 'east', 'west'):
        u1, v1, u2, v2 = c['faces'][k]
        u, v, w, h = min(u1, u2), min(v1, v2), abs(u2 - u1), abs(v2 - v1)
        restore[f'{u},{v},{w},{h}'] = old_im.crop((u, v, u + w, v + h)).tobytes().hex()
grown = [c for c in cur['cubes'] if c['n'] == 'forearm_r'][0]['faces']['north']
gu, gv = min(grown[0], grown[2]), min(grown[1], grown[3])
clear = [gu, gv, 8, 10]
def rects(c):
    if c['box']:
        w, h, d = [math.floor(abs(c['t'][i] - c['f'][i]) + 1e-6) for i in range(3)]
        u, v = c['uvo'] or [0, 0]
        return [(u, v, 2 * (w + d), d + h)]
    return [(math.floor(min(f[0], f[2])), math.floor(min(f[1], f[3])), math.ceil(abs(f[2] - f[0])), math.ceil(abs(f[3] - f[1])))
            for f in c['faces'].values() if f]
px = im.load()
used = [[px[x, y][3] > 0 for x in range(W)] for y in range(H)]
for c in cur['cubes']:
    for (u, v, w, h) in rects(c):
        if (u, v, w, h) == tuple(clear): continue
        for y in range(max(0, v), min(H, v + h)):
            for x in range(max(0, u), min(W, u + w)): used[y][x] = True
for key in restore:                                       # the restored rects are taken again
    u, v, w, h = map(int, key.split(','))
    for y in range(v, v + h):
        for x in range(u, u + w): used[y][x] = True
for y in range(gv, gv + 10):                              # the grown-forearm rect is free again
    for x in range(gu, gu + 8): used[y][x] = px[x, y][3] > 0 and False
def alloc(w, h):
    for v in range(H - h + 1):
        for u in range(W - w + 1):
            if all(not used[y][x] for y in range(v, v + h) for x in range(u, u + w)):
                for y in range(v, v + h):
                    for x in range(u, u + w): used[y][x] = True
                return [u, v]
    raise SystemExit(f'no room for {w}x{h}')
rng = random.Random(23)
IRON = ['2f3437'] * 6 + ['25292c'] * 3 + ['3b4246'] * 2 + ['1a1d1f'] * 2     # the upper arm's noise mix
side, end = alloc(6, 8), alloc(6, 5)
hexs = lambda rows: ''.join(c + 'ff' for r in rows for c in r)
json.dump({'restore': restore, 'clear': clear, 'side': side, 'end': end,
           'side_hex': hexs([[rng.choice(IRON) for _ in range(6)] for _ in range(8)]),
           'end_hex': hexs([[rng.choice(IRON) for _ in range(6)] for _ in range(5)])}, open('inner_plan.json', 'w'))
print('restore', list(restore), 'clear', clear, 'side', side, 'end', end)
