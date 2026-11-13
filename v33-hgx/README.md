# v33 draft: CxChanger mechanism on a CNC Tap V2, HGX gears

**Draft. Checked on the model only. Nothing here has been print-checked or printed.**

This branch holds the first v33 model: the extruder, coupling and dock of
[CxChanger](https://github.com/cx330-TXY/CxChanger) (GPL-3.0) adapted to a ChaoticLab CNC Tap V2.
`docs/index.html` on this branch is the v33 viewer. The README, BOM and assembly guide in the repo root still describe v32.4.

- Extruder: HGX gear set, 17/44 dual gear, LDO-36STH20 motor with 10T pinion, stock CW2 idler spring.
- Tool: one body for TZ-V6 3.0 and Dragon HF (v32 shrouds), three ball pins and magnets.
- Dock: 50 mm pitch, hook screws, Ø5 opener pin. Motion: in, shift 3 mm left, out 14 mm.
- Part cooling: the v32 duct and fan mount, unchanged.
- EBB SB2209 USB: landscape behind the motor on a printed bracket.

## Files

- `build33.py` builds the parts, `sweep33.py` runs the collision checks, `apply33.py` writes the viewer page.
- `extract_old.py` makes `old_parts.pkl` (v32 meshes the scripts reuse). Needs numpy, trimesh, manifold3d.
- `stl_draft/` holds the new parts in assembly position, not print orientation.

## Not done

Print checks (overhangs, walls, loads), print orientation, STEP export, assembly instructions.
Unverified: Tap bottom-hole thread depth, HGX and dual-gear sizes (taken from the CxChanger CAD), magnet holding force.
