"""AR Glasses for the frame (model/art/frame_model.py, GLASSES=shield|sleek; 2026-11-20).

Early-game head item: goes in the helmet slot, provides no armour, no seal, no machine mind, and takes no wear;
lets the pilot see the suit's floating HUD readouts and night vision (no steel helmet visor corners).
Reference: Meta VR Glasses (.scratch/glasses/ref.jpg) — continuous dark glossy wraparound shield lens with an
arched nose-bridge cutout, ultra-thin matte charcoal rim, tapered dark temple arms, and a tiny indicator LED
that lights up when the suit is powered (lenses stay dark sunglasses in third person).

Geometry: follows the exact 9 x 9 x 9 helmet box (-4.5, 25.5, -4.5) .. (4.5, 34.5, 4.5) at 2 texels per px
(18 x 18 faces, compact: only north, east, west painted; top/back/bottom blank), keeping the helmet's exact
0.5 px clearance off Steve's 8 x 8 x 8 head (zero z-fighting; PilotLayer hides the hat layer just like a helmet).

Round 2 options (env GLASSES):
  shield — 7-texel-tall (3.5 px) Meta VR wraparound shield + tapered temple arms with ear hook + indicator LED
  sleek  — 5-texel-tall (2.5 px) slimmer wraparound visor + slim temple arms + indicator LED

Reserved indicator LED colour (GLASSES_LED_DARK in textures; lit by glowmask power_frame_glow_glasses_led):
  'G' -> dark green-grey off-state in game texture (0x1b, 0x3b, 0x26), bright amber/green in reviews (GLASSES_LED=lit).
"""

# Reserved dark colour for the power indicator LED (lit by SuitGlowLayer in the visor colour when powered).
LED_DARK = (0x1b, 0x3b, 0x26, 255)
LED_LIT = (0xff, 0xc8, 0x48, 255)   # piloted amber for review sheets

FRAME = {
    '0': (0x14, 0x16, 0x19, 255),
    '1': (0x1f, 0x23, 0x28, 255),
    '2': (0x2d, 0x32, 0x38, 255),
    '3': (0x3f, 0x46, 0x4e, 255),
    '4': (0x56, 0x5f, 0x69, 255),
    'c': (0x3a, 0x4b, 0x5c, 255),   # tiny camera lens dot
}

N = 18


def _resolve(faces, led_lit=False):
    pal = dict(FRAME, G=LED_LIT if led_lit else LED_DARK)
    return {f: [[pal.get(c, c) for c in r] for r in rows] for f, rows in faces.items()}


# North face (cols 0..17 run +x -> -x; col 0 meets east's front col 17, col 17 meets west's front col 0).
# Rows 0..17 run top (y 34.5) -> bottom (y 25.5); Steve's eyes sit behind rows 9..10 (y 29..30).
# Note: 'W' = GLASS_SHADE (darker smoked lens), 'V' = GLASS (slightly clearer over eyes), 'T' = GLINT (glossy sheen),
# 'G' = tiny power indicator LED on the upper-left corner of the frame (col 1, row 7/8 — like Meta glasses' LED).

SHIELD_NORTH = (
    ['.' * N] * 6 + [
        '..33333333333333..',  # row 6  (y 31.0..31.5) sleek rounded matte brow rim
        '.2WWWWWWWWWWWWWW2.',  # row 7  (y 30.5..31.0) top of dark glossy visor
        '32WWTWWWWWWWWWWW23',  # row 8  (y 30.0..30.5) full-width shield + temple anchor
        '21WTWWWWWWWWWWWW12',  # row 9  (y 29.5..30.0) uniform dark smoked glass lens
        '11WWWWWW11WWWWWW11',  # row 10 (y 29.0..29.5) curved nose-bridge arch starts
        '.1WWWW1....1WWWW1.',  # row 11 (y 28.5..29.0) cheeks dip down round nose cutout
        '..1111......1111..',  # row 12 (y 28.0..28.5) slim matte bottom rim
    ] + ['.' * N] * 5
)

# East face (pilot's right temple, +x) runs back (z +4.5, col 0) -> front (z -4.5, col 17).
# Col 17 matches SHIELD_NORTH col 0 row-for-row: rows 8..10 = '3', '2', '1' (seamless corner wrap!).
SHIELD_EAST = (
    ['.' * N] * 8 + [
        '.......33333333233',  # row 8  (y 30.0..30.5) sleek top temple edge + hinge seam (col 15)
        '.....2222222212c22',  # row 9  (y 29.5..30.0) tapered matte arm + camera dot 'c' near front
        '.....111.......111',  # row 10 (y 29.0..29.5) subtle ear-tip hook at back + front temple flare
    ] + ['.' * N] * 7
)

# West face (pilot's left temple, -x) runs front (z -4.5, col 0) -> back (z +4.5, col 17).
# Carries the little power indicator LED ('G', col 2, row 9) on the side of the left arm instead of the front.
SHIELD_WEST = (
    ['.' * N] * 8 + [
        '33233333333.......',  # row 8  (y 30.0..30.5) sleek top temple edge + hinge seam (col 2)
        '22G2122222222.....',  # row 9  (y 29.5..30.0) tiny indicator LED 'G' on the left arm's side
        '111.......111.....',  # row 10 (y 29.0..29.5) front temple flare + subtle ear-tip hook at back
    ] + ['.' * N] * 7
)

SLEEK_NORTH = (
    ['.' * N] * 7 + [
        '.2333333333333332.',  # row 7  (y 30.5..31.0) slim matte brow rim
        '3GWWTWWWWWWWWWWW23',  # row 8  (y 30.0..30.5) dark glossy shield + power LED 'G'
        '21WTWWVWWWWWWVWW12',  # row 9  (y 29.5..30.0) eyes behind smoked lens
        '11WWWW11..11WWWW11',  # row 10 (y 29.0..29.5) tight arched nose cutout
        '.11111......11111.',  # row 11 (y 28.5..29.0) slim bottom rim
    ] + ['.' * N] * 6
)

# Col 17 matches SLEEK_NORTH col 0 row-for-row: rows 8..10 = '3', '2', '1'.
SLEEK_EAST = (
    ['.' * N] * 8 + [
        '......333333333233',  # row 8  (y 30.0..30.5) slim top edge + hinge seam
        '.....2222222221c22',  # row 9  (y 29.5..30.0) sleek straight arm + camera dot
        '.....1111111110111',  # row 10 (y 29.0..29.5) clean shaded underside
    ] + ['.' * N] * 7
)


def faces(style='shield', led_lit=False):
    blank = ['.' * N for _ in range(N)]
    if style == 'shield':
        north, east, west = SHIELD_NORTH, SHIELD_EAST, SHIELD_WEST
    elif style == 'sleek':
        north, east = SLEEK_NORTH, SLEEK_EAST
        west = [r[::-1] for r in east]
    else:
        raise ValueError(style)
    return _resolve({'north': north, 'south': blank, 'east': east, 'west': west, 'up': blank, 'down': blank}, led_lit=led_lit)


def build(style='shield', led_lit=False):
    """One 9 x 9 x 9 hollow box (same dimensions as the helmets, compact so blank faces take no texture space)."""
    return [{
        'name': 'glasses',
        'box': ((-4.5, 25.5, -4.5), (4.5, 34.5, 4.5)),
        'faces': faces(style, led_lit=led_lit),
        'hollow': True,
        'compact': True,
    }]
