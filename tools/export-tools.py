#!/usr/bin/env python3
"""Builds standalone Blockbench source files and GeckoLib assets for every frame power tool.

Each tool is generated from its existing script in model/art/frame_<tool>_art.py with its socket at (0, 0, 0):

  model/tools/<tool>.bbmodel                                        (Blockbench source, one clean file per tool)
  assets/power_suits/geckolib/models/tool/<tool>.geo.json           (left arm / symmetric)
  assets/power_suits/geckolib/models/tool/<tool>_r.geo.json         (right arm, only for handed tools: drill, chainsaw, flamethrower)
  assets/power_suits/textures/tool/<tool>.png                       (compact 64x64 / 128x64 texture)
  assets/power_suits/textures/tool/<tool>_glow_<mask>.png           (only the glowmasks that tool actually uses)

Run: python3 tools/export-tools.py        (no dependencies; stdlib only)
"""
import base64, json, os, struct, sys, uuid, zlib

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
ASSETS = os.path.join(ROOT, 'src', 'main', 'resources', 'assets', 'power_suits')
OUT_BB = os.path.join(ROOT, 'model', 'tools')
sys.path.insert(0, os.path.join(ROOT, 'model', 'art'))

FACES = ('north', 'east', 'south', 'west', 'up', 'down')
HANDED = {'drill', 'chainsaw', 'flamethrower'}

_h = lambda v: tuple(int(v[i:i + 2], 16) for i in (0, 2, 4))
GLOW_MAPS = {
    'pilot':     {_h('1b2638'): _h('2a6cff'), _h('22304a'): _h('8ec2ff')},
    'lamp_idle': {_h('3d2622'): _h('ffb0a0'), _h('2e1915'): _h('e8402a')},
    'lamp_run':  {_h('3d2622'): _h('c8ffc0'), _h('2e1915'): _h('4fe05a')},
    'gun_light': {_h('c8ffc0'): _h('c8ffc0'), _h('3cf060'): _h('3cf060')},
    'em_core':   {_h('3a0e0c'): _h('7a0600'), _h('4b1310'): _h('b81206'), _h('5c1813'): _h('f0200c'), _h('701f17'): _h('ff6a4a')},
    'em_arc':    {_h('4e1411'): _h('c01206'), _h('621a14'): _h('ff2a14')},
    **{f'rail_flow_{n}': {_h(('1d3f5e', '1d3f6f', '1d3f7f')[n]): _h('2f9cff'), _h(('254e73', '254e74', '254e75')[n]): _h('a8f0ff')}
       for n in range(3)},
}


def r(v):
    v = round(v, 4)
    return int(v) if v == int(v) else v


def png(w, h, rows):
    raw = b''.join(b'\x00' + b''.join(bytes(p) for p in row) for row in rows)
    def chunk(t, d):
        return struct.pack('>I', len(d)) + t + d + struct.pack('>I', zlib.crc32(t + d) & 0xffffffff)
    return b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', w, h, 8, 6, 0, 0, 0)) + \
        chunk(b'IDAT', zlib.compress(raw, 9)) + chunk(b'IEND', b'')


def tool_specs():
    import frame_drill_art as drill_art
    import frame_saw_art as saw_art
    import frame_gun_art as gun_art
    import frame_flame_art as flame_art
    import frame_rail_art as rail_art
    import frame_tnt_art as tnt_art
    import frame_em_art as em_art

    glow = dict(GLOW_MAPS) | gun_art.HEAT_GLOW
    return [
        ('drill', ('drill', 'drill_bit'), {}, ('lamp_idle', 'lamp_run'),
         drill_art.build(0, 0, lamp='dark', art='B', mode='open', fit='sleeve_box', band='slate', head_scale=True), glow),
        ('chainsaw', ('chainsaw', 'chainsaw_chain'), {}, ('lamp_idle', 'lamp_run'),
         saw_art.build(0, 0, lamp='dark', kind='B', art='B', fins='A', cowl='slate', barrel='copper',
                       bar_shape='box', low='fins', look='rancher', sleeve=True, head_scale=True), glow),
        ('chaingun', ('chaingun', 'chaingun_barrels'), {}, ('gun_light', 'heat', 'heat_barrel'),
         gun_art.build(0, 0, lamp='dark', kind='A', body='ref', look='doom', barrels='4', handle='paint',
                       top_art='stack', drum='dark', body_h=4.0, barrel_l=5.0, accent='vents', heat='dark',
                       sleeve=True, head_scale=True), glow),
        ('flamethrower', ('flamethrower', 'flamethrower_bit'), {}, ('pilot',),
         flame_art.build(0, 0, kind='D', pilot='dark', glow='lit', body_art='pump', body_h=3.0, holes='even',
                         tank_h=4.0, tank_w=3.0, sleeve=True, head_scale=True), glow),
        ('rail_cannon', ('rail_cannon', 'rail_fork_out'), {'fork_in': 'rail_fork_in'},
         ('rail_flow_0', 'rail_flow_1', 'rail_flow_2'),
         rail_art.build(0, 0, 'dark', kind='ori_concave_channel', core='dark', length=6.0, sleeve=True, head_scale=True), glow),
        ('tnt_launcher', ('tnt_launcher', 'tnt_launcher_drum'), {}, (),
         tnt_art.build(0, 0, kind='wide', sleeve=True), glow),
        ('em_projector', ('em_projector', 'em_projector_poles'), {}, ('em_core', 'em_arc'),
         em_art.build(0, 0, kind='claw_b2', glow='dark', sleeve=True, head_scale=True), glow),
    ]


def pack_texture(parts):
    """Packs every non-transparent face of `parts` into the smallest power-of-two RGBA texture."""
    strips = []
    for p in parts:
        used_faces = [(f, p['faces'][f]) for f in FACES
                      if not all(c == '.' for row in p['faces'][f] for c in row)]
        if not used_faces:
            continue
        w = sum(len(rows[0]) for _, rows in used_faces)
        h = max(len(rows) for _, rows in used_faces)
        strips.append((p['name'], used_faces, w, h))

    # Try compact power-of-two canvas sizes
    for tw, th in ((64, 64), (128, 64), (128, 128), (256, 128)):
        u = v = rh = 0
        placed = {}
        ok = True
        for name, used_faces, w, h in sorted(strips, key=lambda s: -s[3]):
            if w > tw:
                ok = False
                break
            if u + w > tw:
                u, v, rh = 0, v + rh, 0
            if v + h > th:
                ok = False
                break
            fx = u
            for f, rows in used_faces:
                fw, fh = len(rows[0]), len(rows)
                placed[(name, f)] = (fx, v, fw, fh, rows)
                fx += fw
            u += w
            rh = max(rh, h)
        if ok:
            rows = [[(0, 0, 0, 0)] * tw for _ in range(th)]
            for _, (x0, y0, fw, fh, art) in placed.items():
                for j, line in enumerate(art):
                    for i, ch in enumerate(line):
                        if ch != '.':
                            rows[y0 + j][x0 + i] = ch
            return tw, th, rows, placed
    raise AssertionError('tool texture exceeded 256x128')


def build_bbmodel(name, bone_names, extra_bones, parts, tw, th, tex_bytes, placed, side='l'):
    """Builds a Blockbench .bbmodel dict with socket pivot at (0, 0, 0) for `side` ('l' left or 'r' right)."""
    s = 1 if side == 'r' else -1
    uid = lambda: str(uuid.uuid4())
    groups, elements = [], []

    def grp(gname, parent):
        g = {'name': gname, 'uuid': uid(), 'export': True, 'locked': False, 'scope': 0, 'selected': False,
             'visibility': True, 'origin': [0, 0, 0], 'rotation': [0, 0, 0], 'bedrock_binding': '', 'color': 0,
             'children': [], 'reset': False, 'shade': True, 'mirror_uv': False, 'autouv': 0, 'isOpen': True,
             'primary_selected': False}
        groups.append(g)
        if parent is not None:
            parent['children'].append(g)
        return g

    root = grp(bone_names[0], None)
    bones = {'tool': root, 'bit': grp(bone_names[1], root)}
    for k, bname in extra_bones.items():
        bones[k] = grp(bname, root)

    for tp in parts:
        g_ = bones[tp.get('bone', 'tool')]
        (x0, y0, z0), (x1, y1, z1) = tp['box']
        if side == 'l':
            x0, x1 = -x1, -x0
        e = {'name': f"tl_{name}_{tp['name']}", 'box_uv': False, 'render_order': 'default', 'locked': False,
             'export': True, 'scope': 0, 'allow_mirror_modeling': True,
             'from': [r(min(x0, x1)), r(min(y0, y1)), r(min(z0, z1))],
             'to': [r(max(x0, x1)), r(max(y0, y1)), r(max(z0, z1))],
             'autouv': 0, 'color': 1, 'origin': [0, 0, 0], 'faces': {}, 'type': 'cube', 'uuid': uid()}
        for f in FACES:
            src = f if side == 'r' else {'east': 'west', 'west': 'east'}.get(f, f)
            hit = placed.get((tp['name'], src))
            if hit is None:
                e['faces'][f] = {'uv': [0, 0, 0, 0], 'texture': None}
            else:
                u, v, fw, fh, _ = hit
                e['faces'][f] = {'uv': [u, v, u + fw, v + fh] if side == 'r' else [u + fw, v, u, v + fh], 'texture': 0}
        rot = tp.get('rot', 0)
        if rot:
            if isinstance(rot, (list, tuple)):
                rx, ry, rz = rot
                e['rotation'] = [r(rx), r(ry * s), r(rz * s)]
            else:
                e['rotation'] = [0, r(-rot * -s), 0]
            if tp.get('origin'):
                ox, oy, oz = tp['origin']
                e['origin'] = [r(ox * s), r(oy), r(oz)]
        elements.append(e)
        g_['children'].append(e['uuid'])

    def outliner(g):
        return {'uuid': g['uuid'], 'isOpen': True,
                'children': [outliner(c) if isinstance(c, dict) else c for c in g['children']]}

    flat_groups = [dict(g, children=[]) for g in groups]
    return {
        'meta': {'format_version': '5.0', 'model_format': 'bedrock', 'box_uv': False},
        'name': name, 'model_identifier': f'tool_{name}', 'visible_box': [1, 1, 0],
        'variable_placeholders': '', 'variable_placeholder_buttons': [], 'timeline_setups': [],
        'unhandled_root_fields': {}, 'resolution': {'width': tw, 'height': th},
        'elements': elements, 'groups': flat_groups, 'outliner': [outliner(root)],
        'textures': [{'path': '', 'name': f'{name}.png', 'folder': '', 'namespace': '', 'id': '0',
                      'group': '', 'width': tw, 'height': th, 'uv_width': tw, 'uv_height': th,
                      'particle': False, 'use_as_default': False, 'layers_enabled': False,
                      'sync_to_project': '', 'render_mode': 'default', 'render_sides': 'auto',
                      'pbr_channel': 'color', 'frame_time': 1, 'frame_order_type': 'loop',
                      'frame_order': '', 'frame_interpolate': False, 'visible': True, 'internal': True,
                      'saved': True, 'uuid': uid(), 'relative_path': f'{name}.png',
                      'source': 'data:image/png;base64,' + base64.b64encode(tex_bytes).decode()}],
    }


def to_geo(model, ident):
    """Converts a standalone tool .bbmodel dict to Bedrock/GeckoLib .geo.json (same codec as export-frame.py)."""
    groups = {g['uuid']: g for g in model['groups']}
    elements = {e['uuid']: e for e in model['elements']}
    bones = []

    def cube_json(e):
        fr, to = e['from'], e['to']
        cube = {'origin': [r(-to[0]), r(fr[1]), r(fr[2])], 'size': [r(to[i] - fr[i]) for i in range(3)]}
        rot = e.get('rotation') or [0, 0, 0]
        if any(rot):
            o = e['origin']
            cube['pivot'] = [r(-o[0]), r(o[1]), r(o[2])]
            cube['rotation'] = [r(-rot[0]), r(-rot[1]), r(rot[2])]
        uv = {}
        for f in FACES:
            fd = e['faces'].get(f)
            if fd is None or fd.get('texture') is None:
                continue
            u0, v0, u1, v1 = fd['uv']
            face = {'uv': [r(u0), r(v0)], 'uv_size': [r(u1 - u0), r(v1 - v0)]}
            if f in ('up', 'down'):
                face = {'uv': [r(u1), r(v1)], 'uv_size': [r(u0 - u1), r(v0 - v1)]}
            uv[f] = face
        cube['uv'] = uv
        return cube

    def walk(nodes, parent):
        for n in nodes:
            if isinstance(n, str):
                continue
            g = groups[n['uuid']]
            cubes = [elements[c] for c in n['children'] if isinstance(c, str)]
            b = {'name': g['name'], 'pivot': [r(-g['origin'][0]), r(g['origin'][1]), r(g['origin'][2])]}
            if parent:
                b['parent'] = parent
            if cubes:
                b['cubes'] = [cube_json(e) for e in cubes]
            bones.append(b)
            walk(n['children'], g['name'])

    walk(model['outliner'], None)
    tw, th = model['resolution']['width'], model['resolution']['height']
    return {'format_version': '1.12.0', 'minecraft:geometry': [{
        'description': {'identifier': 'geometry.' + ident, 'texture_width': tw, 'texture_height': th,
                        'visible_bounds_width': 2, 'visible_bounds_height': 2, 'visible_bounds_offset': [0, 0, 0]},
        'bones': bones,
    }]}


def write_file(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'wb') as f:
        f.write(data)
    print('wrote', os.path.relpath(path, ROOT), len(data), 'bytes')


def main():
    clear = (0, 0, 0, 0)
    rgba = lambda c: c if len(c) == 4 else c + (255,)
    for name, bone_names, extra_bones, mask_names, parts, glow_maps in tool_specs():
        tw, th, rows, placed = pack_texture(parts)
        tex_bytes = png(tw, th, rows)
        bb_l = build_bbmodel(name, bone_names, extra_bones, parts, tw, th, tex_bytes, placed, side='l')
        write_file(os.path.join(OUT_BB, f'{name}.bbmodel'), json.dumps(bb_l, indent=1).encode())
        write_file(os.path.join(ASSETS, 'geckolib', 'models', 'tool', f'{name}.geo.json'),
                   json.dumps(to_geo(bb_l, f'tool_{name}'), indent=1).encode())
        if name in HANDED:
            bb_r = build_bbmodel(name, bone_names, extra_bones, parts, tw, th, tex_bytes, placed, side='r')
            write_file(os.path.join(ASSETS, 'geckolib', 'models', 'tool', f'{name}_r.geo.json'),
                       json.dumps(to_geo(bb_r, f'tool_{name}_r'), indent=1).encode())
        write_file(os.path.join(ASSETS, 'textures', 'tool', f'{name}.png'), tex_bytes)
        for mname in mask_names:
            cmap = glow_maps[mname]
            mask = [[rgba(cmap[p[:3]]) if p[3] == 255 and p[:3] in cmap else clear for p in row] for row in rows]
            assert any(p != clear for row in mask for p in row), f'{name}: no texels for glowmask {mname}'
            write_file(os.path.join(ASSETS, 'textures', 'tool', f'{name}_glow_{mname}.png'), png(tw, th, mask))


if __name__ == '__main__':
    main()
