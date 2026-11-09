"""Torso = machine core + armour on top (2026-11-09, user: the sides should show the underlying machine; the simple
limbs hang beside the torso like a player's arms, and armour sets (the built-in iron one first) go on top).
  torso_core  13x7x7 (x +-6.5, y 31.625..38.625, z -1..6), machine: rubber cables in channels + a brass clamp, like
              the arms' under-armour (arm_cables_art.py draft D). It starts at the breastplate's back face: a first build reaching
              into the breastplate (z -4) shared its top and bottom planes there and z-fought (zfight.mjs).
  bp_plate    15x7x6 (x +-7.5, z -7..-1), the iron breastplate: one block over the core's front, wrapping 1 px past
              its sides and 6 px back. Front = today's breastplate art (bp_main over bp_lower, chest edge columns).
Replaces chest (15x7x11), bp_main and the sloped bp_lower. Face orientation (Blockbench, as in a box-UV net):
east u2 = front, west u1 = front, up v2 = front.
Run in .scratch/chest/ (source.json = live texture + cubes); writes core_plan.json for torso_core_apply.js.
"""
import json, math, base64, io
from PIL import Image
s = json.loads(open('source.json').read())
im = Image.open(io.BytesIO(base64.b64decode(s['tex'].split(',')[1]))).convert('RGBA')
W, Hh = im.size
cubes = {c['n']: c for c in s['cubes']}
used = [[im.getpixel((x, y))[3] > 0 for x in range(W)] for y in range(Hh)]
for c in s['cubes']:
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
            if all(not used[y][x] for y in range(max(0, v - 1), min(Hh, v + h + 1)) for x in range(max(0, u - 1), min(W, u + w + 1))):
                for y in range(v, v + h):
                    for x in range(u, u + w): used[y][x] = True
                return [u, v, w, h]
    raise SystemExit(f'no room for {w}x{h}')
def face(n, f):
    uv = cubes[n]['faces'][f]
    x0, x1 = sorted([uv[0], uv[2]]); y0, y1 = sorted([uv[1], uv[3]])
    cr = im.crop((math.floor(x0), math.floor(y0), math.floor(x0) + math.floor(x1 - x0 + 1e-6), math.floor(y0) + math.floor(y1 - y0 + 1e-6)))
    if uv[0] > uv[2]: cr = cr.transpose(Image.FLIP_LEFT_RIGHT)
    if uv[1] > uv[3]: cr = cr.transpose(Image.FLIP_TOP_BOTTOM)
    return cr
def canvas(w, h): return Image.new('RGBA', (w, h), (0, 0, 0, 0))
def stack(imgs, horiz):
    out = canvas(sum(i.width for i in imgs) if horiz else max(i.width for i in imgs),
                 max(i.height for i in imgs) if horiz else sum(i.height for i in imgs)); o = 0
    for i in imgs:
        out.alpha_composite(i, (o, 0) if horiz else (0, o)); o += i.width if horiz else i.height
    return out
P = {'.': '1a1d1f', ',': '25292c', '-': '2f3437', 'g': '4c5559', 'b': '6b4a24', 'B': '9c6b32', 'y': 'c99a4e',
     'r': '5b6167', 'k': '34383c', 'R': '474c51', 'K': '25292c',
     '0': '22262e', '1': '3c424c', '2': '58606a', '3': '757c85', '4': '8a9097', '5': '9fa4a9', '6': 'cdcfcf', '7': 'fbf8f0'}
def px(rows):
    img = canvas(len(rows[0]), len(rows))
    for y, r in enumerate(rows):
        assert len(r) == len(rows[0]), rows
        for x, ch in enumerate(r): img.putpixel((x, y), tuple(int(P[ch][i:i + 2], 16) for i in (0, 2, 4)) + (255,))
    return img
def cables(pattern, rows, clamps):
    ring = pattern.replace('r', 'R').replace('k', 'K')
    return [('y' + 'B' * (len(pattern) - 2) + 'b') if r in clamps else (ring if r % 4 == 1 else pattern) for r in range(rows)]
F = {}
# ---- torso_core (machine)
F['core_east'] = px(cables('.rk.rk.', 7, {4}))
F['core_west'] = F['core_east'].transpose(Image.FLIP_LEFT_RIGHT)
F['core_up'] = px(['g' * 13] + ['g' + '-' * 11 + 'g' for _ in range(6)])
F['core_down'] = px(['.' * 13 for _ in range(7)])
F['core_north'] = px(['-' * 13 for _ in range(7)])
F['core_south'] = px(['-' * 13 for _ in range(7)])
# ---- bp_plate (iron breastplate)
bpN = stack([face('bp_main', 'north'), face('bp_lower', 'north').crop((0, 0, 13, 3))], False)
cN = face('chest', 'north')
F['bp_north'] = stack([cN.crop((0, 0, 1, 7)), bpN, cN.crop((14, 0, 15, 7))], True)
bpE = stack([face('bp_main', 'east'), face('bp_lower', 'east').crop((0, 0, 1, 3)).resize((2, 3))], False)
bpW = stack([face('bp_main', 'west'), face('bp_lower', 'west').crop((0, 0, 1, 3)).resize((2, 3))], False)
back4 = ['6666', '1433', '1333', '1343', '1333', '1333', '1222']        # rim row, shaded column where it meets the core
F['bp_east'] = stack([px(back4), bpE], True)
F['bp_west'] = stack([bpW, px([r[::-1] for r in back4])], True)
F['bp_south'] = px(['6' * 15] + ['1' + '2' * 13 + '1' for _ in range(5)] + ['1' * 15])
F['bp_up'] = px(['1' * 15, '5' + '3' * 13 + '2', '5' + '3' * 13 + '2', '5' + '4' * 13 + '2', '6' * 15, '7' + '6' * 14])
F['bp_down'] = px(['1' * 15 for _ in range(6)])
plan = {'rects': {}, 'hex': {}}
for k, img in F.items():
    plan['rects'][k] = alloc(img.width, img.height)
    plan['hex'][k] = img.tobytes().hex()
json.dump(plan, open('core_plan.json', 'w'))
prev = canvas(200, 40); x = 0; y = 0
for k, img in F.items():
    if x + img.width > 200: x, y = 0, y + 12
    prev.alpha_composite(img, (x, y)); x += img.width + 2
prev.resize((1600, 320), Image.NEAREST).save('core_preview.png')
print(plan['rects'])
