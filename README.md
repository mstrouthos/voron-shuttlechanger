# Voron Shuttlechanger

A hotend-only toolchanger for the Voron Trident, inspired by MedusaHC.

**The extruder stays on the head; only the hotends change.** Each tool is a hotend, a 4010 fan and a small printed tool top. The tool hangs on two hardened pins and is held by magnets.

The extruder is a stock Clockwork 2 (CW2) with an LDO-36 motor, on a CNC Tap V2. **Nothing on the head is powered to open the idler: the dock does it.**
- Guidler A (the idler arm) has a mast that ends in a ramped **cam** above the head.
- A **pull rod** with a long spring holds the idler closed and sets the filament tension. The tension is set by turning one nut.
- Each dock has a short **Ø5 steel shaft** that points back towards the head. As the head moves in, the shaft pushes the cam aside, which swings the idler open so the filament can leave the drive gears. When the head leaves, the spring closes it again.

![Head and tool](images/head_front.png)

> **Status: prototype (v32.3).** The design passes automated collision, tool-change, printability, fit-clearance, wall-thickness and load-case checks. It has **not been printed or tested on a printer yet.** Expect changes.

**Building one? Start with the [illustrated assembly guide](docs/ASSEMBLY_GUIDE.md)**: exploded views, the full hardware list and every step, from the CW2 bearings to the docks. The whole head is built on the bench and then bolted to the Tap in one piece.

![Exploded view of the head](images/assembly/exploded_head.png)

## Interactive 3D viewer
`docs/index.html` is a self-contained three.js viewer of the head, tool and dock. It shows all the hardware and has:
- a tool-change animation
- an opener-only slider (the idler pushed open, as the dock does it)
- see-through and section-cut views
- an expandable bill of materials (click a row to isolate the part)

Open the file in a browser, or turn on GitHub Pages for the `docs/` folder.

| Closed: the spring on the pull rod holds the idler on the filament | At the dock: the shaft holds the cam back, the idler is open 11.4° |
|---|---|
| ![closed](images/opener_closed.png) | ![open](images/opener_open.png) |

## How it works
- **Tool mount:** the head carries 2 Ø3×30 dowels and 4 Ø6×2.65 magnets. Each tool top has matching bores and 2 magnets.
- **Filament path:** the filament runs through a printed Ø3.0 bore in the tool top and a tilting guide lever, up to the drive gears.
- **Dock:** the tool slides 9 mm along X onto 2 Ø3 steel pins on the dock, which hold it while the head backs away in Y. The same shift tilts the guide lever so the filament clears the gears. Docks sit on a 2020 rail at a 63 mm pitch.
- **Opener:** no servo, crank or wiring. It works on the motion the tool change already makes.
  - **Pull rod:** an M3×60 runs from the mast on Guidler A, through a fixed anchor on the motor plate, to a spring and a tension nut. It sits in the gap between the CW2 body and the plate.
  - **Cam:** the mast carries on above the head as a cam: a hold face at the back and a 40° ramp in front of it. It reaches 13 mm in front of the CW2 body.
  - **Shaft:** a Ø5 × 60 mm steel shaft is clamped in a printed post on the top slot of the dock rail. Its rounded tip is 40 mm behind the rail, 4 mm above the CW2 body. It stops short of the motor plate.
  - **Opening:** from 27 mm out, the shaft tip rides up the ramp as the head comes in. The 9 mm shift onto the dock pins does the rest: the cam ends up 13 mm back and the idler 11.4° open, before the dock tilts the guide lever.
  - **Closing:** the side of the shaft holds the idler open for the first 11 mm as the head backs out, then the ramp lets the spring close it.
  - **Force:** the shaft pushes with about 11 N at the start and 21 N fully open. The rod force goes from 13.6 N closed to 26 N.
  - **Size:** the cam stands 11 mm above the motor plate (z 143). On the left the mast is 3 mm outside the CW2 body when closed and about 15 mm when open at the dock.
- **Hotends:** Trianglelab TZ-V6 3.0 or Phaetus Dragon HF, each with its own 4010 fan shroud.

![Dock](images/dock.png)

## Repository layout
| Path | Contents |
|---|---|
| `stl/` | Print-ready STLs for every printed part, including the one stock CW2 part (02b), already in print orientation, no supports needed |
| `step/` | STEP (AP214) versions of every part, converted from the meshes: faceted solids, good for measuring and remixing |
| `BOM.csv` | Full bill of materials (per head and per tool) |
| `docs/ASSEMBLY_GUIDE.md` | Complete illustrated assembly: exploded views, full hardware list (stock CW2 included), every insert, bearing, gear, motor and screw, the opener, the dock shafts and the set-up |
| `docs/ASSEMBLY.md` | Assembly notes, tool-change sequence, audit notes |
| `docs/index.html` | Interactive 3D viewer |
| `audit/` | Printability (per-face and layer-by-layer), fit-clearance, wall-thickness, screw-path and load-case reports |

## Printed parts
| # | Part | Qty |
|---|---|---|
| 01 | CW2 main body (stock + front filament slot + front holes for the frame-post screws) | 1 |
| 02 | Guidler A + mast (stock + mast and cam for the pull rod and the dock shaft) | 1 |
| 02b | Guidler B (stock CW2, unmodified) | 1 |
| 05 | Motor plate (stock + spring anchor for the pull rod) | 1 |
| 07 | Receiver (pins + magnets) | 1 |
| 08 | Receiver frame | 1 |
| 09 | Duct + fan mount | 1 |
| 10 / 10b | Tool top / filament guide lever | 1 per tool |
| 11 / 12 | 4010 shroud for TZ-V6 / Dragon HF | 1 per tool |
| 13 | Dock | 1 per tool |
| 14 | Dock shaft post | 1 per tool |

Parts 03, 04 and 06 (trunnion, servo crank, servo bracket) no longer exist.

**Material:** ASA, PETG or PC-CF. Use PC-CF for Guidler A, the receiver and the tool top if you can.

**Settings:** 0.2 mm layers, 4 walls, 40 % infill, no supports.

**Key hardware:**
- hardened dowels: Ø3×30, Ø3×12, Ø3×15 (all Ø3)
- M3×60 SHCS, 1 M3 nyloc, 3 M3 washers and a **0.7 × 6 × 40 mm compression spring** (about 1.2 N/mm) for the pull rod. The short BMG thumbscrew spring can't be used: it goes solid before the idler is open
- Ø6×2.65 magnets
- 10× M3×5×4 heat-set inserts (Ø5 × 4 mm), all in Ø4.7 holes
- stock CW2 drivetrain: Bondtech BMG gear kit, 2× MR85 bearings, LDO-36 motor
- one Ø5 × 60 mm steel shaft per dock
- M3 and M5 screws (exact sizes and counts are in `BOM.csv` and the assembly guide)

## Klipper
The opener needs no config, no pin and no macro. The tool-change moves do the work:

- **Drop:** Y safe at X−9 → Y dock → X dock (slow) → Y safe.
- **Pickup:** Y safe at X dock → Y dock (slow) → X−9 (slow) → Y safe.

Y safe must be at least 35 mm behind the dock position, so the cam is clear of every shaft when the head moves along the docks. Setting the shaft and the tension is in the [assembly guide](docs/ASSEMBLY_GUIDE.md#5-set-up-and-test).

## Credits
- [Voron Design](https://github.com/VoronDesign): Clockwork 2 extruder and Stealthburner parts (GPL-3.0). Parts 01, 02 and 05 are modified Voron parts; 02b is the stock CW2 Guidler B from the Stealthburner release.
- MedusaHC, for the hotend-only toolchanger idea.
- Voron Tap / CNC Tap V2, which the head mounts to.

## License
GPL-3.0, the same license as the Voron parts this project modifies. See `LICENSE`.
