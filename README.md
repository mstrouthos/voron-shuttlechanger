# Voron Shuttlechanger

A hotend-only toolchanger for the Voron Trident, inspired by MedusaHC.

**The extruder stays on the head; only the hotends change.** Each tool is a hotend, a 4010 fan and a small printed tool top. The tool hangs on two hardened pins and is held by magnets.

The extruder is a stock Clockwork 2 (CW2) with an LDO-36 motor, on a CNC Tap V2. A micro servo drives a sliding **spring shuttle** that does three things:
- sets the filament tension when the idler is closed
- takes the spring load off before opening
- pulls the idler open, so the filament can leave the drive gears during a tool change

The tension is set by turning one screw.

![Head and tool](images/head_front.png)

> **Status: prototype (v29).** The design passes automated collision, printability, wall-thickness and load-case checks. It has **not been printed or tested on a printer yet.** Expect changes.

## Interactive 3D viewer
`docs/index.html` is a self-contained three.js viewer of the head, tool and dock. It shows all the hardware and has:
- a tool-change animation
- an opener-only slider
- see-through and section-cut views
- an expandable bill of materials (click a row to isolate the part)

Open the file in a browser, or turn on GitHub Pages for the `docs/` folder.

| Opener closed (spring loaded) | Opener open (spring unloaded, idler pulled open) |
|---|---|
| ![closed](images/opener_closed.png) | ![open](images/opener_open.png) |

## How it works
- **Tool mount:** the head carries 2 Ø4×30 dowels and 4 Ø6×2.65 magnets. Each tool top has matching bores and 2 magnets.
- **Filament path:** the filament runs through a printed Ø3.0 bore in the tool top and a tilting guide lever, up to the drive gears.
- **Dock:** the tool slides 9 mm along X onto 2 Ø3 steel pins on the dock, which hold it while the head backs away in Y. The same shift tilts the guide lever so the filament clears the gears. Docks sit on a 2020 rail at a 63 mm pitch.
- **Opener:** the servo crank's pin runs in a groove in the shuttle. The groove has a dwell at each end. Opening, the shuttle first unloads the stock CW2 spring, then pulls Guidler A open by about 10–11°.
  - Closed tension comes from an M3×40 screw, nuts and the stock spring.
  - Travel is 102° of servo rotation.
- **Hotends:** Trianglelab TZ-V6 3.0 or Phaetus Dragon HF, each with its own 4010 fan shroud.

![Dock](images/dock.png)

## Repository layout
| Path | Contents |
|---|---|
| `stl/` | Print-ready STLs, already in print orientation, no supports needed |
| `step/` | STEP (AP214) versions of every part, converted from the meshes: faceted solids, good for measuring and remixing |
| `BOM.csv` | Full bill of materials (per head and per tool) |
| `docs/ASSEMBLY.md` | Assembly steps, Klipper servo config, tool-change sequence, audit notes |
| `docs/index.html` | Interactive 3D viewer |
| `audit/` | Printability, wall-thickness and load-case reports |

## Printed parts
| # | Part | Qty |
|---|---|---|
| 01 | CW2 main body (stock + front filament slot) | 1 |
| 02 | Guidler A (stock + Ø4.4 arm hole) | 1 |
| 03 | Opener spring shuttle | 1 |
| 04 | Opener servo crank | 1 |
| 05 | Motor plate with shuttle rail | 1 |
| 06 | Servo bracket | 1 |
| 07 | Receiver (pins + magnets) | 1 |
| 08 | Receiver frame | 1 |
| 09 | Duct + fan mount | 1 |
| 10 / 10b | Tool top / filament guide lever | 1 per tool |
| 11 / 12 | 4010 shroud for TZ-V6 / Dragon HF | 1 per tool |
| 13 | Dock | 1 per tool |

**Material:** ASA, PETG or PC-CF. Use PC-CF for the crank, receiver and tool top if you can.

**Settings:** 0.2 mm layers, 4 walls, 40 % infill, no supports.

**Key hardware:**
- FS90 or MG90S micro servo
- hardened dowels: Ø4×30, Ø3×8, Ø3×12, Ø3×15
- Ø6×2.65 magnets
- M3 heat-set inserts
- M3 and M5 screws (exact sizes and counts are in `BOM.csv`)

## Klipper
```ini
[servo opener]
pin: <free PWM pin>
maximum_servo_angle: 180
minimum_pulse_width: 0.0005
maximum_pulse_width: 0.0025
```
Set the closed and open angles on the printer with `SET_SERVO SERVO=opener ANGLE=..`. The full drop and pickup sequence is in `docs/ASSEMBLY.md`.

## Credits
- [Voron Design](https://github.com/VoronDesign): Clockwork 2 extruder and Stealthburner parts (GPL-3.0). Parts 01, 02 and 05 are modified Voron parts.
- MedusaHC, for the hotend-only toolchanger idea.
- Voron Tap / CNC Tap V2, which the head mounts to.

## License
GPL-3.0, the same license as the Voron parts this project modifies. See `LICENSE`.
