#!/usr/bin/env python3
"""Shared-plane (z-fighting) scan of a .bbmodel file: pairs of cubes with a face in the same plane, facing the same
way, whose outlines overlap. Run on every build of a generated model (SKILL.md §0):

    python3 coplanar.py model.bbmodel [NAME_REGEX]     # only pairs where one cube's name matches (default: all)

Faces normal to z are checked for cubes turned about z only (their z faces stay in a z plane), faces normal to x / y
for unturned cubes. It knows nothing of texels: a match where one face is fully see-through (a decal's edge, a plate's
hidden part) can't flicker. Read each match against the paint; back-to-back faces (opposite directions) aren't
listed (they hide each other).
"""
import itertools, json, math, re, sys


def corners(e, axis):
    """The cube's outline in the plane normal to axis, as a convex quad (z: turned about z)."""
    a, b = [i for i in range(3) if i != axis]
    (f, t) = e['from'], e['to']
    pts = [(x, y) for x in (f[a], t[a]) for y in (f[b], t[b])]
    r = e.get('rotation') or [0, 0, 0]
    if axis == 2 and r[2]:
        o, th = e['origin'], math.radians(r[2])
        pts = [(o[0] + (x - o[0]) * math.cos(th) - (y - o[1]) * math.sin(th),
                o[1] + (x - o[0]) * math.sin(th) + (y - o[1]) * math.cos(th)) for x, y in pts]
    return [pts[0], pts[1], pts[3], pts[2]]


def apart(A, B):
    """Separating-axis test for two convex quads (touching edges count as apart)."""
    for P in (A, B):
        for i in range(4):
            (x0, y0), (x1, y1) = P[i], P[(i + 1) % 4]
            n = (y0 - y1, x1 - x0)
            a = [n[0] * x + n[1] * y for x, y in A]
            b = [n[0] * x + n[1] * y for x, y in B]
            if max(a) <= min(b) + 1e-6 or max(b) <= min(a) + 1e-6: return True
    return False


def main(path, pattern=None):
    els = json.load(open(path))['elements']
    rx = re.compile(pattern) if pattern else None
    out = []
    for a, b in itertools.combinations(els, 2):
        if rx and not (rx.search(a['name']) or rx.search(b['name'])): continue
        for axis in range(3):
            turned = lambda e: any((e.get('rotation') or [0, 0, 0])[i] for i in range(3) if i != 2 or axis != 2)
            if turned(a) or turned(b): continue
            for k, side in ((0, 'from'), (1, 'to')):
                if abs(a[side][axis] - b[side][axis]) < 1e-6 and not apart(corners(a, axis), corners(b, axis)):
                    out.append((a['name'], b['name'], 'xyz'[axis] + ('-' if k == 0 else '+'), a[side][axis]))
    for o in out: print(*o)
    if not out: print('no shared planes')


if __name__ == '__main__':
    main(*sys.argv[1:])
