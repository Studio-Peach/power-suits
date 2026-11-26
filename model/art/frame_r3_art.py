"""Round 3 (2026-11-23): Open-skeleton exosuit frame directions — zero leather, rich hue-shifted shading, real variety.

Directly built on user feedback after R1/R2:
- Keep the OPEN EXOSKELETON silhouette (R2-C was the favourite shape: Steve's torso, arms & legs show cleanly inside,
  not buried inside chunky closed robot armour).
- Fix flat coloring: 5-step hue-shifted material ramps, directional top-to-bottom light falloff, ambient occlusion near
  every joint, strong material contrast between load-bearing frame vs dark oil-iron joints vs metallic actuator hubs,
  and subtle deliberate machined edge wear (zero ruler-straight flat stripes, zero random grain noise).
- Apply the 2D-texture + 0.5 px cutout outer-layer design system to an OPEN skeleton (A, B, D): dark oil-iron joints sit
  on the inner 5x5 limb box (with wide open windows to Steve!), while sculpted outer exo-rails, shoulder caps, and
  knee/elbow guards float 0.5 px proud over the joints and Steve. C tests the sleekest flush silhouette with rich
  blued-steel + chrome + copper shading.

Styles (env FRAME_LOOK in frame_model.py):
  fallout_bone   R3-A: Weathered warm bone-titanium open 2-layer exo-frame + oil-black iron joints + machined brass hubs
  loader_ochre   R3-B: Industrial safety-ochre open 2-layer power-loader rig + dark cast-iron joints + chrome pistons
  forged_cobalt  R3-C: Sleek flush blued-gunmetal open skeleton + brushed-chrome collars + burnished copper joint rings
  olive_mil      R3-D: Military olive-drab open 2-layer exo-frame + charcoal iron joints + steel spine & red lock pins
"""

R3_STYLES = {
    'fallout_bone': dict(
        layered_limbs=True,
        # Warm weathered bone-titanium / Fallout T-45 raw metal (hue shifts warm ivory -> khaki-taupe -> dark umber-iron)
        fr=((0xee, 0xe7, 0xd7), (0xd0, 0xc7, 0xb4), (0xa8, 0x9f, 0x8d), (0x7c, 0x73, 0x64), (0x4c, 0x46, 0x3d)),
        # Deep oil-rubbed charcoal cast-iron joints, boots, fists & spine core
        jt=((0x52, 0x58, 0x60), (0x39, 0x3e, 0x44), (0x26, 0x2a, 0x2f), (0x19, 0x1c, 0x20), (0x11, 0x13, 0x16)),
        # Machined warm brass hydraulic hubs, pistons & rivets
        ac=((0xe8, 0xcc, 0x82), (0xbe, 0x9b, 0x4d), (0x7c, 0x61, 0x2c)),
        # Brushed raw-steel spine vertebrae (ties frame to engine bay cleanly)
        sp=((0xd8, 0xd4, 0xc8), (0xa6, 0xa2, 0x97), (0x6e, 0x6a, 0x62)),
        # Subtle worn-metal chip colour on corners
        chip=(0x5e, 0x58, 0x4e),
    ),
    'loader_ochre': dict(
        layered_limbs=True,
        # Heavy industrial caterpillar safety ochre (bright warm sun-gold -> rich mustard -> deep burnt umber)
        fr=((0xf7, 0xd8, 0x74), (0xe2, 0xad, 0x3c), (0xbd, 0x84, 0x22), (0x8c, 0x5c, 0x16), (0x54, 0x36, 0x0d)),
        # Dark heavy cast-iron joints, boots & fists
        jt=((0x54, 0x5b, 0x63), (0x3a, 0x40, 0x47), (0x26, 0x2a, 0x2f), (0x18, 0x1b, 0x1f), (0x10, 0x12, 0x15)),
        # Gleaming brushed chrome pistons & hydraulic rams
        ac=((0xf2, 0xf5, 0xf8), (0xb4, 0xbd, 0xc7), (0x66, 0x6f, 0x7a)),
        # Industrial dark-steel + chrome spine
        sp=((0xc4, 0xcc, 0xd4), (0x86, 0x8f, 0x99), (0x4e, 0x55, 0x5e)),
        # Chipped bare-steel edge wear on yellow paint!
        chip=(0x6f, 0x76, 0x80),
    ),
    'forged_cobalt': dict(
        layered_limbs=False,
        # Rich blued-steel / aerospace gunmetal (cool sky-steel highlight -> rich slate-blue -> deep navy iron)
        fr=((0xa8, 0xbc, 0xd4), (0x7a, 0x90, 0xa8), (0x53, 0x67, 0x7e), (0x36, 0x46, 0x59), (0x20, 0x2a, 0x37)),
        # Deep matte graphite joints, boots & fists
        jt=((0x4b, 0x52, 0x5c), (0x34, 0x3a, 0x42), (0x23, 0x27, 0x2d), (0x16, 0x19, 0x1d), (0x0f, 0x11, 0x14)),
        # Burnished copper hydraulic collars & joint actuators
        ac=((0xf2, 0xb4, 0x7e), (0xc8, 0x78, 0x42), (0x80, 0x44, 0x22)),
        # Brushed silver-steel spine & hydraulic rods
        sp=((0xe4, 0xe8, 0xee), (0xa4, 0xae, 0xba), (0x64, 0x6e, 0x7a)),
        chip=(0x8b, 0x9c, 0xb0),
    ),
    'olive_mil': dict(
        layered_limbs=True,
        # Weathered military olive-drab (matches Flamethrower's approved military palette!)
        fr=((0xb2, 0xbe, 0x88), (0x8b, 0x99, 0x64), (0x65, 0x72, 0x46), (0x46, 0x50, 0x30), (0x2a, 0x31, 0x1c)),
        # Charcoal forged-iron joints, boots & fists
        jt=((0x58, 0x60, 0x68), (0x3e, 0x44, 0x4c), (0x29, 0x2d, 0x33), (0x1a, 0x1d, 0x21), (0x11, 0x13, 0x16)),
        # Crisp military orange-red hydraulic lock pins / safety tabs
        ac=((0xe8, 0x6d, 0x42), (0xb8, 0x42, 0x22), (0x6e, 0x23, 0x12)),
        # Brushed steel spine & engine socket hardware
        sp=((0xd2, 0xd6, 0xda), (0x98, 0x9f, 0xa8), (0x5d, 0x64, 0x6d)),
        chip=(0x76, 0x7d, 0x84),
    ),
}

CONTACT = (0x2c, 0xe3, 0xd9)


def _rgba(rgb):
    return rgb + (255,)


def _grid(w, h, fill='.'):
    return [[fill] * w for _ in range(h)]


def _rect(g, x0, y0, x1, y1, val):
    h, w = len(g), len(g[0])
    for y in range(max(0, y0), min(h, y1)):
        for x in range(max(0, x0), min(w, x1)):
            g[y][x] = val


def _hline(g, y, x0, x1, val):
    _rect(g, x0, y, x1, y + 1, val)


def _vline(g, x, y0, y1, val):
    _rect(g, x, y0, x + 1, y1, val)


def _grad_rail(g, x0, y0, y1, w, st, lit_left=True, ao_rows=(), chip_rows=()):
    """Paint a richly shaded vertical structural rail with top-to-bottom light falloff, rounded cross-section,
    joint AO darkening, and subtle corner edge chips (never a flat monotone stripe!)."""
    rim, hi, mid, sh, dk = [_rgba(c) for c in st['fr']]
    chip = _rgba(st['chip'])
    span = max(1, y1 - y0 - 1)
    for y in range(y0, y1):
        t = (y - y0) / span  # 0 at top -> 1 at bottom
        in_ao = y in ao_rows
        # Choose cross-section tones based on vertical height + AO proximity
        if in_ao:
            c_lit, c_body, c_sh = sh, dk, _rgba(st['jt'][3])
        elif t < 0.28:
            c_lit, c_body, c_sh = rim, hi, mid
        elif t < 0.72:
            c_lit, c_body, c_sh = hi, mid, sh
        else:
            c_lit, c_body, c_sh = mid, sh, dk

        if w == 3:
            cols = (c_lit, c_body, c_sh) if lit_left else (c_sh, c_body, c_lit)
        elif w == 2:
            cols = (c_lit, c_sh) if lit_left else (c_sh, c_lit)
        else:
            cols = (c_body,)
        for i, col in enumerate(cols):
            g[y][x0 + i] = col
        if y in chip_rows and not in_ao:
            cx = x0 if lit_left else (x0 + w - 1)
            g[y][cx] = chip


def _plate_band(g, x0, y0, x1, y1, st, rim_top=True, roll_bot=True, chips=()):
    """Paint a directional beveled plate band in the frame's hue-shifted metallic ramp (like Iron Armour's plates)."""
    rim, hi, mid, sh, dk = [_rgba(c) for c in st['fr']]
    ink = _rgba(st['jt'][4])
    chip = _rgba(st['chip'])
    h = y1 - y0
    for dy in range(h):
        y = y0 + dy
        for x in range(x0, x1):
            if dy == 0 and rim_top:
                c = rim if x < x1 - 1 else hi
            elif dy == 1 and h >= 4:
                c = hi if x == x0 else mid if x < x1 - 1 else sh
            elif dy == h - 1 and roll_bot:
                c = ink
            elif dy == h - 2 and roll_bot and h >= 3:
                c = sh if x < x1 - 1 else dk
            else:
                c = hi if x == x0 else sh if x == x1 - 1 else mid
            g[y][x] = c
    for cx, cy in chips:
        if x0 <= cx < x1 and y0 <= cy < y1:
            g[cy][cx] = chip


def _rotary_hub(g, cx, cy, st):
    """Paint a 4x4 sculpted dark-iron rotary joint drum with metallic accent center axle at (cx..cx+4, cy..cy+4)."""
    jhi, jmid, jsh, jdk, ink = [_rgba(c) for c in st['jt']]
    ahi, amid, ash = [_rgba(c) for c in st['ac']]
    _rect(g, cx, cy, cx + 4, cy + 4, ink)
    # Beveled circular outer iron housing
    g[cy][cx + 1] = g[cy][cx + 2] = jhi
    g[cy + 1][cx] = g[cy + 2][cx] = jhi
    g[cy + 1][cx + 3] = g[cy + 2][cx + 3] = jsh
    g[cy + 3][cx + 1] = g[cy + 3][cx + 2] = jdk
    # 2x2 machined metallic accent pivot pin in center!
    g[cy + 1][cx + 1] = ahi
    g[cy + 1][cx + 2] = amid
    g[cy + 2][cx + 1] = amid
    g[cy + 2][cx + 2] = ash


# ---------------------------------------------------------------- 2x dark oil-iron fist, boot & socket
def _r3_fist(st):
    """Heavy dark forged-iron mechanical gauntlet with subtle frame-coloured knuckle guard."""
    jhi, jmid, jsh, jdk, ink = [_rgba(c) for c in st['jt']]
    frim, fhi, fmid, fsh, fdk = [_rgba(c) for c in st['fr']]
    ahi, amid, _ = [_rgba(c) for c in st['ac']]

    def side(knuckles=False, thumb=False):
        g = _grid(10, 8, jsh)
        # Wrist joint collar
        _hline(g, 0, 0, 10, ink)
        _hline(g, 1, 0, 10, jmid)
        _hline(g, 1, 2, 8, jhi)
        # Back-of-hand sculpted iron block (rows 2..4) + subtle frame-painted knuckle plate
        _rect(g, 0, 2, 10, 5, jmid)
        _hline(g, 2, 0, 10, jhi)
        _vline(g, 0, 2, 5, jhi)
        _vline(g, 9, 2, 5, jdk)
        _hline(g, 4, 0, 10, jdk)
        if knuckles:
            # Frame-coloured beveled knuckle guard bar across rows 2..3 (ties fist to frame!)
            _rect(g, 2, 2, 8, 4, fmid)
            _hline(g, 2, 2, 8, fhi)
            g[2][2] = frim
            _hline(g, 3, 2, 8, fsh)
            g[2][4] = g[2][5] = ahi  # tiny machined accent center rivet
        # Articulated dark iron fingers (rows 5..7)
        _hline(g, 5, 0, 10, ink)
        _rect(g, 0, 6, 10, 8, jsh)
        _hline(g, 6, 1, 9, jmid)
        _hline(g, 7, 0, 10, jdk)
        if knuckles:
            _vline(g, 3, 6, 8, ink)
            _vline(g, 6, 6, 8, ink)
        if thumb:
            _rect(g, 5, 3, 9, 6, jhi)
            _rect(g, 6, 4, 8, 6, jmid)
            _vline(g, 4, 3, 6, ink)
        return g

    down = _grid(10, 10, jdk)
    _rect(down, 1, 1, 9, 9, jsh)
    _rect(down, 2, 2, 8, 8, jmid)
    _hline(down, 4, 1, 9, ink)
    _hline(down, 7, 1, 9, ink)
    return {'north': side(knuckles=True), 'east': side(), 'south': side(knuckles=True), 'west': side(thumb=True), 'down': down}


def _r3_boot(st):
    """Heavy dark forged-iron platform boot with frame-painted toe bumper & crisp sole tread."""
    jhi, jmid, jsh, jdk, ink = [_rgba(c) for c in st['jt']]
    frim, fhi, fmid, fsh, fdk = [_rgba(c) for c in st['fr']]
    ahi, amid, _ = [_rgba(c) for c in st['ac']]

    def side(toe=False, back=False):
        g = _grid(10, 8, jsh)
        _hline(g, 0, 0, 10, ink)
        _hline(g, 1, 0, 10, jmid)
        _rect(g, 0, 2, 10, 5, jmid)
        _hline(g, 2, 0, 10, jhi)
        _vline(g, 0, 2, 5, jhi)
        _vline(g, 9, 2, 5, jdk)
        _hline(g, 4, 0, 10, jdk)
        if toe:
            # Frame-coloured armored toe cap (ties boot cleanly to the exo-leg!)
            _rect(g, 2, 2, 8, 5, fmid)
            _hline(g, 2, 2, 8, fhi)
            g[2][2] = g[2][3] = frim
            _hline(g, 4, 2, 8, fsh)
            _vline(g, 1, 2, 5, ink)
            _vline(g, 8, 2, 5, ink)
        elif back:
            # Heel hydraulic stabilizer + accent pin
            _rect(g, 3, 1, 7, 5, jhi)
            _rect(g, 4, 2, 6, 4, amid)
            g[2][4] = ahi
            _vline(g, 2, 1, 5, ink)
            _vline(g, 7, 1, 5, ink)
        # Heavy notched platform sole (rows 5..7)
        _hline(g, 5, 0, 10, ink)
        _rect(g, 0, 6, 10, 8, jdk)
        _hline(g, 6, 1, 9, jsh)
        if back:
            _hline(g, 7, 0, 10, ink)
        elif toe:
            _hline(g, 7, 0, 10, ink)
            _rect(g, 2, 7, 8, 8, jmid)
        else:
            for x in (0, 1, 4, 5, 8, 9):
                g[7][x] = ink
            for x in (2, 3, 6, 7):
                g[7][x] = jmid
        return g

    down = _grid(10, 10, ink)
    for y in (2, 3, 6, 7):
        _hline(down, y, 1, 9, jsh)
    _rect(down, 2, 9, 8, 10, jmid)
    return {'north': side(toe=True), 'south': side(back=True), 'east': side(), 'west': side(), 'down': down}


def _r3_socket_down(st):
    jhi, jmid, jsh, jdk, ink = [_rgba(c) for c in st['jt']]
    ahi = _rgba(st['ac'][0])
    g = _grid(10, 10, jsh)
    _rect(g, 1, 1, 9, 9, jmid)
    _rect(g, 2, 2, 8, 8, jdk)
    _rect(g, 3, 3, 7, 7, ink)
    _rect(g, 4, 4, 6, 6, _rgba(CONTACT))
    for x, y in ((1, 1), (8, 1), (1, 8), (8, 8)):
        g[y][x] = ahi
    return g


# ---------------------------------------------------------------- OPEN 2-layer torso (wide open flanks around Steve!)
def _r3_torso(st, chest_x):
    """Open sculpted exoskeleton torso:
    - Outer shell (z +-3.0): richly shaded collarbone yoke, tapered side struts, machined engine bay bezel, sculpted 3D spine,
      wide open windows showing Steve's torso cleanly!
    - Inner core (z +-2.5, 0.5 px recessed): ONLY behind the engine mounting bay & spine column (flanks stay '.' OPEN!),
      giving real 0.5 px architectural depth to the engine socket & spine without hiding the pilot!
    """
    frim, fhi, fmid, fsh, fdk = [_rgba(c) for c in st['fr']]
    jhi, jmid, jsh, jdk, ink = [_rgba(c) for c in st['jt']]
    ahi, amid, ash = [_rgba(c) for c in st['ac']]
    shi, smid, ssh = [_rgba(c) for c in st['sp']]
    chip = _rgba(st['chip'])

    cw = round(chest_x * 4)   # 24 wide, 22 slim
    aw = 20
    D = 12
    edge_c = (cw - 16) // 2   # 4 wide, 3 slim
    mid_c = cw // 2

    # ---- CHEST OUTER (cw x 12 x 12) ----
    cf = _grid(cw, 12, '.')
    # Sculpted collarbone yoke across top (rows 0..2) with rich directional bevel
    _plate_band(cf, 0, 0, cw, 3, st, rim_top=True, roll_bot=True, chips=((2, 1), (cw - 3, 1)))
    # Tapered load-bearing side pillars (outside Steve's torso) with top-to-bottom light falloff!
    pw_top, pw_bot = edge_c + 1, edge_c
    for side_left in (True, False):
        x_base = 0 if side_left else (cw - pw_top)
        _grad_rail(cf, 0 if side_left else (cw - pw_bot), 2, 11, pw_bot, st,
                   lit_left=side_left, ao_rows=(2, 10), chip_rows=(5,))
        # Extra 1-texel shoulder gusset at rows 2..4
        gx = pw_bot if side_left else (cw - pw_top)
        cf[2][gx] = fhi if side_left else fsh
        cf[3][gx] = fmid if side_left else fdk
        cf[4][gx] = ink
        # Accent shoulder lock pin on upper chest pillar
        px = 1 if side_left else (cw - 2)
        cf[1][px] = ahi
        cf[2][px] = ash
    # Bottom sternum bar (beveled, slightly darker than upper yoke for vertical light falloff!)
    _hline(cf, 10, 0, cw, fmid)
    _hline(cf, 10, 1, cw - 1, fhi)
    _hline(cf, 11, 0, cw, fdk)
    cf[11][0] = cf[11][cw - 1] = ink
    # Central dark-iron engine mounting bay bezel (cols mid_c-4 .. mid_c+4, rows 2..9) — 6x6 open window into recessed socket!
    bx0, bx1 = mid_c - 4, mid_c + 4
    _hline(cf, 2, bx0, bx1, jhi)
    _hline(cf, 9, bx0, bx1, jdk)
    _vline(cf, bx0, 2, 10, jhi)
    _vline(cf, bx1 - 1, 2, 10, jsh)
    # Angled frame collar struts locking the bezel to the yoke (breaks boxy grid!)
    cf[2][bx0 - 1] = fhi; cf[2][bx1] = fsh
    cf[3][bx0 - 1] = fsh; cf[3][bx1] = fdk
    cf[9][bx0 - 1] = fsh; cf[9][bx1] = fdk
    # Corner mounting lugs on bezel
    for lx, ly in ((bx0 + 1, 3), (bx1 - 2, 3), (bx0 + 1, 8), (bx1 - 2, 8)):
        cf[ly][lx] = amid
    cf[3][bx0 + 1] = cf[3][bx1 - 2] = ahi

    # Back: sculpted open exo-frame + rich 3D articulated mechanical spine (hero 3rd-person back view!)
    cb = _grid(cw, 12, '.')
    _plate_band(cb, 0, 0, cw, 3, st, rim_top=True, roll_bot=True, chips=((3, 1), (cw - 4, 1)))
    for side_left in (True, False):
        _grad_rail(cb, 0 if side_left else (cw - pw_bot), 2, 11, pw_bot, st,
                   lit_left=side_left, ao_rows=(2, 10), chip_rows=(6,))
        gx = pw_bot if side_left else (cw - pw_top)
        cb[2][gx] = fhi if side_left else fsh
        cb[3][gx] = fmid if side_left else fdk
        cb[4][gx] = ink
        px = 1 if side_left else (cw - 2)
        cb[1][px] = ahi
        cb[2][px] = ash
    _hline(cb, 10, 0, cw, fmid)
    _hline(cb, 11, 0, cw, fdk)
    # 3D-sculpted dorsal spine (6 texels wide: alternating brushed-steel vertebrae + dark oil-iron flex joints + accent pistons!)
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
            cb[y][mid_c - 1] = amid
            cb[y][mid_c] = ash
    # Clean open shoulder-blade cutouts flank the spine -> Steve's back/shirt shows cleanly!

    # Chest sides (12 x 12, closed because arms touch here — dark iron housing + subtle vertical accent piston)
    cs = _grid(D, 12, jsh)
    _plate_band(cs, 0, 0, D, 3, st, rim_top=True, roll_bot=True)
    _rect(cs, 2, 3, D - 2, 10, jdk)
    _rect(cs, 4, 3, D - 4, 10, jmid)
    _vline(cs, 5, 4, 9, ahi)
    _vline(cs, 6, 4, 9, amid)
    _hline(cs, 10, 0, D, jmid)
    _hline(cs, 11, 0, D, ink)

    # Chest up (beveled shoulder platforms outside Steve + crisp collar rims)
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

    # ---- ABDOMEN OUTER (20 x 10 x 12) ----
    # Clean open flanks + tapered side rails + central dark-iron & steel abdominal piston column!
    def _abd_face(is_back):
        g = _grid(aw, 10, '.')
        _hline(g, 0, 0, aw, ink)  # crisp AO shadow under chest!
        # Left & right tapered load rails (2 texels wide, rich vertical falloff!)
        _grad_rail(g, 0, 1, 9, 2, st, lit_left=True, ao_rows=(1, 8), chip_rows=(4,))
        _grad_rail(g, aw - 2, 1, 9, 2, st, lit_left=False, ao_rows=(1, 8), chip_rows=(5,))
        # Central 6-texel articulated mechanical spine / abdominal hydraulic strut
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
                g[y][9] = ahi if y == 3 else amid
                g[y][10] = ash
        # Dark oil-iron waist ring (rows 8..9) — frames the lower torso cleanly without a bright horizontal stripe!
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

    # ---- CHEST INNER CORE (0.5 px recessed: z +-2.5) — OPEN FLANKS, ONLY ENGINE BAY & SPINE BACKING! ----
    icw = cw - 2
    imid = icw // 2
    bx0_i, bx1_i = imid - 4, imid + 4
    ci_f = _grid(icw, 12, '.')
    # Machined dark-iron engine mounting socket inside the central 8x8 bay (looks mechanical bare, hides under engines!)
    _rect(ci_f, bx0_i, 2, bx1_i, 10, ink)
    _rect(ci_f, bx0_i + 1, 3, bx1_i - 1, 9, jsh)
    _hline(ci_f, 3, bx0_i + 2, bx1_i - 2, jhi)
    _rect(ci_f, bx0_i + 2, 4, bx1_i - 2, 8, ink)
    # Central machined contact ring in accent metal
    ci_f[5][imid - 1] = ahi; ci_f[5][imid] = amid
    ci_f[6][imid - 1] = amid; ci_f[6][imid] = ash

    ci_b = _grid(icw, 12, '.')
    # Dark oil-iron backing ONLY behind the spine column (flanks stay wide open to Steve!)
    _rect(ci_b, imid - 3, 2, imid + 3, 11, ink)
    _rect(ci_b, imid - 2, 3, imid + 2, 10, jdk)

    chest_inner = {'north': ci_f, 'south': ci_b,
                   'east': _grid(10, 12, '.'), 'west': _grid(10, 12, '.'),
                   'up': _grid(icw, 10, '.'), 'down': _grid(icw, 10, '.')}

    # ---- ABDOMEN INNER CORE (0.5 px recessed: z +-2.5) — OPEN FLANKS, ONLY SPINE BACKING! ----
    iaw = aw - 2
    def _abd_in():
        g = _grid(iaw, 10, '.')
        _rect(g, 6, 0, 12, 9, ink)
        _rect(g, 7, 1, 11, 8, jdk)
        return g
    abdomen_inner = {'north': _abd_in(), 'south': _abd_in(),
                     'east': _grid(10, 10, '.'), 'west': _grid(10, 10, '.'),
                     'up': _grid(iaw, 10, '.'), 'down': _grid(iaw, 10, '.')}

    # ---- BELT (20 x 2 x 12) — dark oil-iron pelvic ring with frame-painted center clasp ----
    bf = _grid(aw, 2, jsh)
    _hline(bf, 0, 0, aw, jdk)
    _hline(bf, 1, 0, aw, jmid)
    _rect(bf, 7, 0, 13, 2, fmid)
    _hline(bf, 0, 8, 12, fhi)
    _hline(bf, 1, 8, 12, fsh)
    bb = _grid(aw, 2, jsh)
    _hline(bb, 0, 0, aw, jdk)
    _rect(bb, 7, 0, 13, 2, jmid)
    bs = _grid(D, 2, jsh)
    _hline(bs, 0, 0, D, jdk)
    bup = _grid(aw, D, '.')
    _hline(bup, 0, 0, aw, jmid); _hline(bup, D - 1, 0, aw, jsh)
    _vline(bup, 0, 0, D, jhi); _vline(bup, aw - 1, 0, D, jsh)
    bdn = [r[:] for r in bup]
    for j in range(1, D - 1):
        bdn[j][0] = bdn[j][-1] = 'T'

    belt = {'north': bf, 'south': bb, 'east': bs, 'west': bs, 'up': bup, 'down': bdn}
    return chest_outer, abdomen_outer, chest_inner, abdomen_inner, belt


def _r3_shoulder_cap(st):
    """Richly shaded curved shoulder cap for flush style C (forged_cobalt, 11 x 7 x 12, DECAL=0.5)."""
    frim, fhi, fmid, fsh, fdk = [_rgba(c) for c in st['fr']]
    jhi, jmid, jsh, jdk, ink = [_rgba(c) for c in st['jt']]
    ahi, amid, _ = [_rgba(c) for c in st['ac']]
    chip = _rgba(st['chip'])
    W, D, H = 11, 12, 7

    up = _grid(W, D, fmid)
    _hline(up, 0, 0, W, frim); _hline(up, 1, 0, W, fhi)
    _hline(up, D - 1, 0, W, fsh)
    _vline(up, 0, 1, D - 1, fsh); _vline(up, W - 1, 1, D - 1, frim)
    # Recessed dark mounting rail with metallic accent bar
    _rect(up, 4, 1, 7, D - 1, ink)
    _vline(up, 5, 2, D - 2, amid)
    up[2][5] = ahi
    for x, y in ((2, 2), (W - 3, 2), (2, D - 3), (W - 3, D - 3)):
        up[y][x] = jdk

    def band(depths, bolts=()):
        g = _grid(len(depths), H, '.')
        for i, d in enumerate(depths):
            for j in range(d):
                g[j][i] = frim if j == 0 else fhi if j == 1 else ink if j == d - 1 else fsh if j == d - 2 else fmid
        for i in bolts:
            g[2][i] = ahi
        if len(depths) > 4:
            g[1][len(depths) // 2] = chip
        return g

    side = [3 + round(3 * i / (W - 1)) for i in range(W)]
    return {
        'north': band(side[::-1], bolts=(1,)),
        'south': band(side, bolts=(W - 2,)),
        'east': band([6] * D, bolts=(2, D - 3)),
        'west': _grid(D, H, '.'),
        'up': up,
        'down': _grid(W, D, '.'),
    }


# ---------------------------------------------------------------- arms (OPEN 2-layer skeleton OR sleek flush skeleton)
def _r3_arm(st):
    """Open sculpted exo-arm:
    - Layered (A, B, D): inner 5x5 arm is WIDE OPEN on upper arm & forearm (Steve clearly visible!), holding ONLY dark
      oil-iron rotary elbow joint, wrist collar, inner chest-facing wall, and heavy fist; outer 0.5 px cutout layer
      carries ONLY the richly shaded curved shoulder cap, slim 3-texel outer structural rail, and floating elbow bumper!
    - Flush (C): sleek 2x open cage with blued-steel graduated rails + dark-iron rotary elbow & copper collar rings.
    """
    frim, fhi, fmid, fsh, fdk = [_rgba(c) for c in st['fr']]
    jhi, jmid, jsh, jdk, ink = [_rgba(c) for c in st['jt']]
    ahi, amid, ash = [_rgba(c) for c in st['ac']]
    chip = _rgba(st['chip'])
    fist = _r3_fist(st)

    if not st['layered_limbs']:
        # ---- SLEEK FLUSH OPEN SKELETON (R3-C: forged_cobalt) ----
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
            # Beveled upper shoulder ring
            _hline(g, 0, 0, 10, frim); _hline(g, 1, 0, 10, fhi); _hline(g, 2, 0, 10, ink)
            # Graduated blued-steel vertical load rails (2 texels each, rich top-to-bottom light falloff + joint AO!)
            _grad_rail(g, 0, 2, 23, 2, st, lit_left=(kind != 'south'), ao_rows=(2, 10, 15, 22), chip_rows=(6, 18))
            _grad_rail(g, 8, 2, 23, 2, st, lit_left=(kind == 'south'), ao_rows=(2, 10, 15, 22), chip_rows=(7,))
            # Dark oil-iron rotary elbow joint drum (rows 10..15) with burnished copper collar!
            _hline(g, 10, 0, 10, ink)
            _rect(g, 0, 11, 10, 15, jsh)
            _hline(g, 11, 1, 9, jhi)
            _hline(g, 12, 1, 9, jmid)
            _hline(g, 13, 1, 9, jdk)
            _hline(g, 14, 0, 10, ink)
            if kind == 'east':
                _rotary_hub(g, 3, 11, st)
            else:
                # Burnished copper hydraulic collar band peeking cleanly across the dark elbow!
                _hline(g, 12, 2, 8, amid)
                _hline(g, 12, 3, 6, ahi)
                _hline(g, 13, 2, 8, ash)
            # Dark iron wrist collar above fist
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
        return arm_hand, arm_sock, None

    # ---- OPEN 2-LAYER EXOSKELETON ARM (R3-A fallout_bone, R3-B loader_ochre, R3-D olive_mil) ----
    # Inner 5x5 box: WIDE OPEN on BOTH upper arm (rows 3..9) AND forearm (rows 16..21) so Steve is clearly visible!
    # Only carries the recessed dark oil-iron elbow rotary joint, slim dark inner stabilization bars & wrist cuff!
    def inner_face(kind):
        if kind == 'west':
            g = _grid(10, 24, jdk)
            _rect(g, 0, 0, 10, 3, jsh)
            _rect(g, 0, 10, 10, 15, jsh)
            _rect(g, 2, 3, 8, 10, jmid)
            _rect(g, 2, 15, 8, 22, jmid)
            _rect(g, 0, 22, 10, 24, jsh)
            return g
        g = _grid(10, 24, '.')
        # Top shoulder mounting ring (tucked under outer shoulder cap)
        _hline(g, 0, 0, 10, jmid); _hline(g, 1, 0, 10, jdk); _hline(g, 2, 0, 10, ink)
        # Thin 1-texel dark inner structural trim along edges (frames Steve cleanly without blocking him!)
        _vline(g, 0, 2, 24, jsh); _vline(g, 9, 2, 24, jdk)
        # Recessed dark oil-iron rotary elbow actuator (rows 10..15) — sits 0.5 px deeper than the outer elbow bumper!
        _hline(g, 10, 0, 10, ink)
        _rect(g, 0, 11, 10, 15, jsh)
        _hline(g, 11, 1, 9, jhi)
        _hline(g, 12, 1, 9, jmid)
        _hline(g, 13, 1, 9, jdk)
        _hline(g, 14, 0, 10, ink)
        if kind == 'east':
            _rotary_hub(g, 3, 11, st)
        else:
            # Subtle machined accent piston bar across recessed elbow joint
            _hline(g, 12, 3, 7, amid)
            g[12][3] = ahi
            _hline(g, 13, 3, 7, ash)
        # Forearm lower frame: slim graduated rails framing a wide 6x6 open window to Steve's forearm!
        _grad_rail(g, 0, 15, 22, 2, st, lit_left=(kind != 'south'), ao_rows=(15, 21), chip_rows=(18,))
        _grad_rail(g, 8, 15, 22, 2, st, lit_left=(kind == 'south'), ao_rows=(15, 21))
        _hline(g, 22, 0, 10, jhi); _hline(g, 23, 0, 10, ink)
        return g

    cage = {f: inner_face(f) for f in ('north', 'east', 'south', 'west')}
    up = _grid(10, 10, '.')
    _hline(up, 0, 0, 10, jmid); _hline(up, 9, 0, 10, jsh); _vline(up, 9, 0, 10, jhi)
    up[0][0] = up[9][0] = 'T'
    arm_hand = {f: cage[f] + fist[f] for f in ('north', 'east', 'south', 'west')}
    arm_hand['up'] = up; arm_hand['down'] = fist['down']
    arm_sock = {f: cage[f][:18] for f in ('north', 'east', 'south', 'west')}
    arm_sock['up'] = up; arm_sock['down'] = _r3_socket_down(st)

    # Outer 0.5 px floating exoskeleton layer (W=11, H=19 [raw y 26.5..17.0], D=12) — SLEEK & OPEN!
    # Curved shoulder yoke + slim 3-texel outer structural spine rail + floating cutout elbow guard (WIDE OPEN windows!)
    W, H, D = 11, 19, 12
    oup = _grid(W, D, fmid)
    _hline(oup, 0, 0, W, frim); _hline(oup, 1, 0, W, fhi)
    _hline(oup, D - 1, 0, W, fsh)
    _vline(oup, 0, 1, D - 1, fsh); _vline(oup, W - 1, 1, D - 1, frim)
    _rect(oup, 4, 2, 7, D - 2, ink)
    _vline(oup, 5, 2, D - 2, amid)
    oup[2][5] = ahi

    def outer_ns(outer_left):
        g = _grid(W, H, '.')
        # Sleek curved shoulder cap (5 deep at outer corner sweeping cleanly up to 3 near chest)
        for i in range(W):
            d_out = i if outer_left else (W - 1 - i)
            depth = 5 if d_out < 3 else 4 if d_out < 7 else 3
            for j in range(depth):
                g[j][i] = frim if j == 0 else fhi if j == 1 else ink if j == depth - 1 else fsh if j == depth - 2 else fmid
        g[2][1 if outer_left else W - 2] = ahi
        # Slim 3-texel outer structural exo-strut descending to elbow (leaves inner 8 texels WIDE OPEN to Steve!)
        ox0 = 0 if outer_left else (W - 3)
        _grad_rail(g, ox0, 4, 17, 3, st, lit_left=outer_left, ao_rows=(4, 11, 16), chip_rows=(8,))
        # Floating elbow bumper cuff (rows 11..16, outer 8 texels, with clean cutout window showing dark elbow actuator!)
        ex0, ex1 = (0, 9) if outer_left else (2, W)
        _plate_band(g, ex0, 11, ex1, 17, st, rim_top=True, roll_bot=True)
        # Cutout slot showing recessed dark rotary joint & metallic accent!
        wx0 = 3 if outer_left else 4
        _rect(g, wx0, 13, wx0 + 4, 15, '.')
        g[13][wx0 - 1] = g[14][wx0 - 1] = ink
        g[13][wx0 + 4] = g[14][wx0 + 4] = ink
        return g

    oe = _grid(D, H, '.')
    # Shoulder cap across east (rows 0..4, matches outer depth=5!)
    for j in range(5):
        c = frim if j == 0 else fhi if j == 1 else ink if j == 4 else fsh if j == 3 else fmid
        _hline(oe, j, 0, D, c)
    oe[2][2] = oe[2][D - 3] = ahi
    # Twin slim 2-texel exo-rails (rows 4..16) framing a WIDE 8x7 open window straight onto Steve's arm!
    _grad_rail(oe, 0, 4, 17, 2, st, lit_left=False, ao_rows=(4, 11, 16), chip_rows=(7,))
    _grad_rail(oe, D - 2, 4, 17, 2, st, lit_left=True, ao_rows=(4, 11, 16), chip_rows=(8,))
    # Floating elbow bumper (rows 11..16, matches outer_ns!) with 6x2 cutout exposing the 4x4 rotary hub!
    _plate_band(oe, 0, 11, D, 17, st, rim_top=True, roll_bot=True)
    _rect(oe, 3, 13, 9, 15, '.')
    oe[13][2] = oe[14][2] = ink
    oe[13][9] = oe[14][9] = ink

    arm_outer = {
        'north': outer_ns(True), 'south': outer_ns(False), 'east': oe,
        'west': _grid(D, H, '.'), 'up': oup, 'down': _grid(W, D, '.'),
    }
    return arm_hand, arm_sock, arm_outer


# ---------------------------------------------------------------- legs (OPEN 2-layer skeleton OR sleek flush skeleton)
def _r3_leg(st):
    """Open sculpted exo-leg:
    - Layered (A, B, D): inner 5x5 leg is WIDE OPEN on thigh (rows 3..9) AND shin (rows 16..21) so Steve's legs show
      cleanly! Inner layer holds dark oil-iron rotary knee joint, hip/ankle cuffs & heavy platform boot; outer 0.5 px
      cutout layer floats a sculpted outer exo-strut, hip bumper, floating knee guard & ankle brace!
    - Flush (C): sleek 2x open cage with blued-steel graduated rails + dark-iron rotary knee & copper collar.
    """
    frim, fhi, fmid, fsh, fdk = [_rgba(c) for c in st['fr']]
    jhi, jmid, jsh, jdk, ink = [_rgba(c) for c in st['jt']]
    ahi, amid, ash = [_rgba(c) for c in st['ac']]
    boot = _r3_boot(st)

    if not st['layered_limbs']:
        # ---- SLEEK FLUSH OPEN SKELETON (R3-C: forged_cobalt) ----
        def face(kind):
            if kind == 'west':
                g = _grid(10, 23, jdk)
                _rect(g, 0, 0, 10, 3, jsh)
                _rect(g, 0, 10, 10, 15, jsh)
                _rect(g, 2, 3, 8, 10, jmid)
                _rect(g, 2, 15, 8, 22, jmid)
                return g
            g = _grid(10, 23, '.')
            # Dark iron hip collar
            _hline(g, 0, 0, 10, jhi); _hline(g, 1, 0, 10, jmid); _hline(g, 2, 0, 10, ink)
            # Richly graduated blued-steel vertical struts (2 texels each, wide open thigh & shin windows!)
            _grad_rail(g, 0, 2, 22, 2, st, lit_left=(kind != 'south'), ao_rows=(2, 10, 15, 21), chip_rows=(6, 18))
            _grad_rail(g, 8, 2, 22, 2, st, lit_left=(kind == 'south'), ao_rows=(2, 10, 15, 21), chip_rows=(17,))
            # Dark oil-iron knee joint (rows 10..15) + sculpted frame knee cap on north + rotary hub on east!
            _hline(g, 10, 0, 10, ink)
            _rect(g, 0, 11, 10, 15, jsh)
            _hline(g, 14, 0, 10, ink)
            if kind == 'north':
                _plate_band(g, 2, 10, 8, 15, st, rim_top=True, roll_bot=True)
                g[12][4] = ahi; g[12][5] = amid
            elif kind == 'east':
                _rotary_hub(g, 3, 11, st)
            else:
                _hline(g, 11, 2, 8, jhi)
                _hline(g, 12, 2, 8, amid)
                _hline(g, 13, 2, 8, ash)
            _hline(g, 22, 0, 10, jhi)
            return g

        cage = {f: face(f) for f in ('north', 'east', 'south', 'west')}
        leg_in = {f: cage[f] + boot[f] for f in ('north', 'east', 'south', 'west')}
        leg_in['up'] = _grid(10, 10, '.'); leg_in['down'] = boot['down']
        return leg_in, None

    # ---- OPEN 2-LAYER EXOSKELETON LEG (R3-A/B/D) ----
    # Inner 5x5 leg: WIDE OPEN on BOTH thigh (rows 3..9) AND shin (rows 16..21) — zero boxy armor panels hiding Steve!
    def inner_face(kind):
        if kind == 'west':
            g = _grid(10, 23, jdk)
            _rect(g, 0, 0, 10, 3, jsh)
            _rect(g, 0, 10, 10, 15, jsh)
            _rect(g, 2, 3, 8, 10, jmid)
            _rect(g, 2, 15, 8, 22, jmid)
            return g
        g = _grid(10, 23, '.')
        # Dark oil-iron hip band
        _hline(g, 0, 0, 10, jhi); _hline(g, 1, 0, 10, jmid); _hline(g, 2, 0, 10, ink)
        # Thin 1-texel dark inner structural frame edge
        _vline(g, 0, 2, 23, jsh); _vline(g, 9, 2, 23, jdk)
        # Recessed dark oil-iron knee rotary joint (rows 10..15)
        _hline(g, 10, 0, 10, ink)
        _rect(g, 0, 11, 10, 15, jsh)
        _hline(g, 11, 1, 9, jhi)
        _hline(g, 12, 1, 9, jmid)
        _hline(g, 13, 1, 9, jdk)
        _hline(g, 14, 0, 10, ink)
        if kind == 'east':
            _rotary_hub(g, 3, 11, st)
        else:
            _hline(g, 12, 3, 7, amid)
            g[12][3] = ahi
            _hline(g, 13, 3, 7, ash)
        # Ankle dark iron collar
        _hline(g, 21, 0, 10, jmid); _hline(g, 22, 0, 10, jhi)
        return g

    cage = {f: inner_face(f) for f in ('north', 'east', 'south', 'west')}
    leg_in = {f: cage[f] + boot[f] for f in ('north', 'east', 'south', 'west')}
    leg_in['up'] = _grid(10, 10, '.'); leg_in['down'] = boot['down']

    # Outer 0.5 px floating exoskeleton leg (W=11, H=23, D=12) — SLEEK & WIDE OPEN around Steve!
    W, H, D = 11, 23, 12
    def outer_ns(outer_left):
        g = _grid(W, H, '.')
        ox0 = 0 if outer_left else (W - 3)
        # Tapered hip yoke cap (outer 7 texels, rows 0..3)
        for i in range(W):
            d_out = i if outer_left else (W - 1 - i)
            depth = 4 if d_out < 3 else 3 if d_out < 6 else 2 if d_out < 8 else 0
            for j in range(depth):
                g[j][i] = frim if j == 0 else fhi if j == 1 else ink if j == depth - 1 else fmid
        g[1][1 if outer_left else W - 2] = ahi
        # Slim 3-texel outer structural exo-leg rail (rows 2..22) — inner 8 texels WIDE OPEN to Steve's jeans!
        _grad_rail(g, ox0, 2, 23, 3, st, lit_left=outer_left, ao_rows=(3, 10, 15, 20), chip_rows=(7, 18))
        # Floating sculpted knee guard (rows 10..15) with crisp cutout window over the dark rotary joint!
        kx0, kx1 = (0, 9) if outer_left else (2, W)
        _plate_band(g, kx0, 10, kx1, 16, st, rim_top=True, roll_bot=True)
        wx0 = 3 if outer_left else 4
        _rect(g, wx0, 12, wx0 + 4, 14, '.')
        g[12][wx0 - 1] = g[13][wx0 - 1] = ink
        g[12][wx0 + 4] = g[13][wx0 + 4] = ink
        # Sleek ankle brace (rows 20..22)
        _plate_band(g, kx0, 20, kx1, 23, st, rim_top=True, roll_bot=True)
        g[21][1 if outer_left else W - 2] = ahi
        return g

    oe = _grid(D, H, '.')
    # Hip cap (rows 0..3, matches outer depth=4!)
    for j in range(4):
        c = frim if j == 0 else fhi if j == 1 else ink if j == 3 else fmid
        _hline(oe, j, 0, D, c)
    oe[1][2] = oe[1][D - 3] = ahi
    # Twin slim 2-texel outer vertical exo-rails (rows 3..22) framing WIDE 8-wide open thigh & shin windows!
    _grad_rail(oe, 0, 3, 23, 2, st, lit_left=False, ao_rows=(3, 10, 15, 20), chip_rows=(6, 17))
    _grad_rail(oe, D - 2, 3, 23, 2, st, lit_left=True, ao_rows=(3, 10, 15, 20), chip_rows=(7, 18))
    # Floating knee guard (rows 10..15, matches outer_ns!) with 6x2 window over rotary knee hub
    _plate_band(oe, 0, 10, D, 16, st, rim_top=True, roll_bot=True)
    _rect(oe, 3, 12, 9, 14, '.')
    oe[12][2] = oe[13][2] = ink
    oe[12][9] = oe[13][9] = ink
    # Ankle brace (rows 20..22)
    _plate_band(oe, 0, 20, D, 23, st, rim_top=True, roll_bot=True)
    oe[21][2] = oe[21][D - 3] = ahi

    leg_outer = {
        'north': outer_ns(True), 'south': outer_ns(False), 'east': oe,
        'west': _grid(D, H, '.'), 'up': _grid(W, D, '.'), 'down': _grid(W, D, '.'),
    }
    return leg_in, leg_outer


def build(style, chest_x):
    assert style in R3_STYLES, (style, tuple(R3_STYLES))
    st = R3_STYLES[style]
    chest_out, abd_out, chest_in, abd_in, belt = _r3_torso(st, chest_x)
    arm_hand, arm_sock, arm_out = _r3_arm(st)
    leg_in, leg_out = _r3_leg(st)
    shoulder = None if st['layered_limbs'] else _r3_shoulder_cap(st)
    return dict(
        layered_limbs=st['layered_limbs'],
        chest_shell=chest_out,
        abdomen_shell=abd_out,
        chest_inner=chest_in,
        abdomen_inner=abd_in,
        belt_shell=belt,
        arm_shell=arm_hand,
        arm_socket_shell=arm_sock,
        arm_outer=arm_out,
        shoulder_plate=shoulder,
        leg_shell=leg_in,
        leg_outer=leg_out,
    )
