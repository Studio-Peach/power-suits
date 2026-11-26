"""Redesigned bare-frame chassis art in the 2D-texture + 0.5 px cutout outer-layer design system (2026-11-23).

Addresses playtest feedback that the original 1x-density bare frame read noisy and hard to distinguish (both parked
with far-wall cutout collision and mixed with iron/copper armour or engines).

Every part is authored at 2 texels per px (K=2), matching the helmets, engines, shoulder caps, and all 7 reworked
tools:
- Zero random/diagonal grain noise, zero 1-texel checkerboards, zero 1-texel slivers.
- Clean value hierarchy so bare frame, pilot, engines, copper armour, and iron armour read apart immediately.
- 2-layer architectural depth (0.5 px separation):
  - Torso always uses a 0.5 px recessed inner core (z +-2.5, x +-4.5 / CHEST_X-0.5) behind the z +-3.0 outer shell
    so the outer envelope never grows into the engine harnesses (z +-3.5) or armour planes.
  - 'exo_layered' (B) and 'heavy_harness' (D) also wrap limbs in a 0.5 px proud outer cutout exo-layer (matching
    shoulder_plate's DECAL=0.5 offset, stopping cleanly at SOCKET_Y=17 on arms so 6x6 tool cuffs clamp flush below).

Draft options (env FRAME_LOOK in frame_model.py):
  current        original 1x frame (default until a pick is made)
  dark_cage      A: flush dark-gunmetal open chassis + 2-layer recessed torso bay & warm leather straps
  exo_layered    B: full 2-layer 0.5 px cutout exo-struts over calm dark-slate/leather pilot harness
  clean_steel    C: flush refined mid-steel open cage (keeps steel DNA, strips 1x noise & clutter)
  heavy_harness  D: full 2-layer 0.5 px cutout charcoal frame + saddle-leather harness + muted brass joint pins

Face column conventions (frame_model.py, right side; left mirrored automatically):
  north  outer (+x) -> inner (-x) on limbs; +x -> -x on torso (symmetric)
  south  inner (-x) -> outer (+x) on limbs; -x -> +x on torso (symmetric)
  east   back (+z) -> front (-z)
  west   front (-z) -> back (+z)
  up     rows front -> back, cols inner -> outer (limbs) or -x -> +x (torso)
  down   rows back -> front, cols inner -> outer (limbs) or -x -> +x (torso)
"""

# Self-contained palette resolved to (R, G, B, 255) RGBA tuples by build(), avoiding any letter collisions
# with frame_model.PAL / ARMPAL / engine / helmet palettes (frame_model.paint_shells accepts 4-tuples directly).
PAL = {
    # Iron armour steel ramp (frame_iron_art.py)
    'z': (0x22, 0x26, 0x2e), 's': (0x3c, 0x42, 0x4c), 'p': (0x58, 0x60, 0x6a),
    'l': (0x75, 0x7c, 0x85), 'e': (0x8a, 0x90, 0x97), 'h': (0x9f, 0xa4, 0xa9),
    # Neutral dark slate ramp (frame_iron_art.py)
    'x': (0x1a, 0x1d, 0x1f), 'd': (0x25, 0x29, 0x2c), 'k': (0x2f, 0x34, 0x37),
    'm': (0x3b, 0x42, 0x46), 'n': (0x4c, 0x55, 0x59), 'O': (0x62, 0x67, 0x6c),
    # Dark cool forged-iron (sits cleanly below iron armour's p/l/e/h)
    'u': (0x32, 0x38, 0x40), 'r': (0x44, 0x4c, 0x54), 't': (0x5c, 0x65, 0x70),
    # Warm saddle leather ramp
    'c': (0x2d, 0x1c, 0x13), 'H': (0x40, 0x29, 0x1d), 'L': (0x5e, 0x3e, 0x2c), 'b': (0x7a, 0x52, 0x3b),
    # Muted industrial brass (restrained joint pins / pistons)
    'Z': (0x6a, 0x58, 0x38), 'a': (0x8f, 0x7b, 0x52), 'Y': (0xa8, 0x91, 0x60),
    # Tool-matched specular & copper servo ramps (from frame_drill_art / frame_iron_art)
    'g': (0xcd, 0xcf, 0xcf), 'w': (0xfb, 0xf8, 0xf0),
    'F': (0xf2, 0xb8, 0x80), 'f': (0xe0, 0x98, 0x68), 'Q': (0xc0, 0x74, 0x40),
    'R': (0x80, 0x44, 0x26), 'C': (0x5a, 0x2c, 0x16),
    # Tool socket contact cyan
    '+': (0x2c, 0xe3, 0xd9),
}

STYLES = {
    'dark_cage': dict(
        layered_limbs=False,
        # Outer structural frame: calm dark gunmetal/slate (clearly darker than iron armour)
        hi='O', mid='n', sh='m', dk='k', ink='x',
        # Inner core / harness backing
        in_hi='m', in_mid='k', in_sh='d',
        # Leather straps
        l_hi='b', l_mid='L', l_sh='H', l_dk='c',
        # Joint actuator accents (quiet gunmetal)
        pin_hi='O', pin_mid='n', pin_sh='d',
        # Solid inner backplates on limbs? No, wide clean open windows
        limb_open=True,
    ),
    'exo_layered': dict(
        layered_limbs=True,
        # Outer 0.5 px cutout exo-struts: cool dark forged iron (distinct from bright iron armour)
        hi='t', mid='r', sh='u', dk='d', ink='x',
        # Inner pilot harness sleeve: very calm deep slate
        in_hi='m', in_mid='k', in_sh='d',
        # Leather harness trim
        l_hi='b', l_mid='L', l_sh='H', l_dk='c',
        # Joint hubs
        pin_hi='p', pin_mid='r', pin_sh='x',
        limb_open=False,
    ),
    'clean_steel': dict(
        layered_limbs=False,
        # Mid-steel frame stepped clearly darker than iron armour (l/p/s instead of g/h/e)
        hi='l', mid='p', sh='s', dk='z', ink='x',
        # Inner dark slate backing
        in_hi='m', in_mid='k', in_sh='d',
        # Leather harness
        l_hi='b', l_mid='L', l_sh='H', l_dk='c',
        # Joint accents
        pin_hi='n', pin_mid='m', pin_sh='d',
        limb_open=True,
    ),
    'heavy_harness': dict(
        layered_limbs=True,
        # Outer 0.5 px cutout exo-struts: matte industrial charcoal
        hi='n', mid='m', sh='k', dk='d', ink='x',
        # Inner pilot harness: deep dark slate + prominent saddle leather
        in_hi='k', in_mid='d', in_sh='x',
        # Saddle leather
        l_hi='b', l_mid='L', l_sh='H', l_dk='c',
        # Muted brass actuator pins / pistons (recessed strictly into joint sockets)
        pin_hi='Y', pin_mid='a', pin_sh='Z',
        limb_open=False,
    ),
}


def _grid(w, h, fill='.'):
    return [[fill] * w for _ in range(h)]


def _str(g):
    return [''.join(r) for r in g]


def _rect(g, x0, y0, x1, y1, ch):
    h, w = len(g), len(g[0])
    for y in range(max(0, y0), min(h, y1)):
        for x in range(max(0, x0), min(w, x1)):
            g[y][x] = ch


def _hline(g, y, x0, x1, ch):
    _rect(g, x0, y, x1, y + 1, ch)


def _vline(g, x, y0, y1, ch):
    _rect(g, x, y0, x + 1, y1, ch)


# ---------------------------------------------------------------- 2x mechanical fist, boot & socket
def _fist_2x(st):
    """Clean 2x (10x8 side, 10x10 down) dark mechanical gauntlet matching the suit's fist silhouette."""
    hi, mid, sh, dk, ink = st['in_hi'], st['in_mid'], st['in_sh'], 'd', st['ink']
    fhi, fmid, fsh = st['mid'], st['sh'], st['dk']

    def side(knuckles=False, thumb=False):
        g = _grid(10, 8, mid)
        # Wrist cuff collar (rows 0..1)
        _hline(g, 0, 0, 10, dk)
        _hline(g, 1, 0, 10, fsh)
        # Back-of-hand armour plate (rows 2..4)
        _rect(g, 0, 2, 10, 5, fmid)
        _hline(g, 2, 1, 9, fhi)
        _vline(g, 0, 2, 5, fhi)
        _vline(g, 9, 2, 5, fsh)
        # Lower finger block (rows 5..7)
        _rect(g, 0, 5, 10, 8, dk)
        _hline(g, 5, 0, 10, ink)
        _rect(g, 1, 6, 9, 8, mid)
        if knuckles:
            # Subtle 2-finger groove split at bottom
            _vline(g, 3, 6, 8, ink)
            _vline(g, 6, 6, 8, ink)
        if thumb:
            _rect(g, 6, 3, 9, 6, fhi)
            _vline(g, 5, 3, 6, ink)
        return _str(g)

    down = _grid(10, 10, dk)
    _rect(down, 1, 1, 9, 9, mid)
    _hline(down, 4, 1, 9, ink)
    _hline(down, 7, 1, 9, ink)
    return {
        'north': side(knuckles=True),
        'east': side(knuckles=False),
        'south': side(knuckles=True),
        'west': side(thumb=True),
        'down': _str(down),
    }


def _boot_2x(st):
    """Clean 2x (10x8 side, 10x10 down) heavy platform boot with crisp sole & tread notches."""
    fhi, fmid, fsh, dk, ink = st['hi'], st['mid'], st['sh'], st['dk'], st['ink']

    def side(toe=False, back=False):
        g = _grid(10, 8, dk)
        # Ankle collar (rows 0..1)
        _hline(g, 0, 0, 10, ink)
        _hline(g, 1, 0, 10, fsh)
        # Upper boot bumper (rows 2..4)
        _rect(g, 0, 2, 10, 5, fmid)
        _hline(g, 2, 0, 10, fhi)
        _vline(g, 0, 2, 5, fhi)
        _vline(g, 9, 2, 5, fsh)
        if toe:
            # Clean reinforced toe cap across center
            _rect(g, 2, 2, 8, 5, fhi)
            _rect(g, 3, 3, 7, 5, fmid)
            _vline(g, 1, 2, 5, ink)
            _vline(g, 8, 2, 5, ink)
        # Thick rubber/iron platform sole (rows 5..7)
        _hline(g, 5, 0, 10, ink)
        _rect(g, 0, 6, 10, 8, dk)
        if back:
            _hline(g, 7, 0, 10, ink)
        elif toe:
            _hline(g, 7, 0, 10, ink)
            _rect(g, 2, 7, 8, 8, fsh)
        else:
            # Side tread lugs matching underside
            for x in (0, 1, 4, 5, 8, 9):
                g[7][x] = ink
            for x in (2, 3, 6, 7):
                g[7][x] = fsh
        return _str(g)

    down = _grid(10, 10, ink)
    for y in (2, 3, 6, 7):
        _hline(down, y, 1, 9, fsh)
    _rect(down, 2, 9, 8, 10, fsh)
    return {
        'north': side(toe=True),
        'south': side(back=True),
        'east': side(),
        'west': side(),
        'down': _str(down),
    }


def _socket_down_2x(st):
    """2x (10x10) tool socket underside plate with glowing cyan contact."""
    g = _grid(10, 10, st['sh'])
    _rect(g, 1, 1, 9, 9, st['mid'])
    _rect(g, 2, 2, 8, 8, st['dk'])
    _rect(g, 4, 4, 6, 6, '+')
    for x, y in ((1, 1), (8, 1), (1, 8), (8, 8)):
        g[y][x] = st['ink']
    return _str(g)


# ---------------------------------------------------------------- torso (2-layer: z +-3.0 outer shell + z +-2.5 inner core)
def _torso(st, chest_x):
    """Returns (chest_outer, abdomen_outer, chest_inner, abdomen_inner, belt).

    Outer torso (z +-3.0): clean structural exoskeleton yoke, side load pillars, central engine mounting bay cutout
    (x +-2, y 21..25 -> rows 2..9 on chest), and clean waist trusses.
    Inner torso (z +-2.5, 0.5 px recessed): calm dark-slate engine socket backing + warm leather pilot vest / harness
    so parked suits have real mechanical depth instead of see-through far-wall confetti, while keeping clean rectangular
    side windows over the pilot's torso.
    """
    hi, mid, sh, dk, ink = st['hi'], st['mid'], st['sh'], st['dk'], st['ink']
    ih, im, is_ = st['in_hi'], st['in_mid'], st['in_sh']
    lh, lm, ls, ld = st['l_hi'], st['l_mid'], st['l_sh'], st['l_dk']
    ph, pm, ps = st['pin_hi'], st['pin_mid'], st['pin_sh']

    cw = round(chest_x * 4)       # 24 wide, 22 slim
    aw = 20                       # abdomen width (x +-5)
    D = 12                        # z +-3 -> 12 texels
    edge_c = (cw - 16) // 2       # 4 wide, 3 slim (outside Steve's 16-texel torso)
    edge_a = 2                    # 2 texels outside Steve's torso on abdomen

    # ---- CHEST OUTER (cw x 12 x 12) ----
    # Front: clean upper shoulder yoke (rows 0..1), sturdy side pillars (edge_c + 1), clean octagonal-ish recessed
    # engine bay window in the middle 8x8 (cols cw//2-4 .. cw//2+4, rows 2..9), bottom sternum crossbar (rows 10..11).
    cf = _grid(cw, 12, '.')
    # Top yoke bar
    _hline(cf, 0, 0, cw, hi)
    _hline(cf, 1, 0, cw, mid)
    # Bottom chest crossbar
    _hline(cf, 10, 0, cw, mid)
    _hline(cf, 11, 0, cw, sh)
    # Left & right structural side pillars (solid outside Steve's torso + 1 texel collar)
    pw = edge_c + 2
    _rect(cf, 0, 1, pw, 11, mid)
    _rect(cf, cw - pw, 1, cw, 11, mid)
    _vline(cf, 0, 0, 12, hi)
    _vline(cf, cw - 1, 0, 12, sh)
    _vline(cf, pw - 1, 2, 10, ink)
    _vline(cf, cw - pw, 2, 10, ink)
    # Subtle bevel groove on side pillars (rows 4..7)
    _rect(cf, 1, 4, pw - 1, 8, sh)
    _rect(cf, cw - pw + 1, 4, cw - 1, 8, sh)
    # Shoulder bolt pins (1 clean accent per side)
    cf[2][1] = cf[2][cw - 2] = ph
    cf[9][1] = cf[9][cw - 2] = dk
    # Engine bay frame (1-texel bezel around the central 8x8 cutout, keeping 6x6 open window to the inner engine bay!)
    bx0, bx1 = cw // 2 - 4, cw // 2 + 4
    _hline(cf, 2, bx0, bx1, ink)
    _hline(cf, 9, bx0, bx1, ink)
    _vline(cf, bx0, 2, 10, sh)
    _vline(cf, bx1 - 1, 2, 10, sh)
    # Clean diagonal collar struts from shoulder yoke into engine bay corners
    _hline(cf, 1, bx0 - 1, bx1 + 1, sh)
    _hline(cf, 10, bx0, bx1, sh)
    # Open windows flanking the engine bay (between side pillar and engine bezel) show the recessed inner harness / pilot!

    # Back: clean spinal exo-frame ready for any engine pack (firebox / tidal / star) OR clean when bare!
    cb = _grid(cw, 12, '.')
    _hline(cb, 0, 0, cw, hi)
    _hline(cb, 1, 0, cw, mid)
    _hline(cb, 10, 0, cw, mid)
    _hline(cb, 11, 0, cw, sh)
    _rect(cb, 0, 1, pw, 11, mid)
    _rect(cb, cw - pw, 1, cw, 11, mid)
    _vline(cb, 0, 0, 12, hi)
    _vline(cb, cw - 1, 0, 12, sh)
    _vline(cb, pw - 1, 2, 10, ink)
    _vline(cb, cw - pw, 2, 10, ink)
    # Central spine truss (4 texels wide down the center, with recessed louver slots)
    sx0, sx1 = cw // 2 - 2, cw // 2 + 2
    _rect(cb, sx0, 1, sx1, 11, mid)
    _vline(cb, sx0, 2, 10, hi)
    _vline(cb, sx1 - 1, 2, 10, sh)
    for y in (3, 5, 7):
        _hline(cb, y, sx0 + 1, sx1 - 1, dk)
    # Clean open shoulder-blade cutouts between side pillars and spine (show inner harness/pilot cleanly)

    # Chest sides (12 x 12, closed because arms touch here — calm dark slate structural wall)
    cs = _grid(D, 12, sh)
    _hline(cs, 0, 0, D, hi)
    _hline(cs, 1, 0, D, mid)
    _rect(cs, 2, 2, D - 2, 10, dk)
    _rect(cs, 3, 3, D - 3, 9, im)
    _hline(cs, 10, 0, D, mid)
    _hline(cs, 11, 0, D, ink)

    # Chest up (open over Steve's neck/shoulders, solid shoulder platforms outside Steve)
    cup = _grid(cw, D, '.')
    for j in range(D):
        c = hi if j == 0 else sh if j == D - 1 else mid
        for i in range(edge_c):
            cup[j][i] = c
            cup[j][cw - 1 - i] = c
        # 1-texel front & back collar rims across the chest top
        if j in (0, 1):
            for i in range(edge_c, cw - edge_c):
                cup[j][i] = hi if j == 0 else ink
        elif j in (D - 2, D - 1):
            for i in range(edge_c, cw - edge_c):
                cup[j][i] = sh if j == D - 1 else ink
    # Chest down (ledge where chest overhangs abdomen)
    ov = round((chest_x - 5.0) * 4)
    cdn = _grid(cw, D, '.')
    if ov > 0:
        for j in range(D):
            for i in range(ov):
                cdn[j][i] = sh
                cdn[j][cw - 1 - i] = sh

    chest_outer = {'north': _str(cf), 'south': _str(cb), 'east': _str(cs), 'west': _str(cs),
                   'up': _str(cup), 'down': _str(cdn)}

    # ---- ABDOMEN OUTER (20 x 10 x 12) ----
    # Clean lower-torso side rails + central spine/sternum column + wide open cutouts showing the recessed leather vest!
    af = _grid(aw, 10, '.')
    _hline(af, 0, 0, aw, dk)       # shadow tuck under chest
    _hline(af, 8, 0, aw, mid)      # waist crossbar
    _hline(af, 9, 0, aw, sh)
    # Outer hip-to-chest side struts (3 texels wide)
    _rect(af, 0, 0, 3, 10, mid)
    _rect(af, aw - 3, 0, aw, 10, mid)
    _vline(af, 0, 0, 10, hi)
    _vline(af, aw - 1, 0, 10, sh)
    _vline(af, 2, 1, 8, ink)
    _vline(af, aw - 3, 1, 8, ink)
    # Central 4-texel vertical hydraulic sternum/spine beam
    _rect(af, 8, 0, 12, 9, mid)
    _vline(af, 8, 1, 8, hi)
    _vline(af, 11, 1, 8, sh)
    for y in (2, 4, 6):
        _hline(af, y, 9, 11, dk)
    # Waist buckle accent
    _rect(af, 8, 8, 12, 10, pm)
    _hline(af, 8, 9, 11, ph)

    ab = _grid(aw, 10, '.')
    _hline(ab, 0, 0, aw, dk)
    _hline(ab, 8, 0, aw, mid)
    _hline(ab, 9, 0, aw, sh)
    _rect(ab, 0, 0, 3, 10, mid)
    _rect(ab, aw - 3, 0, aw, 10, mid)
    _vline(ab, 0, 0, 10, hi)
    _vline(ab, aw - 1, 0, 10, sh)
    _vline(ab, 2, 1, 8, ink)
    _vline(ab, aw - 3, 1, 8, ink)
    _rect(ab, 8, 0, 12, 9, mid)
    _vline(ab, 8, 1, 8, hi)
    _vline(ab, 11, 1, 8, sh)
    for y in (2, 4, 6):
        _hline(ab, y, 9, 11, dk)

    aside = _grid(D, 10, sh)
    _hline(aside, 0, 0, D, dk)
    _rect(aside, 2, 1, D - 2, 8, lm)     # clean recessed leather flank panel
    _hline(aside, 1, 2, D - 2, ls)
    _hline(aside, 2, 2, D - 2, lh)
    _hline(aside, 8, 0, D, mid)
    _hline(aside, 9, 0, D, ink)

    abdomen_outer = {'north': _str(af), 'south': _str(ab), 'east': _str(aside), 'west': _str(aside),
                     'up': _str(_grid(aw, D, '.')), 'down': _str(_grid(aw, D, '.'))}

    # ---- CHEST INNER CORE (0.5 px recessed: z +-2.5, (cw-2) x 12 x 10) ----
    # Holds the clean recessed engine mounting bay behind the chest cutout + calm dark leather/slate harness straps,
    # while leaving clean side windows so Steve's torso still peeks through cleanly when piloted!
    icw = cw - 2
    ci_f = _grid(icw, 12, '.')
    # Recessed engine mounting socket (center 8x8, rows 2..9) — clean matte dark bay with subtle cross-ring
    cx0, cx1 = icw // 2 - 4, icw // 2 + 4
    _rect(ci_f, cx0, 2, cx1, 10, is_)
    _rect(ci_f, cx0 + 1, 3, cx1 - 1, 9, im)
    _rect(ci_f, cx0 + 2, 4, cx1 - 2, 8, is_)
    # Subtle socket contact pins in corners of the bay
    for px, py in ((cx0 + 1, 3), (cx1 - 2, 3), (cx0 + 1, 8), (cx1 - 2, 8)):
        ci_f[py][px] = pm
    # Clean horizontal leather shoulder-harness strap across rows 4..7 behind the flanking windows (or open on open-cage)
    if not st['limb_open']:
        _rect(ci_f, 0, 1, icw, 11, is_)
        # Re-stamp engine bay on top
        _rect(ci_f, cx0, 2, cx1, 10, ink)
        _rect(ci_f, cx0 + 1, 3, cx1 - 1, 9, im)
        _rect(ci_f, cx0 + 2, 4, cx1 - 2, 8, is_)
        for px, py in ((cx0 + 1, 3), (cx1 - 2, 3), (cx0 + 1, 8), (cx1 - 2, 8)):
            ci_f[py][px] = pm
        # Warm leather pectoral harness straps flanking the engine bay
        _rect(ci_f, 1, 3, cx0, 9, lm)
        _hline(ci_f, 3, 1, cx0, ls)
        _hline(ci_f, 4, 1, cx0, lh)
        _rect(ci_f, cx1, 3, icw - 1, 9, lm)
        _hline(ci_f, 3, cx1, icw - 1, ls)
        _hline(ci_f, 4, cx1, icw - 1, lh)
        # Clean 2x2 pilot peep-slot under the collar on each side? No — keep chest calm & solid so engines pop!
    else:
        # Open-cage styles: keep flanking vertical slots open ('.') so pilot's shirt shows cleanly, with one neat leather strap
        _rect(ci_f, 1, 5, cx0, 8, lm)
        _hline(ci_f, 5, 1, cx0, ls)
        _rect(ci_f, cx1, 5, icw - 1, 8, lm)
        _hline(ci_f, 5, cx1, icw - 1, ls)

    ci_b = _grid(icw, 12, is_)
    # Clean dark backplate with warm leather shoulder-blade padding (stops parked see-through confetti!)
    _rect(ci_b, 2, 2, icw - 2, 10, im)
    _rect(ci_b, 3, 3, icw // 2 - 2, 9, lm)
    _hline(ci_b, 3, 3, icw // 2 - 2, ls)
    _rect(ci_b, icw // 2 + 2, 3, icw - 3, 9, lm)
    _hline(ci_b, 3, icw // 2 + 2, icw - 3, ls)

    chest_inner = {'north': _str(ci_f), 'south': _str(ci_b),
                   'east': _str(_grid(10, 12, '.')), 'west': _str(_grid(10, 12, '.')),
                   'up': _str(_grid(icw, 10, '.')), 'down': _str(_grid(icw, 10, '.'))}

    # ---- ABDOMEN INNER CORE (0.5 px recessed: z +-2.5, 18 x 10 x 10) ----
    # Warm saddle leather abdomen harness behind the outer steel/slate struts!
    iaw = aw - 2  # 18
    def _abd_inner(open_window):
        g = _grid(iaw, 10, is_)
        # Two broad clean saddle-leather panels flanking the spine/sternum
        _rect(g, 1, 1, 7, 8, lm)
        _hline(g, 1, 1, 7, ls)
        _hline(g, 2, 1, 7, lh)
        _hline(g, 7, 1, 7, ld)
        _rect(g, 11, 1, 17, 8, lm)
        _hline(g, 1, 11, 17, ls)
        _hline(g, 2, 11, 17, lh)
        _hline(g, 7, 11, 17, ld)
        if open_window:
            # One clean 3x4 pilot window on each flank
            _rect(g, 2, 3, 6, 7, '.')
            _rect(g, 12, 3, 16, 7, '.')
        return _str(g)

    abdomen_inner = {'north': _abd_inner(st['limb_open']), 'south': _abd_inner(False),
                     'east': _str(_grid(10, 10, '.')), 'west': _str(_grid(10, 10, '.')),
                     'up': _str(_grid(iaw, 10, '.')), 'down': _str(_grid(iaw, 10, '.'))}

    # ---- BELT (20 x 2 x 12) ----
    # Calm dark-slate pelvic ring (no bright horizontal stripe cutting the waist!)
    bf = _grid(aw, 2, sh)
    _hline(bf, 0, 0, aw, dk)
    _hline(bf, 1, 0, aw, sh)
    _rect(bf, 8, 0, 12, 2, pm)
    _hline(bf, 0, 9, 11, ph)
    bb = _grid(aw, 2, sh)
    _hline(bb, 0, 0, aw, dk)
    bs = _grid(D, 2, sh)
    _hline(bs, 0, 0, D, dk)
    bup = _grid(aw, D, '.')
    _hline(bup, 0, 0, aw, sh)
    _hline(bup, D - 1, 0, aw, sh)
    _vline(bup, 0, 0, D, sh)
    _vline(bup, aw - 1, 0, D, sh)
    bdn = [r[:] for r in bup]
    for j in range(1, D - 1):
        bdn[j][0] = bdn[j][-1] = 'T'

    belt = {'north': _str(bf), 'south': _str(bb), 'east': _str(bs), 'west': _str(bs),
            'up': _str(bup), 'down': _str(bdn)}

    return chest_outer, abdomen_outer, chest_inner, abdomen_inner, belt


# ---------------------------------------------------------------- shoulder cap (for flush styles A & C)
def _shoulder_cap(st):
    """Clean 2x shoulder cap decal (11 x 7 x 12, DECAL=0.5) in the option's own palette."""
    hi, mid, sh, dk, ink = st['hi'], st['mid'], st['sh'], st['dk'], st['ink']
    ph = st['pin_hi']
    W, D, H = 11, 12, 7
    up = _grid(W, D, mid)
    _hline(up, 0, 0, W, hi)
    _hline(up, D - 1, 0, W, sh)
    _vline(up, 0, 1, D - 1, sh)
    _vline(up, W - 1, 1, D - 1, hi)
    # Subtle mounting rail + 2 corner bolts
    _rect(up, 4, 1, 7, D - 1, dk)
    _vline(up, 5, 1, D - 1, sh)
    for x, y in ((2, 2), (W - 3, 2), (2, D - 3), (W - 3, D - 3)):
        up[y][x] = ink

    def band(depths, bolts=()):
        g = _grid(len(depths), H, '.')
        for i, d in enumerate(depths):
            for j in range(d):
                g[j][i] = hi if j == 0 else ink if j == d - 1 else sh if j == d - 2 else mid
        for i in bolts:
            g[2][i] = ph
        return _str(g)

    side = [3 + round(2 * i / (W - 1)) for i in range(W)]  # inner -> outer: 3..5 rows
    return {
        'north': band(side[::-1], bolts=(1,)),
        'south': band(side, bolts=(W - 2,)),
        'east': band([5] * D, bolts=(2, D - 3)),
        'west': _str(_grid(D, H, '.')),
        'up': _str(up),
        'down': _str(_grid(W, D, '.')),
    }


# ---------------------------------------------------------------- arms (flush 2x OR 2-layer cutout)
def _arm(st):
    """Returns (arm_hand, arm_socket, arm_outer_or_None).

    Arm cage is 12 px tall (24 texels: rows 0..23), over 4 px fist (8 texels: rows 24..31).
    Socket arm keeps top 9 px (18 texels: rows 0..17, raw y 17..26), with socket plate on down.
    """
    hi, mid, sh, dk, ink = st['hi'], st['mid'], st['sh'], st['dk'], st['ink']
    ih, im, is_ = st['in_hi'], st['in_mid'], st['in_sh']
    lh, lm, ls, ld = st['l_hi'], st['l_mid'], st['l_sh'], st['l_dk']
    ph, pm, ps = st['pin_hi'], st['pin_mid'], st['pin_sh']

    fist = _fist_2x(st)

    if not st['layered_limbs']:
        # ---- FLUSH 2x OPEN CHASSIS (A: dark_cage, C: clean_steel) ----
        # 10 x 24 cage faces (rows 0..23):
        #   0..2   shoulder collar
        #   3..10  upper arm: sturdy 2-texel outer/inner rails + 1 clean horizontal leather strap (rows 4..6) + open pilot window (rows 7..10)
        #  11..14  elbow cuff (clean calm gunmetal band, single outer actuator pin — NO checkerboards!)
        #  15..21  forearm: sturdy 2-texel rails + ONE wide clean open pilot window (cols 2..7, rows 15..20)
        #  22..23  wrist collar above fist
        def face(kind):
            g = _grid(10, 24, '.')
            if kind == 'west':
                # Inner touching wall against chest: solid calm dark slate (no holes)
                g = _grid(10, 24, is_)
                _rect(g, 0, 0, 10, 3, sh)
                _rect(g, 0, 11, 10, 15, dk)
                _rect(g, 0, 22, 10, 24, dk)
                _rect(g, 2, 4, 8, 10, im)
                _rect(g, 2, 15, 8, 22, im)
                return _str(g)

            # Shoulder collar (rows 0..2)
            _rect(g, 0, 0, 10, 3, mid)
            _hline(g, 0, 0, 10, hi)
            _hline(g, 2, 0, 10, ink)
            # Outer & inner vertical rails (2 texels each, clean bevel)
            _rect(g, 0, 2, 2, 24, mid)
            _rect(g, 8, 2, 10, 24, mid)
            if kind == 'north':      # col 0 = outer, col 9 = inner
                _vline(g, 0, 0, 24, hi)
                _vline(g, 1, 3, 22, sh)
                _vline(g, 8, 3, 22, sh)
                _vline(g, 9, 0, 24, dk)
            elif kind == 'south':    # col 0 = inner, col 9 = outer
                _vline(g, 0, 0, 24, dk)
                _vline(g, 1, 3, 22, sh)
                _vline(g, 8, 3, 22, sh)
                _vline(g, 9, 0, 24, hi)
            else:                    # east: col 0 = back, col 9 = front
                _vline(g, 0, 0, 24, sh)
                _vline(g, 1, 3, 22, dk)
                _vline(g, 8, 3, 22, mid)
                _vline(g, 9, 0, 24, hi)

            # Upper arm leather retention strap (rows 4..6) across the window, leaving rows 7..10 cleanly open to Steve!
            _rect(g, 2, 4, 8, 7, lm)
            _hline(g, 4, 2, 8, ls)
            _hline(g, 5, 2, 8, lh)
            _hline(g, 6, 2, 8, ld)
            if kind == 'east':
                # Small outer buckle clasp on the leather strap
                _rect(g, 4, 4, 6, 7, pm)
                g[5][4] = ph

            # Elbow joint cuff (rows 11..14) — calm solid mechanical band
            _rect(g, 0, 11, 10, 15, dk)
            _hline(g, 11, 0, 10, ink)
            _hline(g, 12, 1, 9, sh)
            _hline(g, 14, 0, 10, ink)
            if kind == 'east':
                # Clean circular/2x2 outer elbow pivot hub
                _rect(g, 3, 11, 7, 15, sh)
                _rect(g, 4, 12, 6, 14, pm)
                g[12][4] = ph
            elif kind in ('north', 'south'):
                # Clean recessed joint rib
                _hline(g, 12, 2, 8, mid)
                _hline(g, 13, 2, 8, dk)

            # Forearm open viewport (rows 15..21, cols 2..7 stay '.' -> clean unobstructed view of pilot forearm!)
            # Wrist cuff (rows 22..23)
            _rect(g, 0, 22, 10, 24, dk)
            _hline(g, 22, 1, 9, sh)
            return _str(g)

        cage = {f: face(f) for f in ('north', 'east', 'south', 'west')}
        up = _grid(10, 10, '.')
        _hline(up, 0, 0, 10, mid); _hline(up, 9, 0, 10, mid)
        _vline(up, 9, 0, 10, hi)
        up[0][0] = up[9][0] = 'T'

        arm_hand = {f: cage[f] + fist[f] for f in ('north', 'east', 'south', 'west')}
        arm_hand['up'] = _str(up)
        arm_hand['down'] = fist['down']

        arm_sock = {f: cage[f][:18] for f in ('north', 'east', 'south', 'west')}
        arm_sock['up'] = _str(up)
        arm_sock['down'] = _socket_down_2x(st)
        return arm_hand, arm_sock, None

    # ---- 2-LAYER CUTOUT EXOSUIT (B: exo_layered, D: heavy_harness) ----
    # Inner arm box (10 x 24): calm dark pilot harness sleeve with ONE clean forearm open window (rows 17..21)
    # and clean recessed warm leather upper-arm wrap (rows 4..10) + muted brass/slate elbow actuator core (rows 11..14).
    # Outer arm cutout shell (11 x 19 x 12, raw y 17..26.5, DECAL=0.5 proud on north/south/east/up; west & down blank!):
    # integrated shoulder cap + 0.5 px proud outer exo-strut running down the arm into a sculpted cutout elbow brace!
    def inner_face(kind):
        if kind == 'west':
            g = _grid(10, 24, is_)
            _rect(g, 0, 11, 10, 15, dk)
            _rect(g, 0, 22, 10, 24, dk)
            return _str(g)
        g = _grid(10, 24, is_)
        # Upper-arm recessed leather wrap (rows 3..10)
        _rect(g, 1, 3, 9, 11, lm)
        _hline(g, 3, 1, 9, ls)
        _hline(g, 4, 1, 9, lh)
        _hline(g, 10, 1, 9, ld)
        # Elbow mechanical actuator core (rows 11..14)
        _rect(g, 0, 11, 10, 15, dk)
        _hline(g, 11, 0, 10, ink)
        _hline(g, 14, 0, 10, ink)
        _rect(g, 2, 12, 8, 14, im)
        if kind == 'east':
            # Recessed joint piston / pivot cylinder visible through the outer cutout elbow window!
            _rect(g, 3, 12, 7, 14, pm)
            _hline(g, 12, 4, 6, ph)
            _hline(g, 13, 4, 6, ps)
        # Lower forearm: clean dark cuff + wide unobstructed pilot window (rows 17..21, cols 2..7)
        _rect(g, 0, 15, 10, 17, sh)
        _hline(g, 15, 0, 10, mid)
        _rect(g, 0, 17, 10, 22, is_)
        _vline(g, 0, 17, 22, mid if kind != 'south' else dk)
        _vline(g, 9, 17, 22, dk if kind == 'north' else mid)
        _rect(g, 2, 17, 8, 21, '.')  # clean pilot forearm window!
        _rect(g, 0, 22, 10, 24, dk)
        _hline(g, 22, 1, 9, sh)
        return _str(g)

    cage = {f: inner_face(f) for f in ('north', 'east', 'south', 'west')}
    up = _grid(10, 10, is_)
    up[0][0] = up[9][0] = 'T'

    arm_hand = {f: cage[f] + fist[f] for f in ('north', 'east', 'south', 'west')}
    arm_hand['up'] = _str(up)
    arm_hand['down'] = fist['down']

    arm_sock = {f: cage[f][:18] for f in ('north', 'east', 'south', 'west')}
    arm_sock['up'] = _str(up)
    arm_sock['down'] = _socket_down_2x(st)

    # Outer cutout layer (W=11 inner->outer, H=19 rows [row 0 = top cap y 26.5..26, rows 1..18 = y 26..17], D=12)
    W, H, D = 11, 19, 12
    oup = _grid(W, D, mid)
    _hline(oup, 0, 0, W, hi)
    _hline(oup, D - 1, 0, W, sh)
    _vline(oup, 0, 1, D - 1, sh)
    _vline(oup, W - 1, 1, D - 1, hi)
    _rect(oup, 4, 1, 7, D - 1, dk)
    _vline(oup, 5, 1, D - 1, sh)

    # North (outer col 0 .. inner col 10) & South (inner col 0 .. outer col 10)
    # Row 0..4: sleek tapered shoulder cap; rows 5..11: vertical outer exo-strut (3 texels wide on outer edge, leaving
    # inner 8 texels open so the recessed leather upper-arm wrap shows clearly!); rows 12..16: wrapped elbow brace cuff!
    # Rows 17..18: tapered lower collar stopping cleanly at SOCKET_Y!
    def outer_ns(outer_left):
        g = _grid(W, H, '.')
        # Shoulder cap (rows 0..4 at outer edge, stepping up to rows 0..3 at inner edge)
        for i in range(W):
            dist_outer = i if outer_left else (W - 1 - i)
            depth = 5 if dist_outer < 4 else 4 if dist_outer < 8 else 3
            for j in range(depth):
                g[j][i] = hi if j == 0 else ink if j == depth - 1 else sh if j == depth - 2 else mid
        # Outer exo-rail running down rows 4..16 (3 texels on outer side)
        ox0, ox1 = (0, 3) if outer_left else (W - 3, W)
        _rect(g, ox0, 4, ox1, 17, mid)
        _vline(g, ox0 if outer_left else ox1 - 1, 0, 17, hi)
        _vline(g, ox1 - 1 if outer_left else ox0, 5, 12, ink)
        # Elbow brace band (rows 12..16, full width on outer 9 texels, open 2-texel cutout slot in center showing actuator!)
        ex0, ex1 = (0, W - 1) if outer_left else (1, W)
        _rect(g, ex0, 12, ex1, 17, mid)
        _hline(g, 12, ex0, ex1, hi)
        _hline(g, 16, ex0, ex1, ink)
        # Clean 4x2 recessed elbow slot showing inner actuator core
        _rect(g, 4, 13, 7, 15, '.')
        g[13][3] = g[14][3] = ink
        g[13][7] = g[14][7] = ink
        # Clean bolt on shoulder cap
        g[2][1 if outer_left else W - 2] = ph
        return _str(g)

    # East (outer side, D=12 back->front, H=19): matches north/south row-for-row at cols 0 (south) and 11 (north)!
    oe = _grid(D, H, '.')
    # Shoulder cap across all 12 cols (rows 0..4, matches outer depth=5!)
    for j in range(5):
        c = hi if j == 0 else ink if j == 4 else sh if j == 3 else mid
        _hline(oe, j, 0, D, c)
    oe[2][2] = oe[2][D - 3] = ph
    # Twin edge struts down to elbow (rows 5..11) framing a clean 6x7 central cutout window over the recessed leather!
    _rect(oe, 0, 4, 3, 17, mid)
    _rect(oe, D - 3, 4, D, 17, mid)
    _vline(oe, 0, 0, 17, sh)
    _vline(oe, 2, 5, 12, ink)
    _vline(oe, D - 3, 5, 12, ink)
    _vline(oe, D - 1, 0, 17, hi)
    # Elbow actuator guard (rows 12..16, matches north/south rows 12..16!) with a 4x2 central aperture showing the pivot pin!
    _rect(oe, 0, 12, D, 17, mid)
    _hline(oe, 12, 0, D, hi)
    _hline(oe, 16, 0, D, ink)
    _rect(oe, 4, 13, 8, 15, '.')
    oe[13][3] = oe[14][3] = ink
    oe[13][8] = oe[14][8] = ink

    arm_outer = {
        'north': outer_ns(outer_left=True),
        'south': outer_ns(outer_left=False),
        'east': _str(oe),
        'west': _str(_grid(D, H, '.')),
        'up': _str(oup),
        'down': _str(_grid(W, D, '.')),
    }
    return arm_hand, arm_sock, arm_outer


# ---------------------------------------------------------------- legs (flush 2x OR 2-layer cutout)
def _leg(st):
    """Returns (leg_inner, leg_outer_or_None).

    Leg cage is 11.5 px tall (23 texels: rows 0..22, raw y 15.5..4.0), over 4 px boot (8 texels: rows 23..30).
      0..2   hip collar
      3..10  thigh
     11..14  knee joint
     15..21  shin
        22   ankle seam
    """
    hi, mid, sh, dk, ink = st['hi'], st['mid'], st['sh'], st['dk'], st['ink']
    ih, im, is_ = st['in_hi'], st['in_mid'], st['in_sh']
    lh, lm, ls, ld = st['l_hi'], st['l_mid'], st['l_sh'], st['l_dk']
    ph, pm, ps = st['pin_hi'], st['pin_mid'], st['pin_sh']

    boot = _boot_2x(st)

    if not st['layered_limbs']:
        # ---- FLUSH 2x OPEN CHASSIS (A: dark_cage, C: clean_steel) ----
        def face(kind):
            if kind == 'west':
                g = _grid(10, 23, is_)
                _rect(g, 0, 0, 10, 3, dk)
                _rect(g, 0, 11, 10, 15, dk)
                _rect(g, 2, 3, 8, 11, im)
                _rect(g, 2, 15, 8, 22, im)
                _hline(g, 22, 0, 10, dk)
                return _str(g)

            g = _grid(10, 23, '.')
            # Hip collar (rows 0..2)
            _rect(g, 0, 0, 10, 3, dk)
            _hline(g, 0, 0, 10, sh)
            _hline(g, 2, 0, 10, ink)
            # Outer & inner vertical rails (2 texels each)
            _rect(g, 0, 2, 2, 23, mid)
            _rect(g, 8, 2, 10, 23, mid)
            if kind == 'north':
                _vline(g, 0, 0, 23, hi); _vline(g, 1, 3, 22, sh)
                _vline(g, 8, 3, 22, sh); _vline(g, 9, 0, 23, dk)
            elif kind == 'south':
                _vline(g, 0, 0, 23, dk); _vline(g, 1, 3, 22, sh)
                _vline(g, 8, 3, 22, sh); _vline(g, 9, 0, 23, hi)
            else:
                _vline(g, 0, 0, 23, sh); _vline(g, 1, 3, 22, dk)
                _vline(g, 8, 3, 22, mid); _vline(g, 9, 0, 23, hi)

            # Thigh leather harness strap (rows 4..6), leaving rows 7..10 cleanly open to Steve's leg!
            _rect(g, 2, 4, 8, 7, lm)
            _hline(g, 4, 2, 8, ls)
            _hline(g, 5, 2, 8, lh)
            _hline(g, 6, 2, 8, ld)
            if kind == 'east':
                _rect(g, 4, 4, 6, 7, pm)
                g[5][4] = ph

            # Knee joint (rows 11..14) — clean cap on front, single pivot hub on outer side
            _rect(g, 0, 11, 10, 15, dk)
            _hline(g, 11, 0, 10, ink)
            _hline(g, 14, 0, 10, ink)
            if kind == 'north':
                _rect(g, 2, 11, 8, 15, mid)
                _hline(g, 11, 2, 8, hi)
                _hline(g, 14, 2, 8, sh)
                _vline(g, 2, 11, 15, hi)
                _vline(g, 7, 11, 15, sh)
            elif kind == 'east':
                _rect(g, 3, 11, 7, 15, sh)
                _rect(g, 4, 12, 6, 14, pm)
                g[12][4] = ph
            else:
                _hline(g, 12, 2, 8, sh)
                _hline(g, 13, 2, 8, dk)

            # Shin wide open viewport (rows 15..21, cols 2..7 stay '.' -> clean unobstructed view of pilot leg!)
            # Ankle collar (row 22)
            _hline(g, 22, 0, 10, dk)
            return _str(g)

        cage = {f: face(f) for f in ('north', 'east', 'south', 'west')}
        leg_inner = {f: cage[f] + boot[f] for f in ('north', 'east', 'south', 'west')}
        leg_inner['up'] = _str(_grid(10, 10, '.'))
        leg_inner['down'] = boot['down']
        return leg_inner, None

    # ---- 2-LAYER CUTOUT EXOSUIT (B: exo_layered, D: heavy_harness) ----
    # Inner leg (10 x 23): calm dark-slate thigh/shin sleeve + warm leather thigh wrap (rows 3..10) + mechanical knee
    # actuator (rows 11..14) + clean open pilot shin viewport (rows 16..20).
    # Outer leg cutout layer (11 x 23 x 12, raw y 4..15.5, DECAL=0.5 proud on north/south/east; west/up/down blank!):
    # outer-side exo-strut + sculpted cutout knee brace + lower ankle stabilizer!
    def inner_face(kind):
        if kind == 'west':
            g = _grid(10, 23, is_)
            _rect(g, 0, 0, 10, 3, dk)
            _rect(g, 0, 11, 10, 15, dk)
            _hline(g, 22, 0, 10, dk)
            return _str(g)
        g = _grid(10, 23, is_)
        # Hip band
        _rect(g, 0, 0, 10, 3, dk)
        _hline(g, 0, 0, 10, sh)
        # Warm leather thigh wrap (rows 3..10)
        _rect(g, 1, 3, 9, 11, lm)
        _hline(g, 3, 1, 9, ls)
        _hline(g, 4, 1, 9, lh)
        _hline(g, 10, 1, 9, ld)
        # Mechanical knee core (rows 11..14)
        _rect(g, 0, 11, 10, 15, dk)
        _hline(g, 11, 0, 10, ink)
        _hline(g, 14, 0, 10, ink)
        _rect(g, 2, 12, 8, 14, im)
        if kind == 'east':
            _rect(g, 3, 12, 7, 14, pm)
            _hline(g, 12, 4, 6, ph)
            _hline(g, 13, 4, 6, ps)
        elif kind == 'north':
            _rect(g, 3, 12, 7, 14, pm)
            _hline(g, 12, 3, 7, ph)
        # Shin cuff with clean open pilot viewport (rows 16..20, cols 2..7)
        _rect(g, 0, 15, 10, 23, is_)
        _vline(g, 0, 15, 22, mid if kind != 'south' else dk)
        _vline(g, 9, 15, 22, dk if kind == 'north' else mid)
        _rect(g, 2, 16, 8, 21, '.')
        _hline(g, 22, 0, 10, dk)
        return _str(g)

    cage = {f: inner_face(f) for f in ('north', 'east', 'south', 'west')}
    leg_inner = {f: cage[f] + boot[f] for f in ('north', 'east', 'south', 'west')}
    leg_inner['up'] = _str(_grid(10, 10, '.'))
    leg_inner['down'] = boot['down']

    # Outer cutout exo-layer on leg (W=11 inner->outer, H=23 rows [0..22 = raw y 15.5..4.0], D=12)
    W, H, D = 11, 23, 12
    def outer_ns(outer_left):
        g = _grid(W, H, '.')
        ox0, ox1 = (0, 3) if outer_left else (W - 3, W)
        # Hip stabilizer cap (rows 0..2 on outer 6 texels)
        hx0, hx1 = (0, 7) if outer_left else (W - 7, W)
        _rect(g, hx0, 0, hx1, 3, mid)
        _hline(g, 0, hx0, hx1, hi)
        _hline(g, 2, hx0, hx1, ink)
        # Continuous outer exo-leg hydraulic rail (rows 0..22, 3 texels wide on outer edge)
        _rect(g, ox0, 1, ox1, 23, mid)
        _vline(g, ox0 if outer_left else ox1 - 1, 0, 23, hi)
        _vline(g, ox1 - 1 if outer_left else ox0, 3, 22, ink)
        # Sculpted knee guard brace (rows 10..15 across outer 9 texels, with crisp central aperture showing actuator!)
        kx0, kx1 = (0, W - 1) if outer_left else (1, W)
        _rect(g, kx0, 10, kx1, 16, mid)
        _hline(g, 10, kx0, kx1, hi)
        _hline(g, 15, kx0, kx1, ink)
        _rect(g, 4, 12, 7, 14, '.')
        g[12][3] = g[13][3] = ink
        g[12][7] = g[13][7] = ink
        # Lower ankle stabilizer cuff (rows 20..22)
        _rect(g, kx0, 20, kx1, 23, mid)
        _hline(g, 20, kx0, kx1, hi)
        _hline(g, 22, kx0, kx1, ink)
        # Subtle hip & ankle bolts
        g[1][1 if outer_left else W - 2] = ph
        g[21][1 if outer_left else W - 2] = ph
        return _str(g)

    oe = _grid(D, H, '.')
    # Matches outer_ns row-for-row at cols 0 (south) and 11 (north):
    # Hip cap (rows 0..2)
    _rect(oe, 0, 0, D, 3, mid); _hline(oe, 0, 0, D, hi); _hline(oe, 2, 0, D, ink)
    # Twin vertical edge struts (rows 1..22) framing upper thigh leather cutout (rows 3..9) & lower shin cutout (rows 16..19)
    _rect(oe, 0, 1, 3, 23, mid); _rect(oe, D - 3, 1, D, 23, mid)
    _vline(oe, 0, 0, 23, sh); _vline(oe, D - 1, 0, 23, hi)
    _vline(oe, 2, 3, 10, ink); _vline(oe, D - 3, 3, 10, ink)
    _vline(oe, 2, 16, 20, ink); _vline(oe, D - 3, 16, 20, ink)
    # Knee brace (rows 10..15) with 4x2 pivot window
    _rect(oe, 0, 10, D, 16, mid); _hline(oe, 10, 0, D, hi); _hline(oe, 15, 0, D, ink)
    _rect(oe, 4, 12, 8, 14, '.')
    oe[12][3] = oe[13][3] = ink
    oe[12][8] = oe[13][8] = ink
    # Ankle cuff (rows 20..22)
    _rect(oe, 0, 20, D, 23, mid); _hline(oe, 20, 0, D, hi); _hline(oe, 22, 0, D, ink)
    oe[1][2] = oe[1][D - 3] = ph
    oe[21][2] = oe[21][D - 3] = ph

    leg_outer = {
        'north': outer_ns(outer_left=True),
        'south': outer_ns(outer_left=False),
        'east': _str(oe),
        'west': _str(_grid(D, H, '.')),
        'up': _str(_grid(W, D, '.')),
        'down': _str(_grid(W, D, '.')),
    }
    return leg_inner, leg_outer


def _resolve(faces):
    """Resolve letter grids into RGBA tuples (preserving '.' holes and 'T' tucked texels)."""
    if faces is None:
        return None
    return {
        f: [[ch if ch in ('.', 'T') else PAL[ch] + (255,) for ch in row] for row in rows]
        for f, rows in faces.items()
    }


# ================================================================================================
# Round 2 (2026-11-23): Sculpted 3D-shaded, zero-leather industrial exoskeleton directions
#   exo_pistons   R2-A: Dark forged-gunmetal 2-layer exo-frame + gleaming chrome-steel hydraulic pistons
#   forge_copper  R2-B: Tool-matched iron/slate 2-layer exo-skeleton + recessed copper servo drums
#   open_skeleton R2-C: Sculpted beveled open steel skeleton + rotary joint drums (max pilot visibility)
#   tactical_rig  R2-D: Chamfered matte-graphite 2-layer exo-chassis + bright brushed-steel inner spine/ribs
# ================================================================================================

R2_STYLES = {
    'exo_pistons': dict(
        layered_limbs=True,
        open_torso=False,
        open_upper_limbs=False,
        # Outer 0.5 px sculpted gunmetal plates: real 5-step bevel ramp (g/e specular -> n/m body -> k/d shade -> x AO)
        rim='e', hi='O', mid='n', sh='m', dk='k', deep='d', ink='x',
        # Inner mechanical core: gleaming chrome-steel hydraulic cylinders inside pitch-black AO bays!
        mech='piston',   # vertical brushed-steel cylinders (w/g/h/e/l/p/s)
        acc_hi='g', acc_mid='l', acc_sh='p',
        spine_hi='g', spine_mid='e', spine_sh='p',
    ),
    'forge_copper': dict(
        layered_limbs=True,
        open_torso=False,
        open_upper_limbs=False,
        # Outer 0.5 px sculpted cool iron exo-trusses (matching the reworked tools' cuff ramp!)
        rim='g', hi='h', mid='p', sh='s', dk='z', deep='d', ink='x',
        # Inner mechanical core: warm 3D-shaded horizontal copper servo drums (drill/chaingun/EM language!)
        mech='copper',   # horizontal copper rotor drums (F/f/Q/R/C) + bright steel rings
        acc_hi='F', acc_mid='Q', acc_sh='R',
        spine_hi='h', spine_mid='l', spine_sh='s',
    ),
    'open_skeleton': dict(
        layered_limbs=False,
        open_torso=True,
        open_upper_limbs=True,
        # Sleek sculpted open steel skeleton (bright specular bevels + deep AO edges, max pilot visibility!)
        rim='g', hi='h', mid='l', sh='p', dk='s', deep='z', ink='x',
        mech='open',     # wide clean pilot windows + bold 3D rotary joint drums
        acc_hi='g', acc_mid='e', acc_sh='s',
        spine_hi='g', spine_mid='h', spine_sh='p',
    ),
    'tactical_rig': dict(
        layered_limbs=True,
        open_torso=False,
        open_upper_limbs=False,
        # Chamfered dark matte-graphite outer armour-chassis with razor-sharp specular corner bevels
        rim='h', hi='n', mid='k', sh='d', dk='x', deep='x', ink='x',
        # Inner core: bright brushed-steel skeletal ribs & pistons peeking cleanly through angled cutouts!
        mech='steel_ribs',
        acc_hi='w', acc_mid='h', acc_sh='l',
        spine_hi='w', spine_mid='g', spine_sh='l',
    ),
}


def _v_piston(g, x0, y0, y1, w=4):
    """Draw a 3D cylindrical vertical brushed-steel hydraulic piston (bright specular highlight -> shaded cylinder)
    with dark collar rings inside an AO recess."""
    # Columns across piston (w=4 -> 'h g l s', w=3 -> 'g l s', w=2 -> 'g p')
    ramp = {4: 'hgls', 3: 'gls', 2: 'gp'}[w]
    for y in range(y0, y1):
        if y == y0 or y == y1 - 1:
            # Top/bottom machined steel collar ring
            for i in range(w):
                g[y][x0 + i] = 'e' if i < w - 1 else 's'
        elif y == y0 + 1:
            # Cast shadow under upper collar
            for i in range(w):
                g[y][x0 + i] = 'p' if i < w // 2 else 'z'
        else:
            for i, ch in enumerate(ramp):
                g[y][x0 + i] = ch
                if y == y0 + 2 and ch == 'g':
                    g[y][x0 + i] = 'w'  # crisp top specular glint!


def _h_copper_drum(g, x0, y0, x1, y1, steel_ring=True):
    """Draw a 3D cylindrical horizontal wound copper servo drum (F -> f -> Q -> R -> C top-to-bottom)
    with optional bright central brushed-steel commutator ring (matching mining drill / chaingun!)."""
    h = y1 - y0
    w = x1 - x0
    midx = (x0 + x1) // 2
    for dy in range(h):
        # Vertical cylinder shading from top (AO shadow under lip) -> bright specular -> warm mid -> deep underside
        if dy == 0:
            c_cu, c_st = 'R', 'p'
        elif dy == 1:
            c_cu, c_st = 'F', 'g'
        elif dy == 2:
            c_cu, c_st = 'f', 'h'
        elif dy < h - 1:
            c_cu, c_st = 'Q', 'l'
        else:
            c_cu, c_st = 'C', 's'
        for x in range(x0, x1):
            is_ring = steel_ring and w >= 5 and (x == midx - 1 or x == midx)
            if x == x0 or x == x1 - 1:
                g[y0 + dy][x] = 'C' if not is_ring else 's'
            else:
                g[y0 + dy][x] = c_st if is_ring else c_cu


def _v_steel_ribs(g, x0, y0, x1, y1):
    """Draw high-contrast brushed-steel angled mechanical ribs inside a pitch-black recess (tactical_rig)."""
    for y in range(y0, y1):
        for x in range(x0, x1):
            phase = (y - y0) % 3
            if phase == 0:
                g[y][x] = 'x'
            elif phase == 1:
                g[y][x] = 'g' if x == x0 else 'h' if x < x1 - 1 else 'l'
            else:
                g[y][x] = 'l' if x == x0 else 'p' if x < x1 - 1 else 's'


def _mech_fill(g, x0, y0, x1, y1, st, orient='v'):
    """Fill a recessed mechanical bay with AO shadow rim + the style's 3D-shaded inner hardware."""
    _rect(g, x0, y0, x1, y1, 'x')
    ix0, iy0, ix1, iy1 = x0 + 1, y0 + 1, x1 - 1, y1 - 1
    if ix1 <= ix0 or iy1 <= iy0:
        return
    m = st['mech']
    if m == 'piston':
        w = ix1 - ix0
        if w >= 6:
            # Twin gleaming vertical pistons with pitch-black gap between!
            _v_piston(g, ix0, iy0, iy1, 2)
            _v_piston(g, ix1 - 2, iy0, iy1, 2)
        elif w >= 4:
            cx = ix0 + (w - 4) // 2
            _v_piston(g, cx, iy0, iy1, 4)
        elif w >= 3:
            _v_piston(g, ix0, iy0, iy1, 3)
        elif w >= 2:
            _v_piston(g, ix0, iy0, iy1, 2)
    elif m == 'copper':
        _h_copper_drum(g, ix0, iy0, ix1, iy1, steel_ring=(ix1 - ix0) >= 4)
    elif m == 'steel_ribs':
        _v_steel_ribs(g, ix0, iy0, ix1, iy1)
    else:
        _rect(g, ix0, iy0, ix1, iy1, '.')


def _r2_fist(st):
    """Sculpted 2x mechanical gauntlet (10x8) with crisp top bevel, knuckle ridge & finger grooves."""
    rim, hi, mid, sh, dk, ink = st['rim'], st['hi'], st['mid'], st['sh'], st['dk'], st['ink']
    ahi = st['acc_hi']

    def side(knuckles=False, thumb=False):
        g = _grid(10, 8, dk)
        # Wrist joint groove + lit collar
        _hline(g, 0, 0, 10, ink)
        _hline(g, 1, 0, 10, sh)
        _hline(g, 1, 1, 9, mid)
        # Beveled hand armour plate (rows 2..4) with bright specular top rim!
        _rect(g, 0, 2, 10, 5, mid)
        _hline(g, 2, 0, 10, hi)
        _hline(g, 2, 1, 8, rim)
        _vline(g, 0, 2, 5, hi)
        _vline(g, 9, 2, 5, sh)
        _hline(g, 4, 0, 10, sh)
        if knuckles:
            g[2][2] = g[2][5] = g[2][7] = ahi
        # Articulated fingers block (rows 5..7)
        _hline(g, 5, 0, 10, ink)
        _rect(g, 0, 6, 10, 8, sh)
        _hline(g, 6, 1, 9, mid)
        _hline(g, 7, 0, 10, dk)
        if knuckles:
            for x in (3, 6):
                _vline(g, x, 6, 8, ink)
        if thumb:
            _rect(g, 5, 3, 9, 6, hi)
            _rect(g, 6, 4, 8, 6, mid)
            _vline(g, 4, 3, 6, ink)
        return _str(g)

    down = _grid(10, 10, dk)
    _rect(down, 1, 1, 9, 9, sh)
    _rect(down, 2, 2, 8, 8, mid)
    _hline(down, 4, 1, 9, ink)
    _hline(down, 7, 1, 9, ink)
    return {'north': side(knuckles=True), 'east': side(), 'south': side(knuckles=True), 'west': side(thumb=True), 'down': _str(down)}


def _r2_boot(st):
    """Sculpted 2x platform boot (10x8) with armored toe bumper, beveled heel & crisp tread."""
    rim, hi, mid, sh, dk, ink = st['rim'], st['hi'], st['mid'], st['sh'], st['dk'], st['ink']

    def side(toe=False, back=False):
        g = _grid(10, 8, dk)
        # Ankle joint ring
        _hline(g, 0, 0, 10, ink)
        _hline(g, 1, 0, 10, sh)
        # Heavy upper bumper (rows 2..4) with bright chamfered top rim
        _rect(g, 0, 2, 10, 5, mid)
        _hline(g, 2, 0, 10, hi)
        _hline(g, 2, 1, 9, rim)
        _vline(g, 0, 2, 5, hi)
        _vline(g, 9, 2, 5, sh)
        _hline(g, 4, 0, 10, sh)
        if toe:
            _rect(g, 2, 2, 8, 5, hi)
            _hline(g, 2, 2, 8, rim)
            _rect(g, 3, 3, 7, 5, mid)
            _vline(g, 1, 2, 5, ink)
            _vline(g, 8, 2, 5, ink)
        elif back:
            # Heel stabilizer strut
            _rect(g, 3, 1, 7, 5, hi)
            _rect(g, 4, 2, 6, 5, mid)
            _vline(g, 2, 1, 5, ink)
            _vline(g, 7, 1, 5, ink)
        # Heavy notched platform sole (rows 5..7)
        _hline(g, 5, 0, 10, ink)
        _rect(g, 0, 6, 10, 8, dk)
        _hline(g, 6, 1, 9, sh)
        if back:
            _hline(g, 7, 0, 10, ink)
        elif toe:
            _hline(g, 7, 0, 10, ink)
            _rect(g, 2, 7, 8, 8, mid)
        else:
            for x in (0, 1, 4, 5, 8, 9):
                g[7][x] = ink
            for x in (2, 3, 6, 7):
                g[7][x] = mid
        return _str(g)

    down = _grid(10, 10, ink)
    for y in (2, 3, 6, 7):
        _hline(down, y, 1, 9, sh)
    _rect(down, 2, 9, 8, 10, mid)
    return {'north': side(toe=True), 'south': side(back=True), 'east': side(), 'west': side(), 'down': _str(down)}


def _r2_socket_down(st):
    g = _grid(10, 10, st['sh'])
    _rect(g, 1, 1, 9, 9, st['mid'])
    _rect(g, 2, 2, 8, 8, st['dk'])
    _rect(g, 3, 3, 7, 7, 'x')
    _rect(g, 4, 4, 6, 6, '+')
    for x, y in ((1, 1), (8, 1), (1, 8), (8, 8)):
        g[y][x] = st['rim']
    return _str(g)


def _r2_torso(st, chest_x):
    """Sculpted 2-layer torso (no leather): angled shoulder yoke, octagonal engine bay, 3D spinal column & hydraulic flanks."""
    rim, hi, mid, sh, dk, deep, ink = st['rim'], st['hi'], st['mid'], st['sh'], st['dk'], st['deep'], st['ink']
    shi, smid, ssh = st['spine_hi'], st['spine_mid'], st['spine_sh']
    ahi, amid = st['acc_hi'], st['acc_mid']

    cw = round(chest_x * 4)   # 24 wide, 22 slim
    aw = 20
    D = 12
    edge_c = (cw - 16) // 2   # 4 wide, 3 slim
    mid_c = cw // 2

    # ---- CHEST OUTER (cw x 12 x 12) ----
    # Front: sculpted chamfered collar yoke + angled chest struts framing an octagonal engine bay + flanking piston/pilot cutouts!
    cf = _grid(cw, 12, '.')
    # Sculpted top shoulder yoke (beveled bright top rim -> mid -> shaded underside)
    _hline(cf, 0, 0, cw, rim)
    _hline(cf, 1, 0, cw, hi)
    _hline(cf, 2, 0, cw, sh)
    # Tapered outer shoulder pillars (wider at top rows 0..4, stepping inward cleanly at rows 5..9 for athletic V-taper!)
    pw_top = edge_c + 2
    pw_bot = edge_c + 1
    for y in range(1, 11):
        w_ = pw_top if y <= 4 else pw_bot
        _rect(cf, 0, y, w_, y + 1, mid)
        _rect(cf, cw - w_, y, cw, y + 1, mid)
        cf[y][0] = hi
        cf[y][cw - 1] = sh
        cf[y][w_ - 1] = ink
        cf[y][cw - w_] = ink
        if y == 4:
            cf[y][w_ - 2] = sh
            cf[y][cw - w_ + 1] = sh
    # Specular corner bolts on upper chest pillars
    cf[1][1] = cf[1][cw - 2] = rim
    cf[2][1] = cf[2][cw - 2] = dk
    # Bottom sternum bar (beveled rolled rim!)
    _hline(cf, 10, 0, cw, hi)
    _hline(cf, 11, 0, cw, sh)
    cf[10][0] = rim
    cf[11][0] = cf[11][cw - 1] = ink
    # Octagonal engine bay bezel (cols mid_c-4 .. mid_c+4, rows 2..9) — 6x6 open aperture in center!
    bx0, bx1 = mid_c - 4, mid_c + 4
    _hline(cf, 2, bx0, bx1, hi)
    _hline(cf, 9, bx0, bx1, sh)
    _vline(cf, bx0, 2, 10, hi)
    _vline(cf, bx1 - 1, 2, 10, sh)
    # Chamfered corners inside engine bezel (gives octagonal machined socket silhouette!)
    for cx, cy in ((bx0 + 1, 3), (bx1 - 2, 3), (bx0 + 1, 8), (bx1 - 2, 8)):
        cf[cy][cx] = dk
    # Diagonal collar braces connecting yoke to bezel
    cf[2][bx0 - 1] = cf[2][bx1] = mid
    cf[3][bx0 - 1] = cf[3][bx1] = ink
    cf[9][bx0 - 1] = cf[9][bx1] = sh
    # Clean flanking bays (cols pw .. bx0-1 and bx1 .. cw-pw-1, rows 3..9) stay '.' to show inner pistons / copper / pilot!

    # Back: sculpted 3D segmented exoskeleton spine + flanking vertical damper cutouts (hero 3rd-person view!)
    cb = _grid(cw, 12, '.')
    _hline(cb, 0, 0, cw, rim)
    _hline(cb, 1, 0, cw, hi)
    _hline(cb, 2, 0, cw, sh)
    _hline(cb, 10, 0, cw, hi)
    _hline(cb, 11, 0, cw, sh)
    for y in range(1, 11):
        w_ = pw_top if y <= 4 else pw_bot
        _rect(cb, 0, y, w_, y + 1, mid)
        _rect(cb, cw - w_, y, cw, y + 1, mid)
        cb[y][0] = hi
        cb[y][cw - 1] = sh
        cb[y][w_ - 1] = ink
        cb[y][cw - w_] = ink
    # Sculpted 3D spinal column (6 texels wide at center: 3 articulated vertebrae plates with bright top bevels + AO slots!)
    sx0, sx1 = mid_c - 3, mid_c + 3
    for y in range(1, 11):
        cb[y][sx0] = ink
        cb[y][sx1 - 1] = ink
        if y in (2, 5, 8):
            # Vertebra bright top bevel!
            _hline(cb, y, sx0 + 1, sx1 - 1, shi)
            cb[y][sx0 + 1] = rim
        elif y in (3, 6, 9):
            # Vertebra mid plate
            _hline(cb, y, sx0 + 1, sx1 - 1, smid)
            cb[y][sx1 - 2] = ssh
        else:
            # Deep AO flex groove between vertebrae
            _hline(cb, y, sx0 + 1, sx1 - 1, ink)
    cb[1][1] = cb[1][cw - 2] = rim

    # Chest sides (12 x 12, solid because arms touch here — clean beveled industrial housing)
    cs = _grid(D, 12, sh)
    _hline(cs, 0, 0, D, rim)
    _hline(cs, 1, 0, D, hi)
    _rect(cs, 2, 2, D - 2, 10, deep)
    _mech_fill(cs, 2, 2, D - 2, 10, st) if not st['open_torso'] else _rect(cs, 3, 3, D - 3, 9, dk)
    _hline(cs, 10, 0, D, mid)
    _hline(cs, 11, 0, D, ink)

    # Chest up (beveled shoulder platforms outside Steve + crisp collar rims)
    cup = _grid(cw, D, '.')
    for j in range(D):
        c = rim if j == 0 else hi if j == 1 else sh if j == D - 1 else mid
        for i in range(edge_c):
            cup[j][i] = c
            cup[j][cw - 1 - i] = c
        if j == 0:
            for i in range(edge_c, cw - edge_c):
                cup[j][i] = rim
        elif j == 1:
            for i in range(edge_c, cw - edge_c):
                cup[j][i] = dk
        elif j == D - 1:
            for i in range(edge_c, cw - edge_c):
                cup[j][i] = hi
        elif j == D - 2:
            for i in range(edge_c, cw - edge_c):
                cup[j][i] = dk
    ov = round((chest_x - 5.0) * 4)
    cdn = _grid(cw, D, '.')
    if ov > 0:
        for j in range(D):
            for i in range(ov):
                cdn[j][i] = cdn[j][cw - 1 - i] = sh

    chest_outer = {'north': _str(cf), 'south': _str(cb), 'east': _str(cs), 'west': _str(cs),
                   'up': _str(cup), 'down': _str(cdn)}

    # ---- ABDOMEN OUTER (20 x 10 x 12) ----
    # Sculpted V-tapered waist frame + central articulated abdominal spine + clean flanking bays!
    def _abd_face(is_back):
        g = _grid(aw, 10, '.')
        _hline(g, 0, 0, aw, ink)   # crisp shadow under chest overhang!
        # Tapered outer side trusses (3 wide at top -> 2 wide mid -> 3 wide at waist)
        for y in range(1, 9):
            w_ = 3 if y in (1, 7, 8) else 2
            _rect(g, 0, y, w_, y + 1, mid)
            _rect(g, aw - w_, y, aw, y + 1, mid)
            g[y][0] = hi
            g[y][aw - 1] = sh
            g[y][w_ - 1] = ink
            g[y][aw - w_] = ink
        # Central 6-texel articulated column (matches chest spine!)
        cx0, cx1 = 7, 13
        for y in range(1, 9):
            g[y][cx0] = ink
            g[y][cx1 - 1] = ink
            if y in (1, 4, 7):
                _hline(g, y, cx0 + 1, cx1 - 1, shi)
                g[y][cx0 + 1] = rim
            elif y in (2, 5):
                _hline(g, y, cx0 + 1, cx1 - 1, smid)
                g[y][cx1 - 2] = ssh
            else:
                _hline(g, y, cx0 + 1, cx1 - 1, ink)
        # Beveled waist collar (rows 8..9)
        _hline(g, 8, 0, aw, hi)
        _hline(g, 9, 0, aw, sh)
        if not is_back:
            _rect(g, 8, 8, 12, 10, amid)
            _hline(g, 8, 8, 12, ahi)
        return _str(g)

    aside = _grid(D, 10, sh)
    _hline(aside, 0, 0, D, ink)
    _mech_fill(aside, 1, 1, D - 1, 8, st) if not st['open_torso'] else _rect(aside, 2, 1, D - 2, 8, dk)
    _hline(aside, 8, 0, D, hi)
    _hline(aside, 9, 0, D, ink)

    abdomen_outer = {'north': _abd_face(False), 'south': _abd_face(True), 'east': _str(aside), 'west': _str(aside),
                     'up': _str(_grid(aw, D, '.')), 'down': _str(_grid(aw, D, '.'))}

    # ---- CHEST INNER CORE (0.5 px recessed: z +-2.5, (cw-2) x 12 x 10) ----
    icw = cw - 2
    imid = icw // 2
    bx0_i, bx1_i = imid - 4, imid + 4
    if st['open_torso']:
        # Open skeleton: keep flanking bays open ('.') so pilot's shirt shows cleanly, ONLY paint the machined engine bay!
        ci_f = _grid(icw, 12, '.')
        _rect(ci_f, bx0_i, 2, bx1_i, 10, 'x')
        # Machined octagonal engine mounting flange inside the dark socket
        _rect(ci_f, bx0_i + 1, 3, bx1_i - 1, 9, 'k')
        _hline(ci_f, 3, bx0_i + 2, bx1_i - 2, 'l')
        _rect(ci_f, bx0_i + 2, 4, bx1_i - 2, 8, 'x')
        _rect(ci_f, bx0_i + 3, 5, bx1_i - 3, 7, 'm')
        for px, py in ((bx0_i + 1, 3), (bx1_i - 2, 3), (bx0_i + 1, 8), (bx1_i - 2, 8)):
            ci_f[py][px] = ahi
        ci_b = _grid(icw, 12, '.')
        # Spine backing behind the open back so spine slots have dark AO depth instead of holes
        _rect(ci_b, imid - 3, 1, imid + 3, 11, 'x')
        _rect(ci_b, imid - 2, 2, imid + 2, 10, 'd')
    else:
        # 2-layer industrial core: pitch-black AO bay + 3D-shaded pistons / copper servos / steel ribs + machined engine socket!
        ci_f = _grid(icw, 12, 'x')
        # Flanking mechanical bays (rows 2..10)
        _mech_fill(ci_f, 1, 2, bx0_i, 10, st)
        _mech_fill(ci_f, bx1_i, 2, icw - 1, 10, st)
        # Central recessed engine mounting bay (crisp machined circular flange + gleaming socket pins!)
        _rect(ci_f, bx0_i, 2, bx1_i, 10, 'x')
        _rect(ci_f, bx0_i + 1, 3, bx1_i - 1, 9, 'd')
        _hline(ci_f, 3, bx0_i + 2, bx1_i - 2, 'l')
        _hline(ci_f, 8, bx0_i + 2, bx1_i - 2, 's')
        _vline(ci_f, bx0_i + 1, 4, 8, 'p')
        _vline(ci_f, bx1_i - 2, 4, 8, 'k')
        _rect(ci_f, bx0_i + 2, 4, bx1_i - 2, 8, 'x')
        _rect(ci_f, bx0_i + 3, 5, bx1_i - 3, 7, amid)
        ci_f[5][bx0_i + 3] = ahi
        for px, py in ((bx0_i + 1, 3), (bx1_i - 2, 3), (bx0_i + 1, 8), (bx1_i - 2, 8)):
            ci_f[py][px] = ahi

        # Back core: twin vertical mechanical bays flanking the 3D spine!
        ci_b = _grid(icw, 12, 'x')
        _mech_fill(ci_b, 1, 2, imid - 2, 10, st)
        _mech_fill(ci_b, imid + 2, 2, icw - 1, 10, st)
        _rect(ci_b, imid - 2, 1, imid + 2, 11, 'd')

    chest_inner = {'north': _str(ci_f), 'south': _str(ci_b),
                   'east': _str(_grid(10, 12, '.')), 'west': _str(_grid(10, 12, '.')),
                   'up': _str(_grid(icw, 10, '.')), 'down': _str(_grid(icw, 10, '.'))}

    # ---- ABDOMEN INNER CORE (0.5 px recessed: z +-2.5, 18 x 10 x 10) ----
    iaw = aw - 2  # 18
    if st['open_torso']:
        # Clean open flanks showing pilot torso cleanly; solid AO backing only behind central spine
        def _abd_in_open():
            g = _grid(iaw, 10, '.')
            _rect(g, 6, 0, 12, 9, 'x')
            _rect(g, 7, 1, 11, 8, 'd')
            return _str(g)
        abdomen_inner = {'north': _abd_in_open(), 'south': _abd_in_open(),
                         'east': _str(_grid(10, 10, '.')), 'west': _str(_grid(10, 10, '.')),
                         'up': _str(_grid(iaw, 10, '.')), 'down': _str(_grid(iaw, 10, '.'))}
    else:
        def _abd_in_mech():
            g = _grid(iaw, 10, 'x')
            # Twin recessed piston / copper / steel-rib bays flanking the spine (rows 1..9)
            _mech_fill(g, 1, 1, 7, 9, st)
            _mech_fill(g, 11, 1, 17, 9, st)
            _rect(g, 7, 1, 11, 9, 'd')
            return _str(g)
        abdomen_inner = {'north': _abd_in_mech(), 'south': _abd_in_mech(),
                         'east': _str(_grid(10, 10, '.')), 'west': _str(_grid(10, 10, '.')),
                         'up': _str(_grid(iaw, 10, '.')), 'down': _str(_grid(iaw, 10, '.'))}

    # ---- BELT (20 x 2 x 12) ----
    bf = _grid(aw, 2, sh)
    _hline(bf, 0, 0, aw, dk)
    _hline(bf, 1, 0, aw, mid)
    _rect(bf, 7, 0, 13, 2, hi)
    _hline(bf, 0, 8, 12, rim)
    _hline(bf, 1, 8, 12, sh)
    bb = _grid(aw, 2, sh)
    _hline(bb, 0, 0, aw, dk)
    _rect(bb, 7, 0, 13, 2, mid)
    bs = _grid(D, 2, sh)
    _hline(bs, 0, 0, D, dk)
    bup = _grid(aw, D, '.')
    _hline(bup, 0, 0, aw, mid); _hline(bup, D - 1, 0, aw, sh)
    _vline(bup, 0, 0, D, hi); _vline(bup, aw - 1, 0, D, sh)
    bdn = [r[:] for r in bup]
    for j in range(1, D - 1):
        bdn[j][0] = bdn[j][-1] = 'T'

    belt = {'north': _str(bf), 'south': _str(bb), 'east': _str(bs), 'west': _str(bs),
            'up': _str(bup), 'down': _str(bdn)}
    return chest_outer, abdomen_outer, chest_inner, abdomen_inner, belt


def _r2_shoulder_cap(st):
    """Sculpted beveled shoulder yoke cap for open_skeleton (11 x 7 x 12, DECAL=0.5)."""
    rim, hi, mid, sh, dk, ink = st['rim'], st['hi'], st['mid'], st['sh'], st['dk'], st['ink']
    W, D, H = 11, 12, 7
    up = _grid(W, D, mid)
    _hline(up, 0, 0, W, rim)
    _hline(up, 1, 0, W, hi)
    _hline(up, D - 1, 0, W, sh)
    _vline(up, 0, 1, D - 1, sh)
    _vline(up, W - 1, 1, D - 1, rim)
    # Recessed dark actuator channel down top center
    _rect(up, 4, 1, 7, D - 1, 'x')
    _vline(up, 5, 1, D - 1, st['acc_hi'])
    for x, y in ((2, 2), (W - 3, 2), (2, D - 3), (W - 3, D - 3)):
        up[y][x] = ink

    def band(depths):
        g = _grid(len(depths), H, '.')
        for i, d in enumerate(depths):
            for j in range(d):
                g[j][i] = rim if j == 0 else hi if j == 1 else ink if j == d - 1 else sh if j == d - 2 else mid
        return _str(g)

    side = [3 + round(3 * i / (W - 1)) for i in range(W)]  # inner -> outer: 3..6 rows (bold angled sweep!)
    return {
        'north': band(side[::-1]), 'south': band(side),
        'east': band([6] * D), 'west': _str(_grid(D, H, '.')),
        'up': _str(up), 'down': _str(_grid(W, D, '.')),
    }


def _r2_arm(st):
    """Sculpted 2x arm: either open beveled skeleton (R2-C) or full 2-layer 0.5 px cutout exo-arm (R2-A/B/D)."""
    rim, hi, mid, sh, dk, deep, ink = st['rim'], st['hi'], st['mid'], st['sh'], st['dk'], st['deep'], st['ink']
    ahi, amid, ash = st['acc_hi'], st['acc_mid'], st['acc_sh']
    fist = _r2_fist(st)

    if not st['layered_limbs']:
        # ---- R2-C: OPEN SCULPTED STEEL SKELETON (flush 2x, gleaming beveled beams + chunky rotary elbow!) ----
        def face(kind):
            if kind == 'west':
                g = _grid(10, 24, 'd')
                _rect(g, 0, 0, 10, 3, sh)
                _rect(g, 0, 11, 10, 15, dk)
                _rect(g, 0, 22, 10, 24, dk)
                _rect(g, 2, 3, 8, 11, 'k')
                _rect(g, 2, 15, 8, 22, 'k')
                return _str(g)
            g = _grid(10, 24, '.')
            # Beveled upper shoulder ring (rows 0..2)
            _hline(g, 0, 0, 10, rim); _hline(g, 1, 0, 10, hi); _hline(g, 2, 0, 10, ink)
            # 3D cylinder-shaded vertical edge struts (2 texels each, bright outer bevel + dark inner AO edge!)
            if kind == 'north':
                _vline(g, 0, 0, 24, rim); _vline(g, 1, 2, 23, sh)
                _vline(g, 8, 2, 23, hi); _vline(g, 9, 0, 24, dk)
            elif kind == 'south':
                _vline(g, 0, 0, 24, dk); _vline(g, 1, 2, 23, hi)
                _vline(g, 8, 2, 23, sh); _vline(g, 9, 0, 24, rim)
            else:  # east: back -> front
                _vline(g, 0, 0, 24, sh); _vline(g, 1, 2, 23, dk)
                _vline(g, 8, 2, 23, hi); _vline(g, 9, 0, 24, rim)
            # Chunky 3D rotary elbow joint drum (rows 10..15) — rounded bevel + bright center pivot!
            _hline(g, 10, 0, 10, ink)
            _rect(g, 0, 11, 10, 15, dk)
            _hline(g, 11, 1, 9, hi)
            _hline(g, 12, 1, 9, mid)
            _hline(g, 13, 1, 9, sh)
            _hline(g, 14, 0, 10, ink)
            if kind == 'east':
                # Sculpted 4x4 rotary servo hub on outer elbow!
                _rect(g, 3, 11, 7, 15, 'x')
                _hline(g, 11, 4, 6, rim)
                _rect(g, 3, 12, 7, 14, hi)
                g[12][4] = 'w'; g[12][5] = ahi
                g[13][4] = sh; g[13][5] = 'x'
            else:
                _hline(g, 11, 2, 8, rim)
                _hline(g, 13, 2, 8, 'x')
            # Clean wrist collar above fist (rows 22..23)
            _hline(g, 22, 0, 10, hi); _hline(g, 23, 0, 10, ink)
            return _str(g)

        cage = {f: face(f) for f in ('north', 'east', 'south', 'west')}
        up = _grid(10, 10, '.')
        _hline(up, 0, 0, 10, hi); _hline(up, 9, 0, 10, sh); _vline(up, 9, 0, 10, rim)
        up[0][0] = up[9][0] = 'T'
        arm_hand = {f: cage[f] + fist[f] for f in ('north', 'east', 'south', 'west')}
        arm_hand['up'] = _str(up); arm_hand['down'] = fist['down']
        arm_sock = {f: cage[f][:18] for f in ('north', 'east', 'south', 'west')}
        arm_sock['up'] = _str(up); arm_sock['down'] = _r2_socket_down(st)
        return arm_hand, arm_sock, None

    # ---- FULL 2-LAYER CUTOUT EXO-ARM (R2-A exo_pistons, R2-B forge_copper, R2-D tactical_rig) ----
    # Inner arm (10 x 24): pitch-black AO mechanical housing with gleaming pistons / copper servos / steel ribs
    # on upper arm (rows 3..11) + glowing-bright rotary elbow core (rows 11..15) + clean open pilot forearm window (17..21)!
    def inner_face(kind):
        if kind == 'west':
            g = _grid(10, 24, 'd')
            _rect(g, 0, 11, 10, 15, dk)
            _rect(g, 0, 22, 10, 24, dk)
            return _str(g)
        g = _grid(10, 24, 'x')
        # Upper mechanical bay (rows 3..11) — shows through the 0.5 px outer cutout window with huge 3D contrast!
        _mech_fill(g, 1, 3, 9, 11, st)
        # Elbow rotary actuator core (rows 11..15) — bright machined cylinder peeking through outer elbow slot!
        _rect(g, 0, 11, 10, 15, 'x')
        _rect(g, 1, 12, 9, 14, 'k')
        if kind == 'east':
            _rect(g, 2, 11, 8, 15, 'x')
            _hline(g, 12, 3, 7, ahi)
            _hline(g, 13, 3, 7, amid)
            g[12][3] = 'w' if st['mech'] != 'copper' else 'F'
        else:
            _hline(g, 12, 2, 8, ahi)
            _hline(g, 13, 2, 8, ash)
        # Forearm cuff (rows 15..16) + sleek open pilot forearm window (rows 17..21) + wrist collar (22..23)
        _hline(g, 15, 0, 10, hi); _hline(g, 16, 0, 10, sh)
        _rect(g, 0, 17, 10, 22, dk)
        _vline(g, 0, 17, 22, hi if kind != 'south' else sh)
        _vline(g, 9, 17, 22, sh if kind == 'north' else hi)
        _rect(g, 2, 17, 8, 21, '.')  # clean open pilot forearm window!
        _hline(g, 22, 0, 10, hi); _hline(g, 23, 0, 10, ink)
        return _str(g)

    cage = {f: inner_face(f) for f in ('north', 'east', 'south', 'west')}
    up = _grid(10, 10, 'd')
    up[0][0] = up[9][0] = 'T'
    arm_hand = {f: cage[f] + fist[f] for f in ('north', 'east', 'south', 'west')}
    arm_hand['up'] = _str(up); arm_hand['down'] = fist['down']
    arm_sock = {f: cage[f][:18] for f in ('north', 'east', 'south', 'west')}
    arm_sock['up'] = _str(up); arm_sock['down'] = _r2_socket_down(st)

    # Outer 0.5 px cutout exo-arm (W=11 inner->outer, H=19 [y 26.5..17.0], D=12) — sculpted chamfers & bevels!
    W, H, D = 11, 19, 12
    oup = _grid(W, D, mid)
    _hline(oup, 0, 0, W, rim); _hline(oup, 1, 0, W, hi)
    _hline(oup, D - 1, 0, W, sh)
    _vline(oup, 0, 1, D - 1, sh); _vline(oup, W - 1, 1, D - 1, rim)
    _rect(oup, 4, 2, 7, D - 2, 'x')
    _vline(oup, 5, 2, D - 2, ahi)

    def outer_ns(outer_left):
        g = _grid(W, H, '.')
        # Angled chamfered shoulder cap (sweeps 6 rows deep at outer corner up to 3 rows near chest!)
        for i in range(W):
            d_out = i if outer_left else (W - 1 - i)
            depth = 6 if d_out < 3 else 5 if d_out < 6 else 4 if d_out < 9 else 3
            for j in range(depth):
                g[j][i] = rim if j == 0 else hi if j == 1 else ink if j == depth - 1 else sh if j == depth - 2 else mid
        # Sculpted outer exo-strut running down rows 5..16 (3 texels wide, crisp bevel highlight!)
        ox0, ox1 = (0, 3) if outer_left else (W - 3, W)
        _rect(g, ox0, 5, ox1, 17, mid)
        _vline(g, ox0 if outer_left else ox1 - 1, 0, 17, rim)
        _vline(g, (ox0 + 1) if outer_left else (ox1 - 2), 5, 16, hi)
        _vline(g, (ox1 - 1) if outer_left else ox0, 6, 12, ink)
        # Beveled elbow brace collar (rows 11..16, angled outer notch + wide 4x2 cutout window exposing bright actuator!)
        ex0, ex1 = (0, W - 1) if outer_left else (1, W)
        _rect(g, ex0, 11, ex1, 17, mid)
        _hline(g, 11, ex0, ex1, rim)
        _hline(g, 12, ex0, ex1, hi)
        _hline(g, 15, ex0, ex1, sh)
        _hline(g, 16, ex0, ex1, ink)
        # Wide 5x2 recessed actuator window (cols 3..7, rows 13..14)
        _rect(g, 3, 13, 8, 15, '.')
        g[13][2] = g[14][2] = ink
        g[13][8] = g[14][8] = ink
        # Crisp shoulder bolt glint
        g[2][1 if outer_left else W - 2] = rim
        return _str(g)

    oe = _grid(D, H, '.')
    # Shoulder cap (rows 0..5, matches outer depth=6!)
    for j in range(6):
        c = rim if j == 0 else hi if j == 1 else ink if j == 5 else sh if j == 4 else mid
        _hline(oe, j, 0, D, c)
    oe[2][2] = oe[2][D - 3] = rim
    # Sculpted twin vertical struts (rows 5..16) framing a crisp 6x6 cutout bay over pistons/copper/ribs!
    _rect(oe, 0, 5, 3, 17, mid); _rect(oe, D - 3, 5, D, 17, mid)
    _vline(oe, 0, 0, 17, sh); _vline(oe, 1, 5, 16, mid); _vline(oe, 2, 6, 11, ink)
    _vline(oe, D - 3, 6, 11, ink); _vline(oe, D - 2, 5, 16, hi); _vline(oe, D - 1, 0, 17, rim)
    # Elbow actuator guard (rows 11..16, matches outer_ns!) with 6x2 bright rotary window
    _rect(oe, 0, 11, D, 17, mid)
    _hline(oe, 11, 0, D, rim); _hline(oe, 12, 0, D, hi)
    _hline(oe, 15, 0, D, sh); _hline(oe, 16, 0, D, ink)
    _rect(oe, 3, 13, 9, 15, '.')
    oe[13][2] = oe[14][2] = ink
    oe[13][9] = oe[14][9] = ink

    arm_outer = {
        'north': outer_ns(True), 'south': outer_ns(False), 'east': _str(oe),
        'west': _str(_grid(D, H, '.')), 'up': _str(oup), 'down': _str(_grid(W, D, '.')),
    }
    return arm_hand, arm_sock, arm_outer


def _r2_leg(st):
    """Sculpted 2x leg: open beveled steel skeleton (R2-C) or full 2-layer 0.5 px cutout exo-leg (R2-A/B/D)."""
    rim, hi, mid, sh, dk, ink = st['rim'], st['hi'], st['mid'], st['sh'], st['dk'], st['ink']
    ahi, amid, ash = st['acc_hi'], st['acc_mid'], st['acc_sh']
    boot = _r2_boot(st)

    if not st['layered_limbs']:
        # ---- R2-C: OPEN SCULPTED STEEL SKELETON ----
        def face(kind):
            if kind == 'west':
                g = _grid(10, 23, 'd')
                _rect(g, 0, 0, 10, 3, dk)
                _rect(g, 0, 10, 10, 15, dk)
                _rect(g, 2, 3, 8, 10, 'k')
                _rect(g, 2, 15, 8, 22, 'k')
                return _str(g)
            g = _grid(10, 23, '.')
            _hline(g, 0, 0, 10, hi); _hline(g, 1, 0, 10, mid); _hline(g, 2, 0, 10, ink)
            if kind == 'north':
                _vline(g, 0, 0, 23, rim); _vline(g, 1, 2, 22, sh)
                _vline(g, 8, 2, 22, hi); _vline(g, 9, 0, 23, dk)
            elif kind == 'south':
                _vline(g, 0, 0, 23, dk); _vline(g, 1, 2, 22, hi)
                _vline(g, 8, 2, 22, sh); _vline(g, 9, 0, 23, rim)
            else:
                _vline(g, 0, 0, 23, sh); _vline(g, 1, 2, 22, dk)
                _vline(g, 8, 2, 22, hi); _vline(g, 9, 0, 23, rim)
            # Sculpted 3D knee cap & rotary outer drum (rows 10..15)
            _hline(g, 10, 0, 10, ink)
            _rect(g, 0, 11, 10, 15, dk)
            _hline(g, 15, 0, 10, ink)
            if kind == 'north':
                _rect(g, 2, 10, 8, 15, mid)
                _hline(g, 10, 2, 8, rim); _hline(g, 11, 2, 8, hi)
                _hline(g, 14, 2, 8, sh)
                _vline(g, 2, 10, 15, hi); _vline(g, 7, 10, 15, sh)
            elif kind == 'east':
                _rect(g, 3, 11, 7, 15, 'x')
                _hline(g, 11, 4, 6, rim)
                _rect(g, 3, 12, 7, 14, hi)
                g[12][4] = 'w'; g[12][5] = ahi
                g[13][4] = sh; g[13][5] = 'x'
            else:
                _hline(g, 11, 2, 8, hi); _hline(g, 13, 2, 8, 'x')
            _hline(g, 22, 0, 10, hi)
            return _str(g)

        cage = {f: face(f) for f in ('north', 'east', 'south', 'west')}
        leg_in = {f: cage[f] + boot[f] for f in ('north', 'east', 'south', 'west')}
        leg_in['up'] = _str(_grid(10, 10, '.')); leg_in['down'] = boot['down']
        return leg_in, None

    # ---- FULL 2-LAYER CUTOUT EXO-LEG (R2-A/B/D) ----
    def inner_face(kind):
        if kind == 'west':
            g = _grid(10, 23, 'd')
            _rect(g, 0, 0, 10, 3, dk)
            _rect(g, 0, 10, 10, 15, dk)
            return _str(g)
        g = _grid(10, 23, 'x')
        _hline(g, 0, 0, 10, hi); _hline(g, 1, 0, 10, mid)
        # Upper thigh mechanical actuator bay (rows 2..10)
        _mech_fill(g, 1, 2, 9, 10, st)
        # Knee rotary joint core (rows 10..15)
        _rect(g, 0, 10, 10, 15, 'x')
        _rect(g, 1, 11, 9, 14, 'k')
        _hline(g, 12, 2, 8, ahi)
        _hline(g, 13, 2, 8, amid)
        if kind == 'east':
            g[12][3] = 'w' if st['mech'] != 'copper' else 'F'
        # Lower shin: clean unobstructed pilot shin window (rows 16..20) + ankle collar
        _rect(g, 0, 15, 10, 23, dk)
        _vline(g, 0, 15, 22, hi if kind != 'south' else sh)
        _vline(g, 9, 15, 22, sh if kind == 'north' else hi)
        _rect(g, 2, 16, 8, 21, '.')  # clean open pilot shin window!
        _hline(g, 22, 0, 10, hi)
        return _str(g)

    cage = {f: inner_face(f) for f in ('north', 'east', 'south', 'west')}
    leg_in = {f: cage[f] + boot[f] for f in ('north', 'east', 'south', 'west')}
    leg_in['up'] = _str(_grid(10, 10, '.')); leg_in['down'] = boot['down']

    # Outer 0.5 px cutout exo-leg (W=11, H=23, D=12) — sculpted hip cap, outer hydraulic rail, beveled knee guard & ankle cuff!
    W, H, D = 11, 23, 12
    def outer_ns(outer_left):
        g = _grid(W, H, '.')
        ox0, ox1 = (0, 3) if outer_left else (W - 3, W)
        # Chamfered hip yoke (rows 0..3 tapering inward!)
        for i in range(W):
            d_out = i if outer_left else (W - 1 - i)
            depth = 4 if d_out < 3 else 3 if d_out < 7 else 2 if d_out < 9 else 0
            for j in range(depth):
                g[j][i] = rim if j == 0 else hi if j == 1 else ink if j == depth - 1 else mid
        # Sculpted outer vertical exo-strut (rows 2..22)
        _rect(g, ox0, 2, ox1, 23, mid)
        _vline(g, ox0 if outer_left else ox1 - 1, 0, 23, rim)
        _vline(g, (ox0 + 1) if outer_left else (ox1 - 2), 2, 22, hi)
        _vline(g, (ox1 - 1) if outer_left else ox0, 4, 21, ink)
        # Beveled sculpted knee guard (rows 10..15) with crisp cutout actuator slot
        kx0, kx1 = (0, W - 1) if outer_left else (1, W)
        _rect(g, kx0, 10, kx1, 16, mid)
        _hline(g, 10, kx0, kx1, rim); _hline(g, 11, kx0, kx1, hi)
        _hline(g, 14, kx0, kx1, sh); _hline(g, 15, kx0, kx1, ink)
        _rect(g, 3, 12, 8, 14, '.')
        g[12][2] = g[13][2] = ink; g[12][8] = g[13][8] = ink
        # Beveled ankle stabilizer collar (rows 20..22)
        _rect(g, kx0, 20, kx1, 23, mid)
        _hline(g, 20, kx0, kx1, rim); _hline(g, 21, kx0, kx1, hi); _hline(g, 22, kx0, kx1, ink)
        return _str(g)

    oe = _grid(D, H, '.')
    # Hip cap (rows 0..3, matches outer depth=4!)
    for j in range(4):
        c = rim if j == 0 else hi if j == 1 else ink if j == 3 else mid
        _hline(oe, j, 0, D, c)
    # Twin beveled vertical struts (rows 3..22) framing upper thigh actuator bay (4..9) & lower shin cutout (16..19)
    _rect(oe, 0, 3, 3, 23, mid); _rect(oe, D - 3, 3, D, 23, mid)
    _vline(oe, 0, 0, 23, sh); _vline(oe, 1, 3, 22, mid); _vline(oe, 2, 4, 10, ink); _vline(oe, 2, 16, 20, ink)
    _vline(oe, D - 3, 4, 10, ink); _vline(oe, D - 3, 16, 20, ink); _vline(oe, D - 2, 3, 22, hi); _vline(oe, D - 1, 0, 23, rim)
    # Beveled knee brace (rows 10..15) with 6x2 bright actuator window
    _rect(oe, 0, 10, D, 16, mid)
    _hline(oe, 10, 0, D, rim); _hline(oe, 11, 0, D, hi)
    _hline(oe, 14, 0, D, sh); _hline(oe, 15, 0, D, ink)
    _rect(oe, 3, 12, 9, 14, '.')
    oe[12][2] = oe[13][2] = ink; oe[12][9] = oe[13][9] = ink
    # Ankle cuff (rows 20..22)
    _rect(oe, 0, 20, D, 23, mid)
    _hline(oe, 20, 0, D, rim); _hline(oe, 21, 0, D, hi); _hline(oe, 22, 0, D, ink)
    oe[1][2] = oe[1][D - 3] = rim
    oe[21][2] = oe[21][D - 3] = rim

    leg_outer = {
        'north': outer_ns(True), 'south': outer_ns(False), 'east': _str(oe),
        'west': _str(_grid(D, H, '.')), 'up': _str(_grid(W, D, '.')), 'down': _str(_grid(W, D, '.')),
    }
    return leg_in, leg_outer


def build(style, chest_x):
    """Build all bare-frame shell face dictionaries for a given FRAME_LOOK style."""
    import frame_r4_art as r4
    if style in r4.R4_STYLES:
        return r4.build(style, chest_x)
    import frame_r3_art as r3
    if style in r3.R3_STYLES:
        return r3.build(style, chest_x)
    if style in R2_STYLES:
        st = R2_STYLES[style]
        chest_out, abd_out, chest_in, abd_in, belt = _r2_torso(st, chest_x)
        arm_hand, arm_sock, arm_out = _r2_arm(st)
        leg_in, leg_out = _r2_leg(st)
        shoulder = None if st['layered_limbs'] else _r2_shoulder_cap(st)
        return dict(
            layered_limbs=st['layered_limbs'],
            chest_shell=_resolve(chest_out),
            abdomen_shell=_resolve(abd_out),
            chest_inner=_resolve(chest_in),
            abdomen_inner=_resolve(abd_in),
            belt_shell=_resolve(belt),
            arm_shell=_resolve(arm_hand),
            arm_socket_shell=_resolve(arm_sock),
            arm_outer=_resolve(arm_out),
            shoulder_plate=_resolve(shoulder),
            leg_shell=_resolve(leg_in),
            leg_outer=_resolve(leg_out),
        )
    assert style in STYLES, (style, tuple(STYLES) + tuple(R2_STYLES))
    st = STYLES[style]
    chest_out, abd_out, chest_in, abd_in, belt = _torso(st, chest_x)
    arm_hand, arm_sock, arm_out = _arm(st)
    leg_in, leg_out = _leg(st)
    shoulder = None if st['layered_limbs'] else _shoulder_cap(st)
    return dict(
        layered_limbs=st['layered_limbs'],
        chest_shell=_resolve(chest_out),
        abdomen_shell=_resolve(abd_out),
        chest_inner=_resolve(chest_in),
        abdomen_inner=_resolve(abd_in),
        belt_shell=_resolve(belt),
        arm_shell=_resolve(arm_hand),
        arm_socket_shell=_resolve(arm_sock),
        arm_outer=_resolve(arm_out),
        shoulder_plate=_resolve(shoulder),
        leg_shell=_resolve(leg_in),
        leg_outer=_resolve(leg_out),
    )
