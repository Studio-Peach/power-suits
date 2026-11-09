"""Cables (draft D) locked in: clear the texels of drafts A-C and of the old noise faces, keeping every pixel any
cube's face still uses. Writes final_clear.json [[x, y], ...].
Run in .scratch/armtex/ (reads final_source.json; the cleared texels go through a tex.edit clearRect).
"""
import json, math
s = json.load(open('final_source.json'))
def face_px(uv):
    u1, v1, u2, v2 = uv
    return {(x, y) for x in range(math.floor(min(u1, u2)), math.ceil(max(u1, u2)))
            for y in range(math.floor(min(v1, v2)), math.ceil(max(v1, v2)))}
used = set()
for c in s['cubes']:
    if c['box']:
        w, h, d = [math.floor(abs(c['t'][i] - c['f'][i]) + 1e-6) for i in range(3)]
        u, v = c['uvo'] or [0, 0]
        used |= {(x, y) for x in range(u, u + 2 * (w + d)) for y in range(v, v + d + h)}
    else:
        for f in c['faces'].values():
            if f: used |= face_px(f)
gone = set()
for d in ('A', 'B', 'C'):
    for (u, v, w, h) in s['drafts'][d].values():
        gone |= {(x, y) for x in range(u, u + w) for y in range(v, v + h)}
for faces in s['orig'].values():
    for uv in faces.values(): gone |= face_px(uv)
clear = sorted(gone - used)
json.dump(clear, open('final_clear.json', 'w'))
print('clear', len(clear), 'of', len(gone), '(kept in use:', len(gone & used), ')')
