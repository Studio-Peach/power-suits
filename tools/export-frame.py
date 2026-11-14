#!/usr/bin/env python3
"""Exports the frame (model/power_frame.bbmodel, the wide Steve build, and power_frame_slim.bbmodel, Alex's) into the
mod as GeckoLib files, without Blockbench (the frame is script-built: model/art/frame_model.py writes the .bbmodels):

  geckolib/models/entity/power_frame.geo.json, power_frame_slim.geo.json
  textures/entity/power_frame.png, power_frame_slim.png
  geckolib/animations/entity/power_frame.animation.json

Run: python3 tools/export-frame.py        (no dependencies)

The geometry follows Blockbench's own Bedrock exporter (Codecs.bedrock): x negated on pivots / origins / rotations
(GeckoLib negates it back), cube origin = its corner at (-to.x, from.y, from.z), per-face UVs as [u, v] + size with the
up and down faces flipped (their uv at the far corner, a negative size). `--check model.bbmodel geo.json` compares this
exporter with a Blockbench export of the same model, cube by cube (run on the big suit, 2026-11-14: identical).

What the game needs that the design file doesn't hold:
- The pilot (st_* cubes) is left out: the game draws the player's own skin with vanilla's player model parts at the
  pilot_* bones (client/PilotLayer). Those bones are moved to where vanilla's part pivots sit relative to their part's
  box (head: the bottom centre, body and legs: the top centre, arms 2 px under the top, 1 px in from the inner side),
  so a vanilla part drawn at the bone with no offset of its own covers the st_* cube exactly. Moving a pivot of a bone
  with no rotation and no cubes changes nothing else.
- `right_hand`: the grip where the pilot's held item is drawn (HeldItemLayer), in the right fist.
- Draft groups (proto_*) never ship (GeckoLib would draw them, hidden or not).

The animation file holds every animation name the suit's controllers ask for (SuitAnimator, the tools' run loops),
each empty: the frame is posed in code (PowerSuitRenderer), and an empty animation keeps GeckoLib's controllers and
their states (hold the last frame, loop, play once) as they were without moving a bone.
"""
import base64, json, os, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
ASSETS = os.path.join(ROOT, 'src', 'main', 'resources', 'assets', 'power_suits')
BUILDS = {'power_frame': 'model/power_frame.bbmodel', 'power_frame_slim': 'model/power_frame_slim.bbmodel'}
# The old suit's animation file: the names the controllers use (kept so the code needn't change per model).
SUIT_ANIMS = os.path.join(ASSETS, 'geckolib', 'animations', 'entity', 'power_suit.animation.json')


def r(v):
    """Numbers as Blockbench writes them: whole numbers without a fraction, the rest rounded to 4 places."""
    v = round(v, 4)
    return int(v) if v == int(v) else v


def outline(model):
    """The outliner as (group, parent name, [elements]) in order; groups may be inline dicts (old files) or refs."""
    groups = {g['uuid']: g for g in model.get('groups', [])}
    elements = {e['uuid']: e for e in model['elements']}
    out = []

    def walk(children, parent):
        for c in children:
            if isinstance(c, str):
                continue
            g = groups.get(c['uuid'], c)
            cubes = [elements[x] for x in c.get('children', []) if isinstance(x, str)]
            out.append((g, parent, cubes))
            walk(c.get('children', []), g['name'])
    walk(model['outliner'], None)
    return out


def cube_json(e):
    fr, to = e['from'], e['to']
    cube = {'origin': [r(-to[0]), r(fr[1]), r(fr[2])], 'size': [r(to[i] - fr[i]) for i in range(3)]}
    if e.get('inflate'):
        cube['inflate'] = r(e['inflate'])
    rot = e.get('rotation') or [0, 0, 0]
    if any(rot):
        o = e['origin']
        cube['pivot'] = [r(-o[0]), r(o[1]), r(o[2])]
        cube['rotation'] = [r(-rot[0]), r(-rot[1]), r(rot[2])]
    if e.get('box_uv'):
        cube['uv'] = [r(x) for x in e.get('uv_offset', [0, 0])]
        if e.get('mirror_uv'):
            cube['mirror'] = True
        return cube
    uv = {}
    for name in ('north', 'east', 'south', 'west', 'up', 'down'):
        f = e['faces'].get(name)
        if f is None or f.get('texture') is None:
            continue   # a face with no texture isn't drawn (the frame's all see-through faces)
        u0, v0, u1, v1 = f['uv']
        face = {'uv': [r(u0), r(v0)], 'uv_size': [r(u1 - u0), r(v1 - v0)]}
        if name in ('up', 'down'):
            face = {'uv': [r(u1), r(v1)], 'uv_size': [r(u0 - u1), r(v0 - v1)]}
        if f.get('rotation'):
            face['uv_rotation'] = f['rotation']
        uv[name] = face
    cube['uv'] = uv
    return cube


# Vanilla's player parts: where each part's box sits relative to its pivot, in the model's (Blockbench) axes (vanilla's
# are y-down and x-mirrored: drawn through scale(-1, -1, 1)). pivot = box corner - offset: the x of the box's low
# corner, its top or bottom y, its centre z.
def vanilla_pivot(bone, cube):
    fr, to = cube['from'], cube['to']
    if bone == 'pilot_head':
        return [(fr[0] + to[0]) / 2, fr[1], (fr[2] + to[2]) / 2]      # bottom centre (the neck)
    if bone in ('pilot_torso', 'pilot_right_leg', 'pilot_left_leg'):
        return [(fr[0] + to[0]) / 2, to[1], (fr[2] + to[2]) / 2]      # top centre
    if bone == 'pilot_right_arm':
        return [fr[0] + 1, to[1] - 2, (fr[2] + to[2]) / 2]            # vanilla: box x -3..1 (wide) / -2..1 (slim)
    if bone == 'pilot_left_arm':
        return [to[0] - 1, to[1] - 2, (fr[2] + to[2]) / 2]            # mirrored: -1..3 / -1..2
    raise ValueError(bone)


# The right fist's grip (HeldItemLayer draws the item there as vanilla's ItemInHandLayer does at a hand): the middle of
# the fist block under his hand (the arm box's last 4 px, raw y 10..14 = built 12..16), so the item comes out of it.
GRIP_Y = 14


def geo(model, ident):
    bones, drafts = [], set()
    for g, parent, cubes in outline(model):
        if g['name'].startswith('proto_') or parent in drafts:
            drafts.add(g['name'])
            continue
        o = g['origin']
        pivot = list(o)
        kept = [c for c in cubes if not c['name'].startswith('st_')]
        pilot = [c for c in cubes if c['name'].startswith('st_')]
        if g['name'].startswith('pilot_'):
            assert len(pilot) == 1 and not kept, g['name']
            pivot = vanilla_pivot(g['name'], pilot[0])
        bone = {'name': g['name']}
        if parent:
            bone['parent'] = parent
        bone['pivot'] = [r(-pivot[0]), r(pivot[1]), r(pivot[2])]
        rot = g.get('rotation') or [0, 0, 0]
        if any(rot):
            bone['rotation'] = [r(-rot[0]), r(-rot[1]), r(rot[2])]
        if kept:
            bone['cubes'] = [cube_json(c) for c in kept]
        bones.append(bone)
        if g['name'] == 'right_arm':
            shell = next(c for c in kept if c['name'].startswith('fr_arm_shell'))
            x = (shell['from'][0] + shell['to'][0]) / 2
            bones.append({'name': 'right_hand', 'parent': 'right_arm', 'pivot': [r(-x), GRIP_Y, 0]})
    res = model['resolution']
    return {'format_version': '1.12.0', 'minecraft:geometry': [{
        'description': {'identifier': 'geometry.' + ident, 'texture_width': res['width'], 'texture_height': res['height'],
                        'visible_bounds_width': 3, 'visible_bounds_height': 3.5, 'visible_bounds_offset': [0, 1.25, 0]},
        'bones': bones}]}


def animations():
    names = json.load(open(SUIT_ANIMS))['animations']
    out = {}
    for name, a in names.items():
        empty = {'animation_length': a.get('animation_length', 0.05), 'bones': {}}
        if 'loop' in a:
            empty['loop'] = a['loop']
        out[name] = empty
    return {'format_version': '1.8.0', 'animations': out}


def write(rel, data):
    path = os.path.join(ASSETS, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'wb') as f:
        f.write(data)
    print('wrote', os.path.relpath(path, ROOT), len(data), 'bytes')


def check(bbmodel, geo_file):
    """Compares cube_json with a Blockbench export, cube by cube (matched by bone and position)."""
    model = json.load(open(bbmodel))
    exported = {}
    for b in json.load(open(geo_file))['minecraft:geometry'][0]['bones']:
        for c in b.get('cubes', []):
            exported[(b['name'], tuple(c['origin']), tuple(c['size']))] = c
    same = diff = missing = 0
    for g, _, cubes in outline(model):
        for e in cubes:
            mine = cube_json(e)
            theirs = exported.get((g['name'], tuple(mine['origin']), tuple(mine['size'])))
            if theirs is None:
                missing += 1
            elif json.dumps(theirs, sort_keys=True) == json.dumps(mine, sort_keys=True):
                same += 1
            else:
                diff += 1
                if diff <= 3:
                    print('differs:', e['name'], '\n  bb  ', json.dumps(theirs, sort_keys=True), '\n  mine', json.dumps(mine, sort_keys=True))
    print(f'{same} identical, {diff} different, {missing} not in the export (changed since)')
    return diff == 0


if __name__ == '__main__':
    if len(sys.argv) == 4 and sys.argv[1] == '--check':
        sys.exit(0 if check(sys.argv[2], sys.argv[3]) else 1)
    for ident, rel in BUILDS.items():
        model = json.load(open(os.path.join(ROOT, rel)))
        write(f'geckolib/models/entity/{ident}.geo.json', json.dumps(geo(model, ident), indent=1).encode())
        source = model['textures'][0]['source']
        write(f'textures/entity/{ident}.png', base64.b64decode(source.split(',', 1)[1]))
    write('geckolib/animations/entity/power_frame.animation.json', json.dumps(animations(), indent=1).encode())
