# Practical Bench Experiment Guide: NPN Transistor Switching Circuit

## Course: Electronic Devices & Circuits (EDC) — Assignment #2
**Experiment Title:** Characterization and Verification of an NPN Bipolar Junction Transistor (BJT) as a Binary Digital Switch Driving an LED Load

---

## 1. Objective
To construct, test, and experimentally characterize an NPN BJT switching circuit on a solderless breadboard. This experiment bridges theoretical semiconductor concepts (cutoff vs saturation) with real-world electrical measurements, establishing the physical foundation of binary digital logic.

> **CRITICAL LABORATORY NOTE:**
> Software simulators use simplified mathematical equations (piecewise linear models). Physical hardware circuits exhibit component tolerances (e.g. ±5% resistor tolerance, variable transistor current gain $\beta_{FE}$), ambient thermal dependencies, non-zero lead resistances, and diode exponential conduction knees. This guide instructs students on conducting physical hardware measurements.

---

## 2. Required Equipment and Components

| Item | Component / Equipment | Specifications / Value | Quantity | Purpose |
|---|---|---|---|---|
| 1 | NPN Bipolar Junction Transistor | 2N2222, 2N3904, or BC547 (TO-92) | 1 | Primary active switching element |
| 2 | Light Emitting Diode (LED) | Standard 5mm Red LED ($V_F \approx 1.8\text{V} - 2.1\text{V}$) | 1 | Visual indicator of collector conduction |
| 3 | Collector Load Resistor ($R_C$) | $330\ \Omega$ (or $470\ \Omega$), $1/4$ Watt (5%) | 1 | Limits collector current to safe levels ($\sim 10\text{ mA}$) |
| 4 | Base Drive Resistor ($R_B$) | $1.0\ \text{k}\Omega$ to $4.7\ \text{k}\Omega$, $1/4$ Watt (5%) | 1 | Sets base drive current to ensure saturation |
| 5 | DC Power Supply | Dual-output regulated DC bench supply (or 5.0V source) | 1 | Provides $V_{CC} = +5.0\text{V}$ and variable $V_{in}$ |
| 6 | Digital Multimeter (DMM) | True-RMS DC voltmeter and ammeter | 1 | Measures $V_{BE}$, $V_{CE}$, and $I_C$ |
| 7 | Prototyping Board & Wires | Solderless breadboard and solid-core jumper wires | 1 set | Circuit assembly |

---

## 3. Transistor Pinout Diagram & Identification

### TO-92 Plastic Package Identification:
Hold the transistor with the **flat face pointing directly toward you** and the leads pointing downwards.

```
       _____
      /     \
     | FLAT  |
     | FACE  |
     |_______|
       | | |
       1 2 3
```

- **For 2N2222 / 2N3904:**
  - Pin 1 (Left): **Emitter (E)**
  - Pin 2 (Center): **Base (B)**
  - Pin 3 (Right): **Collector (C)**
- **For BC547 / BC548:**
  - Pin 1 (Left): **Collector (C)**
  - Pin 2 (Center): **Base (B)**
  - Pin 3 (Right): **Emitter (E)**

*(Always verify pinout using the DMM diode check function: forward bias from Base to Emitter should read $\sim 0.65\text{V} - 0.72\text{V}$; Base to Collector should read $\sim 0.65\text{V} - 0.70\text{V}$)*.

---

## 4. Circuit Schematic

```
          +V_CC (+5.0 V)
               |
               +---[ R_Load = 330 Ω ]---+
                                        |
                                     (Anode)
                                      LED
                                     (Cathode)
                                        |
                                        +----> Collector (C)
                                               |
  V_in O---[ R_Base = 1 kΩ ]---> Base (B)     NPN BJT
                                               |
                                        +----> Emitter (E)
                                        |
                                       GND (0.0 V)
```

---

## 5. Step-by-Step Breadboard Assembly Procedure

1. **Power Isolation:** Ensure the bench power supply is powered OFF before placing components.
2. **Ground Bus:** Connect the negative lead of the 5.0V power supply to the breadboard blue/negative rail (**GND**).
3. **Supply Bus:** Connect the positive lead of the 5.0V power supply to the red/positive rail (**+5V**).
4. **Insert Transistor:** Insert the NPN BJT into three separate tie-point rows on the breadboard (e.g., Rows 10, 11, 12).
5. **Emitter to Ground:** Insert a jumper wire from the Emitter pin directly to the GND rail.
6. **Collector-LED Branch:**
   - Connect one terminal of the $330\ \Omega$ resistor to the $+5$V rail.
   - Connect the other terminal of the $330\ \Omega$ resistor to an unused row (e.g., Row 15).
   - Insert the **Anode** (longer lead) of the LED into Row 15.
   - Insert the **Cathode** (shorter lead with flat spot on rim) of the LED into the transistor Collector row.
7. **Base Drive Branch:**
   - Connect one lead of the $1\ \text{k}\Omega$ resistor to the Base row.
   - Connect the free lead of the $1\ \text{k}\Omega$ resistor to a variable DC voltage supply terminal or switched jumper wire ($V_{in}$).

---

## 6. Physical Measurement Procedure

### Experiment Part 1: Verification of Cutoff State (Logic LOW Input)
1. Tie the input lead $V_{in}$ directly to **GND** ($V_{in} = 0.00\text{ V}$).
2. Turn on the 5.0V bench power supply.
3. Observe the LED: It must remain **completely unlit (DARK)**.
4. Set the DMM to DC Volts:
   - Measure $V_{BE}$ across Base and Emitter. Expected: $V_{BE} \approx 0.00\text{ V} < 0.60\text{ V}$.
   - Measure $V_{CE}$ across Collector and Emitter. Expected: $V_{CE} \approx V_{CC} = 5.00\text{ V}$.
5. Record measurements in the observation table.

### Experiment Part 2: Verification of Saturation State (Logic HIGH Input)
1. Connect $V_{in}$ to the $+5.0\text{V}$ rail through $R_B$ ($V_{in} = 5.00\text{ V}$).
2. Observe the LED: It must turn **ON brightly**.
3. Set the DMM to DC Volts:
   - Measure $V_{BE}$. Expected: Clamped at diode forward drop $V_{BE} \approx 0.68\text{V} - 0.74\text{ V}$.
   - Measure $V_{CE}$. Expected: Drops to saturation level $V_{CE(sat)} \approx 0.10\text{V} - 0.25\text{ V}$.
   - Measure voltage drop across $R_C$ ($V_{RC}$). Expected: $V_{RC} = V_{CC} - V_F - V_{CE} \approx 5.0 - 2.0 - 0.2 = 2.8\text{ V}$.
4. Calculate actual collector current:
   $$I_C = \frac{V_{RC}}{R_C} = \frac{2.80\text{ V}}{330\ \Omega} \approx 8.48\text{ mA}$$
5. Record measurements in the observation table.

### Experiment Part 3: Characterization of Switching Threshold ($V_{th}$)
1. Connect $V_{in}$ to a continuously variable DC power supply.
2. Slowly increment $V_{in}$ from $0.0\text{V}$ to $1.2\text{V}$ in steps of $0.05\text{V}$.
3. Record the exact $V_{in}$ at which the LED first visibly begins conducting light ($V_{th}$).
4. Notice the transition region between cutoff and saturation.

---

## 7. Laboratory Safety & Best Practices
- **Never omit the base resistor ($R_B$):** Applying $+5$V directly to the base will cause destructive overcurrent through the base-emitter PN junction ($I_B > 500\text{ mA}$), immediately destroying the transistor.
- **Never short the collector to $+V_{CC}$:** Omitting $R_C$ will burn out the LED or cause transistor thermal runaway.
- **Confirm LED Polarity:** Reverse-biased LEDs will block conduction regardless of transistor switching state.
