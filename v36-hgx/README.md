# v36 draft: CxChanger mechanism on a CNC Tap V2, HGX gears

**Draft. Checked on the model only; nothing here has been printed.**

The extruder, coupling and dock of [CxChanger](https://github.com/cx330-TXY/CxChanger) (GPL-3.0), adapted to a
ChaoticLab CNC Tap V2. The swing arm is on the left, as the idler arm on a CW2, and the EBB SB2209 USB stands on
the right side in its CW2 orientation. Each dock is one part with a nozzle wiper built in.

- [ASSEMBLY.md](ASSEMBLY.md): build steps.
- [BOM.csv](BOM.csv): every part, per head and per tool.
- `stl/`: eight printed parts, already in print orientation. The duct (09) and shrouds (11, 12) are the v32 files in the repo's `stl/`.
- `audit/`: layer-by-layer print check, thin-wall scan, load cases.
- `scripts/`: the model (`build35.py` builds it, `build36.py` mirrors it), checks and viewer builder.
  Run `python extract_old.py` in this folder first: it writes `old_parts.pkl` (v32 meshes the scripts reuse) from branch `redesign-v31`. Needs numpy, trimesh, manifold3d, shapely.
- `docs/index.html` on this branch is the v36 viewer.

The README, BOM and guides in the repo root still describe v32.4. This folder replaces the first HGX draft on branch `v33-hgx`.

## Checks

- Every part prints without islands, bridges over 10 mm or lips over 3 mm.
- No collisions with the tool on the head, through the arm swing, or through a release and pickup with neighbours 54 mm away.
- Load cases within 20 MPa along the layers and 8 MPa across. With a 40 N grip the push on the dock pin runs from about 22 N to 29 N.
- Left thin on purpose: 0.8 to 1.0 mm floors behind the top magnets and groove in the coupling plate; 45 degree chamfer edges.

## Not verified

HGX and dual-gear dimensions (from the CxChanger CAD), Tap bottom-hole thread depth, magnet holding force,
clearance of the SB2209 to the belts and to the printer's right side. No STEP files and no illustrations yet.
