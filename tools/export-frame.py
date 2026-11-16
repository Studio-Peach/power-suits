#!/usr/bin/env python3
"""Exports the frame (model/power_frame.bbmodel, the wide Steve build, and power_frame_slim.bbmodel, Alex's) into the
mod as GeckoLib files, without Blockbench (the frame is script-built: model/art/frame_model.py writes the .bbmodels):

  geckolib/models/entity/power_frame.geo.json, power_frame_slim.geo.json
  textures/entity/power_frame.png, power_frame_slim.png (the opaque texels; see-through ones are alpha 0)
  textures/entity/power_frame_glass(_slim).png (only the partly see-through texels: the helmet's visor glass)
  textures/entity/power_frame_glow_visor(_slim).png (the visor's glowmask: the glass texels, opaque white)
  textures/entity/power_frame_glow_fire(_slim).png (the engine's fire: the reserved coal colours of
      tools/make-glowmasks.py, painted dark in the texture (frame_model.py FIRE=dark), each lit to its glow colour)
  textures/entity/power_frame_glow_core(_slim).png (the same texels in white -> grey: the tidal engine's and the star
      reactor's light on the heart until they have frame art, tinted in their own colours)
  textures/entity/power_frame_glow_robot_<face>(_slim).png: the robot helmet's visor faces (robot_faces below)
  textures/entity/power_frame_glow_<light>(_slim).png for the tools' lights (TOOL_GLOW below): the flamethrower's pilot
      light, the status lamp red (idle) and green (running), the chaingun's green muzzle lights
  geckolib/animations/entity/power_frame.animation.json
  geckolib/models/view/frame_arm.geo.json, frame_arm_slim.geo.json (the cockpit's right arm, below)
  geckolib/models/view/frame_tool.geo.json, frame_tool_slim.geo.json (the cockpit's socket tool, below)

Run: python3 tools/export-frame.py        (no dependencies)

The geometry follows Blockbench's own Bedrock exporter (Codecs.bedrock): x negated on pivots / origins / rotations
(GeckoLib negates it back), cube origin = its corner at (-to.x, from.y, from.z), per-face UVs as [u, v] + size with the
up and down faces flipped (their uv at the far corner, a negative size). `--check model.bbmodel geo.json` compares this
exporter with a Blockbench export of the same model, cube by cube (run on the big suit, 2026-11-14: identical).

The glass is split out of the texture because the frame is drawn in a cutout pass (a texel is drawn opaque or not at
all): the glass gets a translucent pass of its own (client/HelmetGlassLayer), drawn over the pilot's face, and the
visor's light is drawn over the glass (SuitGlowLayer).

What the game needs that the design file doesn't hold:
- The pilot (st_* cubes) is left out: the game draws the player's own skin with vanilla's player model parts at the
  pilot_* bones (client/PilotLayer). Those bones are moved to where vanilla's part pivots sit relative to their part's
  box (head: the bottom centre, body and legs: the top centre, arms 2 px under the top, 1 px in from the inner side),
  so a vanilla part drawn at the bone with no offset of its own covers the st_* cube exactly. Moving a pivot of a bone
  with no rotation and no cubes changes nothing else.
- `right_hand`: the grip where the pilot's held item is drawn (HeldItemLayer), in the right fist.
- Draft groups (proto_*) never ship (GeckoLib would draw them, hidden or not).

The cockpit's arm (client/CockpitHands): the right arm bone's cubes (its shell and shoulder plate) under one bone
`view_arm`, moved so the pilot's arm pivot (pilot_right_arm, vanilla's) is the origin; since the armour (frame step
6c) its bare frame and its piece under it as `frame_right_arm` / `armor_right_arm`, shown by what's worn. The cockpit draws his skin arm
where vanilla draws a player's empty hand and this round it: one transform for both.

The cockpit's tool arm (client/CockpitHands): the left arm's shell and shoulder plate and every tool bone (with its
moving parts, the same names as on the frame, so the run animations play there too) under one bone `view_tool`, moved
so the pilot's left arm pivot (pilot_left_arm, vanilla's) is the origin, like the right arm's: the cockpit draws his
left arm where vanilla draws a left hand and this round it, the tool at its end.

The animation file holds every animation name the suit's controllers ask for (SuitAnimator, the tools' run loops).
The frame is posed in code (PowerSuitRenderer), so an animation keying any bone the frame hasn't (the big suit's body,
elbows, feet) is written empty: that keeps GeckoLib's controllers and their states (hold the last frame, loop, play
once) as they were without moving a bone. One keying only the frame's bones is kept as it is: the tools' run loops
(drill_run spins drill_bit, chainsaw_run runs chainsaw_chain), whose bones the frame names the same.
"""
import base64, json, os, struct, sys, zlib

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
        if g['name'] == 'right_arm':   # (its shell may sit in a frame_right_arm group: ARMOR=game)
            shell = next(c for c in model['elements'] if c['name'] == 'fr_arm_shell_r')
            x = (shell['from'][0] + shell['to'][0]) / 2
            bones.append({'name': 'right_hand', 'parent': 'right_arm', 'pivot': [r(-x), GRIP_Y, 0]})
    res = model['resolution']
    return {'format_version': '1.12.0', 'minecraft:geometry': [{
        'description': {'identifier': 'geometry.' + ident, 'texture_width': res['width'], 'texture_height': res['height'],
                        'visible_bounds_width': 3, 'visible_bounds_height': 3.5, 'visible_bounds_offset': [0, 1.25, 0]},
        'bones': bones}]}


def arm_parts(bones, arm, root, shift):
    """An arm bone's cubes for the cockpit: its own under the view's root bone, its bare frame's and its armour piece's
    (ARMOR=game: frame_<arm> / armor_<arm>, which the cockpit shows by what's worn, client/ArmourBones) as child bones of
    the same names, every cube moved by `shift`."""
    def moved(cubes):
        out = []
        for c in json.loads(json.dumps(cubes)):
            c['origin'] = shift(c['origin'])
            if 'pivot' in c:
                c['pivot'] = shift(c['pivot'])
            out.append(c)
        return out
    parts = [{'name': root, 'pivot': [0, 0, 0], 'cubes': moved(bones[arm].get('cubes', []))}]
    for name in (f'frame_{arm}', f'armor_{arm}'):
        if name in bones:
            parts.append({'name': name, 'parent': root, 'pivot': [0, 0, 0], 'cubes': moved(bones[name].get('cubes', []))})
    return parts


def arm_view(model, ident):
    """The right arm's cubes about the pilot's arm pivot (see the docstring)."""
    built = geo(model, ident)['minecraft:geometry'][0]
    bones = {b['name']: b for b in built['bones']}
    px, py, pz = bones['pilot_right_arm']['pivot']   # geo axes (x negated), like the cubes' origins
    shift = lambda v: [r(v[0] - px), r(v[1] - py), r(v[2] - pz)]
    built['description'] = dict(built['description'], identifier='geometry.' + ident,
                                visible_bounds_width=2, visible_bounds_height=2, visible_bounds_offset=[0, 0, 0])
    built['bones'] = arm_parts(bones, 'right_arm', 'view_arm', shift)
    return {'format_version': '1.12.0', 'minecraft:geometry': [built]}


TOOL_BONES = ('drill', 'chainsaw', 'chaingun', 'flamethrower', 'rail_cannon', 'tnt_launcher', 'em_projector')


def tool_view(model, ident):
    """The left arm and its tools about the pilot's left arm pivot (see the docstring)."""
    built = geo(model, ident)['minecraft:geometry'][0]
    keep, bones = set(TOOL_BONES), []
    by_name = {b['name']: b for b in built['bones']}
    for b in built['bones']:
        if b['name'] in keep or b.get('parent') in keep:
            keep.add(b['name'])
            bones.append(json.loads(json.dumps(b)))
    sx, sy, sz = by_name['pilot_left_arm']['pivot']
    shift = lambda v: [r(v[0] - sx), r(v[1] - sy), r(v[2] - sz)]
    for b in bones:
        b['pivot'] = shift(b['pivot'])
        if b['name'] in TOOL_BONES:
            b['parent'] = 'view_tool'
        for c in b.get('cubes', []):
            c['origin'] = shift(c['origin'])
            if 'pivot' in c:
                c['pivot'] = shift(c['pivot'])
    built['description'] = dict(built['description'], identifier='geometry.' + ident,
                                visible_bounds_width=2, visible_bounds_height=2, visible_bounds_offset=[0, 0, 0])
    built['bones'] = arm_parts(by_name, 'left_arm', 'view_tool', shift) + bones
    return {'format_version': '1.12.0', 'minecraft:geometry': [built]}


def animations(bones):
    names = json.load(open(SUIT_ANIMS))['animations']
    out = {}
    for name, a in names.items():
        if a.get('bones') and set(a['bones']) <= bones:
            out[name] = a
            continue
        empty = {'animation_length': a.get('animation_length', 0.05), 'bones': {}}
        if 'loop' in a:
            empty['loop'] = a['loop']
        out[name] = empty
    return {'format_version': '1.8.0', 'animations': out}


def unpng(data):
    """An 8-bit RGBA PNG (what frame_model.py writes) -> (width, height, rows of RGBA tuples)."""
    pos, idat, head = 8, b'', None
    while pos < len(data):
        n, t = struct.unpack('>I4s', data[pos:pos + 8])
        if t == b'IHDR':
            head = struct.unpack('>IIBBBBB', data[pos + 8:pos + 8 + 13])
        elif t == b'IDAT':
            idat += data[pos + 8:pos + 8 + n]
        pos += 12 + n
    w, h, depth, ctype = head[:4]
    assert depth == 8 and ctype == 6, head   # RGBA
    raw, rows, prev, stride = zlib.decompress(idat), [], bytearray(w * 4), w * 4
    for y in range(h):
        f, line = raw[y * (stride + 1)], bytearray(raw[y * (stride + 1) + 1:(y + 1) * (stride + 1)])
        for x in range(stride):
            a = line[x - 4] if x >= 4 else 0
            b, c = prev[x], (prev[x - 4] if x >= 4 else 0)
            if f == 1: line[x] = (line[x] + a) & 255
            elif f == 2: line[x] = (line[x] + b) & 255
            elif f == 3: line[x] = (line[x] + (a + b) // 2) & 255
            elif f == 4:
                pa, pb, pc = abs(b - c), abs(a - c), abs(a + b - 2 * c)
                line[x] = (line[x] + (a if pa <= pb and pa <= pc else b if pb <= pc else c)) & 255
        rows.append([tuple(line[i:i + 4]) for i in range(0, stride, 4)])
        prev = line
    return w, h, rows


def png(w, h, rows):
    raw = b''.join(b'\x00' + b''.join(bytes(p) for p in row) for row in rows)
    def chunk(t, d): return struct.pack('>I', len(d)) + t + d + struct.pack('>I', zlib.crc32(t + d) & 0xffffffff)
    return b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', w, h, 8, 6, 0, 0, 0)) + \
        chunk(b'IDAT', zlib.compress(raw, 9)) + chunk(b'IEND', b'')


# The fire's reserved coal colours (tools/make-glowmasks.py GLOW, 'fire') -> their glow colours.
FIRE = {(0x3f, 0x21, 0x1b): (0xff, 0xdc, 0x6e), (0x37, 0x1d, 0x19): (0xff, 0x96, 0x32), (0x2f, 0x1a, 0x17): (0xd2, 0x46, 0x19)}


# The tools' lights (client/SuitGlowLayer FRAME_TOOL_MASKS): mask name -> {texel colour: glow colour}.
_h = lambda v: tuple(int(v[i:i + 2], 16) for i in (0, 2, 4))
TOOL_GLOW = {
    'pilot': {_h('1b2638'): _h('2a6cff'), _h('22304a'): _h('8ec2ff')},   # make-glowmasks.py's pilot colours
    'lamp_idle': {_h('3d2622'): _h('ffb0a0'), _h('2e1915'): _h('e8402a')},   # frame_drill_art LAMPS dark -> red
    'lamp_run': {_h('3d2622'): _h('c8ffc0'), _h('2e1915'): _h('4fe05a')},    # ... -> green
    'gun_light': {_h('c8ffc0'): _h('c8ffc0'), _h('3cf060'): _h('3cf060')},  # the chaingun's green lights, as painted
    # the EM projector's lens and vents (em_core) and pole tips (em_arc): frame_em_art's reserved dark reds -> the big suit's lit ones
    'em_core': {_h('3a0e0c'): _h('7a0600'), _h('4b1310'): _h('b81206'), _h('5c1813'): _h('f0200c'), _h('701f17'): _h('ff6a4a')},
    'em_arc': {_h('4e1411'): _h('c01206'), _h('621a14'): _h('ff2a14')},
    # the rail cannon's core in three bands along the prongs (frame_rail_art.CORE dark colours -> the lit blue / hot white)
    **{f'rail_flow_{n}': {_h(('1d3f5e', '1d3f6f', '1d3f7f')[n]): _h('2f9cff'), _h(('254e73', '254e74', '254e75')[n]): _h('a8f0ff')}
       for n in range(3)},
}


def textures(data):
    """The texture split (see the docstring): opaque, glass, the visor's glowmask, the fire's glowmask."""
    w, h, rows = unpng(data)
    glass = lambda p: 0 < p[3] < 255
    clear = (0, 0, 0, 0)
    opaque = [[clear if glass(p) else p for p in row] for row in rows]
    panes = [[p if glass(p) else clear for p in row] for row in rows]
    visor = [[(255, 255, 255, 255) if glass(p) else clear for p in row] for row in rows]
    fire = [[FIRE[p[:3]] + (255,) if p[3] == 255 and p[:3] in FIRE else clear for p in row] for row in rows]
    lit = sum(p != clear for row in fire for p in row)
    assert lit, 'no fire texels: build the saved files with the engine (ENGINE=heart, FIRE=dark)'
    grey = {k: (v,) * 3 for k, v in zip(FIRE, (255, 225, 190))}   # hottest -> coolest, as the fire's yellow -> red
    core = [[grey[p[:3]] + (255,) if p[3] == 255 and p[:3] in FIRE else clear for p in row] for row in rows]
    tools = {}
    for name, colours in TOOL_GLOW.items():
        mask = [[colours[p[:3]] + (255,) if p[3] == 255 and p[:3] in colours else clear for p in row] for row in rows]
        assert any(p != clear for row in mask for p in row), f'no {name} texels: build the saved files with every tool (TOOL=all, LAMP=dark)'
        tools[name] = png(w, h, mask)
    return png(w, h, opaque), png(w, h, panes), png(w, h, visor), png(w, h, fire), png(w, h, core), tools


def robot_faces(model, data):
    """The robot helmet's visor faces (model/art/frame_helmet_art.py ROBOT_FACES; client/SuitGlowLayer, entity/SuitFace):
    one glowmask each, its texels white on the robot helmet's front face (the visor's colour tints them)."""
    sys.path.insert(0, os.path.join(ROOT, 'model', 'art'))
    import frame_helmet_art
    w, h, _ = unpng(data)
    helm = [e for e in model['elements'] if e['name'] == 'ar_helmet_robot']
    assert len(helm) == 1, 'no robot helmet: build the saved files with it (HELMET_VARIANTS ...,robot)'
    u0, v0 = (int(round(x)) for x in helm[0]['faces']['north']['uv'][:2])
    out = {}
    for name in frame_helmet_art.ROBOT_FACES:
        grid = frame_helmet_art.robot_face(name)
        mask = [[(0, 0, 0, 0)] * w for _ in range(h)]
        for j, row in enumerate(grid):
            for i, c in enumerate(row):
                if c == '#':
                    mask[v0 + j][u0 + i] = (255, 255, 255, 255)
        out[name] = png(w, h, mask)
    return out


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
        arm = ident.replace('power_frame', 'frame_arm')
        write(f'geckolib/models/view/{arm}.geo.json', json.dumps(arm_view(model, arm), indent=1).encode())
        tool = ident.replace('power_frame', 'frame_tool')
        write(f'geckolib/models/view/{tool}.geo.json', json.dumps(tool_view(model, tool), indent=1).encode())
        source = model['textures'][0]['source']
        opaque, glass, visor, fire, core, tools = textures(base64.b64decode(source.split(',', 1)[1]))
        slim = ident[len('power_frame'):]
        write(f'textures/entity/{ident}.png', opaque)
        write(f'textures/entity/power_frame_glass{slim}.png', glass)
        write(f'textures/entity/power_frame_glow_visor{slim}.png', visor)
        write(f'textures/entity/power_frame_glow_fire{slim}.png', fire)
        write(f'textures/entity/power_frame_glow_core{slim}.png', core)
        for name, mask in tools.items():
            write(f'textures/entity/power_frame_glow_{name}{slim}.png', mask)
        for name, mask in robot_faces(model, base64.b64decode(source.split(',', 1)[1])).items():
            write(f'textures/entity/power_frame_glow_robot_{name}{slim}.png', mask)
    bones = {b['name'] for b in geo(json.load(open(os.path.join(ROOT, BUILDS['power_frame']))), 'x')['minecraft:geometry'][0]['bones']}
    anims = animations(bones)
    write('geckolib/animations/entity/power_frame.animation.json', json.dumps(anims, indent=1).encode())
    print('kept animations:', ', '.join(k for k, v in anims['animations'].items() if v['bones']))
