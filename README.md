# Voron Shuttlechanger

A hotend-only toolchanger for the Voron Trident on a CNC Tap V2.

**The extruder stays on the head; only the hotends change.** Each tool is a hotend, a 4010 fan and a printed tool body that carries the filament up between the extruder gears. The tool sits on three ball pins and is held by magnets. Nothing on the head is powered to release it: the dock does it.

The mechanism is [CxChanger](https://github.com/cx330-TXY/CxChanger)'s (GPL-3.0), repackaged for the Tap:
- **Extruder:** two HGX hobbed gears, one fixed and one on a swing arm, driven by the CW2 motor through a 17/44 dual gear.
- **Swing arm:** a spring holds it on the filament. A steel pin on each dock pushes its foot as the head shifts 3 mm sideways, which opens the gears.
- **Coupling:** three ball pins on the tool sit in three V grooves on the head, with six pairs of magnets.
- **Dock:** one printed part per tool. It hangs the tool on two screws, carries the opener pin, and has a floor with a silicone strip that wipes and plugs the nozzle.

![Head and tool](images/head_front.png)

> **Status: draft (v36).** Checked on the model only: collisions through a full tool change, layer-by-layer printability, wall thickness and load cases. **Nothing has been printed or tested on a printer yet.** Expect changes.

**Building one? Start with the [assembly guide](docs/ASSEMBLY_GUIDE.md).** Background, the tool-change moves and the check results are in the [design notes](docs/ASSEMBLY.md).

| Extruder with the gear housing removed | Right side: the EBB SB2209 USB, as on a CW2 |
|---|---|
| ![Extruder](images/extruder.png) | ![Right side](images/head_right.png) |

## Interactive 3D viewer
`docs/index.html` is a self-contained three.js viewer of the head, tools and docks. It shows all the hardware and has:
- a tool-change animation
- a swing-arm slider
- see-through and section-cut views
- an expandable bill of materials (click a row to isolate the part)

Open the file in a browser, or turn on GitHub Pages for the `docs/` folder.

## How it works
- **Filament path:** the tool body has a lower and an upper filament guide joined by a beam on its front. Between them, 21 mm of filament is free, and that is where the two gears grip it.
- **Tool change:** the head moves in until the tool's two hook screws pass through the large holes in the dock. A 3 mm shift to the right slides the hooks into slots and pushes the swing arm open. The head then backs straight out: the magnets let go and the gears slide off the filament.
- **Opening force:** with a 40 N grip the dock pin is pushed with about 22 N at the start and 29 N fully open. The idler opens 1.5 mm.
- **Spring:** the stock CW2 idler spring, on an M3 adjuster at the top of the head.
- **Wiper:** the nozzle slides 3 mm across the silicone strip at every change and rests on it while parked.
- **Part cooling:** the v32 duct and fan mount, unchanged, hung from two ears on the back plate.
- **Electronics:** the EBB SB2209 USB stands on the right side of the head, long edge front to back, the same way up as on a CW2.
- **Hotends:** Trianglelab TZ-V6 3.0 or Phaetus Dragon HF, each with its own 4010 fan shroud.

| A tool | Docks, seen from behind |
|---|---|
| ![Tool](images/tool.png) | ![Docks](images/dock.png) |

## Repository layout
| Path | Contents |
|---|---|
| `stl/` | Print-ready STLs, already in print orientation, no supports needed |
| `step/` | STEP versions of the three parts carried over from v32 (09, 11, 12). The v36 parts have no STEP files yet |
| `BOM.csv` | Full bill of materials (per head and per tool) |
| `docs/ASSEMBLY_GUIDE.md` | Build steps, from the printed parts to the first tool change |
| `docs/ASSEMBLY.md` | Design notes: layout, tool-change moves, check results, version history |
| `docs/index.html` | Interactive 3D viewer |
| `audit/` | Layer-by-layer printability, wall-thickness and load-case reports |
| `model/` | The scripts that build the model, run the checks, export the STLs and write the viewer |

## Printed parts
![Printed parts as they lie on the bed](images/printed_parts.png)

| # | Part | Qty |
|---|---|---|
| 01 | Back plate body (bolts to the Tap) | 1 |
| 02 | Back plate front slab (motor, dual gear, pivot, spring adjuster) | 1 |
| 03 | Coupling plate (top groove and magnets; covers the dual gear) | 1 |
| 04 | Gear housing | 1 |
| 05 | Swing arm | 1 |
| 06 | SB2209 spacer | 2 |
| 09 | Duct + fan mount (from v32) | 1 |
| 10 | Tool body | 1 per tool |
| 11 / 12 | 4010 shroud for TZ-V6 / Dragon HF (from v32) | 1 per tool |
| 13 | Dock with wiper | 1 per tool |

**Material:** ABS or ASA. **Settings:** 0.2 mm layers, 4 walls, 40 % infill or more, no supports.

**Key hardware:**
- HGX Lite gear kit: two hobbed 36-tooth gears and the 17/44 dual gear, module 0.5 (the kit as CxChanger buys it holds all three)
- 2 MR63 bearings (HGX Lite kits come with bearings; check their size), dowel pins Ø3 × 16 (2) and Ø3 × 24 (1)
- the CW2's LDO-36 motor with its 10-tooth pinion, and its idler spring
- 6 dowel pins Ø1.5 × 5, and 3 round-head pins Ø3 × 6 per tool
- Ø6 × 2.65 magnets: 6 on the head, 7 per tool
- per dock: a Ø5 × 30 steel pin and a strip of self-adhesive silicone
- M3, M2.5 and M5 screws (exact sizes and counts are in `BOM.csv`)

## Klipper
The tool change needs no pin and no servo, only moves. Dock pitch is 54 mm.

- **Release:** 30 mm behind the dock → in → 3 mm right (slow) → out 30 mm → 3 mm left.
- **Pickup:** 30 mm behind the dock → 3 mm right → in (slow) → 3 mm left (slow) → out.

Do not move sideways while less than 30 mm out with a tool parked: the cooling duct would catch a Dragon heater block. CxChanger's macros are a good starting point; reverse the sign of its side shift.

## Not verified
- HGX and dual-gear dimensions come from the CxChanger CAD, not from parts in hand.
- Thread depth of the Tap's two bottom holes.
- Holding force of the magnets against nozzle drag.
- Clearance of the SB2209 to the belts and to the printer's right side.
- The docks must sit in front of the bed: their floor is 6 mm below the nozzle tip.

## Credits
- [CxChanger](https://github.com/cx330-TXY/CxChanger) by cx330-TXY: the extruder, coupling and dock concept, and the gear layout (GPL-3.0).
- [Voron Design](https://github.com/VoronDesign): the Trident, Tap and the Clockwork 2 motor and spring this reuses.
- BigTreeTech: the EBB SB2209 USB board model used to place the board.
- MedusaHC, for the hotend-only toolchanger idea.

## License
GPL-3.0. See `LICENSE`.
