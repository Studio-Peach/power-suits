"""Chest + collar as fewer, plainer blocks (2026-11-09 "minecraftier" pass; shapes only, art copied from today's faces).

Chest drafts (bone torso_armor; today: chest 15x7x11 + breastplate bp_main 13x4x2 + sloped bp_lower):
  A  one block 15x7x13 (x +-7.5, y 31.625..38.625, z -7..6): the breastplate and its slope only painted on the front
  B  chest + one flat 13x7x2 breastplate slab (z -7..-5), full height, no slope
  C  chest + bp_main + an 11x3x1 step (z -6..-5) under it instead of the sloped bp_lower
Collar drafts (today: 4 walls + gorget_lip):
  1  one solid 13x3x12 gorget block (x +-6.5, y 38.625..41.625, z -6..6), the neck well painted on its top
  2  the ring as it is minus the gorget lip (no new cube)     3  no collar (the chest top's painted well only)
Faces are composites of the current faces (crops in uv order), so A/B/C differ in shape, not in paint.
Run in .scratch/chest/ (reads source.json = live texture + cubes; writes plan.json for chest_block_drafts_apply.js).
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
    """A cube face's texels in uv order (u1 -> u2, v1 -> v2), whole texels."""
    uv = cubes[n]['faces'][f]
    x0, x1 = sorted([uv[0], uv[2]]); y0, y1 = sorted([uv[1], uv[3]])
    cr = im.crop((math.floor(x0), math.floor(y0), math.floor(x0) + math.floor(x1 - x0 + 1e-6), math.floor(y0) + math.floor(y1 - y0 + 1e-6)))
    if uv[0] > uv[2]: cr = cr.transpose(Image.FLIP_LEFT_RIGHT)
    if uv[1] > uv[3]: cr = cr.transpose(Image.FLIP_TOP_BOTTOM)
    return cr
def canvas(w, h): return Image.new('RGBA', (w, h), (0, 0, 0, 0))
def paste(dst, src, x, y, box=None):
    dst.alpha_composite(src.crop(box) if box else src, (x, y)); return dst
def stack_v(*imgs):
    out = canvas(max(i.width for i in imgs), sum(i.height for i in imgs)); y = 0
    for i in imgs: out.alpha_composite(i, (0, y)); y += i.height
    return out
def stack_h(*imgs):
    out = canvas(sum(i.width for i in imgs), max(i.height for i in imgs)); x = 0
    for i in imgs: out.alpha_composite(i, (x, 0)); x += i.width
    return out
def rows(img, n): return img.crop((0, 0, img.width, n))
F = {}
# ---- A: one 15x7x13 block
bpN = stack_v(face('bp_main', 'north'), rows(face('bp_lower', 'north'), 3))             # 13x7
cN = face('chest', 'north')
F['A_north'] = stack_h(cN.crop((0, 0, 1, 7)), bpN, cN.crop((14, 0, 15, 7)))
bpE = stack_v(face('bp_main', 'east'), rows(face('bp_lower', 'east'), 3).resize((2, 3)))  # 2x7 (lower one is 1.6 wide)
bpW = stack_v(face('bp_main', 'west'), rows(face('bp_lower', 'west'), 3).resize((2, 3)))
F['A_east'] = stack_h(face('chest', 'east'), bpE)        # east face: u2 end = front (checked on the render)
F['A_west'] = stack_h(bpW, face('chest', 'west'))
cU = face('chest', 'up')
F['A_up'] = stack_v(stack_h(cU.crop((0, 0, 1, 2)), face('bp_main', 'up'), cU.crop((14, 0, 15, 2))), cU)
cD = face('chest', 'down')
F['A_down'] = stack_v(cD, cD.crop((0, 0, 15, 2)))
F['A_south'] = face('chest', 'south')
# ---- B: flat 13x7x2 breastplate slab
F['B_north'] = bpN
F['B_east'], F['B_west'] = bpE, bpW
F['B_up'] = face('bp_main', 'up')
F['B_down'] = face('bp_main', 'down')
F['B_south'] = stack_v(face('bp_main', 'south'), face('bp_main', 'south').crop((0, 0, 13, 3)))
# ---- C: 11x3x1 step under bp_main
lN = rows(face('bp_lower', 'north'), 3)
F['C_north'] = lN.crop((1, 0, 12, 3))
F['C_east'] = rows(face('bp_lower', 'east'), 3).crop((0, 0, 1, 3))
F['C_west'] = rows(face('bp_lower', 'west'), 3).crop((0, 0, 1, 3))
F['C_up'] = face('bp_lower', 'up').crop((1, 0, 12, 1))
F['C_down'] = face('bp_lower', 'down').crop((1, 0, 12, 1))
F['C_south'] = F['C_north']
# ---- collar 1: solid 13x3x12 gorget block, fresh paint in the steel ramp + the chest top's well colours
S = ['22262e', '3c424c', '58606a', '757c85', '8a9097', '9fa4a9', 'cdcfcf', 'fbf8f0']
WELL, WELL_IN, WELL_RIM = '2f3437', '25292c', '4c5559'
def px(rows_): 
    img = canvas(len(rows_[0]), len(rows_))
    for y, r in enumerate(rows_):
        for x, c in enumerate(r): img.putpixel((x, y), tuple(int(c[i:i + 2], 16) for i in (0, 2, 4)) + (255,))
    return img
def side(w, h):
    return px([[S[6] if y == 0 else S[2] if y == h - 1 else S[5] if x == 0 else S[1] if x == w - 1 else S[3]
                for x in range(w)] for y in range(h)])
def well(w, d):
    out = []
    for z in range(d):
        r = []
        for x in range(w):
            e = min(x, w - 1 - x, z, d - 1 - z)
            r.append(S[6] if e == 0 else WELL_RIM if e == 1 else WELL if e == 2 else WELL_IN)
        out.append(r)
    return px(out)
F['G_north'] = side(13, 3); F['G_south'] = side(13, 3)
F['G_east'] = side(12, 3); F['G_west'] = side(12, 3)
F['G_up'] = well(13, 12)
F['G_down'] = px([[WELL] * 13 for _ in range(12)])
plan = {'rects': {}, 'hex': {}}
for k, img in F.items():
    plan['rects'][k] = alloc(img.width, img.height)
    plan['hex'][k] = img.tobytes().hex()
json.dump(plan, open('plan.json', 'w'))
prev = canvas(400, 200)
x = y = 0
for k, img in F.items():
    if x + img.width > 400: x, y = 0, y + 16
    prev.alpha_composite(img, (x, y)); x += img.width + 2
prev.resize((1600, 800), Image.NEAREST).save('plan_preview.png')
print({k: v for k, v in plan['rects'].items()})
