"""The drill for the frame (frame_model.py, TOOL=drill): the first power tool brought over from the big suit, sized
down to the frame's arm and redrawn.

2026-11-23 2D-layer rework (user picked R1-C diamond spire + R2-C '2d_spire_rotor' base, 8 cubes, 10.0 px overall,
64x64 standalone texture via tools/export-tools.py): rebuilt in the approved 2D-texture + cutout outer-layer design
system (completing all 7 power tools):
- compact 6x3.0x6 dark-slate/brushed-iron 2-layer cuff (`cuff_outer` over `cuff_inner` 5x3.0x5): on/off status lamp
  (`LAMP_IDLE` red / `LAMP_RUN` green) cleanly mounted on the dark-slate outer clamp band (`north`, centered for 1P
  cockpit) leaving the recessed inner layer 100% dedicated to the sculpted copper rotor motor drum + central
  brushed-steel commutator ring framed behind a riveted 6x2 iron inspection window;
- massive 7.0 px 4-stage spinning crystalline diamond spire (`bone='bit'` / `drill_bit`, 4 rev/s via ToolRotors):
  4.5x1.0x4.5 bolted dark-slate/iron rotary chuck, 5.0/4.5 steel-and-diamond 0.25 px-cutout seamless helical flighting,
  3.5/3.0 rotated 45 deg crystalline diamond helical spire flutes, and a 1.5x1.5x1.5 faceted diamond pilot tip.

Other 2026-11-23 2D-layer drafts kept as knobs:
- Round 2 spire bases: 2d_spire_ribbed, 2d_spire_coils, 2d_spire_vents;
- Round 1 concepts   : 2d_big_daddy, 2d_cat_yellow, 2d_diamond_spire, 2d_rock_breaker;
- Earlier 3D design  : classic (2026-11-13 / 2026-11-21 head-scaled).

Coordinates are raw (frame_model.py adds FY), the right arm's (+x; the left mirrors), centred on the arm's axis (x c,
z 0) under the socket (y top). Art at 2 texels per px, RGBA tuples ('.' see-through). Faces as frame_model.py's: north
/ south as seen from the front / back, east back -> front, west front -> back, up rows front -> back.
"""
from frame_radial_art import dims, FACES

_c = lambda h: tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)) + (255,)
# the iron armour's steel ramp (frame_iron_art.PAL) and the big suit's diamond (mining_tools_art.py: vanilla's)
S = {k: _c(v) for k, v in {'z': '22262e', 's': '3c424c', 'p': '58606a', 'l': '757c85', 'e': '8a9097', 'h': '9fa4a9',
                           'g': 'cdcfcf', 'w': 'fbf8f0'}.items()}
SL = {k: _c(v) for k, v in {'d': '25292c', 'k': '2f3437', 'm': '3b4246'}.items()}   # slate
D = {k: _c(v) for k, v in {'0': '0e7b7a', '1': '12a1a0', '2': '2ce3d9', '3': 'a1fbe8', '4': 'e4fffa'}.items()}


def grid(w, h, c='.'): return [[c] * w for _ in range(h)]


def step(f, w, h, metal):
    """A cone step's face: a lit rim, the body (lit column left, shaded right: light from the upper left), a shadow
    row under it; metal 'steel' or 'diamond'. Top and bottom: the body colour, a darker ring."""
    if f in ('up', 'down'):
        g = grid(w, h, S['p'] if metal == 'steel' else D['1'])
        for j in range(h):
            for i in range(w):
                if 0 < i < w - 1 and 0 < j < h - 1: g[j][i] = S['l'] if metal == 'steel' else D['2']
        return g
    lit, body, side, shade = (S['h'], S['e'], S['l'], S['p']) if metal == 'steel' else (D['4'], D['2'], D['1'], D['0'])
    g = grid(w, h, body)
    for j in range(h):
        g[j][0], g[j][-1] = lit if j < h - 1 else body, side
    g[0] = [S['g'] if metal == 'steel' and i % 2 == 0 else lit for i in range(w)]
    g[-1] = [shade] * w
    return g


def part(name, box, paint, rot=0):
    d = dims(box)
    return dict(name=name, box=box, faces={f: paint(f, *d[f]) for f in FACES}, rot=rot)


def studded(f, w, h):
    """The second steel step: diamond studs in its shadow row (the old cone_2's)."""
    g = step(f, w, h, 'steel')
    if f not in ('up', 'down'):
        for i in range(1, w, 3): g[-1][i] = D['2']
    else:
        for j, i in ((0, 0), (0, w - 1), (h - 1, 0), (h - 1, w - 1)): g[j][i] = D['2']
    return g


# The status lamp's colours (red idle, green spinning: LAMP): highlight, lit, rim.
# 'dark' (the saved files', 2026-11-14: in game): the lamp's highlight and lit texels in reserved colours (an unlit
# lamp, dark red), which tools/export-frame.py turns into two glowmasks, the red ('idle') and the green ('run') lamp:
# the game lights one by the suit's state (ToolLight.LAMP_IDLE / LAMP_RUN).
LAMPS = {'red': ('ffb0a0', 'e8402a', '9a2418'), 'green': ('c8ffc0', '4fe05a', '2a8a34'), 'dark': ('3d2622', '2e1915', '9a2418')}
# copper (frame_heart_art.EXTRA, frame_model.PAL Q / R): lit, mid, shade
CU = {'f': _c('e09868'), 'Q': _c('c07440'), 'C': _c('804426')}


def _rows(rows, pal):
    for r in rows: assert len(r) == len(rows[0]), rows
    return [[pal[ch] for ch in r] for r in rows]


def _part_2d(name, box, faces, pal, bone='tool', rot=0):
    """Builds a 2D-layer part from string grids with exact dimension validation."""
    d = dims(box)
    painted = {}
    for f in FACES:
        w, h = d[f]
        g = faces[f](w, h) if callable(faces[f]) else faces[f]
        assert len(g) == h and all(len(row) == w for row in g), (name, f, (w, h), (len(g), len(g[0]) if g else 0))
        painted[f] = [[pal[ch] for ch in row] for row in g]
    return dict(name=name, box=box, faces=painted, rot=rot, bone=bone)


def _blank(w, h):
    return ['.' * w] * h


def _ring_up(hi, mid, sh, dk):
    """12x12 top bevel rim around the 5x5 arm (10x10 center see-through so zero z-fighting with the socket)."""
    return [hi * 11 + mid] + [mid + '.' * 10 + sh] * 10 + [dk * 12]


def _helix_outer(w, h, period, blade_chars, tooth_ch=None, tooth_phase=None, slope=1):
    """Seamless 4-way helical cutout outer shell: wraps north -> west -> south -> east -> north with zero corner seams.
    `shift(i) = (i * period) // w` advances smoothly from 0 at col 0 to period-1 at col w-1, so next face's col 0
    lands at phase +period == 0 (mod period). Unfilled phases are '.' (alpha-0 cutout exposing the recessed core)."""
    out = []
    for j in range(h):
        row = []
        for i in range(w):
            sh = (i * period) // w
            ph = (j - slope * sh) % period
            ch = blade_chars[ph]
            if tooth_ch and ph == tooth_phase and (i + j) % 2 == 0:
                ch = tooth_ch
            row.append(ch)
        out.append(''.join(row))
    return out


def _helix_inner(w, h, period, core_chars, slope=1):
    """Matching recessed helical flute channel painted on the inner core 0.5 px deeper than the cutout spiral."""
    out = []
    for j in range(h):
        row = []
        for i in range(w):
            sh = (i * period) // w
            ph = (j - slope * sh) % period
            row.append(core_chars[ph])
        out.append(''.join(row))
    return out


def _cap_down(w, rim, mid, center, corner=None):
    """Concentric metallic or diamond underside cap (w x w)."""
    g = [[mid] * w for _ in range(w)]
    for j in range(w):
        for i in range(w):
            if i in (0, w - 1) or j in (0, w - 1):
                g[j][i] = rim
            elif 1 < i < w - 2 and 1 < j < w - 2:
                g[j][i] = center
    if corner and w >= 4:
        for j, i in ((1, 1), (1, w - 2), (w - 2, 1), (w - 2, w - 2)):
            g[j][i] = corner
    return [''.join(r) for r in g]


def _diamond_tip_side(w, h):
    """Faceted crystalline Minecraft diamond pilot point (3x3 texels for 1.5x1.5x1.5 px)."""
    assert (w, h) == (3, 3), (w, h)
    return [
        '432',  # top lit diamond crown bevel
        '321',  # mid bright diamond facet
        '210',  # sharp shaded tip point
    ]


def _diamond_tip_down(w, h):
    assert (w, h) == (3, 3), (w, h)
    return [
        '232',
        '343',
        '121',
    ]


def _pal_2d(lamp='dark'):
    W_, L_, r_ = LAMPS[lamp]
    extra = {
        'x': _c('16191c'), 'n': _c('4c5559'), 'N': _c('646e73'),
        'F': _c('f0b07a'), 'U': _c('5a2e18'),
        # Industrial mining ochre-yellow (CAT / DeWalt heavy equipment, weathered not neon)
        'Y': _c('f0be3c'), 'y': _c('d4941c'), 'o': _c('a2680e'), 'u': _c('6c4208'),
        'W': _c(W_), 'L': _c(L_), 'r': _c(r_), '.': '.',
    }
    return S | SL | D | CU | extra


def _cuff_down_chuck(w, rim, body, ring, bore):
    """10x10 underside of cuff_inner: machined plate framing the central rotary chuck bore."""
    g = [[body] * w for _ in range(w)]
    for j in range(w):
        for i in range(w):
            if i in (0, w - 1) or j in (0, w - 1):
                g[j][i] = rim
            elif 2 <= i < w - 2 and 2 <= j < w - 2:
                g[j][i] = bore
            elif i in (1, w - 2) or j in (1, w - 2):
                g[j][i] = ring
    for j, i in ((1, 1), (1, w - 2), (w - 2, 1), (w - 2, w - 2)):
        g[j][i] = rim
    return [''.join(r) for r in g]


# ---------------- 2026-11-23 2D-layer Round 1 drafts ----------------

def _build_2d_big_daddy(c, top, lamp='dark'):
    """Draft A (8 cubes, 10.0 px): Big Daddy / dieselpunk industrial bore.
    6x3.5x6 riveted iron outer shell with 0.5 px recessed copper motor coil bay & recessed status lamp,
    dark milled rotary chuck collar, and wide 3-stage 0.25 px-fluted helical steel-and-diamond auger."""
    P = _pal_2d(lamp)
    sq = lambda n, y0, y1: ((c - n / 2, y0, -n / 2), (c + n / 2, y1, n / 2))
    t = top - 3.5

    # Cuff inner (5x3.5x5 -> 10x7): dark slate housing + wound copper armature coils (rows 3-4) + recessed lamp on north
    in_side = [
        'nkkkkkkkkd',
        'kddddddddx',
        'dxxxxxxxxx',
        'xfQfQfQfQx',  # upper copper coil turn
        'xCQfCQfCQx',  # lower copper coil turn
        'dxxxxxxxxx',
        'kddddddddx',
    ]
    in_north = list(in_side)
    in_north[1] = 'kddrWLrddx'  # recessed status lamp centered on north (top in 1P cockpit!)

    # Cuff outer (6x3.5x6 -> 12x7): riveted iron shell w/ 0.5 px cutout coil bay (rows 3-4, cols 2..9) + lamp bezel on north
    out_side = [
        'hhhhhhhhhhhe',
        'egllllllllsp',
        'elppppppppzs',
        'ep........zp',  # open cutout exposing copper coils 0.5 px deeper
        'ep........zs',
        'eszzzzzzzzzs',
        'zssssssssssz',
    ]
    out_north = list(out_side)
    out_north[1] = 'egllk..kllsp'  # recessed framed bezel exposing the status lamp on north!

    # Rotary chuck collar (5.0x0.5x5.0 -> 10x1, bone='bit'): milled dark gunmetal jaw ring
    chuck_side = ['nxmxmxmxkx']

    # Stage 1 (y -6.5..-4.0, 2.5 px): 5.0 cutout steel/diamond helical flighting 0.25 px proud of 4.5 fluted gunmetal core
    s1_out = _helix_outer(10, 5, 5, ('g', 'e', '2', '.', '.'))
    s1_in = _helix_inner(9, 5, 5, ('m', 'k', 'd', 'x', 'd'))

    # Stage 2 (y -8.5..-6.5, 2.0 px, rot 45): 3.5 cutout diamond helical blades 0.25 px proud of 3.0 deep-teal core
    s2_out = _helix_outer(7, 4, 4, ('4', '3', '2', '.'))
    s2_in = _helix_inner(6, 4, 4, ('1', '0', 'd', 'x'))

    return [
        _part_2d('cuff_inner', sq(5.0, t, top), {
            'north': in_north, 'south': in_side, 'east': in_side, 'west': in_side,
            'up': _blank, 'down': _cuff_down_chuck(10, 's', 'p', 'l', 'x'),
        }, P, 'tool'),
        _part_2d('cuff_outer', sq(6.0, t, top), {
            'north': out_north, 'south': out_side, 'east': out_side, 'west': out_side,
            'up': _ring_up('h', 'e', 'p', 's'), 'down': _blank,
        }, P, 'tool'),
        _part_2d('chuck', sq(5.0, t - 0.5, t), {
            'north': chuck_side, 'south': chuck_side, 'east': chuck_side, 'west': chuck_side,
            'up': _blank, 'down': _cap_down(10, 'd', 'k', 'x', 'm'),
        }, P, 'bit'),
        _part_2d('s1_in', sq(4.5, t - 3.0, t - 0.5), {
            'north': s1_in, 'south': s1_in, 'east': s1_in, 'west': s1_in,
            'up': _blank, 'down': _cap_down(9, 's', 'p', 'k', '2'),
        }, P, 'bit'),
        _part_2d('s1_out', sq(5.0, t - 3.0, t - 0.5), {
            'north': s1_out, 'south': s1_out, 'east': s1_out, 'west': s1_out,
            'up': _blank, 'down': _blank,
        }, P, 'bit'),
        _part_2d('s2_in', sq(3.0, t - 5.0, t - 3.0), {
            'north': s2_in, 'south': s2_in, 'east': s2_in, 'west': s2_in,
            'up': _blank, 'down': _cap_down(6, '0', '1', '2'),
        }, P, 'bit', rot=45),
        _part_2d('s2_out', sq(3.5, t - 5.0, t - 3.0), {
            'north': s2_out, 'south': s2_out, 'east': s2_out, 'west': s2_out,
            'up': _blank, 'down': _blank,
        }, P, 'bit', rot=45),
        _part_2d('tip', sq(1.5, t - 6.5, t - 5.0), {
            'north': _diamond_tip_side, 'south': _diamond_tip_side,
            'east': _diamond_tip_side, 'west': _diamond_tip_side,
            'up': _blank, 'down': _diamond_tip_down,
        }, P, 'bit'),
    ]


def _build_2d_cat_yellow(c, top, lamp='dark'):
    """Draft B (7 cubes, 9.5 px): Heavy Construction TBM — weathered Caterpillar industrial ochre-yellow cowling
    with dark gunmetal roll-cage corners, recessed copper motor bay & status lamp, and meaty aligned 0.25 px-fluted
    helical diamond TBM cone."""
    P = _pal_2d(lamp)
    sq = lambda n, y0, y1: ((c - n / 2, y0, -n / 2), (c + n / 2, y1, n / 2))
    t = top - 3.5

    # Cuff inner (5x3.5x5 -> 10x7): dark engine core + copper cooling coils + recessed status lamp
    in_side = [
        'mkkkkkkkkd',
        'kddddddddx',
        'dxxxxxxxxx',
        'xdfQfQfQdx',
        'xdCQfCQfdx',
        'dxxxxxxxxx',
        'kddddddddx',
    ]
    in_north = list(in_side)
    in_north[1] = 'kddrWLrddx'

    # Cuff outer (6x3.5x6 -> 12x7): CAT industrial yellow cowling framed by heavy dark gunmetal roll-cage corners
    out_side = [
        'mnYYYYYYYYnm',  # lit yellow crown between dark gunmetal corner caps
        'mkYyyyyyyYkd',  # weathered yellow upper panel
        'mkoyyyyyyokd',  # yellow body with lower shadow edge
        'mdo......okd',  # 0.5 px cutout radiator/coil bay
        'mdo......okd',
        'mduoooooooud',  # shaded yellow lower sill
        'dddddddddddd',  # heavy gunmetal bumper collar
    ]
    out_north = list(out_side)
    out_north[1] = 'mkYyk..kyYkd'  # symmetric framed status lamp cutout centered on yellow brow

    # Stage 1 (y -6.0..-3.5, 2.5 px, rot 0): heavy 5.0 cutout steel/diamond spiral 0.25 px proud of 4.5 gunmetal core
    s1_out = _helix_outer(10, 5, 5, ('h', 'e', '3', '.', '.'))
    s1_in = _helix_inner(9, 5, 5, ('k', 'd', 'x', 'x', 'd'))

    # Stage 2 (y -8.0..-6.0, 2.0 px, rot 0 — aligned smooth taper 5.0 -> 4.0): 4.0 cutout diamond helix over 3.5 core
    s2_out = _helix_outer(8, 4, 4, ('4', '3', '2', '.'))
    s2_in = _helix_inner(7, 4, 4, ('1', '0', 'd', 'x'))

    return [
        _part_2d('cuff_inner', sq(5.0, t, top), {
            'north': in_north, 'south': in_side, 'east': in_side, 'west': in_side,
            'up': _blank, 'down': _cuff_down_chuck(10, 'x', 'd', 'k', 'x'),
        }, P, 'tool'),
        _part_2d('cuff_outer', sq(6.0, t, top), {
            'north': out_north, 'south': out_side, 'east': out_side, 'west': out_side,
            'up': _ring_up('Y', 'y', 'o', 'u'), 'down': _blank,
        }, P, 'tool'),
        _part_2d('s1_in', sq(4.5, t - 2.5, t), {
            'north': s1_in, 'south': s1_in, 'east': s1_in, 'west': s1_in,
            'up': _blank, 'down': _cap_down(9, 'd', 'k', 'x', '2'),
        }, P, 'bit'),
        _part_2d('s1_out', sq(5.0, t - 2.5, t), {
            'north': s1_out, 'south': s1_out, 'east': s1_out, 'west': s1_out,
            'up': _blank, 'down': _blank,
        }, P, 'bit'),
        _part_2d('s2_in', sq(3.5, t - 4.5, t - 2.5), {
            'north': s2_in, 'south': s2_in, 'east': s2_in, 'west': s2_in,
            'up': _blank, 'down': _cap_down(7, '0', '1', '2'),
        }, P, 'bit'),
        _part_2d('s2_out', sq(4.0, t - 4.5, t - 2.5), {
            'north': s2_out, 'south': s2_out, 'east': s2_out, 'west': s2_out,
            'up': _blank, 'down': _blank,
        }, P, 'bit'),
        _part_2d('tip', sq(1.5, t - 6.0, t - 4.5), {
            'north': _diamond_tip_side, 'south': _diamond_tip_side,
            'east': _diamond_tip_side, 'west': _diamond_tip_side,
            'up': _blank, 'down': _diamond_tip_down,
        }, P, 'bit', rot=45),
    ]


def _spire_bit(c, t, P):
    """The 7.0 px 4-stage crystalline twisted diamond spire picked in Round 1 (C: 2d_diamond_spire)."""
    sq = lambda n, y0, y1: ((c - n / 2, y0, -n / 2), (c + n / 2, y1, n / 2))
    chuck_side = [
        'nlnknlnkn',
        'dxdxdxdxd',
    ]
    s1_out = _helix_outer(10, 5, 5, ('g', '3', '2', '.', '.'))
    s1_in = _helix_inner(9, 5, 5, ('p', 's', '0', 'x', '0'))
    s2_out = _helix_outer(7, 4, 4, ('4', '3', '2', '.'))
    s2_in = _helix_inner(6, 4, 4, ('2', '1', '0', 'x'))
    return [
        _part_2d('chuck', sq(4.5, t - 1.0, t), {
            'north': chuck_side, 'south': chuck_side, 'east': chuck_side, 'west': chuck_side,
            'up': _blank, 'down': _cap_down(9, 's', 'p', 'x', 'l'),
        }, P, 'bit'),
        _part_2d('s1_in', sq(4.5, t - 3.5, t - 1.0), {
            'north': s1_in, 'south': s1_in, 'east': s1_in, 'west': s1_in,
            'up': _blank, 'down': _cap_down(9, '0', '1', '2', '3'),
        }, P, 'bit'),
        _part_2d('s1_out', sq(5.0, t - 3.5, t - 1.0), {
            'north': s1_out, 'south': s1_out, 'east': s1_out, 'west': s1_out,
            'up': _blank, 'down': _blank,
        }, P, 'bit'),
        _part_2d('s2_in', sq(3.0, t - 5.5, t - 3.5), {
            'north': s2_in, 'south': s2_in, 'east': s2_in, 'west': s2_in,
            'up': _blank, 'down': _cap_down(6, '0', '1', '3'),
        }, P, 'bit', rot=45),
        _part_2d('s2_out', sq(3.5, t - 5.5, t - 3.5), {
            'north': s2_out, 'south': s2_out, 'east': s2_out, 'west': s2_out,
            'up': _blank, 'down': _blank,
        }, P, 'bit', rot=45),
        _part_2d('tip', sq(1.5, t - 7.0, t - 5.5), {
            'north': _diamond_tip_side, 'south': _diamond_tip_side,
            'east': _diamond_tip_side, 'west': _diamond_tip_side,
            'up': _blank, 'down': _diamond_tip_down,
        }, P, 'bit'),
    ]


def _build_2d_diamond_spire(c, top, lamp='dark'):
    """Draft C (8 cubes, 10.0 px): Compact 3.0 px Power-Suit iron/slate cuff + massive 7.0 px 4-stage crystalline
    diamond spire (Round 1 baseline)."""
    P = _pal_2d(lamp)
    sq = lambda n, y0, y1: ((c - n / 2, y0, -n / 2), (c + n / 2, y1, n / 2))
    t = top - 3.0

    in_side = [
        'nkkkkkkkkd',
        'kddddddddx',
        'xfQfQfQfQx',
        'xCQfCQfCQx',
        'dxxxxxxxxx',
        'kddddddddx',
    ]
    in_north = list(in_side)
    in_north[1] = 'kddrWLrddx'

    out_side = [
        'nnnnnnnnnnnm',
        'mkmmmmmmmmkd',
        'ep........zp',
        'es........zs',
        'elppppppppzs',
        'zssssssssssz',
    ]
    out_north = list(out_side)
    out_north[1] = 'mkmmk..kmmkd'

    return [
        _part_2d('cuff_inner', sq(5.0, t, top), {
            'north': in_north, 'south': in_side, 'east': in_side, 'west': in_side,
            'up': _blank, 'down': _cuff_down_chuck(10, 's', 'p', 'l', 'x'),
        }, P, 'tool'),
        _part_2d('cuff_outer', sq(6.0, t, top), {
            'north': out_north, 'south': out_side, 'east': out_side, 'west': out_side,
            'up': _ring_up('n', 'm', 'k', 'd'), 'down': _blank,
        }, P, 'tool'),
    ] + _spire_bit(c, t, P)


def _build_2d_spire_base(c, top, lamp, in_side, out_side, north_lamp_row):
    """Round 2 polished bases for the picked diamond spire: pure sculpted motor on cuff_inner,
    on/off status lamp cleanly mounted on cuff_outer's north clamp band."""
    P = _pal_2d(lamp)
    sq = lambda n, y0, y1: ((c - n / 2, y0, -n / 2), (c + n / 2, y1, n / 2))
    t = top - 3.0
    out_north = list(out_side)
    out_north[1] = north_lamp_row
    return [
        _part_2d('cuff_inner', sq(5.0, t, top), {
            'north': in_side, 'south': in_side, 'east': in_side, 'west': in_side,
            'up': _blank, 'down': _cuff_down_chuck(10, 's', 'p', 'l', 'x'),
        }, P, 'tool'),
        _part_2d('cuff_outer', sq(6.0, t, top), {
            'north': out_north, 'south': out_side, 'east': out_side, 'west': out_side,
            'up': _ring_up('n', 'm', 'k', 'd'), 'down': _blank,
        }, P, 'tool'),
    ] + _spire_bit(c, t, P)


def _build_2d_spire_ribbed(c, top, lamp='dark'):
    """R2-A: Twin sculpted 3x2 copper motor drums behind a central iron stator bridge; on/off lamp on outer band."""
    in_side = [
        'nkkkkkkkkd',
        'dxxxxxxxxx',
        'xffQddffQx',  # twin solid top-lit copper coils separated by dark center stator
        'xQCCxxQCCx',  # shaded underside of each copper coil
        'dxxxxxxxxx',
        'kddddddddx',
    ]
    out_side = [
        'nnnnnnnnnnnm',
        'mkmmmmmmmmkd',
        'ep...el...zp',  # twin 3x2 cutout motor bays split by a solid 2-texel iron bridge
        'es...ps...zs',
        'elppppppppzs',
        'zssssssssssz',
    ]
    return _build_2d_spire_base(c, top, lamp, in_side, out_side, 'mkmmkWLkmmkd')


def _build_2d_spire_coils(c, top, lamp='dark'):
    """R2-B: Wide open motor bay revealing 3 clean, solid 2-texel vertical copper stator coils w/ dark pole gaps."""
    in_side = [
        'nkkkkkkkkd',
        'dxxxxxxxxx',
        'xffxffxffx',  # 3 crisp lit copper coil drums (zero 1px checkerboard noise)
        'xQCxQCxQCx',  # shaded lower curve of each coil drum
        'dxxxxxxxxx',
        'kddddddddx',
    ]
    out_side = [
        'nnnnnnnnnnnm',
        'mkmmmmmmmmkd',
        'ep........zp',  # clean open 8x2 motor bay framed by iron shell
        'es........zs',
        'elppppppppzs',
        'zssssssssssz',
    ]
    return _build_2d_spire_base(c, top, lamp, in_side, out_side, 'mkmmkWLkmmkd')


def _build_2d_spire_rotor(c, top, lamp='dark'):
    """R2-C: Framed 6x2 riveted inspection window over a sculpted copper rotor drum + bright central steel commutator."""
    in_side = [
        'nkkkkkkkkd',
        'dxxxxxxxxx',
        'xxfQhhQfxx',  # smooth copper rotor flanks + bright central brushed-steel drive ring
        'xxQCppCQxx',  # shaded lower curve of copper rotor + steel ring
        'dxxxxxxxxx',
        'kddddddddx',
    ]
    out_side = [
        'nnnnnnnnnnnm',
        'mkmmmmmmmmkd',
        'egp......pzs',  # riveted iron flanks framing a clean 6x2 motor window
        'elp......pzs',
        'elppppppppzs',
        'zssssssssssz',
    ]
    return _build_2d_spire_base(c, top, lamp, in_side, out_side, 'mkmmkWLkmmkd')


def _build_2d_spire_vents(c, top, lamp='dark'):
    """R2-D: Heavy armoured iron grille with 3 twin-texel vertical cooling slots over a smooth horizontal copper motor drum."""
    in_side = [
        'nkkkkkkkkd',
        'dxxxxxxxxx',
        'xFffffffFx',  # clean horizontal top-lit copper motor cylinder
        'xQQQQQQQQx',  # warm mid-copper motor core
        'xCCCCCCCCx',  # deep shaded underside
        'kddddddddx',
    ]
    out_side = [
        'nnnnnnnnnnnm',
        'mkmmmmmmmmkd',
        'ep..p..p..zs',  # 3 crisp 2-texel-wide vertical iron grille vents
        'es..s..s..zs',
        'elppppppppzs',
        'zssssssssssz',
    ]
    return _build_2d_spire_base(c, top, lamp, in_side, out_side, 'mkmmkWLkmmkd')


def _build_2d_rock_breaker(c, top, lamp='dark'):
    """Draft D (7 cubes, 10.0 px): Deep-Core Rotary Rock-Breaker — burnished copper & dark forged slate cuff
    with wide recessed hydraulic piston bay and a static 0.5 px cutout debris-guard cage framing the upper spinning auger."""
    P = _pal_2d(lamp)
    sq = lambda n, y0, y1: ((c - n / 2, y0, -n / 2), (c + n / 2, y1, n / 2))
    t = top - 3.5

    # Cuff inner (5x3.5x5 -> 10x7): dark forged slate + bright twin recessed steel hydraulic pistons + lamp on north
    in_side = [
        'nkkkkkkkkd',
        'kddddddddx',
        'dxxxxxxxxx',
        'xxghxxhgxx',  # twin recessed vertical brushed-steel piston rods
        'xxelxxlexx',
        'xxpsxxspxx',
        'kddddddddx',
    ]
    in_north = list(in_side)
    in_north[1] = 'kddrWLrddx'

    # Cuff outer (6x3.5x6 -> 12x7): burnished copper & dark gunmetal industrial casing w/ wide piston bay cutout
    out_side = [
        'mmFFFFFFFFmm',
        'mkfQQQQQQfkd',
        'mkCQQQQQQCkd',
        'md........kd',  # wide 0.5 px cutout exposing twin steel hydraulic pistons inside dark bay
        'md........kd',
        'mdUUUUUUUUkd',
        'dddddddddddd',
    ]
    out_north = list(out_side)
    out_north[1] = 'mkfQk..kQfkd'

    # Static 0.5 px cutout scalloped debris-guard shroud (5.0x2.0x5.0 -> 10x4, bone='tool') wrapping the spinning auger!
    shroud_side = [
        'nmmmmmmmmk',  # heavy dark-slate bolted torque ring
        'mk......kd',  # wide open cutout inspection bay (cols 2..7 open!) showing spinning helical auger inside
        'md......kd',
        'dx......xd',  # dark forged guard teeth gripping around the spinning bore
    ]

    # Spinning upper auger shaft (4.0x3.5x4.0 -> 8x7, bone='bit'): clean crisp helical steel & diamond flutes
    auger_side = _helix_outer(8, 7, 4, ('h', '3', '2', 'x'))

    # Stage 2 diamond cutter crown (y -8.5..-7.0, 1.5 px, rot 45): 3.5 cutout diamond crown 0.25 px proud of 3.0 core
    s2_out = _helix_outer(7, 3, 3, ('4', '2', '.'))
    s2_in = _helix_inner(6, 3, 3, ('1', '0', 'x'))

    return [
        _part_2d('cuff_inner', sq(5.0, t, top), {
            'north': in_north, 'south': in_side, 'east': in_side, 'west': in_side,
            'up': _blank, 'down': _cuff_down_chuck(10, 'x', 'd', 'k', 'x'),
        }, P, 'tool'),
        _part_2d('cuff_outer', sq(6.0, t, top), {
            'north': out_north, 'south': out_side, 'east': out_side, 'west': out_side,
            'up': _ring_up('F', 'f', 'Q', 'C'), 'down': _blank,
        }, P, 'tool'),
        _part_2d('shroud_outer', sq(5.0, t - 2.0, t), {
            'north': shroud_side, 'south': shroud_side, 'east': shroud_side, 'west': shroud_side,
            'up': _blank, 'down': _blank,
        }, P, 'tool'),
        _part_2d('auger_shaft', sq(4.0, t - 3.5, t), {
            'north': auger_side, 'south': auger_side, 'east': auger_side, 'west': auger_side,
            'up': _blank, 'down': _cap_down(8, 's', 'p', '0', '2'),
        }, P, 'bit'),
        _part_2d('s2_in', sq(3.0, t - 5.0, t - 3.5), {
            'north': s2_in, 'south': s2_in, 'east': s2_in, 'west': s2_in,
            'up': _blank, 'down': _cap_down(6, '0', '1', '2'),
        }, P, 'bit', rot=45),
        _part_2d('s2_out', sq(3.5, t - 5.0, t - 3.5), {
            'north': s2_out, 'south': s2_out, 'east': s2_out, 'west': s2_out,
            'up': _blank, 'down': _blank,
        }, P, 'bit', rot=45),
        _part_2d('tip', sq(1.5, t - 6.5, t - 5.0), {
            'north': _diamond_tip_side, 'south': _diamond_tip_side,
            'east': _diamond_tip_side, 'west': _diamond_tip_side,
            'up': _blank, 'down': _diamond_tip_down,
        }, P, 'bit'),
    ]


BUILDERS_2D = {
    '2d_big_daddy': _build_2d_big_daddy,
    '2d_cat_yellow': _build_2d_cat_yellow,
    '2d_diamond_spire': _build_2d_diamond_spire,
    '2d_rock_breaker': _build_2d_rock_breaker,
    '2d_spire_ribbed': _build_2d_spire_ribbed,
    '2d_spire_coils': _build_2d_spire_coils,
    '2d_spire_rotor': _build_2d_spire_rotor,
    '2d_spire_vents': _build_2d_spire_vents,
}


# BODY (2026-11-13, user: the drill's 3D housing and guard didn't feel right; like the shoulder plates, the heart
# engine and the helmet it reads better as a simple block with the elements painted on, so they replaced it with one
# block, then: fit it to the shoulder plate above it, just bigger than the arm). One 6 x 4 x 6 block, 0.5 px past the
# arm on every side (as the plate is past its top), its top 2 px round the arm's end (the base: it clamps on the
# socket), the bottom 2 px under it (the motor), the bit under that. 2 texels per px: sides 12 x 8, top / bottom 12 x 12.
# The base: a slate clamp band (lit top row, two bolts a face, the status lamp at the front's outer end), a dark seam;
# the motor under it in steel, its middle rows the draft's element (DRILL_ART): A vent slots | B a copper winding
# window | C cooling fins.
# (rows drawn for a face w texels wide: 12 on the 6 px block, 10 on the 5 px one, FIT)
def BASE(w):
    bolts = list('m' * (w - 1) + 'k'); bolts[2] = bolts[w - 3] = 'h'
    return ['n' * (w - 1) + 'm', 'm' * (w - 1) + 'k', ''.join(bolts), 'x' * w]
def LAMP_AT(w):   # the front's base row 1 (its outer end first): the lamp 2 x 1 texels, its top row (2026-11-13,
    # user: the 2 x 2 lamp's bottom row gone, the bolts' row under it as on the other faces, its bolt back)
    return {1: 'mWL' + 'm' * (w - 4) + 'k'}
def MOTOR(art, w):
    vents = list('e' + 'l' * (w - 2) + 'p')
    for i in (2, 4, w - 5, w - 3): vents[i] = 'z'
    mid = {'A': [''.join(vents)] * 2, 'B': ['elz' + 'f' * (w - 6) + 'zlp', 'elz' + ('QC' * w)[:w - 6] + 'zlp'],
           'C': ['z' * w, 'h' * (w - 1) + 'e']}[art]
    return ['h' * (w - 1) + 'e'] + mid + ['z' * w if art == 'C' else 's' * w]
# underneath (rows front -> back): the motor's steel round a dark chuck hole the bit hangs from, a bolt in each corner;
# on top only its 1-texel rim shows round the arm: the base's lit slate
def DOWN(w): return ['p' * w, 'ph' + 'l' * (w - 4) + 'hp'] + ['pl' + 'x' * (w - 4) + 'lp'] * (w - 4) + ['ph' + 'l' * (w - 4) + 'hp', 'p' * w]
def UP(w): return ['n' * w] + ['n' + 'k' * (w - 2) + 'n'] * (w - 2) + ['n' * w]


# The base open behind and inside (DRILL_BASE=open, 2026-11-13, user, picking B: the inner and back sides without the
# dark band, see-through, for an asymmetric look): the clamp wraps only the front and outer side, a plate 0.5 px off
# the arm like the shoulder plate's decal, and the arm's end shows behind and inside. 'wrap' keeps the closed band.
# So the block is two boxes, base over motor, the same outside: open, one box let the eye down the 0.5 px gap into
# its inside (the bit's top and the block's bottom, back to back there, flickered); the motor's own top closes it,
# its 1-texel rim round the arm a lit ledge.
OPEN = ('south', 'west')   # the back, and the inner side (the right arm's west; the left mirrors it)
LEDGE = ['e' * 12] + ['e' + 'l' * 10 + 'p'] * 10 + ['p' * 12]


def _pal(lamp):
    W_, L_, r_ = LAMPS[lamp]
    return S | SL | {'x': _c('1a1d1f'), 'n': _c('4c5559')} | CU | {'W': _c(W_), 'L': _c(L_), 'r': _c(r_), '.': '.'}


def base(lamp, mode='open'):
    front = [LAMP_AT(12).get(j, r) for j, r in enumerate(BASE(12))]
    faces = {'north': front, 'up': UP(12), 'down': ['.' * 12] * 12}
    if mode == 'open':
        for f in OPEN: faces[f] = ['.' * 12] * len(BASE(12))
        # the top's rim along the open sides goes too (rows front -> back, columns inner -> outer on the right arm)
        faces['up'] = ['.' + r[1:] for r in UP(12)[:-1]] + ['.' * 12]
    return lambda f, w, h: _rows(faces.get(f, BASE(12)), _pal(lamp))


def motor(art, lamp):
    faces = {'up': LEDGE, 'down': DOWN(12)}
    return lambda f, w, h: _rows(faces.get(f, MOTOR(art, 12)), _pal(lamp))


# The fist fit (DRILL_FIT=fist, 2026-11-13, user: the block bigger than the arm made the tool arm look differently sized
# from the other; the right arm's hand is 4 px tall and 5 wide, so the body as the arm instead of round it, the drill
# its extension): the body a 5 x 4 x 5 box flush with the arm where the right arm's fist is (the arm's own footprint,
# under the socket), base over motor painted as before (closed all round: nothing of the arm is inside it to show),
# the bit under it. Picked (2026-11-13: the arms match from behind, every tool can take the fist's place and grow from
# its bottom, the bit stands out). 'sleeve' is the 6 x 4 x 6 body round the arm's end.
# DRILL_BAND (2026-11-13, user: the drill and chainsaw should look more alike; draft): 'slate' the base band slate and
# the motor's window copper | 'copper' the two swapped, the band in copper as the chainsaw's cowl, the window slate.
def fist(art, lamp, band='slate', w=10):
    side = BASE(w) + MOTOR(art, w)
    front = [LAMP_AT(w).get(j, r) for j, r in enumerate(side)]
    faces = {'north': front, 'up': UP(w) if w > 10 else ['k' * w] * w, 'down': DOWN(w)}
    pal = _pal(lamp)
    if band == 'copper':   # slate n / m / k (lit, mid, shade) <-> copper f / Q / C: on this body only those parts use them
        pal = pal | {'n': pal['f'], 'm': pal['Q'], 'k': pal['C'], 'f': pal['n'], 'Q': pal['m'], 'C': pal['k']}
    return lambda f, w, h: _rows(faces.get(f, side), pal)


def build(c, top, lamp='red', art='B', mode='open', fit='sleeve', band='slate', head_scale=False, kind='2d_spire_rotor'):
    """The drill's parts on an arm centred at x c (right side) whose end (the socket) is at y top: name, box (raw),
    faces, rot (deg about the arm's axis, y), bone ('tool': still; 'bit': spins). The body (base, motor) is still,
    the steps under it spin."""
    if kind in BUILDERS_2D:
        return BUILDERS_2D[kind](c, top, lamp=lamp)
    sq = lambda n, y0, y1: ((c - n / 2, y0, -n / 2), (c + n / 2, y1, n / 2))
    t = top
    if fit in ('fist', 'sleeve_box'):
        bw = 6 if fit == 'sleeve_box' else 5
        parts = [part('body', sq(bw, t - 4, t), fist(art, lamp, band, bw * 2))]
        t -= 2   # the bit hangs 2 px lower (under the 4 px body, not the sleeve's 2 below the socket)
    else:
        parts = [part('base', sq(6, t, t + 2), base(lamp, mode)), part('motor', sq(6, t - 2, t), motor(art, lamp))]
    s2, s3, tip_w = (4.5, 3.0, 1.5) if head_scale else (4, 3, 1)
    bit = [part('s2', sq(s2, t - 4, t - 2), studded, -22.5),
           part('s3', sq(s3, t - 6, t - 4), lambda f, w, h: step(f, w, h, 'diamond'), 22.5),
           part('tip', sq(tip_w, t - 7, t - 6), lambda f, w, h: step(f, w, h, 'diamond'), 45)]
    for p in parts: p['bone'] = 'tool'
    for p in bit: p['bone'] = 'bit'
    return parts + bit
