"""Round 4 (2026-11-23): Iterating on R3-C (forged_cobalt)'s sleek flush open-limb skeleton.

User feedback applied:
1. Keep R3-C's sleek flush open-limb geometry (bare limbs stay slimmer/flush beside iron armour, crisp 0.5 px
   shoulder cap, dark oil-iron rotary elbows/knees, burnished copper joint collars, rich directional shading).
2. Cover the chest completely (2-layer 0.5 px sculpted chest chassis + recessed mechanical conduits & engine bay)
   and widen abdomen side rails to overlap Steve's torso so ZERO empty gap between arms and torso ever shows.
3. Replace cobalt blue with palettes grounded strictly in the frame's actual crafting materials:
     suit_torso: iron_block + copper_block + redstone_block
     suit_arm / suit_leg: iron_block + copper_block + piston

Styles (env FRAME_LOOK in frame_model.py):
  iron_charcoal     R4-A: Dark tempered forged-iron frame + burnished copper collars + subtle redstone chest core
  oxidized_copper   R4-B: Weathered verdigris copper frame (Minecraft copper_block) + dark iron joints + raw copper collars
  raw_iron_redstone R4-C: Warm raw-forged iron frame + dark iron chest/joints + copper collars + redstone conduits
  cast_iron_copper  R4-D: Heavy cast-black iron frame + bold burnished copper trim + brushed-steel piston rods & redstone core
"""

import os
from frame_r3_art import _rgba, _grid, _rect, _hline, _vline, _grad_rail, _plate_band, _rotary_hub
from frame_r3_art import _r3_fist, _r3_boot, _r3_socket_down, _r3_shoulder_cap

R4_STYLES = {
    'iron_charcoal': dict(
        # Pure tempered dark forged iron (neutral/very slight cool iron tone — NO cobalt blue, clearly darker than Iron Armour!)
        fr=((0x96, 0x9c, 0xa3), (0x72, 0x79, 0x82), (0x52, 0x58, 0x61), (0x37, 0x3c, 0x43), (0x21, 0x25, 0x2b)),
        # Deep oil-rubbed cast-iron joints, chest recess, boots & fists
        jt=((0x4b, 0x51, 0x59), (0x34, 0x39, 0x40), (0x23, 0x27, 0x2c), (0x16, 0x19, 0x1d), (0x0f, 0x11, 0x14)),
        # Burnished copper collars & hydraulic rings (from copper_block)
        ac=((0xf2, 0xb4, 0x7e), (0xc8, 0x78, 0x42), (0x80, 0x44, 0x22)),
        # Brushed raw-iron spine plates
        sp=((0xd2, 0xd6, 0xdc), (0x98, 0x9f, 0xa8), (0x5c, 0x63, 0x6c)),
        # Subtle muted redstone conduit accents inside chest bay (from redstone_block)
        rs=((0xd4, 0x3b, 0x30), (0x96, 0x21, 0x1a), (0x58, 0x12, 0x0e)),
        chip=(0x84, 0x8b, 0x94),
        chest_trim='copper',
    ),
    'oxidized_copper': dict(
        # Weathered / oxidized Minecraft copper_block (rich verdigris patina, keeps cool-vs-warm harmony w/ raw copper!)
        fr=((0x8c, 0xc8, 0xb4), (0x62, 0xa4, 0x91), (0x43, 0x7e, 0x70), (0x2b, 0x58, 0x50), (0x1a, 0x38, 0x34)),
        # Deep charcoal forged-iron joints, chest core, boots & fists
        jt=((0x4e, 0x54, 0x5c), (0x36, 0x3b, 0x42), (0x24, 0x28, 0x2d), (0x17, 0x1a, 0x1e), (0x10, 0x12, 0x15)),
        # Warm unoxidized raw copper joint collars & conduits (beautiful warm/cool copper contrast!)
        ac=((0xf5, 0xb8, 0x80), (0xcf, 0x7c, 0x44), (0x85, 0x46, 0x22)),
        # Forged iron spine plates
        sp=((0xc8, 0xce, 0xd4), (0x8c, 0x94, 0x9c), (0x54, 0x5c, 0x64)),
        # Muted redstone chest core
        rs=((0xd4, 0x3b, 0x30), (0x96, 0x21, 0x1a), (0x58, 0x12, 0x0e)),
        chip=(0xb8, 0x72, 0x42),  # chipped patina reveals warm raw copper underneath!
        chest_trim='copper',
    ),
    'raw_iron_redstone': dict(
        # Warm weathered raw forged iron (distinct warm-grey tone vs Iron Armour's crisp cool blue-steel!)
        fr=((0xc2, 0xbe, 0xb5), (0x9c, 0x98, 0x8f), (0x75, 0x72, 0x6b), (0x51, 0x4f, 0x4a), (0x31, 0x30, 0x2d)),
        # Deep forged iron / piston-casing joints & chest core
        jt=((0x4c, 0x4f, 0x54), (0x35, 0x38, 0x3d), (0x24, 0x26, 0x2a), (0x17, 0x19, 0x1c), (0x10, 0x11, 0x14)),
        # Burnished copper joint collars & hydraulics
        ac=((0xf0, 0xb0, 0x78), (0xc6, 0x74, 0x3e), (0x7e, 0x40, 0x1e)),
        # Bright brushed iron spine
        sp=((0xdc, 0xda, 0xd4), (0xa4, 0xa2, 0x9c), (0x68, 0x66, 0x62)),
        # Visible redstone power conduits (chest bay, flanks & spine!)
        rs=((0xe0, 0x40, 0x32), (0xa4, 0x24, 0x1c), (0x62, 0x14, 0x10)),
        chip=(0x5e, 0x5c, 0x57),
        chest_trim='redstone',
    ),
    'cast_iron_copper': dict(
        # Heavy oil-black cast iron structural chassis (maximum contrast vs BOTH bright Iron Armour and Copper Armour!)
        fr=((0x74, 0x7a, 0x82), (0x56, 0x5c, 0x64), (0x3c, 0x41, 0x48), (0x28, 0x2c, 0x31), (0x18, 0x1b, 0x1f)),
        # Deep matte black-iron joints, boots & fists
        jt=((0x46, 0x4b, 0x52), (0x30, 0x34, 0x3a), (0x20, 0x23, 0x28), (0x14, 0x16, 0x1a), (0x0d, 0x0f, 0x12)),
        # Bold burnished copper trim, shoulder inlays, elbow/knee collars & chest rails!
        ac=((0xf5, 0xb8, 0x80), (0xcf, 0x7c, 0x44), (0x85, 0x46, 0x22)),
        # Gleaming steel-piston spine vertebrae
        sp=((0xe0, 0xe4, 0xea), (0xa2, 0xaa, 0xb4), (0x60, 0x68, 0x72)),
        # Deep redstone engine core
        rs=((0xdc, 0x3e, 0x32), (0x9c, 0x22, 0x1b), (0x5c, 0x13, 0x0f)),
        chip=(0x8a, 0x92, 0x9c),
        chest_trim='copper_bold',
    ),
}


def _r4_torso(st, chest_x):
    """Covered 2-layer sculpted mechanical chest + clean gap-free abdomen.

    - Chest (y 20..26): 100% covered front, back & sides (ZERO gap between arms and Steve's torso!).
      Outer z +-3.0 shell carves the sculpted collar yoke, beveled outer chest housing, octagonal engine bay aperture,
      flanking 0.5 px recessed mechanical conduit windows (front & back), and 3D dorsal spine over a solid z +-2.5
      dark forged-iron inner core carrying copper/redstone conduits & the machined engine mounting socket.
    - Abdomen (y 15..20): widened 3-texel outer rails (1.5 px -> overlaps 0.5 px past Steve's x +-4 torso edge!)
      plus recessed inner flanks sealed at the outer edges, leaving clean centered windows over Steve's shirt with
      ZERO air gap visible between arms and torso from any angle!
    """
    frim, fhi, fmid, fsh, fdk = [_rgba(c) for c in st['fr']]
    jhi, jmid, jsh, jdk, ink = [_rgba(c) for c in st['jt']]
    ahi, amid, ash = [_rgba(c) for c in st['ac']]
    shi, smid, ssh = [_rgba(c) for c in st['sp']]
    rhi, rmid, rsh = [_rgba(c) for c in st['rs']]
    chip = _rgba(st['chip'])
    bold_cu = st['chest_trim'] == 'copper_bold'
    red_flank = st['chest_trim'] == 'redstone'

    cw = round(chest_x * 4)   # 24 wide, 22 slim
    aw = 20
    D = 12
    edge_c = (cw - 16) // 2   # 4 wide, 3 slim
    mid_c = cw // 2
    bx0, bx1 = mid_c - 4, mid_c + 4  # central 8x8 engine bay

    # ---- CHEST OUTER (cw x 12 x 12) — COVERED CHASSIS WITH 0.5 px CUTOUT ENGINE BAY & FLANKING CONDUIT SLOTS ----
    cf = _grid(cw, 12, fmid)
    # Top sculpted collarbone yoke (rows 0..2)
    _plate_band(cf, 0, 0, cw, 3, st, rim_top=True, roll_bot=True, chips=((2, 1), (cw - 3, 1)))
    if bold_cu:
        # Subtle burnished copper shoulder collar inlay across upper chest yoke
        _hline(cf, 1, 2, bx0 - 1, amid); cf[1][2] = ahi
        _hline(cf, 1, bx1 + 1, cw - 2, amid); cf[1][cw - 3] = ahi
    # Outer beveled chest ribs (rows 2..10, left & right of engine bay) with directional light falloff!
    for y in range(2, 10):
        t = (y - 2) / 7.0
        body = fhi if t < 0.25 else fmid if t < 0.7 else fsh
        _hline(cf, y, 0, cw, body)
        cf[y][0] = fhi if t < 0.5 else fmid
        cf[y][1] = body
        cf[y][cw - 1] = fdk if t > 0.5 else fsh
    # Crisp mechanical panel seam separating outer shoulder pillars from pectoral bay
    _vline(cf, edge_c, 2, 10, fdk)
    _vline(cf, cw - 1 - edge_c, 2, 10, fdk)
    # Shoulder lock pins (copper accent)
    cf[1][1] = cf[1][cw - 2] = ahi
    cf[2][1] = cf[2][cw - 2] = ash
    cf[9][1] = cf[9][cw - 2] = jdk
    # Flanking 0.5 px cutout mechanical conduit slots (2x4 recessed slots showing copper/redstone conduits on inner core!)
    # Strictly INSIDE the solid inner core — ZERO see-through air gap!
    fl_x0 = edge_c + 1
    fr_x0 = cw - edge_c - 3
    for fx in (fl_x0, fr_x0):
        if fx + 2 <= bx0 or fx >= bx1:
            _rect(cf, fx, 4, fx + 2, 8, '.')
            _hline(cf, 3, fx, fx + 2, ink)
            _hline(cf, 8, fx, fx + 2, fhi)
            cf[4][fx - 1] = cf[5][fx - 1] = cf[6][fx - 1] = cf[7][fx - 1] = ink
            cf[4][fx + 2] = cf[5][fx + 2] = cf[6][fx + 2] = cf[7][fx + 2] = fdk
    # Central octagonal engine bay bezel (rows 2..9, cols bx0..bx1) — 6x6 open aperture into recessed dark engine bay!
    _rect(cf, bx0, 2, bx1, 10, '.')
    _hline(cf, 2, bx0, bx1, jhi)
    _hline(cf, 9, bx0, bx1, jdk)
    _vline(cf, bx0, 2, 10, jhi)
    _vline(cf, bx1 - 1, 2, 10, jsh)
    for lx, ly in ((bx0 + 1, 3), (bx1 - 2, 3), (bx0 + 1, 8), (bx1 - 2, 8)):
        cf[ly][lx] = amid
    cf[3][bx0 + 1] = cf[3][bx1 - 2] = ahi
    # Bottom sternum rolled rim (rows 10..11)
    _hline(cf, 10, 0, cw, fhi)
    cf[10][0] = frim; cf[10][cw - 1] = fsh
    _hline(cf, 11, 0, cw, fdk)
    cf[11][0] = cf[11][cw - 1] = ink

    # Back: COVERED sculpted exo-chassis flanking the 3D dorsal spine (ZERO gap, clean mounting surface for all 3 engines!)
    cb = _grid(cw, 12, fmid)
    _plate_band(cb, 0, 0, cw, 3, st, rim_top=True, roll_bot=True, chips=((3, 1), (cw - 4, 1)))
    if bold_cu:
        _hline(cb, 1, 2, mid_c - 3, amid); cb[1][2] = ahi
        _hline(cb, 1, mid_c + 3, cw - 2, amid); cb[1][cw - 3] = ahi
    for y in range(2, 10):
        t = (y - 2) / 7.0
        body = fhi if t < 0.25 else fmid if t < 0.7 else fsh
        _hline(cb, y, 0, cw, body)
        cb[y][0] = fhi if t < 0.5 else fmid
        cb[y][cw - 1] = fdk if t > 0.5 else fsh
    _vline(cb, edge_c, 2, 10, fdk)
    _vline(cb, cw - 1 - edge_c, 2, 10, fdk)
    cb[1][1] = cb[1][cw - 2] = ahi
    cb[2][1] = cb[2][cw - 2] = ash
    # Flanking 0.5 px recessed dorsal vent/piston slots (solid inner core behind -> zero air gap!)
    for fx in (edge_c + 1, cw - edge_c - 4):
        _rect(cb, fx, 4, fx + 3, 8, '.')
        _hline(cb, 3, fx, fx + 3, ink)
        _hline(cb, 8, fx, fx + 3, fhi)
        for y in range(4, 8):
            cb[y][fx - 1] = ink
            cb[y][fx + 3] = fdk
    # Sculpted 3D dorsal spine (6 texels wide: alternating brushed-iron vertebrae + dark flex joints + copper/redstone core)
    sx0, sx1 = mid_c - 3, mid_c + 3
    for y in range(2, 11):
        cb[y][sx0] = ink
        cb[y][sx1 - 1] = ink
        if y in (2, 5, 8):
            _hline(cb, y, sx0 + 1, sx1 - 1, shi)
            cb[y][sx1 - 2] = smid
        elif y in (3, 6, 9):
            _hline(cb, y, sx0 + 1, sx1 - 1, smid)
            cb[y][sx1 - 2] = ssh
        else:
            _hline(cb, y, sx0 + 1, sx1 - 1, jdk)
            cb[y][mid_c - 1] = rhi if red_flank else amid
            cb[y][mid_c] = rsh if red_flank else ash
    _hline(cb, 10, 0, cw, fhi)
    _hline(cb, 11, 0, cw, fdk)

    # Chest sides (12 x 12, solid dark iron mechanical wall where arms touch)
    cs = _grid(D, 12, jsh)
    _plate_band(cs, 0, 0, D, 3, st, rim_top=True, roll_bot=True)
    _rect(cs, 2, 3, D - 2, 10, jdk)
    _rect(cs, 4, 3, D - 4, 10, jmid)
    _vline(cs, 5, 4, 9, ahi)
    _vline(cs, 6, 4, 9, amid)
    _hline(cs, 10, 0, D, jmid)
    _hline(cs, 11, 0, D, ink)

    # Chest up (solid collar platform outside Steve's neck, beveled front/back neck rim)
    cup = _grid(cw, D, '.')
    for j in range(D):
        c = frim if j == 0 else fhi if j == 1 else fsh if j == D - 1 else fmid
        for i in range(edge_c):
            cup[j][i] = cup[j][cw - 1 - i] = c
        if j == 0:
            for i in range(edge_c, cw - edge_c): cup[j][i] = frim
        elif j == 1:
            for i in range(edge_c, cw - edge_c): cup[j][i] = jdk
        elif j == D - 1:
            for i in range(edge_c, cw - edge_c): cup[j][i] = fhi
        elif j == D - 2:
            for i in range(edge_c, cw - edge_c): cup[j][i] = jdk
    ov = round((chest_x - 5.0) * 4)
    cdn = _grid(cw, D, '.')
    if ov > 0:
        for j in range(D):
            for i in range(ov):
                cdn[j][i] = cdn[j][cw - 1 - i] = fsh

    chest_outer = {'north': cf, 'south': cb, 'east': cs, 'west': cs, 'up': cup, 'down': cdn}

    # ---- CHEST INNER CORE (0.5 px recessed: z +-2.5, (cw-2) x 12 x 10) — 100% SOLID MECHANICAL BACKING! ----
    icw = cw - 2
    imid = icw // 2
    bx0_i, bx1_i = imid - 4, imid + 4
    ci_f = _grid(icw, 12, jdk)
    _rect(ci_f, 0, 0, icw, 12, jdk)
    # Recessed horizontal copper / redstone power conduits visible cleanly inside the flanking 2x4 chest slots!
    c_top = rhi if red_flank else ahi
    c_mid = rmid if red_flank else amid
    c_bot = rsh if red_flank else ash
    for y_row, col in ((4, ink), (5, c_top), (6, c_mid), (7, c_bot)):
        _hline(ci_f, y_row, 1, bx0_i, col)
        _hline(ci_f, y_row, bx1_i, icw - 1, col)
    # Central machined engine mounting bay (dark forged iron socket + subtle redstone core bus from suit_torso recipe!)
    _rect(ci_f, bx0_i, 2, bx1_i, 10, ink)
    _rect(ci_f, bx0_i + 1, 3, bx1_i - 1, 9, jsh)
    _hline(ci_f, 3, bx0_i + 2, bx1_i - 2, jhi)
    _rect(ci_f, bx0_i + 2, 4, bx1_i - 2, 8, ink)
    ci_f[5][imid - 1] = rhi; ci_f[5][imid] = rmid
    ci_f[6][imid - 1] = rmid; ci_f[6][imid] = rsh

    ci_b = _grid(icw, 12, jdk)
    for y_row, col in ((4, ink), (5, c_top), (6, c_mid), (7, c_bot)):
        _hline(ci_b, y_row, 1, imid - 3, col)
        _hline(ci_b, y_row, imid + 3, icw - 1, col)
    _rect(ci_b, imid - 3, 2, imid + 3, 11, ink)
    _rect(ci_b, imid - 2, 3, imid + 2, 10, jdk)

    chest_inner = {'north': ci_f, 'south': ci_b,
                   'east': _grid(10, 12, '.'), 'west': _grid(10, 12, '.'),
                   'up': _grid(icw, 10, '.'), 'down': _grid(icw, 10, '.')}

    # ---- ABDOMEN OUTER (20 x 10 x 12) — 3-TEXEL SIDE RAILS SEAL THE ARM-TORSO GAP, CLEAN BELLY WINDOWS OVER STEVE! ----
    def _abd_face(is_back):
        g = _grid(aw, 10, '.')
        _hline(g, 0, 0, aw, ink)
        # 3-texel side struts (1.5 px -> overlaps 0.5 px past Steve's torso edge so ZERO gap beside arms!)
        _grad_rail(g, 0, 1, 9, 3, st, lit_left=True, ao_rows=(1, 8), chip_rows=(4,))
        _grad_rail(g, aw - 3, 1, 9, 3, st, lit_left=False, ao_rows=(1, 8), chip_rows=(5,))
        # Central 6-texel articulated mechanical spine / sternum column
        cx0, cx1 = 7, 13
        for y in range(1, 9):
            g[y][cx0] = ink
            g[y][cx1 - 1] = ink
            if y in (1, 4, 7):
                _hline(g, y, cx0 + 1, cx1 - 1, shi if is_back else jhi)
                g[y][cx1 - 2] = smid if is_back else jmid
            elif y in (2, 5):
                _hline(g, y, cx0 + 1, cx1 - 1, smid if is_back else jmid)
                g[y][cx1 - 2] = ssh if is_back else jsh
            else:
                _hline(g, y, cx0 + 1, cx1 - 1, jdk)
                g[y][9] = rhi if (red_flank and y == 3) else ahi if y == 3 else amid
                g[y][10] = rsh if (red_flank and y == 3) else ash
        # Dark oil-iron waist ring (rows 8..9)
        _hline(g, 8, 0, aw, jmid)
        _hline(g, 8, 1, aw - 1, jhi)
        _hline(g, 9, 0, aw, jdk)
        if not is_back:
            _rect(g, 8, 8, 12, 10, fmid)
            _hline(g, 8, 8, 12, fhi)
            g[8][9] = g[8][10] = ahi
        return g

    aside = _grid(D, 10, jsh)
    _hline(aside, 0, 0, D, ink)
    _rect(aside, 2, 1, D - 2, 8, jdk)
    _vline(aside, 5, 2, 7, amid)
    _vline(aside, 6, 2, 7, ash)
    _hline(aside, 8, 0, D, jmid)
    _hline(aside, 9, 0, D, ink)

    abdomen_outer = {'north': _abd_face(False), 'south': _abd_face(True), 'east': aside, 'west': aside,
                     'up': _grid(aw, D, '.'), 'down': _grid(aw, D, '.')}

    # Abdomen inner core (0.5 px recessed): dark backing behind outer 2 texels (extra seal against angled arm-torso peek!)
    # + behind central spine; centered 4x7 flanks stay open ('.') so Steve's torso shows cleanly!
    iaw = aw - 2  # 18
    def _abd_in():
        g = _grid(iaw, 10, '.')
        _rect(g, 0, 0, 2, 9, jdk)
        _rect(g, iaw - 2, 0, iaw, 9, jdk)
        _rect(g, 6, 0, 12, 9, ink)
        _rect(g, 7, 1, 11, 8, jdk)
        return g
    abdomen_inner = {'north': _abd_in(), 'south': _abd_in(),
                     'east': _grid(10, 10, '.'), 'west': _grid(10, 10, '.'),
                     'up': _grid(iaw, 10, '.'), 'down': _grid(iaw, 10, '.')}

    # ---- BELT (20 x 2 x 12) ----
    bf = _grid(aw, 2, jsh)
    _hline(bf, 0, 0, aw, jdk); _hline(bf, 1, 0, aw, jmid)
    _rect(bf, 7, 0, 13, 2, fmid); _hline(bf, 0, 8, 12, fhi); _hline(bf, 1, 8, 12, fsh)
    bb = _grid(aw, 2, jsh)
    _hline(bb, 0, 0, aw, jdk); _rect(bb, 7, 0, 13, 2, jmid)
    bs = _grid(D, 2, jsh); _hline(bs, 0, 0, D, jdk)
    bup = _grid(aw, D, '.')
    _hline(bup, 0, 0, aw, jmid); _hline(bup, D - 1, 0, aw, jsh)
    _vline(bup, 0, 0, D, jhi); _vline(bup, aw - 1, 0, D, jsh)
    bdn = [r[:] for r in bup]
    for j in range(1, D - 1): bdn[j][0] = bdn[j][-1] = 'T'

    belt = {'north': bf, 'south': bb, 'east': bs, 'west': bs, 'up': bup, 'down': bdn}
    return chest_outer, abdomen_outer, chest_inner, abdomen_inner, belt


# ---------------------------------------------------------------- Gauntlet iterations (2026-11-23, on locked iron_charcoal)
# Proper anatomical orientation on the right arm (left arm mirrors automatically):
#   east  (+x, outer side):  BACK OF HAND (dorsum, armored wrist cuff, knuckle guard — hero 3/4 & side face!)
#   west  (-x, inner side):  PALM (dark grip pad, thumb base, curled fingertips)
#   north (-z, front):       THUMB SIDE (armored thumb curling on inner-front + index knuckle ridge on outer-front)
#   south (+z, back):        PINKY / BLADE EDGE (ulnar guard + curled pinky finger)
#   down  (-y, bottom):      CURLED ARMORED FINGERS (4 segmented fingers curling east -> west)

def _gauntlet_plated(st):
    """G-A (flush 5x5): Sleek articulated forged-iron gauntlet with armored back-of-hand, thumb guard & curled fingers."""
    frim, fhi, fmid, fsh, fdk = [_rgba(c) for c in st['fr']]
    jhi, jmid, jsh, jdk, ink = [_rgba(c) for c in st['jt']]
    ahi, amid, ash = [_rgba(c) for c in st['ac']]
    shi, smid, ssh = [_rgba(c) for c in st['sp']]

    # Back of hand (east: col 0 = south/pinky .. col 9 = north/thumb; rows 0..7)
    east = _grid(10, 8, jsh)
    # Armored wrist cuff lip (rows 0..1) with burnished copper strap latch
    _hline(east, 0, 0, 10, ink)
    _hline(east, 1, 0, 10, fmid); east[1][9] = frim; east[1][0] = fsh
    _hline(east, 1, 3, 7, amid); east[1][4] = east[1][5] = ahi
    # Sculpted metacarpal backplate (rows 2..4) tapering into raised steel knuckle ridge (row 4..5)
    _rect(east, 0, 2, 10, 5, fmid)
    _hline(east, 2, 1, 10, fhi); east[2][9] = frim
    _vline(east, 0, 2, 5, fsh); _vline(east, 9, 2, 5, fhi)
    _rect(east, 1, 3, 9, 5, fmid)
    _hline(east, 4, 0, 10, shi); east[4][0] = smid; east[4][9] = shi  # crisp raised knuckle plate ridge!
    # Articulated armored fingers (rows 5..7) — 4 distinct finger segments with dark joint grooves!
    _hline(east, 5, 0, 10, ink)
    _rect(east, 0, 6, 10, 8, fsh)
    for fx in (0, 1, 3, 4, 6, 7, 9):
        east[6][fx] = fhi if fx >= 6 else fmid
        east[7][fx] = fsh if fx >= 6 else fdk
    for gx in (2, 5, 8):
        east[6][gx] = east[7][gx] = ink  # 3 crisp inter-finger grooves -> 4 fingers!

    # Thumb side (north: col 0 = east/outer back-of-hand .. col 9 = west/inner palm)
    north = _grid(10, 8, jsh)
    _hline(north, 0, 0, 10, ink)
    _hline(north, 1, 0, 10, fmid); north[1][0] = frim; north[1][9] = jmid
    # Outer back-of-hand & index armor wrapping around col 0..4
    _rect(north, 0, 2, 5, 5, fmid)
    _hline(north, 2, 0, 5, fhi); north[2][0] = frim
    _hline(north, 4, 0, 5, shi)
    _hline(north, 5, 0, 5, ink)
    _rect(north, 0, 6, 5, 8, fmid); _hline(north, 7, 0, 5, fdk)
    # Articulated armored thumb curling down on inner-front (cols 5..9, rows 2..7)!
    _vline(north, 5, 2, 8, ink)
    _rect(north, 6, 2, 9, 6, fhi)
    _hline(north, 2, 6, 9, frim)
    _hline(north, 4, 6, 9, ink)       # thumb knuckle flex crease
    _rect(north, 6, 5, 9, 7, fmid)
    north[3][6] = ahi                  # tiny copper thumb-joint pin
    _vline(north, 9, 2, 8, jdk)        # palm recess edge
    _rect(north, 5, 7, 10, 8, jdk)

    # Blade / pinky side (south: col 0 = west/inner palm .. col 9 = east/outer back-of-hand)
    south = _grid(10, 8, jsh)
    _hline(south, 0, 0, 10, ink)
    _hline(south, 1, 0, 10, fsh); south[1][9] = fhi
    # Outer ulnar armor guard wrapping around col 5..9
    _rect(south, 5, 2, 10, 5, fmid)
    _hline(south, 2, 5, 10, fhi); south[2][9] = frim
    _hline(south, 4, 5, 10, smid)
    _hline(south, 5, 5, 10, ink)
    _rect(south, 5, 6, 10, 8, fsh); _hline(south, 7, 5, 10, fdk)
    # Inner dark palm & curled pinky edge (cols 0..4)
    _rect(south, 0, 2, 5, 8, jdk)
    _rect(south, 1, 3, 4, 7, jmid)
    _hline(south, 5, 0, 5, ink)

    # Palm (west: col 0 = north/thumb .. col 9 = south/pinky)
    west = _grid(10, 8, jdk)
    _hline(west, 0, 0, 10, ink)
    _hline(west, 1, 0, 10, jmid)
    # Thumb pad on north side (cols 0..3)
    _rect(west, 0, 2, 4, 6, jhi); _vline(west, 3, 2, 6, ink)
    # Ribbed dark grip pad in palm center (cols 4..9, rows 2..5)
    _rect(west, 4, 2, 10, 6, jsh)
    _hline(west, 3, 4, 9, jmid); _hline(west, 5, 4, 9, ink)
    # Curled finger tips gripping across bottom (rows 6..7)
    _rect(west, 0, 6, 10, 8, jmid)
    for gx in (2, 5, 8):
        west[6][gx] = west[7][gx] = ink

    # Underside (down: col 0 = west/palm .. col 9 = east/back-of-hand; row 0 = south/pinky .. row 9 = north/thumb)
    down = _grid(10, 10, jdk)
    # 4 armored finger pads running across east -> west (rows 0..1, 2..3, 4..5, 6..7 -> separated by dark ink seams!)
    for ry in (0, 1, 3, 4, 6, 7, 9):
        _rect(down, 3, ry, 10, ry + 1, fmid)
        _rect(down, 7, ry, 10, ry + 1, fhi)
        _rect(down, 1, ry, 3, ry + 1, jmid)
    for gy in (2, 5, 8):
        _hline(down, gy, 0, 10, ink)
    _vline(down, 6, 0, 10, ink)  # mid-finger phalanx hinge!
    _vline(down, 3, 0, 10, ink)  # fingertip curl line!

    return {'north': north, 'east': east, 'south': south, 'west': west, 'down': down}


def _gauntlet_cyber(st):
    """G-D (flush 5x5): High-articulation mechanical exo-glove w/ exposed copper dorsal tendon & overlapping steel phalanges."""
    frim, fhi, fmid, fsh, fdk = [_rgba(c) for c in st['fr']]
    jhi, jmid, jsh, jdk, ink = [_rgba(c) for c in st['jt']]
    ahi, amid, ash = [_rgba(c) for c in st['ac']]
    shi, smid, ssh = [_rgba(c) for c in st['sp']]

    # Start from plated anatomy, then carve exposed mechanical tendon & segmented knuckle plates!
    g = _gauntlet_plated(st)
    east = g['east']
    # Exposed dark recessed dorsal channel + central burnished copper hydraulic tendon on back of hand (rows 1..4)!
    _rect(east, 3, 1, 7, 5, ink)
    _vline(east, 4, 1, 5, ahi)
    _vline(east, 5, 1, 5, amid)
    # Stepped brushed-steel individual knuckle caps (4 raised steel knuckles at row 4..5!)
    _hline(east, 4, 0, 10, ink)
    for kx in (0, 1, 3, 4, 6, 7, 9):
        east[4][kx] = shi
        east[5][kx] = smid
        east[6][kx] = fmid
        east[7][kx] = fdk
    for gx in (2, 5, 8):
        east[4][gx] = east[5][gx] = east[6][gx] = east[7][gx] = ink

    # Copper hydraulic tendon rivet on thumb & blade edge
    g['north'][2][2] = ahi; g['north'][3][2] = amid
    g['north'][4][0] = shi; g['north'][4][1] = smid
    g['south'][2][7] = amid; g['south'][3][7] = ash
    return g


def _fist_down_natural_10(slate_pal):
    """Inner-layer 5x5 (10x10 texel) closed mechanical-fist underside (fist_end_art.py Variant B):
      col 0 = west (-x, palm) .. col 9 = east (+x, outer knuckles)
      row 0 = north (-z, front/index) .. row 9 = south (+z, back/pinky)
    Lives strictly on the inner 5x5 hand box so the outer 0.5 px layer stays purely the armored hand guard!
    Four curled fingers (index 0..1, middle 3..4, ring 6..7, pinky 9) run cleanly from the outer knuckle edge
    (cols 8..9, lit) across into the dark palm (cols 7 -> 0, shaded) with crisp 1-texel gaps (rows 2, 5, 8)
    that wrap 1-to-1 around the corners onto east (cols 7, 4, 1) and west (cols 2, 5, 8)."""
    srim, shi, smid, ssh, sdk, ink = slate_pal
    g = _grid(10, 10, ink)

    along = {7: shi, 6: smid, 5: smid, 4: ssh, 3: ssh, 2: sdk, 1: sdk, 0: ink}
    gap_rows = {2, 5, 8}

    for r in range(10):
        for c in range(10):
            if c >= 8:
                # Lit outer knuckle / finger-back edge (cols 8..9, matches inner east rows 6..7)
                if r in gap_rows:
                    g[r][c] = ssh if c == 9 else ink
                else:
                    g[r][c] = srim if c == 9 and r in (0, 3, 6, 9) else shi if c == 9 else smid
            elif r in gap_rows:
                g[r][c] = ink
            else:
                front_half = r in (0, 3, 6, 9)
                base = along[c]
                if front_half and c == 6:
                    base = shi
                elif not front_half and c == 7:
                    base = smid
                g[r][c] = base
    return g


def _gauntlet_2layer(st, heavy=False, slate_universal=True):
    """G-B ('layered') & G-C ('power_fist'): True 2-layer universal-slate power-suit gauntlet!
    Clean functional split between the two layers:
    - INNER 5x4x5 HAND (arm_shell / arm_armor / cu_arm_armor, raw y 10.0..14.0, 10x8 sides + 10x10 Variant-B down):
      holds the actual articulated dark-slate mechanical hand — recessed copper dorsal actuator (rows 1..3),
      open dark grip palm (west), articulated thumb (north), and the 4 curled fingers protruding 1.0 px cleanly
      below the outer knuckle guard (rows 6..7 + 10x10 clenched-fist down face!).
    - OUTER 0.5 px HAND GUARD ONLY (gauntlet_outer, 6 x 4.5 x 6, raw y 11.0..15.5, 12x9 sides + 12x12 up collar ring,
      down = blank): sculpted neutral dark-slate vambrace wrist cuff, dorsal guard w/ 6x3 copper-piston cutout,
      reinforced beveled knuckle impact bar & thumb guard — stops cleanly 1.0 px above the curled fingers, with the
      inner palm (west rows 3..8) left open!
    """
    if slate_universal:
        srim = _rgba((0x74, 0x7b, 0x82))  # crisp neutral slate specular bevel
        shi_ = _rgba((0x5a, 0x62, 0x68))  # lit slate highlight
        smid = _rgba((0x44, 0x4b, 0x50))  # mid neutral slate body
        ssh  = _rgba((0x30, 0x36, 0x3a))  # shaded slate
        sdk  = _rgba((0x21, 0x25, 0x28))  # deep slate shadow
        ink  = _rgba((0x13, 0x16, 0x18))  # ambient occlusion / seam
        kbar_hi  = _rgba((0x6a, 0x71, 0x78))
        kbar_mid = _rgba((0x4e, 0x55, 0x5b))
        kbar_sh  = _rgba((0x34, 0x3a, 0x3f))
    else:
        srim, shi_, smid, ssh, sdk = [_rgba(c) for c in st['fr']]
        ink = _rgba(st['jt'][4])
        kbar_hi, kbar_mid, kbar_sh = [_rgba(c) for c in st['sp']]

    ahi, amid, ash = [_rgba(c) for c in st['ac']]

    # ---- INNER 5x4x5 MECHANICAL HAND & CURLED FINGERS (10 x 8 sides, 10 x 10 Variant-B down) ----
    # 1. East (back of hand, col 0 = south/pinky .. col 9 = north/index -> col = 9 - k; finger gaps at k=2,5,8 -> cols 7,4,1)
    ie = _grid(10, 8, sdk)
    _hline(ie, 0, 0, 10, ink)
    # Recessed copper dorsal hydraulic piston visible through outer hand guard's 6x3 cutout (rows 1..3)
    _rect(ie, 1, 1, 9, 4, ink)
    _hline(ie, 1, 2, 8, ahi)
    _hline(ie, 2, 2, 8, amid)
    _hline(ie, 3, 2, 8, ash)
    _hline(ie, 4, 0, 10, ssh)
    _hline(ie, 5, 0, 10, ink)                      # crisp cast-shadow crease right under outer knuckle guard!
    # Protruding curled fingers (rows 6..7 = raw y 11.0..10.0, sticking 1.0 px below the outer guard!)
    _rect(ie, 0, 6, 10, 8, smid)
    _hline(ie, 6, 0, 10, shi_)
    _hline(ie, 7, 0, 10, smid)
    for c_lit in (0, 3, 6, 9):
        ie[6][c_lit] = srim
    for gx in (1, 4, 7):
        ie[6][gx] = ie[7][gx] = ink                # wraps 1-to-1 onto down rows 8, 5, 2!

    # 2. North (thumb side, col 0 = east/knuckles .. col 9 = west/palm)
    in_n = _grid(10, 8, sdk)
    _hline(in_n, 0, 0, 10, ink)
    _hline(in_n, 1, 1, 6, ahi); _hline(in_n, 2, 1, 6, amid)
    # Outer curled index finger protruding below guard (cols 0..3, rows 6..7)
    _rect(in_n, 0, 3, 4, 6, ssh); _hline(in_n, 5, 0, 4, ink)
    _rect(in_n, 0, 6, 4, 8, smid); _hline(in_n, 6, 0, 3, shi_); in_n[6][0] = srim
    # Articulated mechanical thumb curling cleanly across inner-front (cols 4..9, rows 2..7)
    _vline(in_n, 4, 2, 8, ink)
    _rect(in_n, 5, 2, 9, 8, smid)
    _hline(in_n, 2, 5, 9, shi_); _hline(in_n, 5, 5, 9, ink)
    _rect(in_n, 5, 6, 9, 8, shi_); _hline(in_n, 7, 5, 9, smid)
    _vline(in_n, 9, 2, 8, sdk)

    # 3. South (pinky / blade edge, col 0 = west/palm .. col 9 = east/knuckles)
    in_s = _grid(10, 8, sdk)
    _hline(in_s, 0, 0, 10, ink)
    _hline(in_s, 1, 4, 9, amid); _hline(in_s, 2, 4, 9, ash)
    _rect(in_s, 1, 3, 9, 6, ssh)
    _hline(in_s, 5, 0, 10, ink)
    # Side view of curled pinky finger across rows 6..7 (lit at knuckle col 9 -> shaded into palm col 0, matching down row 9!)
    for c, col in ((0, ink), (1, sdk), (2, sdk), (3, ssh), (4, ssh), (5, smid), (6, smid), (7, shi_), (8, smid), (9, srim)):
        in_s[6][c] = col
        in_s[7][c] = ink if c == 0 else sdk if c <= 2 else ssh if c <= 5 else smid if c <= 8 else shi_

    # 4. West (inner palm, col 0 = north/index .. col 9 = south/pinky -> aligns 1-to-1 with down rows!)
    in_w = _grid(10, 8, sdk)
    _hline(in_w, 0, 0, 10, ink)
    # Thumb base pad on north side (cols 0..3, rows 1..5)
    _rect(in_w, 0, 1, 4, 6, smid); _vline(in_w, 0, 1, 6, shi_); _vline(in_w, 3, 1, 6, ink)
    # Ribbed dark grip palm (cols 4..9, rows 1..5) — completely visible through open outer west!
    _rect(in_w, 4, 1, 10, 6, sdk)
    _rect(in_w, 5, 2, 9, 5, ssh)
    _hline(in_w, 3, 5, 9, smid)
    # Curled fingertips tucked into palm across rows 6..7 — gaps at cols 2, 5, 8 matching down rows 2, 5, 8!
    _hline(in_w, 5, 0, 10, ink)
    _rect(in_w, 0, 6, 10, 8, ssh)
    _hline(in_w, 6, 0, 10, smid)
    for gx in (2, 5, 8):
        in_w[6][gx] = in_w[7][gx] = ink

    in_hand = {
        'north': in_n, 'east': ie, 'south': in_s, 'west': in_w,
        'down': _fist_down_natural_10((srim, shi_, smid, ssh, sdk, ink)),
    }

    def _slate_band(g, x0, y0, x1, y1):
        h = y1 - y0
        for dy in range(h):
            y = y0 + dy
            for x in range(x0, x1):
                if dy == 0: c = srim if x < x1 - 1 else shi_
                elif dy == 1 and h >= 3: c = shi_ if x == x0 else smid if x < x1 - 1 else ssh
                else: c = smid if x < x1 - 1 else ssh
                g[y][x] = c

    # ---- OUTER 0.5 px HAND GUARD ONLY (6 x 4.5 x 6 -> W=12, H=9 [raw y 15.5..11.0], D=12; down = blank!) ----
    # Stops cleanly 1.0 px above the bottom of the fist so the inner curled fingers protrude naturally beneath!
    W, H, D = 12, 9, 12

    # 1. East (dorsal hand guard + knuckle impact bar, 12 x 9: rows 0..8)
    oe = _grid(D, H, smid)
    _slate_band(oe, 0, 0, D, 3)                    # heavy beveled wrist vambrace collar (rows 0..2)
    oe[1][2] = oe[1][D - 3] = ahi                  # copper cuff latch rivets
    if heavy:
        # Wide 6x3 cutout exposing the recessed copper dorsal piston (rows 3..5, cols 3..8)
        _rect(oe, 0, 3, 3, 9, smid); _rect(oe, D - 3, 3, D, 9, smid)
        _rect(oe, 3, 3, D - 3, 6, '.')
        _hline(oe, 2, 3, D - 3, ink)
        _vline(oe, 2, 3, 6, ink); _vline(oe, D - 3, 3, 6, ink)
        # Reinforced beveled dark-slate knuckle impact bar (rows 6..8, crisp ink bottom lip at row 8!)
        _rect(oe, 0, 6, D, 9, kbar_mid)
        _hline(oe, 6, 0, D, kbar_hi); oe[6][D - 1] = srim
        _hline(oe, 7, 0, D, kbar_sh)
        _hline(oe, 8, 0, D, ink)
    else:
        _rect(oe, 4, 3, 8, 5, '.')
        _hline(oe, 2, 4, 8, ink)
        oe[3][3] = oe[4][3] = ink; oe[3][8] = oe[4][8] = ink
        _hline(oe, 5, 3, 9, shi_)
        _hline(oe, 6, 0, D, kbar_hi); _hline(oe, 7, 0, D, ssh); _hline(oe, 8, 0, D, ink)
    _vline(oe, 0, 0, 9, ssh); _vline(oe, D - 1, 0, 9, srim)
    oe[8][0] = oe[8][D - 1] = ink

    # 2. North (thumb-side guard, 12 x 9: col 0 = east .. col 11 = west; matches east col 11 & west col 0!)
    on = _grid(W, H, '.')
    _slate_band(on, 0, 0, W, 3)                    # continuous wrist cuff (rows 0..2)
    _hline(on, 2, 0, W, ink)
    # Outer back-of-hand & knuckle guard wrapping from east (cols 0..5, rows 3..8)
    _rect(on, 0, 3, 6, 9, smid)
    _vline(on, 0, 0, 9, srim)
    _vline(on, 5, 3, 9, ink)
    # Crisp 2x2 cutout exposing copper wrist actuator (cols 2..4, rows 3..5)
    _rect(on, 2, 3, 4, 5, '.')
    on[3][1] = on[4][1] = ink; on[3][4] = on[4][4] = ink; on[5][2] = on[5][3] = shi_
    _hline(on, 6, 0, 6, kbar_hi); _hline(on, 7, 0, 6, kbar_sh); _hline(on, 8, 0, 6, ink)
    # Floating armored thumb guard over upper thumb (cols 6..10, rows 3..7; stops above inner thumb tip!)
    _rect(on, 6, 3, 11, 8, smid)
    _hline(on, 3, 6, 11, shi_); on[3][6] = srim
    _vline(on, 6, 3, 8, shi_); _vline(on, 10, 3, 8, ssh)
    _hline(on, 6, 6, 11, kbar_hi); _hline(on, 7, 6, 11, ink)
    on[4][7] = ahi
    # col 11 stops cleanly at row 2 to match west col 0!

    # 3. South (pinky / ulnar guard, 12 x 9: col 0 = west .. col 11 = east; matches east col 0 & west col 11!)
    os_ = _grid(W, H, '.')
    _slate_band(os_, 0, 0, W, 3)                   # continuous wrist cuff (rows 0..2)
    _hline(os_, 2, 0, W, ink)
    # Outer ulnar hand & knuckle guard wrapping from east (cols 6..11, rows 3..8; cols 0..5 open over inner palm!)
    _rect(os_, 6, 3, W, 9, smid)
    _vline(os_, W - 1, 0, 9, ssh)
    _vline(os_, 6, 3, 9, ink)
    _hline(os_, 6, 6, W, kbar_mid); _hline(os_, 7, 6, W, kbar_sh); _hline(os_, 8, 6, W, ink)

    # 4. West (inner wrist cuff ONLY rows 0..2; palm rows 3..8 stay open '.' exposing the inner mechanical palm!)
    ow = _grid(D, H, '.')
    _slate_band(ow, 0, 0, D, 3)
    _hline(ow, 2, 0, D, ink)

    # 5. Up (12 x 12 wrist collar ring sealing cleanly around the 5x5 forearm)
    oup = _grid(W, D, '.')
    _hline(oup, 0, 0, W, srim); _hline(oup, D - 1, 0, W, ssh)
    _vline(oup, 0, 0, D, ssh); _vline(oup, W - 1, 0, D, srim)
    oup[0][0] = oup[D - 1][W - 1] = shi_

    # 6. Down = completely blank '.' (the inner 5x5 curled fingers & Variant-B underside show cleanly beneath!)
    outer = {
        'north': on, 'south': os_, 'east': oe, 'west': ow,
        'up': oup, 'down': _grid(W, D, '.'),
    }
    return in_hand, outer


def _r4_arm(st, gauntlet='default'):
    """Sleek flush open exo-arm (R3-C's winning silhouette) with recipe-grounded metals + copper collars."""
    frim, fhi, fmid, fsh, fdk = [_rgba(c) for c in st['fr']]
    jhi, jmid, jsh, jdk, ink = [_rgba(c) for c in st['jt']]
    ahi, amid, ash = [_rgba(c) for c in st['ac']]
    bold_cu = st['chest_trim'] == 'copper_bold'
    gauntlet_outer = None
    if gauntlet == 'plated':
        fist = _gauntlet_plated(st)
    elif gauntlet == 'cyber':
        fist = _gauntlet_cyber(st)
    elif gauntlet == 'layered':
        fist, gauntlet_outer = _gauntlet_2layer(st, heavy=False)
    elif gauntlet == 'power_fist':
        fist, gauntlet_outer = _gauntlet_2layer(st, heavy=True)
    else:
        fist = _r3_fist(st)

    def face(kind):
        if kind == 'west':
            g = _grid(10, 24, jdk)
            _rect(g, 0, 0, 10, 3, jsh)
            _rect(g, 0, 10, 10, 15, jsh)
            _rect(g, 2, 3, 8, 10, jmid)
            _rect(g, 2, 15, 8, 22, jmid)
            _rect(g, 0, 22, 10, 24, jsh)
            return g
        g = _grid(10, 24, '.')
        _hline(g, 0, 0, 10, frim); _hline(g, 1, 0, 10, fhi); _hline(g, 2, 0, 10, ink)
        _grad_rail(g, 0, 2, 23, 2, st, lit_left=(kind != 'south'), ao_rows=(2, 10, 15, 22), chip_rows=(6, 18))
        _grad_rail(g, 8, 2, 23, 2, st, lit_left=(kind == 'south'), ao_rows=(2, 10, 15, 22), chip_rows=(7,))
        # Dark oil-iron rotary elbow joint (rows 10..15) with burnished copper collar
        _hline(g, 10, 0, 10, ink)
        _rect(g, 0, 11, 10, 15, jsh)
        _hline(g, 11, 1, 9, jhi)
        _hline(g, 12, 1, 9, jmid)
        _hline(g, 13, 1, 9, jdk)
        _hline(g, 14, 0, 10, ink)
        if kind == 'east':
            _rotary_hub(g, 3, 11, st)
        else:
            _hline(g, 12, 2, 8, amid); _hline(g, 12, 3, 6, ahi); _hline(g, 13, 2, 8, ash)
        if gauntlet in ('plated', 'cyber'):
            # Sleek forged-iron gauntlet wrist vambrace cuff wrapping rows 21..23 cleanly into the gauntlet!
            _plate_band(g, 0, 21, 10, 24, st, rim_top=True, roll_bot=False)
            if kind == 'east':
                g[22][4] = ahi; g[22][5] = amid
        elif bold_cu:
            # Extra burnished copper wrist trim band on cast_iron_copper
            _hline(g, 22, 1, 9, amid); g[22][2] = g[22][3] = ahi; _hline(g, 23, 0, 10, ink)
        else:
            _hline(g, 22, 0, 10, jhi); _hline(g, 23, 0, 10, ink)
        return g

    cage = {f: face(f) for f in ('north', 'east', 'south', 'west')}
    up = _grid(10, 10, '.')
    _hline(up, 0, 0, 10, fhi); _hline(up, 9, 0, 10, fsh); _vline(up, 9, 0, 10, frim)
    up[0][0] = up[9][0] = 'T'
    arm_hand = {f: cage[f] + fist[f] for f in ('north', 'east', 'south', 'west')}
    arm_hand['up'] = up; arm_hand['down'] = fist['down']
    arm_sock = {f: cage[f][:18] for f in ('north', 'east', 'south', 'west')}
    arm_sock['up'] = up; arm_sock['down'] = _r3_socket_down(st)
    return arm_hand, arm_sock, gauntlet_outer


def _r4_leg(st):
    """Sleek flush open exo-leg (R3-C's winning silhouette) with recipe-grounded metals + copper collars."""
    jhi, jmid, jsh, jdk, ink = [_rgba(c) for c in st['jt']]
    ahi, amid, ash = [_rgba(c) for c in st['ac']]
    bold_cu = st['chest_trim'] == 'copper_bold'
    boot = _r3_boot(st)

    def face(kind):
        if kind == 'west':
            g = _grid(10, 23, jdk)
            _rect(g, 0, 0, 10, 3, jsh)
            _rect(g, 0, 10, 10, 15, jsh)
            _rect(g, 2, 3, 8, 10, jmid)
            _rect(g, 2, 15, 8, 22, jmid)
            return g
        g = _grid(10, 23, '.')
        _hline(g, 0, 0, 10, jhi); _hline(g, 1, 0, 10, jmid); _hline(g, 2, 0, 10, ink)
        _grad_rail(g, 0, 2, 22, 2, st, lit_left=(kind != 'south'), ao_rows=(2, 10, 15, 21), chip_rows=(6, 18))
        _grad_rail(g, 8, 2, 22, 2, st, lit_left=(kind == 'south'), ao_rows=(2, 10, 15, 21), chip_rows=(17,))
        # Dark oil-iron knee joint (rows 10..15) + sculpted knee plate on north + rotary hub on east
        _hline(g, 10, 0, 10, ink)
        _rect(g, 0, 11, 10, 15, jsh)
        _hline(g, 14, 0, 10, ink)
        if kind == 'north':
            _plate_band(g, 2, 10, 8, 15, st, rim_top=True, roll_bot=True)
            if bold_cu:
                _hline(g, 12, 3, 7, amid); g[12][3] = g[12][4] = ahi
            else:
                g[12][4] = ahi; g[12][5] = amid
        elif kind == 'east':
            _rotary_hub(g, 3, 11, st)
        else:
            _hline(g, 11, 2, 8, jhi)
            _hline(g, 12, 2, 8, amid); _hline(g, 13, 2, 8, ash)
        if bold_cu:
            _hline(g, 22, 1, 9, amid); g[22][2] = g[22][3] = ahi
        else:
            _hline(g, 22, 0, 10, jhi)
        return g

    cage = {f: face(f) for f in ('north', 'east', 'south', 'west')}
    leg_in = {f: cage[f] + boot[f] for f in ('north', 'east', 'south', 'west')}
    leg_in['up'] = _grid(10, 10, '.'); leg_in['down'] = boot['down']
    return leg_in


def build(style, chest_x):
    assert style in R4_STYLES, (style, tuple(R4_STYLES))
    st = R4_STYLES[style]
    gauntlet = os.environ.get('GAUNTLET', 'power_fist')
    assert gauntlet in ('default', 'plated', 'layered', 'power_fist', 'cyber'), gauntlet
    chest_out, abd_out, chest_in, abd_in, belt = _r4_torso(st, chest_x)
    arm_hand, arm_sock, gauntlet_outer = _r4_arm(st, gauntlet=gauntlet)
    leg_in = _r4_leg(st)
    shoulder = _r3_shoulder_cap(st)
    return dict(
        layered_limbs=False,
        chest_shell=chest_out,
        abdomen_shell=abd_out,
        chest_inner=chest_in,
        abdomen_inner=abd_in,
        belt_shell=belt,
        arm_shell=arm_hand,
        arm_socket_shell=arm_sock,
        arm_outer=None,
        gauntlet_outer=gauntlet_outer,
        gauntlet_inner=arm_hand if gauntlet in ('layered', 'power_fist') else None,
        shoulder_plate=shoulder,
        leg_shell=leg_in,
        leg_outer=None,
    )
