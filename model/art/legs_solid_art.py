"""Solid legs, draft G made final (2026-11-09, user: no feet of any kind, the lower legs flush blocks down to the ground
like the player's and other mobs'; no machine showing at the back of the thighs or shins).
Each leg is two iron blocks of one 9x8 footprint (x 1..10, z -4..4 on the right):
  thigh_r   y 12.625..23.625 (11 tall), in iron_thigh_r (right_leg); inflate 0.1 so its sides never share a plane with
            the shin's (the knee only turns about x, so x = 1 / 10 would stay coplanar and flicker while the leg bends)
  shin_r    y -0.375..11.625 (12 tall) down to the ground, in iron_shin_r (right_shin); the foot bone stays empty
  knee_r    7x4x6 machine block inside both (x 2..9, y 10.625..14.625, z -3..3), in frame_knee_r (right_shin): a dark
            1 px band at the knee that fills the gap when it bends
  hip_plate_r/l  7x3x11 iron on the hips bone (draft A's, y 25.525..28.525: 0.1 under the abdomen's top plane), in iron_hips
The left leg mirrors the right (same texels, u flipped). Paint: the pads' steel recipe (pad_block_drafts_art.py: rim row,
lit left columns, shaded right, steel ramp only so dye paint swaps it), the shin with a dark ground row; the knee in the
arms' cable recipe (torso_core_art.py). Clears the texels of the old legs (thigh/cap/shin/knee_joint/boot/hood pieces)
and the leg drafts (lgA_/lgB_/lgG_) that no surviving cube uses.
Run in .scratch/legs/ (source.json = live texture + cubes); writes plan.json for legs_solid_apply.js, preview.png.
"""
import json, math, base64, io, random, re
from PIL import Image
s = json.loads(open('source.json').read())
im = Image.open(io.BytesIO(base64.b64decode(s['tex'].split(',')[1]))).convert('RGBA')
W, H = im.size
OLD = re.compile(r'^(thigh_|cap_[cfb]_|shin_|knee_joint|boot_|hood_|lg[ABG]_)')
def rects(c):
    if c['box']:
        w, h, d = [math.floor(abs(c['t'][i] - c['f'][i]) + 1e-6) for i in range(3)]
        u, v = c['uvo'] or [0, 0]
        return [(u, v, 2 * (w + d), d + h)]
    return [(math.floor(min(f[0], f[2])), math.floor(min(f[1], f[3])), math.ceil(abs(f[2] - f[0])), math.ceil(abs(f[3] - f[1])))
            for f in c['faces'].values() if f]
old = [c for c in s['cubes'] if OLD.match(c['n'])]
keep = [c for c in s['cubes'] if not OLD.match(c['n'])]
cov = lambda cs: {(x, y) for c in cs for (u, v, w, h) in rects(c) for x in range(u, u + w) for y in range(v, v + h) if 0 <= x < W and 0 <= y < H}
kept = cov(keep)
clear = sorted(cov(old) - kept)
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
IRON = '2f3437'
rng = random.Random(11)
def side(w, h, ground=False):
    rows = []
    for y in range(h):
        row = []
        for x in range(w):
            if y == 0: c = 5 if x == 0 else 6                  # rim row catching the light
            elif ground and y == h - 1: c = 0                  # the lower leg's ground edge, darkest steel
            elif y == h - 1 or (ground and y == h - 2): c = 2  # shaded bottom row(s)
            elif x == 0: c = 5
            elif x == 1: c = 4
            elif x == w - 1: c = 1
            elif x == w - 2: c = 2
            else: c = 3
            row.append(S[c])
        rows.append(row)
    for _ in range(max(1, w * h // 40) if h > 5 else 0):        # a few 1 px wear marks
        x, y = rng.randrange(2, w - 2), rng.randrange(2, h - 3)
        rows[y][x] = S[4]
    rows[1][1] = S[7]                                          # highlight pixel in the lit corner
    return rows
def top(w, d):
    return [[S[6 if (x in (0, w - 1) or y in (0, d - 1)) else (5 if x == 1 else 4 if x == 2 else 2 if x == w - 2 else 3)]
             for x in range(w)] for y in range(d)]
flat = lambda w, h, c: [[c] * w for _ in range(h)]
C = {'.': '1a1d1f', 'r': '5b6167', 'k': '34383c', 'R': '474c51', 'K': '25292c'}
def cables(w, h):                                              # vertical rubber cables in dark channels
    pat = ('.rk' * w)[:w]
    return [[C[ch] for ch in (pat if y % 4 != 1 else pat.replace('r', 'R').replace('k', 'K'))] for y in range(h)]
F = {
    'thigh_north': side(9, 11), 'thigh_south': side(9, 11), 'thigh_east': side(8, 11), 'thigh_west': side(8, 11),
    'thigh_up': top(9, 8), 'thigh_down': flat(9, 8, IRON),
    'shin_north': side(9, 12, True), 'shin_south': side(9, 12, True), 'shin_east': side(8, 12, True), 'shin_west': side(8, 12, True),
    'shin_up': flat(9, 8, IRON), 'shin_down': flat(9, 8, IRON),
    'knee_north': cables(7, 4), 'knee_south': cables(7, 4), 'knee_east': cables(6, 4), 'knee_west': cables(6, 4),
    'knee_up': flat(7, 6, IRON), 'knee_down': flat(7, 6, IRON),
    'hip_north': side(7, 3), 'hip_south': side(7, 3), 'hip_east': side(11, 3), 'hip_west': side(11, 3),
    'hip_up': top(7, 11), 'hip_down': flat(7, 11, IRON)}
plan = {'clear': clear, 'rects': {}, 'hex': {}}
for k, rows in F.items():
    plan['rects'][k] = alloc(len(rows[0]), len(rows))
    plan['hex'][k] = ''.join(''.join(c + 'ff' for c in r) for r in rows)
json.dump(plan, open('plan.json', 'w'))
prev = Image.new('RGBA', (120, 60), (255, 255, 255, 255)); x = y = 0
for k, rows in F.items():
    w, h = len(rows[0]), len(rows)
    if x + w > 120: x, y = 0, y + 14
    for j, r in enumerate(rows):
        for i, c in enumerate(r): prev.putpixel((x + i, y + j), tuple(int(c[n:n + 2], 16) for n in (0, 2, 4)) + (255,))
    x += w + 2
prev.resize((960, 480), Image.NEAREST).save('preview.png')
print('cleared', len(clear), 'texels;', plan['rects'])
