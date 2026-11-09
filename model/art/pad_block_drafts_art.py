"""Shoulder pad as ONE block (2026-11-09, user: the suit doesn't look minecrafty; simple models, detail in texture).
Drafts A/B/C = same 9 x 10 footprint (x 7.5..16.5 on the right, z -5..5, top 42.625), heights 9 / 11 / 14.
Painted in the pads' steel recipe (lit columns left, shaded right, rim row on top, shaded bottom row), per-face UV
rects in free texture space (no 38-px-wide box-UV net fits until the old pads' nets are freed).
Writes plan.json: {rects: {key: [u,v,w,h]}, hex: {key: rgba hex rows}}.
Run in .scratch/padblock/ (reads source.json: live texture + cubes; writes plan.json for pad_block_drafts_apply.js).
"""
import json, math, base64, io, random
from PIL import Image
s = json.loads(open('source.json').read())
im = Image.open(io.BytesIO(base64.b64decode(s['tex'].split(',')[1]))).convert('RGBA')
W, Hh = im.size
used = [[im.getpixel((x, y))[3] > 0 for x in range(W)] for y in range(Hh)]
for c in s['cubes']:
    if c['n'].startswith('tmpclip'): continue
    if c['box']:
        w, h, d = [math.floor(abs(c['t'][i] - c['f'][i]) + 1e-6) for i in range(3)]
        u, v = c['uvo'] or [0, 0]
        for y in range(v, min(Hh, v + d + h)):
            for x in range(u, min(W, u + 2 * (w + d))): used[y][x] = True
    else:
        for f in c['faces'].values():
            if not f: continue
            for y in range(math.floor(min(f[1], f[3])), math.ceil(max(f[1], f[3]))):
                for x in range(math.floor(min(f[0], f[2])), math.ceil(max(f[0], f[2]))):
                    if 0 <= x < W and 0 <= y < Hh: used[y][x] = True
def alloc(w, h):
    for v in range(Hh - h + 1):
        for u in range(W - w + 1):
            if all(not used[y][x] for y in range(v - 1 if v else v, min(Hh, v + h + 1)) for x in range(u, u + w)):
                for y in range(v, v + h):
                    for x in range(u, u + w): used[y][x] = True
                return [u, v, w, h]
    raise SystemExit(f'no room for {w}x{h}')
S = ['22262e', '3c424c', '58606a', '757c85', '8a9097', '9fa4a9', 'cdcfcf', 'fbf8f0']
IRON = '2f3437'
rng = random.Random(9)
def side(w, h):
    rows = []
    for y in range(h):
        row = []
        for x in range(w):
            if y == 0: c = 5 if x == 0 else 6                  # rolled rim catching the light
            elif y == h - 1: c = 2                             # shaded underside row
            elif x == 0: c = 5
            elif x == 1: c = 4
            elif x == w - 1: c = 1
            elif x == w - 2: c = 2
            else: c = 3
            row.append(S[c])
        rows.append(row)
    for _ in range(max(1, w * h // 40)):                       # a few 1 px wear marks
        x, y = rng.randrange(2, w - 2), rng.randrange(2, h - 2)
        rows[y][x] = S[4]
    rows[1][1] = S[7] if h > 3 else rows[1][1]                 # highlight pixel in the lit corner
    return rows
def top(w, d):
    rows = []
    for y in range(d):
        row = []
        for x in range(w):
            edge = x in (0, w - 1) or y in (0, d - 1)
            c = 6 if edge else (5 if x == 1 else 4 if x == 2 else 2 if x == w - 2 else 3)
            row.append(S[c])
        rows.append(row)
    return rows
plan = {'rects': {}, 'hex': {}}
def put(key, rows):
    h, w = len(rows), len(rows[0])
    plan['rects'][key] = alloc(w, h)
    plan['hex'][key] = ''.join(''.join(c + 'ff' for c in r) for r in rows)
put('up', top(9, 10))
put('down', [[IRON] * 9 for _ in range(10)])
for name, H in (('A', 9), ('B', 11), ('C', 14)):
    put(name + '_ns', side(9, H))
    put(name + '_ew', side(10, H))
json.dump(plan, open('plan.json', 'w'))
print(plan['rects'])
