# Assembly guide (v30.2)

Step-by-step build of the head, the tools and the docks, with illustrations. Part numbers match `stl/` and `BOM.csv`. The 3D viewer (`docs/index.html`) shows the finished assembly. For the tool-change sequence and audit notes, see [ASSEMBLY.md](ASSEMBLY.md).

## What you need
- All printed parts from `stl/`: ASA, PETG or PC-CF, 0.2 mm layers, 4 walls, 40 % infill, no supports. Print the crank, trunnion, receiver and tool top in PC-CF if you can.
- The hardware in `BOM.csv`, plus a stock Clockwork 2 hardware kit (gears, shafts, bearings, screws, spring).
- A soldering iron with an M3 insert tip, a 2.5 mm hex key, a 5.5 mm nut driver, and a small arbor press or vice for the dowels.

**Heat-set inserts.** Every insert in this build is an **M3×5×4** (Ø5 outer diameter, 4 mm long; the Voron standard). Every insert hole is **Ø4.7**. There are 12: 3 in the CW2 body, 7 in the motor plate and 2 in the duct. Press each one in straight and flush with the surface. Don't push them deeper.

---

## 1. Prepare the printed parts

### 1.1 CW2 main body: 3 inserts
![01 CW2 main body: 3 inserts](../images/assembly/inserts_01_body.png)

- 2 inserts for the receiver-frame posts. Press them in from the back of the front wall. The screws come in from the front, through the new Ø3.4 holes.
- 1 insert in the right side, as for a stock CW2.

### 1.2 Motor plate: 7 inserts
![05 Motor plate: back and right side](../images/assembly/inserts_05_plate_back.png)
![05 Motor plate: front face](../images/assembly/inserts_05_plate_front.png)

- **Back face, 3 inserts:** 2 at the top for the servo bracket, and 1 upper left for the CW2 body screw.
- **Right side, 2 inserts:** they go into the side pockets, as on a stock CW2 plate.
- **Front face, 2 inserts:** the CW2 body screws thread into these.

### 1.3 Duct: 2 inserts
![09 Duct: 2 inserts](../images/assembly/inserts_09_duct.png)

### 1.4 Receiver: dowels and magnets
![07 Receiver](../images/assembly/inserts_07_receiver.png)

- **Dowels:** press 2 Ø4×30 dowels in from the back until **23 mm** stand out at the front.
- **Magnets:** fit 4 Ø6×2.65 magnets from the front, 2 stacked in each pocket. Mark their polarity: the tool magnets must attract them.

### 1.5 Tool top, for each tool
![10 Tool top: magnets](../images/assembly/inserts_10_tool_top_magnets.png)
![10 Tool top: guide-lever pivot](../images/assembly/inserts_10_tool_top_pivot.png)

- **Magnets:** fit 2 Ø6×2.65 magnets from the back, 1 per pocket. Check that they *attract* the receiver magnets before you glue them.
- **Guide lever:** put the guide lever (10b) in place and press the Ø3×12 pivot pin in from the front. The lever must swing freely.

### 1.6 Dock, for each tool
![13 Dock](../images/assembly/inserts_13_dock.png)

Press 2 Ø3×15 dowels **8 mm** into the dock face, so that **7 mm** stand out.

---

## 2. Extruder
Build the Clockwork 2 as in the Voron Stealthburner manual, with these parts:

- **01 main body:** modified (front holes for the frame posts).
- **02 Guidler A + mast**, with the stock **02b Guidler B**. The mast is the upright tab on the left; the old v29 Ø4.4 arm hole is not used.
- **05 motor plate:** modified (crank bore, stop pocket, servo-bracket inserts).

Leave out the stock CW2 tension latch and its spring screw: the pull rod replaces them. Also leave out the two upper-left rear CW2 screws (as in v29).

## 3. Servo and bracket
![Opener: servo and bracket](../images/assembly/opener_servo_bracket.png)

1. Fit the FS90 into the 06 bracket with its own 2 M2 tab screws, from the back. The spline faces the plate.
2. Bolt the bracket to the plate back with 2× **M3×12** into the two top inserts. The spline now sits inside the plate bore.

## 4. Crank and trunnion
![Opener: crank and trunnion](../images/assembly/opener_crank_trunnion.png)

1. Push the 03 trunnion's round end and Ø4 spigot into the 04 crank from the front.
2. From the back of the crank, fit an **M2 washer** and an **M2×3 button head** into the spigot and tighten it. It clamps the spigot end, not the crank, so the trunnion still turns freely. Don't use an M2×4: it would reach the rod hole.
3. Power the servo and send it to the closed angle (section 8.3).
4. From the front, put the crank's hub into the plate bore with its stop tab in the pocket and resting on the pocket's closed end. The trunnion points right, 6° below horizontal.
5. Push the crank onto the spline by hand. The socket is Ø4.75 with three relief slits; if it is too tight, open it with a 4.8 mm drill by hand.
6. Turn the trunnion so its flats face left and right.

## 5. Pull rod and tension
![Opener: pull rod](../images/assembly/opener_pull_rod.png)

Thread the parts onto the M3×55 SHCS in this order, starting from the left:

1. Screw head and a washer, on the left of the Guidler A mast. Push the rod through the mast slot.
2. **Push nyloc:** run it up to the mast's right face, then back it off to about **0.2 mm** of play.
3. **Stop nyloc.**
4. The trunnion's cross hole.
5. The stock CW2 spring.
6. A washer and the **tension nyloc**.

Then:

- **Stop gap:** with the crank closed, set a **2.5 mm** gap between the stop nyloc and the trunnion's left flat. This is how far the spring unloads before the idler starts to open.
- **Tension:** turn the tension nyloc; tighter means more grip. A good starting point is about **10.8 mm** of spring between the trunnion and the washer.

## 6. Receiver, frame, duct and Tap
1. Screw the receiver to the receiver frame with 2× M3×6. They self-tap into Ø2.5 holes.
2. Bolt the frame to the CNC Tap with 2× M3×20.
3. Bolt the frame posts to the CW2 front with 2× **M3×10**. They go through the body's front holes into the inserts from step 1.1.
4. Bolt the duct legs under the frame wings with 2× M3×10, into the duct inserts.

## 7. Tools and docks
1. **Tool:** put the 4010 shroud (11 for TZ-V6, 12 for Dragon HF) under the tool top. Bolt the heatsink up through both with 4× M2.5×10. Fix the 4010 fan with 4× M3×14; they self-tap.
2. **PTFE:** push the 4×2 PTFE 6 mm into the socket at the top of the guide lever.
3. **Wires:** run the hotend loom up the left side of the shroud. Hold it to the wire column with 2 zip ties, with the tie heads on the front or outer face, never at the back.
4. **Docks:** bolt each dock to the 2020 rail with 2× M5×10 and drop-in T-nuts, 63 mm apart.

---

## 8. Electronics: servo on a BTT SB2209

### 8.1 Wiring
![Servo to SB2209](../images/assembly/sb2209_servo_wiring.png)

The servo plugs into **pins 1–3 of the 5-pin BLTouch (Probe) header**:

| Header pin | Signal | Servo wire | SB2209 CAN (STM32G0B1) | SB2209 CAN (RP2040) / SB2209 USB |
|---|---|---|---|---|
| 1 | GND | brown | GND | GND |
| 2 | +5V | red | +5V | +5V |
| 3 | servo signal | orange / yellow | `PB9` | `gpio22` |
| 4 | GND | not used | | |
| 5 | probe input | not used | `PB8` | `gpio21` |

- Re-crimp the servo lead with a 3-pin JST-XH housing that fits pins 1–3, or make a short 3-pin to 5-pin adapter lead.
- The CNC Tap does not use this header, so it is free. Wire the Tap to the Proximity or Endstop input, as in the Tap documentation.
- The pins above are from BTT's published SB2209 pinouts and sample configs. Check them against the silkscreen on your board.

### 8.2 Klipper config
Add this to `printer.cfg`, or to the file that holds your SB2209 config. Use the MCU name from your own `[mcu ...]` section; `EBBCan` is the name in BTT's sample config.

```ini
[servo opener]
pin: EBBCan:PB9                 # SB2209 CAN (STM32G0B1)
#pin: EBBCan:gpio22             # SB2209 CAN (RP2040) or SB2209 USB
maximum_servo_angle: 180
minimum_pulse_width: 0.0005
maximum_pulse_width: 0.0025
# no initial_angle: the servo stays off at start-up, and the over-centre crank holds the idler closed

[gcode_macro OPENER_CLOSE]
description: Close the idler (crank goes over centre), then switch the servo off
variable_angle: 8               # set this on your printer, see 8.3
gcode:
    SET_SERVO SERVO=opener ANGLE={printer["gcode_macro OPENER_CLOSE"].angle}
    G4 P500
    SET_SERVO SERVO=opener WIDTH=0

[gcode_macro OPENER_OPEN]
description: Open the idler, then switch the servo off
variable_angle: 174             # closed angle + 166 (or closed − 166 if your servo turns the other way)
gcode:
    SET_SERVO SERVO=opener ANGLE={printer["gcode_macro OPENER_OPEN"].angle}
    G4 P500
    SET_SERVO SERVO=opener WIDTH=0
```

- Don't define `[bltouch]` on the same pins.
- The servo signal is switched off after every move (`WIDTH=0`). With the crank over centre, the spring holds the idler closed. When open, nothing loads the crank, so the servo doesn't buzz between tool changes.

### 8.3 Setting the angles
1. **Before fitting the crank** (step 4.3), run `SET_SERVO SERVO=opener ANGLE=8`, then fit the crank in the closed position.
2. Step it slowly: `SET_SERVO SERVO=opener ANGLE=30`, then 60, 90 and so on. The crank should swing **up and to the left**, over the top. If it moves down first, your servo turns the other way. In that case, refit the crank at `ANGLE=172` and step it down towards 6.
3. **Open angle:** closed + 166° (or closed − 166°). Use it when the trunnion has swung over the top to the left and Guidler A is fully open (about 11°).
4. **Closed angle:** the angle where the crank tab just rests on its stop in the plate and the servo doesn't buzz. One spline tooth is about 17°. If the end positions are a tooth off, refit the crank one tooth over rather than forcing the angle.
5. Put the two angles into the `variable_angle` lines of `OPENER_CLOSE` and `OPENER_OPEN`.
6. **Check the tension:** with filament loaded and the idler closed, a push on the extruder by hand should feed it without the gears slipping. Adjust with the tension nyloc (step 5).

### 8.4 In the tool-change macros
Call `OPENER_OPEN` before the X shift into the dock, and `OPENER_CLOSE` after the X shift out with the new tool. The full drop and pickup sequence is in [ASSEMBLY.md](ASSEMBLY.md#klipper).
