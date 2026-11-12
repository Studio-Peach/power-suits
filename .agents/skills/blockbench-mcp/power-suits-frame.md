# Power Suits: the frame and its engine (script-built, branch `experimental/frame-concept`)

The frame is the experimental successor to the big suit: an exosuit the player's own Steve / Alex stands in, built
entirely by script (SKILL.md §0). What it taught us, so the next round starts where this one stopped. The files below
live on `experimental/frame-concept`; the frame isn't in the game yet (model only).

## Files
- `model/art/frame_model.py` builds `model/power_frame.bbmodel` (Steve, `BUILD=wide`) and `power_frame_slim.bbmodel`
  (Alex, `BUILD=slim`); `FRAME_OUT=` writes one elsewhere. Its header and comments carry every decision with the date
  and the user's words. `frame_drafts.py` builds a draft round into one file (`/tmp/frame/draft.bbmodel`).
- Engine (`ENGINE=heart`, off by default so the saved files don't show it yet): `frame_heart_art.py` (the front: core
  and hoses as decals), `frame_motor_art.py` (the back: `BACK=blower`, picked; `vtwin`, `inline` drafts),
  `frame_engine_art.py` (porthole core art, the twin-cylinder pack `BACK=pistons` drawn at any size),
  `frame_radial_art.py` (the radial firebox, superseded; its `part()` / `grid()` / `disc()` helpers are shared).
  `FIRE=lit|dark` paints the fire burning (review) or in the reserved coal colours (the in-game texture).
- Checks: `check()` / `check_armor()` run on every build; `model/art/engine_sweep.py` sweeps the head, arm and leg
  against the `en_*` cubes (build with `HELMET=glass` so it has a helmet to swing).

## Coordinates
- The art scripts use **raw** coordinates; the model is lifted `FY = 2` (the 4 px soles). A sweep or a Blockbench
  readout shows built coordinates (raw + 2): the caps' tops are raw y 27.5, Blockbench 29.5.
- 1 px = 1/16 block, the model faces -z, right side +x, 2 texels per px.

## Envelopes (what any part on the torso must clear)
- **The helmet** (9 x 9 x 9, raw y 25.5 up, x / z +-4.5; head pivot raw 26, yaw +-50, pitch +-90): above raw 25.5
  nothing may sit in front of z 4.5 (it clips the helmet at rest); turned 50 deg its back corners sweep a circle of
  radius 6.36, so anything above 25.5 behind the head nearer than that is met when the head turns. The picked back
  parts stand there (supercharger, exhaust caps): the worn helmet's tilt / turn limit is an open decision for the
  renderer. A face in one of the helmet's planes (front z -4.5, back 4.5, sides x 4.5) facing the same way fails
  `check_armor` (a hose and its collar did, in the front plane); back to back is allowed.
- **The arms** start at the chest's sides (`CHEST_X`: 6 wide, 5.5 slim) and swing about x: nothing beyond the chest's
  width (decals included: the slim build's hoses ran into Alex's arms until the layout followed `CHEST_X`).
- **The legs** swing +-60 about the hip (raw y 14): parts low on the back meet them (the full-size pack at -60).
- **The gap under the arm** is 1 px (wide) or 0.5 px (slim) beside the abdomen (x 5): a strip there is a decal, a
  zero-thickness plane in the middle of the slim gap (both sides are planes the arm cage and abdomen use).

## Engine decisions (2026-11-11)
- The front is 2D: a porthole core painted into the chest slot, four copper hoses drawn flat (lit / mid / shade across
  them, a 1-texel ink outline, brass bands), carried over the shoulders, along the waist and down the back by decal
  strips into inlets painted as the hose (ink, three coppers, ink). The rotated 3D ball-and-hose draft is f688cc9.
- The back is a hot-rod blower: a 10 x 8 x 2.5 block flat on the back, the fire window in it (the part that lights:
  keep it uncovered), a ribbed supercharger over its whole top (its top at the helmet's bottom), the big suit's
  exhaust art and caps at the frame's density standing out of the block's back (smoke from the cap holes).
- Light: the core's fire and the fire window are painted in the reserved coal colours of `tools/make-glowmasks.py`
  (`FIRE=dark`), so the fire glowmask lights them by the burn state as on the suit; the smoke code (`ExhaustSmoke`)
  needs the frame's cap positions when the frame goes in game.

## Shoulders (2026-11-12)
- The shoulder plate is a decal too (`SHOULDER=decal`, picked over the 3D 6 x 1 x 6 plate and a bare lid): drawn on
  0.5 px off the arm's top, outer side, front and back, a steel band with an ink edge, 5 rows deep at the outer corner
  running out to 3 at the chest. Next to the 2D engine the 3D plate read as a ledge.

## Limbs (2026-11-12)
- The frame is the inner piece the pilot wears; armour goes on over it, so the limbs stay a cage: the brass bellows
  bands are gone (`BANDS=cage`; steel / gunmetal ribs read as armour). Leather in the torso's two shades wraps the outer
  corners (`LEATHER=wrap`): the front and back windows beside the outer side and both outer-side windows (its rod
  removed), his body showing between. One flat shade, or leather over every window, read flat and hid him.

## Iron armour (2026-11-12)
- Sealed stays: "sealed" is a game mechanic (a full set with the helmet makes the pilot immune to most outside
  debuffs), so the armour covers the whole frame; the frame shows only where a piece is missing.
- Flat, like the engine (`ARMOR_FORM=flat`): the pieces are the frame's boxes (the waist as deep as the chest, the
  step band painted on its top 2 px), the pauldron a decal 0.5 px off the arm piece (from its old inner edge, x 7 /
  6.5 slim, clear of the helmet's corners turned 50 deg; checked as one box: texel by texel the check ran minutes).
- The engine under it, tiered: the upper hoses hidden by the breastplate, the lower pair out from under its painted
  bottom edge over the waist; the core replaced by a radiator grille decal (`GUARD=hot`: three slats in the fire's
  reserved coal colours, hottest in the middle, dark slots), so it glows with the burn state.
- `ALLOW_CLASH=1` builds a model that fails the checks, for a survey before a refit (never for a saved file).
