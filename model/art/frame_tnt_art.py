"""The TNT launcher for the frame (frame_model.py, TOOL=tnt): the sixth power tool brought over from the big suit.

2026-11-22 2D-layer rework (user picked R2-A: '2d_mgl_closed'): rebuilt in the approved 2D-texture + 0.5 px cutout
outer-layer design system (6 cubes, 9.0 px overall, 64x64 standalone texture via tools/export-tools.py) with a closed
mechanical rotary drum (zero exposed vanilla TNT textures, so resource packs never clash):
- 6x1.5x6 dark gunmetal 2-layer breech cuff (`cuff_outer` cutout shell over `cuff_inner` 5x1.5x5) with recessed
  yellow/black demolition hazard warning stripes;
- 6x3.0x6 closed deeply-fluted turning mechanical drum (`drum_outer` cutout ribs over `drum_inner` 5x3.0x5, bone 'bit'
  / tnt_launcher_drum): twin 0.5 px vertical cylinder flutes per face around a dark center rib + 4 recessed dark-bore
  breech sockets on down (90-degree symmetric for ToolRotors quarter-turn per shot);
- offset 3.0x4.5x3.0 dark blued-gunmetal mortar tube wrapped in a 0.5 px proud 4.0x4.5x4.0 iron-steel perforated MGL
  cooling heat-shield jacket with integrated top sight posts, yellow/black demolition hazard collar, and heavy dark
  muzzle brake (9.0 px total, muzzleInsetPixels 0).

Other 2026-11-22 2D-layer drafts kept as knobs:
- Round 2 closed drums: 2d_tf2_closed, 2d_mgl_clean, 2d_octo_closed;
- Round 1 open drums  : 2d_revolver_cutout, 2d_demolition_mgl, 2d_mortar_cannon, 2d_octo_revolver.
Earlier 3D rounds kept as knobs: wide (2026-11-20), flush, chunky, legacy (2026-11-15).

Coordinates raw, right arm (+x; the left mirrors), centred on the arm's axis (x c, z 0). Faces as frame_drill_art.py
(north / south as seen from front / back, east back -> front, west front -> back, up rows front -> back, down rows
back -> front).
"""
import frame_drill_art as drill

_c = drill._c
# Legacy palette (chaingun warm black + TNT)
P_LEGACY = {k: _c(v) for k, v in dict(
    A='6a7077', B='454a50', C='2e3237', D='202327', E='131517', g='9fa4a9',
    i='6e1e14', j='a3301e', l='d2442a', m='e6e2d6', n='3a2f2a', s='a69c8c', x='5a5248',
).items()} | {'.': '.'}

# Rework palette: big suit's gunmetal slate (S/I/U/M/D/V), frame iron steel for the barrel (h/e/l/p/s/z),
# big suit's TNT reds (R lit, r mid, k shade), deep bore black (x).
P = {k: _c(v) for k, v in dict(
    S='747d82', I='5d666b', U='434b4f', M='333a3e', D='25292c', V='16191c',
    h='9fa4a9', e='8a9097', l='757c85', p='58606a', s='3c424c', z='22262e',
    R='d2442a', r='a3301e', k='6e1e14', x='0b0c0d',
).items()} | {'.': '.'}


def _paint(faces, pal=P):
    return lambda f, w, h: [[pal[ch] for ch in row] for row in (faces[f](w, h) if callable(faces[f]) else faces[f])]


def solid(ch):
    return lambda w, h: [ch * w] * h


# ---------------- legacy (2026-11-15) ----------------
def _legacy_build(c, top):
    plate = lambda w, h: ['A' * (w - 1) + 'B'] + ['B' + 'C' * (w - 2) + 'D'] * (h - 2) + ['D' * w]
    slab_side = lambda w, h: ['B' * w] + ['C' * w] * (h - 2) + ['D' * w]

    def round_end(w, h):
        g = [['D'] * w for _ in range(h)]
        for j in range(1, h - 1):
            for i in range(1, w - 1):
                g[j][i] = 'j'
        for i in range(1, w - 1):
            g[1][i] = 'l'
            g[h // 2][i] = 'm'
            g[h // 2 - 1][i] = 'm'
        g[h // 2 - 1][w // 2 - 1] = 'x'
        return [''.join(r) for r in g]

    part = lambda name, box, faces, bone='tool': dict(drill.part(name, box, _paint(faces, P_LEGACY)), bone=bone)
    housing = {f: plate for f in ('north', 'south', 'east', 'west')} | {'up': solid('D'), 'down': solid('E')}
    parts = [part('housing', ((c - 2.5, top - 1, -2.5), (c + 2.5, top, 2.5)), housing)]
    y0, y1 = top - 4, top - 1
    ends = lambda: {'up': solid('D'), 'down': solid('E')}
    parts.append(part('drum_x', ((c - 2.5, y0, -1.5), (c + 2.5, y1, 1.5)),
                      {'north': slab_side, 'south': slab_side, 'east': round_end, 'west': round_end} | ends(), 'bit'))
    parts.append(part('drum_z', ((c - 1.5, y0, -2.5), (c + 1.5, y1, 2.5)),
                      {'east': slab_side, 'west': slab_side, 'north': round_end, 'south': round_end} | ends(), 'bit'))
    parts.append(part('barrel', ((c - 1.5, y0 - 4, -2.5), (c + 1.5, y0, 0.5)),
                      {f: plate for f in ('north', 'south', 'east', 'west')} | {'up': solid('D'), 'down': solid('E')}))
    ring = lambda w, h: ['A' * (w - 1) + 'B'] + ['B' * (w - 1) + 'C'] * (h - 1)
    bore = lambda w, h: [''.join('B' if i in (0, w - 1) or j in (0, h - 1) else 'E' for i in range(w)) for j in range(h)]
    parts.append(part('muzzle', ((c - 2, y0 - 5, -3), (c + 2, y0 - 4, 1)),
                      {f: ring for f in ('north', 'south', 'east', 'west')} | {'up': solid('C'), 'down': bore}))
    return parts


# ---------------- rework painters (after the big suit's round 5 launcher) ----------------
def slate_side(w, h):
    """Gunmetal slate side face: lit top edge, lit left column, shaded right column and bottom row."""
    if h == 1:
        return ['I' + 'U' * max(0, w - 2) + ('D' if w > 1 else '')]
    if h == 2:
        return ['S' * max(1, w - 1) + ('I' if w > 1 else ''),
                'I' + 'U' * max(0, w - 2) + ('D' if w > 1 else '')]
    rows = ['S' * (w - 1) + 'I']
    for _ in range(h - 2):
        rows.append(('I' + 'U' * (w - 2) + 'D') if w > 2 else ('I' + 'D')[:w])
    rows.append('D' * w)
    return rows


def drum_cardinal(w, h):
    """A cardinal side of the octagonal drum: solid dark gunmetal slate with a 2-texel dark vertical flute down its
    middle (like the big suit's fluted slate drum, without extra striping)."""
    rows = [list(r) for r in slate_side(w, h)]
    m0, m1 = w // 2 - 1, w // 2
    for j in range(h):
        rows[j][m0] = 'V'
        rows[j][m1] = 'V'
    return [''.join(r) for r in rows]


def drum_step(w, h):
    """The narrow stepped corner face of the octagonal drum (2 texels wide, or outer margins of drum_x)."""
    rows = [list(r) for r in slate_side(w, h)]
    for j in range(1, h - 1):
        for i in range(w):
            rows[j][i] = 'U' if i == 0 else ('D' if i == w - 1 else 'M')
    return [''.join(r) for r in rows]


def barrel_side(w, h):
    """Light-steel barrel face (the big suit's bright steel contrast against the dark slate drum & muzzle):
    shadow row under the drum, bright steel body (lit left, shaded right), shadow row above the muzzle ring."""
    rows = ['p' * (w - 1) + 's']
    for j in range(1, h - 1):
        if w <= 2:
            rows.append('e' + 'p')
        else:
            body = 'e' if j <= 2 else 'l'
            rows.append('h' + 'e' + body * (w - 4) + 'l' + 'p' if w >= 5 else 'h' + body * (w - 2) + 'p')
    rows.append('s' * (w - 1) + 'z')
    return rows


def muzzle_ring(w, h):
    """Dark slate muzzle ring side (2 texels tall): bright top bevel catching light under the steel barrel, dark base."""
    return ['S' * (w - 1) + 'I', 'U' + 'M' * (w - 2) + 'D']


def muzzle_bore(w, h):
    """Muzzle down face: 1-texel slate lip, 1-texel dark inner bevel, deep black square bore."""
    g = [['x'] * w for _ in range(h)]
    for j in range(h):
        for i in range(w):
            d = min(i, j, w - 1 - i, h - 1 - j)
            if d == 0:
                g[j][i] = 'I' if (i == 0 or j == 0) and not (i == w - 1 or j == h - 1) else 'U' if i < w - 1 and j < h - 1 else 'D'
            elif d == 1:
                g[j][i] = 'V'
    return [''.join(r) for r in g]


def drum_down_painter(c, x0, z1, R, ch_in, ch_out, ch_span):
    """Paints a drum cube's down face in drum-axis coordinates (dx, dz) so all three flush octagon boxes share one
    seamless 90-degree-symmetric muzzle-end pattern: four red TNT chamber ends recessed inside a dark slate outer rim
    (ch_out <= R - 0.5 keeps the top/front chamber completely behind the barrel so no red peeks above it).
    (down face: col i runs -x -> +x, row j runs back +z -> front -z.)"""
    def f(w, h):
        rows = []
        for j in range(h):
            dz = z1 - (j + 0.5) / 2
            row = []
            for i in range(w):
                dx = (x0 - c) + (i + 0.5) / 2
                # Check the 4 chambers symmetrically at 90 deg around (0, 0):
                # radial coordinate u (ch_in..ch_out outward), tangential coordinate v (-ch_span..+ch_span)
                ch = None
                if -ch_out <= dx <= -ch_in and abs(dz) <= ch_span:
                    ch = (-dx, dz)       # left chamber
                elif ch_in <= dx <= ch_out and abs(dz) <= ch_span:
                    ch = (dx, -dz)       # right chamber
                elif ch_in <= dz <= ch_out and abs(dx) <= ch_span:
                    ch = (dz, dx)        # back chamber
                elif -ch_out <= dz <= -ch_in and abs(dx) <= ch_span:
                    ch = (-dz, -dx)      # front chamber (100% hidden behind the barrel)
                if ch is not None:
                    u, v = ch
                    # Vivid TNT round end: bright lit red on one side (R), vivid red body (r), shade (k) on trailing edge
                    if v > ch_span - 0.55:
                        row.append('k')
                    elif v < -ch_span + 0.55 or (u > ch_out - 0.55 and v < 0):
                        row.append('R')
                    else:
                        row.append('r')
                else:
                    # Dark slate drum face with subtle inner hub ring
                    if abs(dx) < 0.75 and abs(dz) < 0.75:
                        row.append('V')
                    elif abs(dx) > R - 0.55 or abs(dz) > R - 0.55:
                        row.append('D')
                    else:
                        row.append('M')
            rows.append(''.join(row))
        return rows
    return f


def drum_up_painter(c, x0, z0, R):
    """Drum top face (mostly covered by the 5 x 5 socket collar; exposed 0.5 px rim on 6 x 6 drums catches light)."""
    def f(w, h):
        rows = []
        for j in range(h):
            dz = z0 + (j + 0.5) / 2
            row = []
            for i in range(w):
                dx = (x0 - c) + (i + 0.5) / 2
                if abs(dx) > R - 0.55 or abs(dz) > R - 0.55:
                    row.append('I' if dx < 0 or dz < 0 else 'U')
                else:
                    row.append('D')
            rows.append(''.join(row))
        return rows
    return f


SPECS = {
    # (drum_W, drum_N, ch_in, ch_out, ch_span, barrel_W, muzzle_W, sight_W, sight_gap)
    # wide: drum_N=5.0 gives crisp 0.5 px (1-texel) octagonal corner bevels AND 0.5 px clearance around Steve's 4x4 arm
    # inside the lifted sleeve (zero z-fighting).
    'wide':   (6.0, 5.0, 1.0, 2.5, 1.0, 3.5, 4.0, 0.5, 1.0),
    'flush':  (5.0, 3.0, 1.0, 2.0, 1.0, 3.0, 3.5, 0.5, 1.0),
    'chunky': (6.0, 4.0, 1.0, 2.5, 1.0, 4.0, 4.5, 1.0, 1.0),
}


# ---------------------------------------------------------------------------
# 2026-11-22: 2D-texture + 0.5 px cutout outer-layer redesign drafts
# ---------------------------------------------------------------------------

P_2D = {k: _c(v) for k, v in dict(
    # Iron armour steel ramp (exact frame_iron_art.PAL)
    z='22262e', s='3c424c', p='58606a', l='757c85', e='8a9097', h='9fa4a9', g='cdcfcf', w='fbf8f0',
    # Neutral dark gunmetal slate ramp (exact frame_iron_art.SLATE + highlight/deep bore)
    V='0d0f11', x='1a1d1f', d='25292c', k='2f3437', m='3b4246', n='4c5559', N='687278',
    # Warm copper / brass primer & blast ring accents
    u='4e2816', q='804426', Q='b86a38', f='dc8f5c', F='f2b482',
    # Minecraft TNT cartridge ramp: crimson red + cream-white label band + ink stripe
    K='6e1e14', r='a82e1e', R='d64128', T='f06244',
    W='e6e0d0', C='c6beb0', c='999184',
    # Demolition hazard yellow/amber (Option B)
    y='b88412', Y='e6b422', Z='ffd854',
).items()} | {'.': '.'}


def _paint_2d(faces, pal=P_2D):
    def fn(f, w, h):
        src = faces[f](w, h) if callable(faces[f]) else faces[f]
        assert len(src) == h and all(len(row) == w for row in src), (f, (w, h), (len(src), [len(row) for row in src]))
        return [[pal[ch] for ch in row] for row in src]
    return fn


def _part_2d(name, box, faces, bone='tool'):
    return dict(drill.part(name, box, _paint_2d(faces), 0), bone=bone)


def _none(w, h):
    return ['.' * w] * h


def _ring_cap(lit, top_c, side_c, shade):
    """1-texel hollow outer ring cap (inner area '.' so zero coplanar overlap with the inner core box)."""
    def fn(w, h):
        grid = [['.'] * w for _ in range(h)]
        for i in range(w):
            grid[0][i] = lit if i < w - 1 else top_c
            grid[h - 1][i] = side_c if i == 0 else shade
        for j in range(1, h - 1):
            grid[j][0] = top_c
            grid[j][w - 1] = shade
        return [''.join(row) for row in grid]
    return fn


def _bore_down(lip_lit, lip_mid, lip_dark, inner_rim='x', bore='V'):
    """Heavy square mortar bore on barrel_inner.down (works for 6x6 and 7x7 texels)."""
    def fn(w, h):
        grid = [[bore] * w for _ in range(h)]
        for j in range(h):
            for i in range(w):
                d = min(i, j, w - 1 - i, h - 1 - j)
                if d == 0:
                    grid[j][i] = lip_lit if (i == 0 or j == 0) and not (i == w - 1 or j == h - 1) else (
                        lip_mid if i < w - 1 and j < h - 1 else lip_dark)
                elif d == 1 and w >= 7:
                    grid[j][i] = inner_rim
        return [''.join(row) for row in grid]
    return fn


def _tnt_drum_down_10():
    """10x10 down face of a 5x3x5 inner revolver drum (90-degree symmetric, zero red peeking past barrel):
    four crisp Minecraft TNT cartridge ends (crimson red + white center primer dot) around a dark slate hub."""
    return [
        'xddddddddx',
        'ddmkRRkmdd',
        'dmkRTTRkmd',
        'dkRKWKRRkd'.replace('KR', 'RK'),  # symmetric -> built mathematically below for exact 90-deg symmetry!
    ]


def _tnt_drum_down_sym(w=10):
    """Exact 90-degree rotationally symmetric TNT chamber face on drum_inner.down (10x10 for 5x5 drum).
    Chambers sit at radial [2..3] (1.0..2.0 px from center, recessed 0.5 px inside drum_inner so top chamber is 100%
    hidden behind the offset barrel while left/right/bottom chambers show vividly!)."""
    g = [['d'] * w for _ in range(w)]
    # Helper to stamp one 2x4 TNT chamber at (i, j) rotated 4x around center (w-1)/2
    cx = (w - 1) / 2.0
    for j in range(w):
        for i in range(w):
            # Border rim
            if i in (0, w - 1) or j in (0, w - 1):
                g[j][i] = 'x'
                continue
            dx, dy = i - cx, j - cx
            # Central hub (2x2)
            if abs(dx) <= 0.6 and abs(dy) <= 0.6:
                g[j][i] = 'V'
                continue
            # Check 4 cardinal chambers symmetrically by rotating into +x half-plane
            # Rotate (dx, dy) so chamber axis is along +u in [1.5..3.5], |v| <= 1.5
            ch = None
            for u, v in ((dx, dy), (-dx, -dy), (dy, -dx), (-dy, dx)):
                if 1.4 <= u <= 3.6 and abs(v) <= 1.6:
                    ch = (u, v)
                    break
            if ch is not None:
                u, v = ch
                # TNT round end: red shell outer, bright white/black TNT primer center!
                if 2.0 <= u <= 3.0 and abs(v) <= 0.6:
                    g[j][i] = 'W' if u > 2.4 else 'C'
                elif v > 1.0:
                    g[j][i] = 'K'
                elif v < -1.0:
                    g[j][i] = 'T' if u > 2.5 else 'R'
                else:
                    g[j][i] = 'R' if u > 2.5 else 'r'
            else:
                g[j][i] = 'k' if abs(dx) + abs(dy) < 4.5 else 'm'
    return [''.join(row) for row in g]


def _tnt_shell_side_10():
    """10x6 side face of drum_inner: rich recessed Minecraft TNT cartridge with crimson red sticks, cream-white
    center TNT label band with dark lettering dashes, and brass/copper primer rim!"""
    return [
        'xddddddddx',   # row 0: recessed drum breech shadow
        'xKRRRRRRKx',   # row 1: vivid red TNT upper body
        'xCWxWWxWCx',   # row 2: iconic cream-white TNT center band with dark ink dashes
        'xCWxWWxWCx',   # row 3: white band lower row
        'xKrrTTTrKx'.replace('rTTTr', 'rRRRr'),   # row 4: red TNT lower body
        'xddddddddx',   # row 5: bottom rim shadow
    ]


def _build_2d_revolver_cutout(c, top):
    """Option A (6 cubes, 9.0 px): TF2 Open-Chamber Rotary Launcher in pure 2D + 0.5 px cutout layer language.
    - cuff_inner + cuff_outer (6x1.5x6, tool): dark gunmetal breech collar with recessed steel locking lugs;
    - drum_inner + drum_outer (6x3.0x6, bit): 90-deg turning dark-gunmetal fluted cylinder shroud with 4 wide
      vertical cutout windows revealing recessed red-and-white Minecraft TNT shells inside (+ 4 chamber ends on down);
    - barrel_inner (3.0x4.5x3.0, tool): bright light-steel heavy mortar tube tucked against front chamber;
    - barrel_outer (4.0x4.5x4.0, tool): 0.5 px dark-gunmetal cutout root collar, heavy muzzle ring, and integrated
      top sight rail (leaving bright light-steel barrel cleanly exposed in the middle!)."""
    t_cuff = top - 1.5
    t_drum = top - 4.5
    t_tip = top - 9.0

    # 1. Breech collar (1.5 px -> 3 rows)
    cuff_in = [
        'xddddddddx',
        'dkhllllhkd',
        'xddddddddx',
    ]
    cuff_out = [
        'NnnnnnnnnnNd',
        'nmk......kmd',
        'xddddddddddx',
    ]

    # 2. Turning rotary TNT drum (3.0 px -> 6 rows, 90-deg symmetric across all 4 faces!)
    drum_in = _tnt_shell_side_10()
    drum_out = [
        'NnnnnnnnnnNd',   # row 0: crisp upper cylinder rim
        'nmk......kmd',   # row 1: wide 6x4 chamber cutout window exposing recessed red/white TNT shell!
        'nmk......kmd',   # row 2: window
        'nmk......kmd',   # row 3: window
        'nmk......kmd',   # row 4: window
        'xddddddddddx',   # row 5: heavy lower cylinder rim
    ]

    # 3. Light-steel offset mortar barrel (3.0x4.5x3.0 inner -> 6x9 sides, 6x6 down)
    bar_in = [
        'spppps',
        'gheeep',
        'helllp',
        'helllp',
        'heeeep',
        'helllp',
        'helllp',
        'spppps',
        'zzzzzz',
    ]
    # Top (north) face of inner barrel carries a flush dark-slate iron sight spine (no floating outer sliver!)
    bar_in_north = [
        'spppps',
        'ghddhp',
        'heddhp',
        'heddhp',
        'ghddhp',
        'heddhp',
        'heNNhp',
        'spppps',
        'zzzzzz',
    ]
    # 4. 0.5 px cutout barrel jacket (4.0x4.5x4.0 -> 8x9 sides):
    #    Root locking collar (row 0) + open middle exposing bright steel tube + heavy dark muzzle ring (rows 7..8).
    #    All 4 faces open together on rows 1..6 so there are zero floating paper-thin slivers in side views!
    bar_out_side = [
        'Nnnnnnnd',   # row 0: dark gunmetal barrel root collar
        '........',   # rows 1..6: open air exposing bright light-steel inner mortar barrel!
        '........',
        '........',
        '........',
        '........',
        '........',
        'Nnnnnnnd',   # row 7: heavy dark gunmetal muzzle ring top bevel
        'dmmmmmmx',   # row 8: muzzle ring body
    ]
    bar_out_north = [
        'Nnnnnnnd',
        '........',
        '........',
        '........',
        '........',
        '........',
        '........',
        'Nnn..nnN',   # row 7: crisp U-notch sight cutout integrated cleanly into the solid muzzle ring!
        'dmmmmmmx',
    ]

    return [
        _part_2d('cuff_inner', ((c - 2.5, t_cuff, -2.5), (c + 2.5, top, 2.5)), {
            'north': cuff_in, 'south': cuff_in, 'east': cuff_in, 'west': cuff_in,
            'up': _none, 'down': _none,
        }),
        _part_2d('cuff_outer', ((c - 3.0, t_cuff, -3.0), (c + 3.0, top, 3.0)), {
            'north': cuff_out, 'south': cuff_out, 'east': cuff_out, 'west': cuff_out,
            'up': _ring_cap('N', 'n', 'm', 'd'), 'down': _none,
        }),
        _part_2d('drum_inner', ((c - 2.5, t_drum, -2.5), (c + 2.5, t_cuff, 2.5)), {
            'north': drum_in, 'south': drum_in, 'east': drum_in, 'west': drum_in,
            'up': _none, 'down': _tnt_drum_down_sym(10),
        }, 'bit'),
        _part_2d('drum_outer', ((c - 3.0, t_drum, -3.0), (c + 3.0, t_cuff, 3.0)), {
            'north': drum_out, 'south': drum_out, 'east': drum_out, 'west': drum_out,
            'up': _none, 'down': _ring_cap('n', 'm', 'k', 'x'),
        }, 'bit'),
        _part_2d('barrel_inner', ((c - 1.5, t_tip, -2.5), (c + 1.5, t_drum, 0.5)), {
            'north': bar_in_north, 'south': bar_in, 'east': bar_in, 'west': bar_in,
            'up': _none, 'down': _bore_down('e', 'l', 's'),
        }),
        _part_2d('barrel_outer', ((c - 2.0, t_tip, -3.0), (c + 2.0, t_drum, 1.0)), {
            'north': bar_out_north, 'south': bar_out_side, 'east': bar_out_side, 'west': bar_out_side,
            'up': _none, 'down': _ring_cap('N', 'n', 'm', 'x'),
        }),
    ]


def _build_2d_demolition_mgl(c, top):
    """Option B (6 cubes, 9.0 px): Industrial Demolition MGL-32 with Hazard Stripes & Perforated Barrel Shroud.
    - cuff_inner + cuff_outer (6x1.5x6, tool): dark gunmetal breech with recessed yellow/black demolition hazard band;
    - drum_inner + drum_outer (6x3.0x6, bit): heavy dark-slate cylinder with arched 0.5 px cutout loading windows
      showing vivid red/white Minecraft TNT rounds turning 90 deg per shot;
    - barrel_inner (3.0x4.5x3.0, tool): dark blued-gunmetal mortar tube;
    - barrel_outer (4.0x4.5x4.0, tool): iron-steel M203/MGL perforated cooling heat-shield jacket + hazard muzzle band
      + heavy dark muzzle brake collar."""
    t_cuff = top - 1.5
    t_drum = top - 4.5
    t_tip = top - 9.0

    # 1. Breech collar w/ recessed demolition hazard yellow/black stripes
    cuff_in = [
        'xddddddddx',
        'xYxYxYxYxx'.replace('xx', 'Yx'),  # 10 chars: xYxYxYxYYx -> symmetric hazard chevron!
        'xddddddddx',
    ]
    cuff_in[1] = 'xYxxYYxxYx'
    cuff_out = [
        'NnnnnnnnnnNd',
        'dkd......dkd',
        'xxxxxxxxxxxx',
    ]

    # 2. Turning drum with bold ribbed dark-slate cage framing recessed TNT rounds
    drum_in = _tnt_shell_side_10()
    drum_out = [
        'NnnnnnnnnnNd',
        'nmk......kmd',
        'nm........md',   # wider 8-texel middle opening so TNT red+white band pops strongly!
        'nm........md',
        'nmk......kmd',
        'xddddddddddx',
    ]

    # 3. Dark blued-gunmetal inner mortar tube (6x9)
    bar_in = [
        'dddddd',
        'dkmmkd',
        'dkkkkd',
        'dkmmkd',
        'dkkkkd',
        'dkmmkd',
        'dkkkkd',
        'dddddd',
        'xxxxxx',
    ]

    # 4. Perforated iron-steel MGL heat-shield outer jacket + hazard warning band + heavy muzzle brake (8x9)
    bar_out = [
        'ghhhhhhe',   # row 0: iron shroud root rim
        'el.ll.lp',   # row 1: cooling vent holes exposing dark gunmetal barrel underneath!
        'ellllllp',   # row 2: solid steel cooling rib
        'el.ll.lp',   # row 3: cooling vent holes
        'ellllllp',   # row 4: solid steel cooling rib
        'el.ll.lp',   # row 5: cooling vent holes
        'xYxYYxYx',   # row 6: bold demolition hazard stripe collar!
        'Nnnnnnnd',   # row 7: heavy dark muzzle brake
        'xddddddx',   # row 8: muzzle lip
    ]
    bar_out_north = [
        'ghhhhhhe',
        'el.ll.lp',
        'ellllllp',
        'el.ll.lp',
        'ellllllp',
        'epN..Npe',   # row 5: crisp integrated twin sight posts on top face
        'xYxYYxYx',   # row 6: demolition hazard stripe collar
        'Nnnnnnnd',
        'xddddddx',
    ]

    return [
        _part_2d('cuff_inner', ((c - 2.5, t_cuff, -2.5), (c + 2.5, top, 2.5)), {
            'north': cuff_in, 'south': cuff_in, 'east': cuff_in, 'west': cuff_in,
            'up': _none, 'down': _none,
        }),
        _part_2d('cuff_outer', ((c - 3.0, t_cuff, -3.0), (c + 3.0, top, 3.0)), {
            'north': cuff_out, 'south': cuff_out, 'east': cuff_out, 'west': cuff_out,
            'up': _ring_cap('N', 'n', 'm', 'd'), 'down': _none,
        }),
        _part_2d('drum_inner', ((c - 2.5, t_drum, -2.5), (c + 2.5, t_cuff, 2.5)), {
            'north': drum_in, 'south': drum_in, 'east': drum_in, 'west': drum_in,
            'up': _none, 'down': _tnt_drum_down_sym(10),
        }, 'bit'),
        _part_2d('drum_outer', ((c - 3.0, t_drum, -3.0), (c + 3.0, t_cuff, 3.0)), {
            'north': drum_out, 'south': drum_out, 'east': drum_out, 'west': drum_out,
            'up': _none, 'down': _ring_cap('n', 'm', 'k', 'x'),
        }, 'bit'),
        _part_2d('barrel_inner', ((c - 1.5, t_tip, -2.5), (c + 1.5, t_drum, 0.5)), {
            'north': bar_in, 'south': bar_in, 'east': bar_in, 'west': bar_in,
            'up': _none, 'down': _bore_down('n', 'm', 'd'),
        }),
        _part_2d('barrel_outer', ((c - 2.0, t_tip, -3.0), (c + 2.0, t_drum, 1.0)), {
            'north': bar_out_north, 'south': bar_out, 'east': bar_out, 'west': bar_out,
            'up': _none, 'down': _ring_cap('N', 'n', 'm', 'x'),
        }),
    ]


def _build_2d_mortar_cannon(c, top):
    """Option C (6 cubes, 9.0 px): Heavy Iron-Clad Siege Mortar (centered broad-bore cannon).
    - cuff_inner + cuff_outer (6x1.5x6, tool): iron-armour breech matching the suit's iron plates w/ recessed copper ring;
    - drum_inner + drum_outer (6x3.0x6, bit): open-frame iron rotary TNT magazine with huge wraparound windows
      showing 4 chunky Minecraft TNT shells all round 360 deg (visible in 3P back, 3P front & 1P cockpit);
    - barrel_inner (3.5x4.5x3.5, centered, tool) + barrel_outer (4.5x4.5x4.5, centered, tool): heavy iron-clad
      siege mortar tube with copper blast collar and cutout side-vented muzzle brake."""
    t_cuff = top - 1.5
    t_drum = top - 4.5
    t_tip = top - 9.0

    # 1. Iron-armour breech w/ recessed copper primer ring
    cuff_in = [
        'xddddddddx',
        'dqQffffQqd',
        'xddddddddx',
    ]
    cuff_out = [
        'ghhhhhhhhhhe',
        'epd......dpe',
        'zssssssssssz',
    ]

    # 2. Open-bay iron rotary TNT drum (4 big windows showing red+white TNT all around!)
    drum_in = _tnt_shell_side_10()
    drum_out = [
        'ghhhhhhhhhhe',   # row 0: iron magazine upper ring
        'ep........pe',   # rows 1..4: wide 8-texel open bay around recessed Minecraft TNT shells!
        'ep........pe',
        'ep........pe',
        'ep........pe',
        'zssssssssssz',   # row 5: iron lower ring
    ]

    # 3. Centered broad-bore mortar inner barrel (3.5x4.5x3.5 -> 7x9 sides, 7x7 down)
    bar_in = [
        'ddddddd',
        'dkmmmkd',
        'dqfffqd',   # copper blast sleeve visible through cutout vents!
        'dkmmmkd',
        'dkkkkd' + 'd',
        'dkmmmkd',
        'dxxVxxd',   # dark exhaust port behind muzzle brake slots!
        'dxxVxxd',
        'xxxxxxx',
    ]

    # 4. Centered iron-clad siege mortar outer jacket (4.5x4.5x4.5 -> 9x9 sides, 9x9 down ring)
    bar_out = [
        'ghhhhhhhe',   # row 0: heavy iron breech collar
        'eplllllps',   # row 1: iron casing
        'ep.....ps',   # row 2: cutout revealing recessed copper blast band!
        'eplllllps',   # row 3: iron barrel mid
        'eplllllps',   # row 4: iron barrel mid
        'zsssssssz',   # row 5: bevel step into muzzle brake
        'Nnn...nnd',   # row 6: side-vented heavy muzzle brake ports!
        'Nnn...nnd',   # row 7: muzzle brake ports
        'dmmmmmmmx',   # row 8: dark muzzle crown
    ]

    return [
        _part_2d('cuff_inner', ((c - 2.5, t_cuff, -2.5), (c + 2.5, top, 2.5)), {
            'north': cuff_in, 'south': cuff_in, 'east': cuff_in, 'west': cuff_in,
            'up': _none, 'down': _none,
        }),
        _part_2d('cuff_outer', ((c - 3.0, t_cuff, -3.0), (c + 3.0, top, 3.0)), {
            'north': cuff_out, 'south': cuff_out, 'east': cuff_out, 'west': cuff_out,
            'up': _ring_cap('g', 'h', 'e', 's'), 'down': _none,
        }),
        _part_2d('drum_inner', ((c - 2.5, t_drum, -2.5), (c + 2.5, t_cuff, 2.5)), {
            'north': drum_in, 'south': drum_in, 'east': drum_in, 'west': drum_in,
            'up': _none, 'down': _tnt_drum_down_sym(10),
        }, 'bit'),
        _part_2d('drum_outer', ((c - 3.0, t_drum, -3.0), (c + 3.0, t_cuff, 3.0)), {
            'north': drum_out, 'south': drum_out, 'east': drum_out, 'west': drum_out,
            'up': _none, 'down': _ring_cap('h', 'l', 'p', 'z'),
        }, 'bit'),
        _part_2d('barrel_inner', ((c - 1.75, t_tip, -1.75), (c + 1.75, t_drum, 1.75)), {
            'north': bar_in, 'south': bar_in, 'east': bar_in, 'west': bar_in,
            'up': _none, 'down': _bore_down('n', 'm', 'd'),
        }),
        _part_2d('barrel_outer', ((c - 2.25, t_tip, -2.25), (c + 2.25, t_drum, 2.25)), {
            'north': bar_out, 'south': bar_out, 'east': bar_out, 'west': bar_out,
            'up': _none, 'down': _ring_cap('N', 'n', 'm', 'x'),
        }),
    ]


def _build_2d_octo_revolver(c, top):
    """Option D (9 cubes, 9.0 px): Beveled Octagonal Revolver upgraded with 2D-layer craft.
    Keeps the true 3D beveled octagonal drum silhouette (6.0 wide x 5.0 flat) with painted recessed TNT chamber slots
    on all 4 cardinal sides + rich red/white TNT chamber ends on down, paired with a 2-layer offset light-steel barrel
    with cutout muzzle ring & a crisp single-cube cutout flip-up ladder sight!"""
    t_cuff = top - 1.5
    t_drum = top - 4.5
    t_tip = top - 9.0
    R, r = 3.0, 2.5

    # 1. 2-layer dark-gunmetal breech cuff with copper primer pins (6x1.5x6)
    cuff_in = [
        'xddddddddx',
        'dkqQffQqk' + 'd',
        'xddddddddx',
    ]
    cuff_out = [
        'NnnnnnnnnnNd',
        'nmk......kmd',
        'xddddddddddx',
    ]

    # 2. Octagonal turning drum (3 flush cubes: drum_x + drum_f + drum_b, 3.0 px = 6 rows)
    #    Cardinal face (10x6): dark gunmetal cylinder with bold recessed TNT chamber slot in the middle!
    octo_cardinal = [
        'NnnnnnnnnN',   # row 0: crisp upper rim
        'nmkKRRKkm' + 'd',   # row 1: red TNT peeking through vertical chamber flute!
        'nmKCWWCKm' + 'd',   # row 2: cream-white TNT label stripe
        'nmKCWWCKm' + 'd',   # row 3: white label stripe
        'nmkKrrKkm' + 'd',   # row 4: red TNT lower end
        'xddddddddx',   # row 5: lower cylinder rim
    ]
    #    Corner step face (1x6? 0.5 px = 1 texel wide on x/z bevels, or 12x6 for drum_x north/south!)
    #    Wait: drum_x is 6.0 x 3.0 x 5.0 -> east/west = 10x6 (cardinal), north/south = 12x6 (only outer 1 texel each side visible!)
    #    drum_f/b are 5.0 x 3.0 x 0.5 -> north/south = 10x6 (cardinal), east/west = 1x6 (bevel step!)
    def octo_step(w, h):
        return ['N' + 'n' * max(0, w - 2) + ('d' if w > 1 else '')] + \
               ['n' + 'm' * max(0, w - 2) + ('d' if w > 1 else '')] * (h - 2) + ['x' * w]

    def octo_down(x0, z1):
        """Shares exact 90-deg symmetric red-and-white TNT rounds across all 3 octagonal drum boxes."""
        def fn(w, h):
            rows = []
            for j in range(h):
                dz = z1 - (j + 0.5) / 2
                row = []
                for i in range(w):
                    dx = (x0 - c) + (i + 0.5) / 2
                    ch = None
                    for u, v in ((dx, dz), (-dx, -dz), (dz, -dx), (-dz, dx)):
                        if 1.0 <= u <= 2.25 and abs(v) <= 0.85:
                            ch = (u, v)
                            break
                    if ch is not None:
                        u, v = ch
                        if 1.35 <= u <= 1.9 and abs(v) <= 0.35:
                            row.append('W')
                        elif v > 0.45:
                            row.append('K')
                        elif v < -0.45:
                            row.append('T' if u > 1.6 else 'R')
                        else:
                            row.append('R')
                    elif abs(dx) < 0.6 and abs(dz) < 0.6:
                        row.append('V')
                    elif abs(dx) > R - 0.55 or abs(dz) > R - 0.55:
                        row.append('x')
                    else:
                        row.append('k')
                rows.append(''.join(row))
            return rows
        return fn

    # 3. 2-layer offset light-steel barrel (3.0x4.5x3.0 inner + 4.0x4.5x4.0 cutout outer)
    bar_in = [
        'spppps',
        'gheeep',
        'helllp',
        'helllp',
        'heeeep',
        'helllp',
        'helllp',
        'spppps',
        'zzzzzz',
    ]
    bar_out = [
        'Nnnnnnnd',
        '........',
        '........',
        '........',
        '........',
        '........',
        '........',
        'Nnnnnnnd',
        'dmmmmmmx',
    ]

    # 4. Crisp 1-cube cutout flip-up ladder sight anchored solidly on barrel_inner's front (z=-2.5),
    #    projecting 0.5 px proud of the muzzle ring (z=-3.0) with a clean open U-notch (north/up/down cutout)!
    sight_up_dn = [
        'N..N',   # front half (z=-3.5..-3.0, projecting proud)
        'd..d',   # rear half anchored onto barrel_inner (z=-3.0..-2.5)
    ]
    sight_fb = [
        'N..N',
        'd..d',
    ]
    sight_side = [
        'Nd',
        'dk',
    ]

    return [
        _part_2d('cuff_inner', ((c - 2.5, t_cuff, -2.5), (c + 2.5, top, 2.5)), {
            'north': cuff_in, 'south': cuff_in, 'east': cuff_in, 'west': cuff_in,
            'up': _none, 'down': _none,
        }),
        _part_2d('cuff_outer', ((c - 3.0, t_cuff, -3.0), (c + 3.0, top, 3.0)), {
            'north': cuff_out, 'south': cuff_out, 'east': cuff_out, 'west': cuff_out,
            'up': _ring_cap('N', 'n', 'm', 'd'), 'down': _none,
        }),
        _part_2d('drum_x', ((c - R, t_drum, -r), (c + R, t_cuff, r)), {
            'east': octo_cardinal, 'west': octo_cardinal,
            'north': octo_step, 'south': octo_step,
            'up': _none, 'down': octo_down(c - R, r),
        }, 'bit'),
        _part_2d('drum_f', ((c - r, t_drum, -R), (c + r, t_cuff, -r)), {
            'north': octo_cardinal, 'south': _none,
            'east': octo_step, 'west': octo_step,
            'up': _none, 'down': octo_down(c - r, -r),
        }, 'bit'),
        _part_2d('drum_b', ((c - r, t_drum, r), (c + r, t_cuff, R)), {
            'south': octo_cardinal, 'north': _none,
            'east': octo_step, 'west': octo_step,
            'up': _none, 'down': octo_down(c - r, R),
        }, 'bit'),
        _part_2d('barrel_inner', ((c - 1.5, t_tip, -2.5), (c + 1.5, t_drum, 0.5)), {
            'north': bar_in, 'south': bar_in, 'east': bar_in, 'west': bar_in,
            'up': _none, 'down': _bore_down('e', 'l', 's'),
        }),
        _part_2d('barrel_outer', ((c - 2.0, t_tip, -3.0), (c + 2.0, t_drum, 1.0)), {
            'north': bar_out, 'south': bar_out, 'east': bar_out, 'west': bar_out,
            'up': _none, 'down': _ring_cap('N', 'n', 'm', 'x'),
        }),
        _part_2d('sight_leaf', ((c - 1.0, top - 8.0, -3.5), (c + 1.0, top - 7.0, -2.5)), {
            'north': sight_fb, 'south': _none, 'east': sight_side, 'west': sight_side,
            'up': sight_up_dn, 'down': sight_up_dn,
        }),
    ]


# ---------------------------------------------------------------------------
# 2026-11-22 Round 2: Closed mechanical drums (zero exposed vanilla TNT textures,
# so the launcher never clashes with resource packs!)
# ---------------------------------------------------------------------------

def _closed_drum_down_sym(w=10, rim='Q', rim_hi='f'):
    """90-degree symmetric closed mechanical breech/chamber face on drum_inner.down (10x10):
    four recessed dark-bore ordnance chambers with subtle metallic/brass breech rings (zero vanilla TNT texture!)."""
    g = [['d'] * w for _ in range(w)]
    cx = (w - 1) / 2.0
    for j in range(w):
        for i in range(w):
            if i in (0, w - 1) or j in (0, w - 1):
                g[j][i] = 'x'
                continue
            dx, dy = i - cx, j - cx
            if abs(dx) <= 0.6 and abs(dy) <= 0.6:
                g[j][i] = 'V'
                continue
            ch = None
            for u, v in ((dx, dy), (-dx, -dy), (dy, -dx), (-dy, dx)):
                if 1.4 <= u <= 3.6 and abs(v) <= 1.6:
                    ch = (u, v)
                    break
            if ch is not None:
                u, v = ch
                # Recessed dark chamber bore framed by a clean metallic/copper breech ring
                if 2.0 <= u <= 3.0 and abs(v) <= 0.6:
                    g[j][i] = 'V'
                elif u > 3.0 or v < -1.0:
                    g[j][i] = rim_hi
                else:
                    g[j][i] = rim
            else:
                g[j][i] = 'k' if abs(dx) + abs(dy) < 4.5 else 'm'
    return [''.join(row) for row in g]


def _build_2d_mgl_closed(c, top):
    """R2 Option A (6 cubes, 9.0 px): Closed Demolition MGL-32 — deeply fluted closed mechanical drum + perforated
    iron heat-shield offset barrel + yellow/black demolition hazard accents (zero vanilla TNT textures!)."""
    t_cuff = top - 1.5
    t_drum = top - 4.5
    t_tip = top - 9.0

    # 1. Breech collar w/ recessed demolition hazard yellow/black stripes
    cuff_in = [
        'xddddddddx',
        'xYxxYYxxYx',
        'xddddddddx',
    ]
    cuff_out = [
        'NnnnnnnnnnNd',
        'dkd......dkd',
        'xxxxxxxxxxxx',
    ]

    # 2. Closed deeply-fluted mechanical drum (5x3x5 inner + 6x3x6 cutout outer, 90-deg symmetric!):
    #    Outer cutout carves twin vertical chamber flutes per face, exposing recessed machined steel chamber cylinders
    #    & a crisp center indexing notch so every 90-degree click reads sharply in motion!
    drum_in = [
        'xddddddddx',
        'xkppllppxk'.replace('pxk', 'pkx'),  # 10 chars
        'xkplNNlpkx',
        'xkplNNlpkx',
        'xkppllppxk'.replace('pxk', 'pkx'),
        'xddddddddx',
    ]
    drum_out = [
        'NnnnnnnnnnNd',   # row 0: upper cylinder rim
        'nm..kNNk..md',   # rows 1..4: twin 2x4 vertical machined flutes flanking a heavy center rib!
        'nm..kmmk..md',
        'nm..kmmk..md',
        'nm..kddk..md',
        'xddddddddddx',   # row 5: lower cylinder rim
    ]

    # 3. Dark blued-gunmetal inner mortar tube + perforated iron-steel MGL heat-shield + hazard collar
    bar_in = [
        'dddddd',
        'dkmmkd',
        'dkkkkd',
        'dkmmkd',
        'dkkkkd',
        'dkmmkd',
        'dkkkkd',
        'dddddd',
        'xxxxxx',
    ]
    bar_out = [
        'ghhhhhhe',
        'el.ll.lp',
        'ellllllp',
        'el.ll.lp',
        'ellllllp',
        'el.ll.lp',
        'xYxYYxYx',
        'Nnnnnnnd',
        'xddddddx',
    ]
    bar_out_north = [
        'ghhhhhhe',
        'el.ll.lp',
        'ellllllp',
        'el.ll.lp',
        'ellllllp',
        'epN..Npe',
        'xYxYYxYx',
        'Nnnnnnnd',
        'xddddddx',
    ]

    return [
        _part_2d('cuff_inner', ((c - 2.5, t_cuff, -2.5), (c + 2.5, top, 2.5)), {
            'north': cuff_in, 'south': cuff_in, 'east': cuff_in, 'west': cuff_in,
            'up': _none, 'down': _none,
        }),
        _part_2d('cuff_outer', ((c - 3.0, t_cuff, -3.0), (c + 3.0, top, 3.0)), {
            'north': cuff_out, 'south': cuff_out, 'east': cuff_out, 'west': cuff_out,
            'up': _ring_cap('N', 'n', 'm', 'd'), 'down': _none,
        }),
        _part_2d('drum_inner', ((c - 2.5, t_drum, -2.5), (c + 2.5, t_cuff, 2.5)), {
            'north': drum_in, 'south': drum_in, 'east': drum_in, 'west': drum_in,
            'up': _none, 'down': _closed_drum_down_sym(10, rim='m', rim_hi='N'),
        }, 'bit'),
        _part_2d('drum_outer', ((c - 3.0, t_drum, -3.0), (c + 3.0, t_cuff, 3.0)), {
            'north': drum_out, 'south': drum_out, 'east': drum_out, 'west': drum_out,
            'up': _none, 'down': _ring_cap('n', 'm', 'k', 'x'),
        }, 'bit'),
        _part_2d('barrel_inner', ((c - 1.5, t_tip, -2.5), (c + 1.5, t_drum, 0.5)), {
            'north': bar_in, 'south': bar_in, 'east': bar_in, 'west': bar_in,
            'up': _none, 'down': _bore_down('n', 'm', 'd'),
        }),
        _part_2d('barrel_outer', ((c - 2.0, t_tip, -3.0), (c + 2.0, t_drum, 1.0)), {
            'north': bar_out_north, 'south': bar_out, 'east': bar_out, 'west': bar_out,
            'up': _none, 'down': _ring_cap('N', 'n', 'm', 'x'),
        }),
    ]


def _build_2d_tf2_closed(c, top):
    """R2 Option B (6 cubes, 9.0 px): Clean Closed TF2 Rotary Launcher — pure dark gunmetal + bright light-steel
    barrel + subtle copper indexing pins (no hazard yellow, no vanilla TNT texture!)."""
    t_cuff = top - 1.5
    t_drum = top - 4.5
    t_tip = top - 9.0

    # 1. Dark gunmetal breech collar with recessed brushed-steel locking lugs
    cuff_in = [
        'xddddddddx',
        'dkhllllhkd',
        'xddddddddx',
    ]
    cuff_out = [
        'NnnnnnnnnnNd',
        'nmk......kmd',
        'xddddddddddx',
    ]

    # 2. Closed fluted gunmetal revolver drum with 0.5 px deep vertical cylinder chambers & copper indexing studs
    drum_in = [
        'xddddddddx',
        'xdmmNNmmxd'.replace('xd', 'dx'),  # wait: keep symmetric 10 chars!
        'xdmQffQmdx',
        'xdmQffQmdx',
        'xdmmNNmmxd'.replace('xd', 'dx'),
        'xddddddddx',
    ]
    drum_in = [
        'xddddddddx',
        'xdkmnnmkdx',
        'xdkQffQkdx',   # recessed copper indexing pin centered in each machined flute!
        'xdkQffQkdx',
        'xdkmnnmkdx',
        'xddddddddx',
    ]
    drum_out = [
        'NnnnnnnnnnNd',
        'nm..kNNk..md',   # twin deep vertical machined flutes + bolted dark center rib
        'nm..kmmk..md',
        'nm..kmmk..md',
        'nm..kddk..md',
        'xddddddddddx',
    ]

    # 3. Clean bright light-steel offset barrel + dark gunmetal root collar & notched heavy muzzle ring
    bar_in = [
        'spppps',
        'gheeep',
        'helllp',
        'helllp',
        'heeeep',
        'helllp',
        'helllp',
        'spppps',
        'zzzzzz',
    ]
    bar_in_north = [
        'spppps',
        'ghddhp',
        'heddhp',
        'heddhp',
        'ghddhp',
        'heddhp',
        'heNNhp',
        'spppps',
        'zzzzzz',
    ]
    bar_out_side = [
        'Nnnnnnnd',
        '........',
        '........',
        '........',
        '........',
        '........',
        '........',
        'Nnnnnnnd',
        'dmmmmmmx',
    ]
    bar_out_north = [
        'Nnnnnnnd',
        '........',
        '........',
        '........',
        '........',
        '........',
        '........',
        'Nnn..nnN',
        'dmmmmmmx',
    ]

    return [
        _part_2d('cuff_inner', ((c - 2.5, t_cuff, -2.5), (c + 2.5, top, 2.5)), {
            'north': cuff_in, 'south': cuff_in, 'east': cuff_in, 'west': cuff_in,
            'up': _none, 'down': _none,
        }),
        _part_2d('cuff_outer', ((c - 3.0, t_cuff, -3.0), (c + 3.0, top, 3.0)), {
            'north': cuff_out, 'south': cuff_out, 'east': cuff_out, 'west': cuff_out,
            'up': _ring_cap('N', 'n', 'm', 'd'), 'down': _none,
        }),
        _part_2d('drum_inner', ((c - 2.5, t_drum, -2.5), (c + 2.5, t_cuff, 2.5)), {
            'north': drum_in, 'south': drum_in, 'east': drum_in, 'west': drum_in,
            'up': _none, 'down': _closed_drum_down_sym(10, rim='Q', rim_hi='f'),
        }, 'bit'),
        _part_2d('drum_outer', ((c - 3.0, t_drum, -3.0), (c + 3.0, t_cuff, 3.0)), {
            'north': drum_out, 'south': drum_out, 'east': drum_out, 'west': drum_out,
            'up': _none, 'down': _ring_cap('n', 'm', 'k', 'x'),
        }, 'bit'),
        _part_2d('barrel_inner', ((c - 1.5, t_tip, -2.5), (c + 1.5, t_drum, 0.5)), {
            'north': bar_in_north, 'south': bar_in, 'east': bar_in, 'west': bar_in,
            'up': _none, 'down': _bore_down('e', 'l', 's'),
        }),
        _part_2d('barrel_outer', ((c - 2.0, t_tip, -3.0), (c + 2.0, t_drum, 1.0)), {
            'north': bar_out_north, 'south': bar_out_side, 'east': bar_out_side, 'west': bar_out_side,
            'up': _none, 'down': _ring_cap('N', 'n', 'm', 'x'),
        }),
    ]


def _build_2d_mgl_clean(c, top):
    """R2 Option C (6 cubes, 9.0 px): Perforated Heat-Shield MGL in Iron, Gunmetal & Copper (recipe-grounded,
    no yellow hazard stripes, no vanilla TNT texture!).
    - cuff_inner + cuff_outer (6x1.5x6, tool): dark gunmetal breech with recessed burnished copper primer band;
    - drum_inner + drum_outer (6x3.0x6, bit): heavy dark-slate rotary cage with wide horizontal cutout slot exposing
      recessed ribbed steel chambers + thin copper pressure ring around the cylinder waist;
    - barrel_inner + barrel_outer (4x4.5x4, tool): iron-steel perforated MGL cooling jacket + thin copper recoil collar
      + heavy dark gunmetal muzzle brake."""
    t_cuff = top - 1.5
    t_drum = top - 4.5
    t_tip = top - 9.0

    # 1. Dark gunmetal breech w/ recessed copper primer ring
    cuff_in = [
        'xddddddddx',
        'dqQffffQqd',
        'xddddddddx',
    ]
    cuff_out = [
        'NnnnnnnnnnNd',
        'nmk......kmd',
        'xddddddddddx',
    ]

    # 2. Closed mechanical rotary drum: vertical steel chamber flutes + recessed copper waist ring
    drum_in = [
        'xddddddddx',
        'xdpllllpdx',
        'xdqQffQqdx',
        'xdqQffQqdx',
        'xdpllllpdx',
        'xddddddddx',
    ]
    drum_out = [
        'NnnnnnnnnnNd',
        'nmk......kmd',   # wide 6x4 recessed mechanical bay with ribbed steel chambers & central copper band!
        'nmk..dd..kmd',   # dark center lock rib breaking each bay cleanly into twin vertical chamber slots
        'nmk..dd..kmd',
        'nmk......kmd',
        'xddddddddddx',
    ]

    # 3. Dark gunmetal inner tube + perforated iron-steel heat shield + copper recoil ring + dark muzzle brake
    bar_in = [
        'dddddd',
        'dkmmkd',
        'dkkkkd',
        'dkmmkd',
        'dkkkkd',
        'dkmmkd',
        'dkkkkd',
        'dddddd',
        'xxxxxx',
    ]
    bar_out = [
        'ghhhhhhe',
        'el.ll.lp',
        'ellllllp',
        'el.ll.lp',
        'ellllllp',
        'el.ll.lp',
        'qQffffQq',   # burnished copper recoil band instead of yellow hazard stripe!
        'Nnnnnnnd',
        'xddddddx',
    ]
    bar_out_north = [
        'ghhhhhhe',
        'el.ll.lp',
        'ellllllp',
        'el.ll.lp',
        'ellllllp',
        'epN..Npe',
        'qQffffQq',
        'Nnnnnnnd',
        'xddddddx',
    ]

    return [
        _part_2d('cuff_inner', ((c - 2.5, t_cuff, -2.5), (c + 2.5, top, 2.5)), {
            'north': cuff_in, 'south': cuff_in, 'east': cuff_in, 'west': cuff_in,
            'up': _none, 'down': _none,
        }),
        _part_2d('cuff_outer', ((c - 3.0, t_cuff, -3.0), (c + 3.0, top, 3.0)), {
            'north': cuff_out, 'south': cuff_out, 'east': cuff_out, 'west': cuff_out,
            'up': _ring_cap('N', 'n', 'm', 'd'), 'down': _none,
        }),
        _part_2d('drum_inner', ((c - 2.5, t_drum, -2.5), (c + 2.5, t_cuff, 2.5)), {
            'north': drum_in, 'south': drum_in, 'east': drum_in, 'west': drum_in,
            'up': _none, 'down': _closed_drum_down_sym(10, rim='Q', rim_hi='f'),
        }, 'bit'),
        _part_2d('drum_outer', ((c - 3.0, t_drum, -3.0), (c + 3.0, t_cuff, 3.0)), {
            'north': drum_out, 'south': drum_out, 'east': drum_out, 'west': drum_out,
            'up': _none, 'down': _ring_cap('n', 'm', 'k', 'x'),
        }, 'bit'),
        _part_2d('barrel_inner', ((c - 1.5, t_tip, -2.5), (c + 1.5, t_drum, 0.5)), {
            'north': bar_in, 'south': bar_in, 'east': bar_in, 'west': bar_in,
            'up': _none, 'down': _bore_down('n', 'm', 'd'),
        }),
        _part_2d('barrel_outer', ((c - 2.0, t_tip, -3.0), (c + 2.0, t_drum, 1.0)), {
            'north': bar_out_north, 'south': bar_out, 'east': bar_out, 'west': bar_out,
            'up': _none, 'down': _ring_cap('N', 'n', 'm', 'x'),
        }),
    ]


def _build_2d_octo_closed(c, top):
    """R2 Option D (8 cubes, 9.0 px): Beveled Octagonal Closed Drum + 2-Layer Perforated Barrel & Flip-Up Sight.
    True 3D beveled octagon drum in dark gunmetal with crisp machined steel flutes & copper indexing pins (zero vanilla
    TNT textures!), paired with the 2-layer offset barrel & 1-cube cutout flip-up ladder sight."""
    t_cuff = top - 1.5
    t_drum = top - 4.5
    t_tip = top - 9.0
    R, r = 3.0, 2.5

    cuff_in = [
        'xddddddddx',
        'dkqQffQqkd',
        'xddddddddx',
    ]
    cuff_out = [
        'NnnnnnnnnnNd',
        'nmk......kmd',
        'xddddddddddx',
    ]

    # Closed machined octagonal drum cardinal face (10x6): deep dark flutes flanking a riveted gunmetal rib w/ copper pin
    octo_cardinal = [
        'NnnnnnnnnN',
        'nmkxNNxkmd',
        'nmkxQfxkmd',
        'nmkxQfxkmd',
        'nmkxddxkmd',
        'xddddddddx',
    ]
    def octo_step(w, h):
        return ['N' + 'n' * max(0, w - 2) + ('d' if w > 1 else '')] + \
               ['n' + 'm' * max(0, w - 2) + ('d' if w > 1 else '')] * (h - 2) + ['x' * w]

    def octo_down_closed(x0, z1):
        """90-deg symmetric closed mechanical chamber rings across all 3 octagonal drum boxes (zero TNT texture!)."""
        def fn(w, h):
            rows = []
            for j in range(h):
                dz = z1 - (j + 0.5) / 2
                row = []
                for i in range(w):
                    dx = (x0 - c) + (i + 0.5) / 2
                    ch = None
                    for u, v in ((dx, dz), (-dx, -dz), (dz, -dx), (-dz, dx)):
                        if 1.0 <= u <= 2.25 and abs(v) <= 0.85:
                            ch = (u, v)
                            break
                    if ch is not None:
                        u, v = ch
                        if 1.35 <= u <= 1.9 and abs(v) <= 0.35:
                            row.append('V')
                        elif u > 1.9 or v < -0.45:
                            row.append('f')
                        else:
                            row.append('Q')
                    elif abs(dx) < 0.6 and abs(dz) < 0.6:
                        row.append('V')
                    elif abs(dx) > R - 0.55 or abs(dz) > R - 0.55:
                        row.append('x')
                    else:
                        row.append('k')
                rows.append(''.join(row))
            return rows
        return fn

    bar_in = [
        'spppps',
        'gheeep',
        'helllp',
        'helllp',
        'heeeep',
        'helllp',
  'helllp',
        'spppps',
        'zzzzzz',
    ]
    bar_out = [
        'Nnnnnnnd',
        '........',
        '........',
        '........',
        '........',
        '........',
        '........',
        'Nnnnnnnd',
        'dmmmmmmx',
    ]
    sight_up_dn = ['N..N', 'd..d']
    sight_fb = ['N..N', 'd..d']
    sight_side = ['Nd', 'dk']

    return [
        _part_2d('cuff_inner', ((c - 2.5, t_cuff, -2.5), (c + 2.5, top, 2.5)), {
            'north': cuff_in, 'south': cuff_in, 'east': cuff_in, 'west': cuff_in,
            'up': _none, 'down': _none,
        }),
        _part_2d('cuff_outer', ((c - 3.0, t_cuff, -3.0), (c + 3.0, top, 3.0)), {
            'north': cuff_out, 'south': cuff_out, 'east': cuff_out, 'west': cuff_out,
            'up': _ring_cap('N', 'n', 'm', 'd'), 'down': _none,
        }),
        _part_2d('drum_x', ((c - R, t_drum, -r), (c + R, t_cuff, r)), {
            'east': octo_cardinal, 'west': octo_cardinal,
            'north': octo_step, 'south': octo_step,
            'up': _none, 'down': octo_down_closed(c - R, r),
        }, 'bit'),
        _part_2d('drum_f', ((c - r, t_drum, -R), (c + r, t_cuff, -r)), {
            'north': octo_cardinal, 'south': _none,
            'east': octo_step, 'west': octo_step,
            'up': _none, 'down': octo_down_closed(c - r, -r),
        }, 'bit'),
        _part_2d('drum_b', ((c - r, t_drum, r), (c + r, t_cuff, R)), {
            'south': octo_cardinal, 'north': _none,
            'east': octo_step, 'west': octo_step,
            'up': _none, 'down': octo_down_closed(c - r, R),
        }, 'bit'),
        _part_2d('barrel_inner', ((c - 1.5, t_tip, -2.5), (c + 1.5, t_drum, 0.5)), {
            'north': bar_in, 'south': bar_in, 'east': bar_in, 'west': bar_in,
            'up': _none, 'down': _bore_down('e', 'l', 's'),
        }),
        _part_2d('barrel_outer', ((c - 2.0, t_tip, -3.0), (c + 2.0, t_drum, 1.0)), {
            'north': bar_out, 'south': bar_out, 'east': bar_out, 'west': bar_out,
            'up': _none, 'down': _ring_cap('N', 'n', 'm', 'x'),
        }),
        _part_2d('sight_leaf', ((c - 1.0, top - 8.0, -3.5), (c + 1.0, top - 7.0, -2.5)), {
            'north': sight_fb, 'south': _none, 'east': sight_side, 'west': sight_side,
            'up': sight_up_dn, 'down': sight_up_dn,
        }),
    ]


BUILDERS_2D = {
    '2d_revolver_cutout': _build_2d_revolver_cutout,
    '2d_demolition_mgl': _build_2d_demolition_mgl,
    '2d_mortar_cannon': _build_2d_mortar_cannon,
    '2d_octo_revolver': _build_2d_octo_revolver,
    '2d_mgl_closed': _build_2d_mgl_closed,
    '2d_tf2_closed': _build_2d_tf2_closed,
    '2d_mgl_clean': _build_2d_mgl_clean,
    '2d_octo_closed': _build_2d_octo_closed,
}


def build(c, top, lamp='dark', kind='2d_mgl_closed', length=0.0, collar_w=5.0, sleeve=False):
    """The TNT launcher's parts on an arm centred at x c whose socket is at y top: the collar, barrel, muzzle ring and
    fork sight (bone 'tool'), and the octagonal drum (bone 'bit': turns 90 deg per shot)."""
    if kind in BUILDERS_2D:
        return BUILDERS_2D[kind](c, top)
    if kind == 'legacy':
        return _legacy_build(c, top)
    assert kind in SPECS, kind
    W, N, ch_in, ch_out, ch_span, bW, mW, sW, sGap = SPECS[kind]
    R, r = W / 2, N / 2

    part = lambda name, box, faces, bone='tool': dict(drill.part(name, box, _paint(faces)), bone=bone)
    parts = []

    # 1. Socket collar: when sleeved (6x6), an octagonal 6x1x6 collar matches the drum's exact outline (zero square
    #    eaves overhanging the drum's beveled corners); otherwise a flush 5x1x5 collar.
    if sleeve:
        cy0, cy1 = top - 1, top
        parts.append(part('housing_x', ((c - R, cy0, -r), (c + R, cy1, r)), {
            'east': slate_side, 'west': slate_side, 'north': slate_side, 'south': slate_side,
            'up': drum_up_painter(c, c - R, -r, R), 'down': solid('V'),
        }))
        parts.append(part('housing_f', ((c - r, cy0, -R), (c + r, cy1, -r)), {
            'north': slate_side, 'south': solid('.'), 'east': slate_side, 'west': slate_side,
            'up': drum_up_painter(c, c - r, -R, R), 'down': solid('V'),
        }))
        parts.append(part('housing_b', ((c - r, cy0, r), (c + r, cy1, R)), {
            'south': slate_side, 'north': solid('.'), 'east': slate_side, 'west': slate_side,
            'up': drum_up_painter(c, c - r, r, R), 'down': solid('V'),
        }))
    else:
        cw = collar_w / 2
        col_up = (lambda w, h: ['S' * w] + ['I' + 'D' * (w - 2) + 'U'] * (h - 2) + ['U' * w]) if collar_w > 5 else solid('D')
        collar = {f: slate_side for f in ('north', 'south', 'east', 'west')} | {'up': col_up, 'down': solid('V')}
        parts.append(part('housing', ((c - cw, top - 1, -cw), (c + cw, top, cw)), collar))

    # 2. Octagonal revolver drum (3 px tall, 3 flush non-overlapping cubes: drum_x + drum_f + drum_b, zero z-fighting!)
    y0, y1 = top - 4, top - 1
    dx_box = ((c - R, y0, -r), (c + R, y1, r))
    df_box = ((c - r, y0, -R), (c + r, y1, -r))
    db_box = ((c - r, y0, r), (c + r, y1, R))
    parts.append(part('drum_x', dx_box, {
        'east': drum_cardinal, 'west': drum_cardinal,
        'north': drum_step, 'south': drum_step,
        'up': drum_up_painter(c, c - R, -r, R),
        'down': drum_down_painter(c, c - R, r, R, ch_in, ch_out, ch_span),
    }, 'bit'))
    parts.append(part('drum_f', df_box, {
        'north': drum_cardinal, 'south': solid('.'),
        'east': drum_step, 'west': drum_step,
        'up': drum_up_painter(c, c - r, -R, R),
        'down': drum_down_painter(c, c - r, -r, R, ch_in, ch_out, ch_span),
    }, 'bit'))
    parts.append(part('drum_b', db_box, {
        'south': drum_cardinal, 'north': solid('.'),
        'east': drum_step, 'west': drum_step,
        'up': drum_up_painter(c, c - r, r, R),
        'down': drum_down_painter(c, c - r, R, R, ch_in, ch_out, ch_span),
    }, 'bit'))

    # 3. Light-steel fat barrel (4 px exposed between drum and muzzle ring), front recessed 0.25 px behind drum front
    # so the muzzle ring (+0.25 px lip) sits flush with the drum's front face (-R), exactly like round 5.
    bz0 = -R + 0.25
    bz1 = bz0 + bW
    parts.append(part('barrel', ((c - bW / 2, y0 - 4, bz0), (c + bW / 2, y0, bz1)), {
        'north': barrel_side, 'south': barrel_side, 'east': barrel_side, 'west': barrel_side,
        'up': solid('.'), 'down': solid('.'),
    }))

    # 4. Dark slate muzzle ring (1 px tall, 0.25 px wider per side than barrel, front flush at -R; 9 px total from socket)
    mz0 = -R
    mz1 = mz0 + mW
    parts.append(part('muzzle', ((c - mW / 2, y0 - 5, mz0), (c + mW / 2, y0 - 4, mz1)), {
        'north': muzzle_ring, 'south': muzzle_ring, 'east': muzzle_ring, 'west': muzzle_ring,
        'up': solid('I'), 'down': muzzle_bore,
    }))

    # 5. Two-prong fork sight on the barrel's front (-z, facing up when raised to fire), right behind the muzzle ring.
    # Depth 1.0 px (tucked 0.25 px into barrel front, projecting 0.5 px proud of drum/muzzle front — exact old projection).
    sz0, sz1 = -R - 0.5, -R + 0.5
    sy0, sy1 = y0 - 4, y0 - 2
    sight_faces = {
        'north': slate_side, 'south': solid('.'), 'east': slate_side, 'west': slate_side,
        'up': solid('S'), 'down': solid('.'),
    }
    x_in = sGap / 2
    parts.append(part('sight_l', ((c - x_in - sW, sy0, sz0), (c - x_in, sy1, sz1)), sight_faces))
    parts.append(part('sight_r', ((c + x_in, sy0, sz0), (c + x_in + sW, sy1, sz1)), sight_faces))

    return parts
