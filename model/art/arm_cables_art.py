"""Machinery paint for the arm's under-armour blocks (2026-11-09, user: the noise should look like the underlying
machinery). Hand-drawn faces, 1 texel = 1 px, light from the viewer's upper left (the left arm gets the mirrored rects).
  upper_arm      7x15x6: front/back 7x15, outer/inner 6x15, ends 7x6. Rows 10-13 show between the pad (y 31.625) and
                 the gauntlet (27.625); the elbow pivot sits on the line between rows 12 and 13, in the middle of the
                 side faces (cols 2|3): the axle is drawn there.
  forearm_inner  6x8x5: front/back 6x8, sides 5x8, ends 6x5; rows 0-2 show when the elbow bends.
Drafts: A hydraulics (front piston, back hoses, side strut + axle), B servo (cable bundles, side gear motor),
C skeleton (I-beam bones with lightening holes, chrome tendons).
Writes plan.json {rects: {draft: {face_key: [u,v,w,h]}}, hex: {...}} for apply.js.
Picked 2026-11-09 (draft D). Run in .scratch/armtex/ after the drafts (writes plan_D.json; applied like arm_machinery_apply.js, switched with arm_machinery_use.js).
"""
import json, math, base64, io
from PIL import Image
P = {'.': '1a1d1f', ',': '25292c', '-': '2f3437', '=': '3b4246', 'g': '4c5559', 'G': '565f63', 'm': '6f797e',
     'M': '89939a', 'l': 'a2acb1', 'L': 'c8d0d3', 'c': 'cdcfcf', 'W': 'fbf8f0',
     'b': '6b4a24', 'B': '9c6b32', 'y': 'c99a4e', 'h': '141617', 'H': '34383c', 'r': '484d52', 'k': '2b2f33'}
D = {}
# ---------- D: B's cables without the servo (2026-11-09, user: none of A-C convinced, try B without the servo) ----------
# Rubber cables 2 px wide (lit left 'r', dark right 'k') in a deep channel '.', a slightly darker ring every 4th row,
# brass clamps; the upper arm's lower clamp (row 11) sits in the strip that shows between pad and gauntlet.
P.update({'r': '5b6167', 'k': '34383c', 'R': '474c51', 'K': '25292c'})
def cables(pattern, rows, clamps, ring_from=1):
    w = len(pattern)
    ring = pattern.replace('r', 'R').replace('k', 'K')
    return [('y' + 'B' * (w - 2) + 'b') if r in clamps else (ring if (r - ring_from) % 4 == 3 else pattern) for r in range(rows)]
D['D'] = {
 'ua_front': cables('.rk.rk.', 15, {4, 11}),
 'ua_back': cables('.rk.rk.', 15, {4, 11}),
 'ua_out': cables('rk..rk', 15, {4, 11}),
 'ua_in': cables('rk..rk', 15, {4, 11}),
 'ua_end': ['.......', '.rk.rk.', '.KK.KK.', '.rk.rk.', '.KK.KK.', '.......'],
 'fi_front': cables('rk..rk', 8, {2}),
 'fi_back': cables('rk..rk', 8, {2}),
 'fi_out': cables('rk.rk', 8, {2}),
 'fi_in': cables('rk.rk', 8, {2}),
 'fi_end': ['......', 'rk..rk', 'KK..KK', 'rk..rk', '......'],
}
SIZE = {'ua_front': (7, 15), 'ua_back': (7, 15), 'ua_out': (6, 15), 'ua_in': (6, 15), 'ua_end': (7, 6),
        'fi_front': (6, 8), 'fi_back': (6, 8), 'fi_out': (5, 8), 'fi_in': (5, 8), 'fi_end': (6, 5)}
for d, faces in D.items():
    for k, rows in faces.items():
        w, h = SIZE[k]
        assert len(rows) == h and all(len(r) == w for r in rows), (d, k, [len(r) for r in rows], len(rows))
# ---------- allocate in free texels ----------
s = json.load(open('source.json'))
im = Image.open(io.BytesIO(base64.b64decode(s['tex'].split(',')[1]))).convert('RGBA')
W, H = im.size
px = im.load()
used = [[px[x, y][3] > 0 for x in range(W)] for y in range(H)]
for c in s['cubes']:
    rs = []
    if c['box']:
        w, h, dd = [math.floor(abs(c['t'][i] - c['f'][i]) + 1e-6) for i in range(3)]
        u, v = c['uvo'] or [0, 0]; rs = [(u, v, 2 * (w + dd), dd + h)]
    else:
        rs = [(math.floor(min(f[0], f[2])), math.floor(min(f[1], f[3])), math.ceil(abs(f[2] - f[0])), math.ceil(abs(f[3] - f[1])))
              for f in c['faces'].values() if f]
    for (u, v, w, h) in rs:
        for y in range(max(0, v), min(H, v + h)):
            for x in range(max(0, u), min(W, u + w)): used[y][x] = True
def alloc(w, h):
    for v in range(H - h + 1):
        for u in range(W - w + 1):
            if all(not used[y][x] for y in range(v, v + h) for x in range(u, u + w)):
                for y in range(v, v + h):
                    for x in range(u, u + w): used[y][x] = True
                return [u, v, w, h]
    raise SystemExit(f'no room for {w}x{h}')
plan = {'rects': {}, 'hex': {}}
order = sorted(SIZE, key=lambda k: -SIZE[k][0] * SIZE[k][1])
for d, faces in D.items():
    plan['rects'][d] = {}
    for k in order:
        plan['rects'][d][k] = alloc(*SIZE[k])
        plan['hex'][d + ':' + k] = ''.join(P[ch] + 'ff' for r in faces[k] for ch in r)
json.dump(plan, open('plan_D.json', 'w'))
# preview: each draft's faces laid out, x12
cell = 12
prev = Image.new('RGB', (len(D) * 30 * cell, 16 * cell * 2 + 20), 'white')
for i, (d, faces) in enumerate(D.items()):
    x0 = i * 30 * cell; x = x0
    for k in ['ua_front', 'ua_back', 'ua_out', 'ua_in', 'fi_front', 'fi_back', 'fi_out', 'fi_in']:
        rows = faces[k]
        y0 = 0 if k.startswith('ua') else 16 * cell + 10
        if k == 'fi_front': x = x0
        for r, row in enumerate(rows):
            for c, ch in enumerate(row):
                col = tuple(int(P[ch][j:j + 2], 16) for j in (0, 2, 4))
                for yy in range(cell):
                    for xx in range(cell): prev.putpixel((x + c * cell + xx, y0 + r * cell + yy), col)
        x += (len(rows[0]) + 1) * cell
prev.save('/private/tmp/shots/armtex_faces_D.png')
print('ok', {d: plan['rects'][d]['ua_front'] for d in D})
