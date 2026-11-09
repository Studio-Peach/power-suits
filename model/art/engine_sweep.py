#!/usr/bin/env python3
"""Sampled sweep for the frame's engine (frame_model.py, ENGINE): which head / arm / leg rotations put a moving box
into an engine part. The clearance check in frame_model.py sees the rest pose only; this turns the helmet (yaw +-50
about the neck, then pitch +-90; negative = looking down), the right arm (-120..60 about its shoulder) and the right
leg (+-60 about its hip) and samples points of every en_* cube (its own x lean applied) inside them.

Run: BUILD=wide HELMET=glass ENGINE=firebox FRAME_OUT=/tmp/f.bbmodel python3 model/art/frame_model.py
     python3 model/art/engine_sweep.py /tmp/f.bbmodel
Points of the core and the front pipes inside the chest box are skipped: the helmet sinks into the chest itself.
"""
import json, math, sys
def rx(p, a):
    c, s = math.cos(a), math.sin(a); x, y, z = p; return (x, y * c - z * s, y * s + z * c)
def ry(p, a):
    c, s = math.cos(a), math.sin(a); x, y, z = p; return (x * c + z * s, y, -x * s + z * c)
def pts(e, step=0.25):
    (x0, y0, z0), (x1, y1, z1) = e['from'], e['to']
    n = lambda a, b: [a + (b - a) * i / max(1, round((b - a) / step)) for i in range(max(1, round((b - a) / step)) + 1)]
    return [(x, y, z) for x in n(x0, x1) for y in n(y0, y1) for z in n(z0, z1)]
def rz(p, a):
    c, s = math.cos(a), math.sin(a); x, y, z = p; return (x * c - y * s, x * s + y * c, z)
def own(e, p):   # the element's own rotation about its origin (single-axis turns; x, then y, then z)
    r = e.get('rotation') or [0, 0, 0]
    if not any(r): return p
    o = e['origin']; q = [p[k] - o[k] for k in range(3)]
    q = rz(ry(rx(q, math.radians(r[0])), math.radians(r[1])), math.radians(r[2]))
    return tuple(q[k] + o[k] for k in range(3))
def inside(p, e, m=0.02):
    return all(e['from'][k] + m < p[k] < e['to'][k] - m for k in range(3))
for f in sys.argv[1:]:
    M = json.load(open(f)); E = {e['name']: e for e in M['elements']}
    G = {g['name']: g for g in M['groups']}
    eng = [e for e in M['elements'] if e['name'].startswith('en_')]
    P = [(e['name'], p) for e in eng for p in map(lambda q, e=e: own(e, q), pts(e)) if not (e['name'].startswith(('en_core', 'en_pipe_front')) and p[2] > -3.01)]   # inside the chest box: the helmet sinks into it anyway
    print('==', f)
    # helmet: yaw (neck) then pitch about the head pivot
    hp = G['head']['origin']; H = E['ar_helmet']; hits = {}
    for yaw in range(-50, 51, 10):
        for pit in range(-90, 91, 5):
            done = set()
            for n, p in P:
                if n in done: continue
                q = [p[k] - hp[k] for k in range(3)]
                q = rx(ry(q, -math.radians(yaw)), -math.radians(pit))
                if inside([q[k] + hp[k] for k in range(3)], H):
                    hits.setdefault(n, []).append((yaw, pit)); done.add(n)
    for n, l in sorted(hits.items()):
        ups = [p for y, p in l if p > 0]; dns = [p for y, p in l if p < 0]
        by = {}
        for y, p in l: by.setdefault(y, []).append(p)
        print(f'  helmet hits {n}:', '; '.join(f'yaw {y}: pitch {min(v)}..{max(v)}' for y, v in sorted(by.items()) if y >= 0))
    if not hits: print('  helmet: clear at yaw +-50, pitch +-90')
    for limb, parts, rng in (('right_arm', ['ar_arm_r', 'ar_pauldron_r', 'fr_arm_shell_r', 'fr_shoulder_plate_r'], range(-120, 61, 5)), ('right_leg', ['ar_leg_r', 'fr_leg_shell_r'], range(-60, 61, 5))):
        o = G[limb]['origin']; bad = []
        for a in rng:
            for n, p in P:
                q = rx([p[k] - o[k] for k in range(3)], -math.radians(a))
                if any(inside([q[k] + o[k] for k in range(3)], E[x]) for x in parts if x in E): bad.append((a, n)); break
        print(f'  {limb} swing hits:', sorted({a for a, _ in bad}) or 'none', sorted({n for _, n in bad}))
