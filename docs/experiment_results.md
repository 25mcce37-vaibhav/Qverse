# Simulated Laboratory Experiment Results Record

## Project: Transistor-to-Qubit Learning Framework (EDC Assignment #2)
**Execution Environment:** Python 3.13.5 • Qiskit 2.5.2 • Qiskit Aer 0.17.2 • NumPy 2.5.4 • Matplotlib 3.11.2

---

## 1. Module A: Transistor Switching Simulator Results

### Experimental Parameters:
- Supply Voltage ($V_{CC}$): $5.0\text{ V}$
- Load Resistor ($R_C$): $330.0\ \Omega$
- Switching Threshold ($V_{th}$): $0.70\text{ V}$
- LED Forward Voltage ($V_F$): $2.00\text{ V}$
- Saturation Voltage ($V_{CE(sat)}$): $0.20\text{ V}$

### Simulated Input vs Output Response Table:

| Trial | Input $V_{in}$ (V) | State Region | $I_C$ (mA) | Output $V_{out}$ (V) | LED Status | Switching Condition / Observation |
|---|---|---|---|---|---|---|
| 1 | 0.00 | Cutoff (OFF) | 0.00 | 5.00 | DARK | $V_{in} < V_{th}$; Base reverse-biased, zero current. |
| 2 | 0.30 | Cutoff (OFF) | 0.00 | 5.00 | DARK | $V_{in} < V_{th}$; Sub-threshold, no conduction. |
| 3 | 0.65 | Cutoff (OFF) | 0.00 | 5.00 | DARK | Immediately below threshold (0.05V margin). |
| 4 | 0.70 | Saturation (ON) | 8.48 | 0.20 | LIT | At exact switching threshold ($V_{in} = V_{th}$). Switch closes. |
| 5 | 1.00 | Saturation (ON) | 8.48 | 0.20 | LIT | Base junction fully conducting; $I_C$ limited by $R_C$. |
| 6 | 2.50 | Saturation (ON) | 8.48 | 0.20 | LIT | Standard logic HIGH level ($2.5\text{V}$ TTL/CMOS). |
| 7 | 3.30 | Saturation (ON) | 8.48 | 0.20 | LIT | Standard $3.3\text{V}$ microcontroller GPIO logic HIGH. |
| 8 | 5.00 | Saturation (ON) | 8.48 | 0.20 | LIT | Full rail drive ($V_{in} = V_{CC}$). Heavy saturation. |

---

## 2. Module B: Classical Logic Gate Truth Table Verification

Every input combination was verified against canonical Boolean definitions using unit tests (`tests/test_logic_gates.py`):

| Gate Name | Input A | Input B | Simulated Output | Validated Truth Table Expected | Status |
|---|---|---|---|---|---|
| **NOT** | 0 | — | 1 | 1 | PASS |
| **NOT** | 1 | — | 0 | 0 | PASS |
| **AND** | 0 | 0 | 0 | 0 | PASS |
| **AND** | 0 | 1 | 0 | 0 | PASS |
| **AND** | 1 | 0 | 0 | 0 | PASS |
| **AND** | 1 | 1 | 1 | 1 | PASS |
| **OR** | 0 | 0 | 0 | 0 | PASS |
| **OR** | 0 | 1 | 1 | 1 | PASS |
| **OR** | 1 | 0 | 1 | 1 | PASS |
| **OR** | 1 | 1 | 1 | 1 | PASS |
| **NAND** | 0 | 0 | 1 | 1 | PASS |
| **NAND** | 0 | 1 | 1 | 1 | PASS |
| **NAND** | 1 | 0 | 1 | 1 | PASS |
| **NAND** | 1 | 1 | 0 | 0 | PASS |
| **NOR** | 0 | 0 | 1 | 1 | PASS |
| **NOR** | 0 | 1 | 0 | 0 | PASS |
| **NOR** | 1 | 0 | 0 | 0 | PASS |
| **NOR** | 1 | 1 | 0 | 0 | PASS |
| **XOR** | 0 | 0 | 0 | 0 | PASS |
| **XOR** | 0 | 1 | 1 | 1 | PASS |
| **XOR** | 1 | 0 | 1 | 1 | PASS |
| **XOR** | 1 | 1 | 0 | 0 | PASS |

### Composite Arithmetic Circuit (Half Adder):
- Input $(0, 0) \to \text{Sum} = 0, \text{Carry} = 0 \to 00_2 = 0_{10}$
- Input $(0, 1) \to \text{Sum} = 1, \text{Carry} = 0 \to 01_2 = 1_{10}$
- Input $(1, 0) \to \text{Sum} = 1, \text{Carry} = 0 \to 01_2 = 1_{10}$
- Input $(1, 1) \to \text{Sum} = 0, \text{Carry} = 1 \to 10_2 = 2_{10}$

---

## 3. Module C: Quantum Simulator Actual Run Results

All circuits simulated on `AerSimulator` backend over $N = 1024$ shots.

### Single-Qubit Basic Gates:
1. **Pauli-X Gate on $|0\rangle$:**
   - Statevector: $|\psi\rangle = 0.00|0\rangle + 1.00|1\rangle$
   - Measurement: $|0\rangle$: 0 counts ($0.0\%$), $|1\rangle$: 1024 counts ($100.0\%$)
   - Result: Deterministic inversion ($X|0\rangle = |1\rangle$).
2. **Pauli-X Gate on $|1\rangle$:**
   - Statevector: $|\psi\rangle = 1.00|0\rangle + 0.00|1\rangle$
   - Measurement: $|0\rangle$: 1024 counts ($100.0\%$), $|1\rangle$: 0 counts ($0.0\%$)
   - Result: Deterministic inversion ($X|1\rangle = |0\rangle$).
3. **Hadamard Gate on $|0\rangle$ (Superposition):**
   - Statevector: $|\psi\rangle = \frac{1}{\sqrt{2}}|0\rangle + \frac{1}{\sqrt{2}}|1\rangle \approx 0.7071|0\rangle + 0.7071|1\rangle$
   - Measurement ($1024$ shots): $|0\rangle$: 518 counts ($50.59\%$), $|1\rangle$: 506 counts ($49.41\%$)
   - Result: Statistical binomial distribution verifying equal superposition ($P(0) \approx P(1) \approx 0.50$).

### Quantum Phase Interference Demonstration:
- **Circuit A (H → H):** $|0\rangle \to H \to H \to |0\rangle$.
  - Measurement: $|0\rangle$: 1024 counts ($100.0\%$), $|1\rangle$: 0 counts ($0.0\%$).
- **Circuit B (H → Z → H):** $|0\rangle \to H \to Z \to H \to |1\rangle$.
  - Measurement: $|0\rangle$: 0 counts ($0.0\%$), $|1\rangle$: 1024 counts ($100.0\%$).
  - Analysis: The Z gate adds a $\pi$ phase shift to the $|1\rangle$ component. The second Hadamard causes destructive interference on $|0\rangle$ and constructive interference on $|1\rangle$, converting a relative phase flip into a $100\%$ measurable bit flip!

### Two-Qubit CNOT & Bell State Entanglement:
- **CNOT Basis Operations (Qiskit ordering $|q_1 q_0\rangle$):**
  - Input $|00\rangle \to \text{CNOT}(0 \to 1) \to |00\rangle$ (1024/1024 shots)
  - Input $|01\rangle \to \text{CNOT}(0 \to 1) \to |11\rangle$ (1024/1024 shots, target flipped because $q_0 = 1$)
  - Input $|10\rangle \to \text{CNOT}(0 \to 1) \to |10\rangle$ (1024/1024 shots, target unchanged because $q_0 = 0$)
  - Input $|11\rangle \to \text{CNOT}(0 \to 1) \to |01\rangle$ (1024/1024 shots, target flipped from 1 to 0)
- **Bell State $|\Phi^+\rangle = \frac{|00\rangle + |11\rangle}{\sqrt{2}}$ ($H_0 \to \text{CNOT}_{0\to 1}$):**
  - Counts: $|00\rangle$: 522 ($50.98\%$), $|11\rangle$: 502 ($49.02\%$), $|01\rangle$: 0 ($0.0\%$), $|10\rangle$: 0 ($0.0\%$).
  - Result: Perfect non-local quantum correlation.

---

## 4. Noise Lab Experimental Results

### Classical Noise Analysis ($V_{ideal} = 5.0\text{V}$, $V_{th} = 2.5\text{V}$):

| Noise Standard Dev $\sigma$ (V) | Signal-to-Noise Ratio (dB) | Total Samples | Errors Observed | Bit Error Rate (BER) |
|---|---|---|---|---|
| $\sigma = 0.20\text{ V}$ | $28.0\text{ dB}$ | 500 | 0 | $0.00\%$ |
| $\sigma = 0.80\text{ V}$ | $15.9\text{ dB}$ | 500 | 1 | $0.20\%$ |
| $\sigma = 1.20\text{ V}$ | $12.4\text{ dB}$ | 500 | 9 | $1.80\%$ |
| $\sigma = 1.80\text{ V}$ | $8.9\text{ dB}$ | 500 | 42 | $8.40\%$ |
| $\sigma = 2.40\text{ V}$ | $6.4\text{ dB}$ | 500 | 81 | $16.20\%$ |

### Quantum Noise Channels ($p = 0.20$, $1024$ shots):
1. **Bit-Flip Noise (Standard Z-Basis):**
   - Measured Counts: $|0\rangle$: 819 ($80.0\%$), $|1\rangle$: 205 ($20.0\%$).
   - Observed BER: $20.02\%$ (matches error rate $p = 0.20$).
2. **Phase-Flip Noise (Standard Z-Basis):**
   - Measured Counts: $|0\rangle$: 1024 ($100.0\%$), $|1\rangle$: 0 ($0.0\%$).
   - Observed BER: $0.00\%$ (**completely undetectable in computational basis**).
3. **Phase-Flip Noise (Phase-Sensitive Circuit $H \to \text{Noise} \to H$):**
   - Measured Counts: $|0\rangle$: 821 ($80.2\%$), $|1\rangle$: 203 ($19.8\%$).
   - Observed BER: $19.82\%$ (**phase error converted to observable bit error via interference**).

### 3-Qubit Bit-Flip Repetition Code Verification:

| Initial Logical State | Injected Error Qubit | Syndrome Detection | Decoded Output | Error Corrected? |
|---|---|---|---|---|
| $|0_L\rangle = |000\rangle$ | None | Parity (0, 0) | $|0\rangle$ (1024/1024) | YES |
| $|0_L\rangle = |000\rangle$ | Qubit $q_0$ | Parity (1, 1) | $|0\rangle$ (1024/1024) | YES |
| $|0_L\rangle = |000\rangle$ | Qubit $q_1$ | Parity (1, 0) | $|0\rangle$ (1024/1024) | YES |
| $|0_L\rangle = |000\rangle$ | Qubit $q_2$ | Parity (0, 1) | $|0\rangle$ (1024/1024) | YES |
| $|1_L\rangle = |111\rangle$ | None | Parity (0, 0) | $|1\rangle$ (1024/1024) | YES |
| $|1_L\rangle = |111\rangle$ | Qubit $q_0$ | Parity (1, 1) | $|1\rangle$ (1024/1024) | YES |
| $|1_L\rangle = |111\rangle$ | Qubit $q_1$ | Parity (1, 0) | $|1\rangle$ (1024/1024) | YES |
| $|1_L\rangle = |111\rangle$ | Qubit $q_2$ | Parity (0, 1) | $|1\rangle$ (1024/1024) | YES |
