"""Pad B made final (per-face UV kept: no 38x21 box net fits even after clearing): one 9x11x10 box-UV block per shoulder (pad_r, pad_l mirrored, one shared net).
Clears the old 7-piece pads' nets (texels no other cube's net uses) and the draft rects, then paints the net in the
draft's steel recipe. Writes final_plan.json {clear: [[u,v,w,h]...], net: [u,v], hex, size}.
Run in .scratch/padblock/ (reads source2.json; writes final_plan.json for pad_block_final_apply.js). Pad B picked.
"""
import json, math, base64, io, random
from PIL import Image
s = json.loads(open('source2.json').read())
im = Image.open(io.BytesIO(base64.b64decode(s['tex'].split(',')[1]))).convert('RGBA')
W, H = im.size
def rects(c):
    if c['box']:
        w, h, d = [math.floor(abs(c['t'][i] - c['f'][i]) + 1e-6) for i in range(3)]
        u, v = c['uvo'] or [0, 0]
        return [(u, v, 2 * (w + d), d + h)]
    out = []
    for f in c['faces'].values():
        if f: out.append((math.floor(min(f[0], f[2])), math.floor(min(f[1], f[3])), math.ceil(abs(f[2] - f[0])), math.ceil(abs(f[3] - f[1]))))
    return out
old = [c for c in s['cubes'] if c['n'].startswith('pad_') or c['n'].startswith('pbkA') or c['n'].startswith('pbkC')]
keep = [c for c in s['cubes'] if c not in old]
cov = lambda cs: {(x, y) for c in cs for (u, v, w, h) in rects(c) for x in range(u, u + w) for y in range(v, v + h) if 0 <= x < W and 0 <= y < H}
kept, gone = cov(keep), cov(old)
clear = gone - kept
px = im.load()
for (x, y) in clear: px[x, y] = (0, 0, 0, 0)
json.dump({'clear': sorted(clear)}, open('final_plan.json', 'w'))
