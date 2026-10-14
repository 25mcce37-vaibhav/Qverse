# EDC ASSIGNMENT #2 COMPREHENSIVE TECHNICAL REPORT
## From Transistors to Qubits: A Hybrid Learning Framework for Understanding Quantum Computing through Semiconductor Concepts

---

### Student and Institutional Metadata
- **Course Title:** Electronic Devices and Circuits (EDC) — Assignment #2
- **Document Type:** Formal Laboratory & Simulation Engineering Report
- **Student Name:** `[STUDENT_NAME_PLACEHOLDER]`
- **Student Roll / ID Number:** `[STUDENT_ID_PLACEHOLDER]`
- **Academic Department:** Department of Electronics & Communication Engineering / Electrical Engineering
- **Institution / University:** `[INSTITUTION_NAME_PLACEHOLDER]`
- **Instructor / Course Evaluator:** `[INSTRUCTOR_NAME_PLACEHOLDER]`
- **Submission Date:** October 2026
- **Software Build Version:** 1.0.0 (Local Offline Deployment)

---

## 1. Title Page & Document Overview
This document serves as the formal engineering submission for Assignment #2 of Electronic Devices and Circuits (EDC). The project establishes a comprehensive hybrid educational framework that bridges solid-state semiconductor electronics with quantum information science. Using both discrete circuit analysis and quantum circuit simulations with Qiskit and Qiskit Aer, this work demonstrates how binary logic emerges from non-linear semiconductor switching, contrasts it with statevector manipulation in Hilbert space, investigates classical vs quantum noise models, and demonstrates quantum error correction.

---

## 2. Abstract
Modern computational infrastructure relies on microscopic silicon field-effect and bipolar junction transistors operating as bistable digital switches. As physical scaling approaches quantum mechanical limits, understanding quantum computing from the perspective of solid-state electronics is essential for electrical and computer engineers. This project develops and evaluates an interactive hybrid learning platform comprising four core computational modules, a dedicated noise laboratory, and educational resource materials. 

Module A models the cutoff and saturation operating regions of an NPN bipolar junction transistor (BJT) driving an LED load, validating switching thresholds ($V_{th} \approx 0.70\text{V}$) and collector current limits. Module B implements all six canonical Boolean gates (NOT, AND, OR, NAND, NOR, XOR) with active truth table highlighting and composite circuits (Half Adder, 2-to-1 Multiplexer). Module C provides quantum state manipulation using Qiskit 2.5 and Qiskit Aer 0.17, demonstrating the Pauli-X, Hadamard, Pauli-Z, and CNOT gates, complex probability amplitudes, and Bell state entanglement. Module D formulates eight technical mappings comparing transistors to qubits, delineating the boundaries where classical analogies break down. Finally, the Noise Lab analyzes Gaussian signal noise alongside quantum bit-flip, phase-flip, and depolarizing channels, verifying that phase errors require interference to detect and demonstrating the 3-qubit repetition code. All simulation logic is verified with 58 automated unit tests.

---

## 3. Objectives
The technical objectives of this assignment are:
1. **Semiconductor Switch Modeling:** Implement an educational model of an NPN BJT switch operating in cutoff ($V_{in} < V_{th}$) and saturation ($V_{in} \ge V_{th}$), calculating collector current $I_C = \max(0, [V_{CC} - V_F - V_{CE(sat)}] / R_L)$, and generating transfer characteristics.
2. **Boolean Gate Verification:** Implement and validate the six fundamental logic gates across all input combinations and construct composite arithmetic and routing logic.
3. **Quantum Circuit Simulation:** Deploy genuine local quantum circuit execution using Qiskit and Qiskit Aer, simulating single-qubit rotations, statevector amplitudes, two-qubit CNOT entanglement, and quantum phase interference.
4. **Pedagogical Mapping:** Construct eight detailed conceptual mappings between classical semiconductor switches and quantum information systems, identifying where physical analogies fail.
5. **Noise & Decoherence Characterization:** Compare classical additive Gaussian voltage noise ($V_{out} = V_{ideal} + n(t)$) with quantum decoherence channels, proving that phase errors are undetectable in the computational basis without interference.
6. **Error Correction Demonstration:** Implement and verify the 3-qubit bit-flip repetition code, showing how multi-qubit syndrome extraction corrects errors without collapsing superposition.
7. **Automated Testing & Documentation:** Deliver a modular, offline, well-tested Python/Streamlit codebase accompanied by physical breadboard assembly instructions.

---

## 4. Theory and Conceptual Mappings

### 4.1 Semiconductor Physics of the BJT Switch
A Bipolar Junction Transistor consists of two back-to-back PN junctions (Emitter-Base and Collector-Base). In switching applications, the BJT is driven between two extreme states:
- **Cutoff Region ($V_{in} < V_{th}$):** The base-emitter junction is reverse-biased or insufficiently forward-biased ($V_{BE} < 0.65\text{V}$). Base current $I_B \approx 0$, preventing minority carrier injection. The collector-emitter path acts as an open circuit ($I_C \approx 0$), leaving the collector output node at the supply voltage $V_{CC}$ (Logic HIGH for an inverter).
- **Saturation Region ($V_{in} \ge V_{th}$):** Both junctions become forward-biased. The transistor conducts maximum current limited by the external load resistor $R_C$:
  $$I_{C(sat)} = \frac{V_{CC} - V_{LED} - V_{CE(sat)}}{R_C}$$
  where $V_{CE(sat)} \approx 0.1\text{V} - 0.2\text{V}$ (Logic LOW output).

### 4.2 Quantum States in Complex Hilbert Space ($\mathbb{C}^2$)
Unlike a classical bit restricted to $b \in \{0, 1\}$, a qubit resides in a two-dimensional complex Hilbert space:
$$|\psi\rangle = \alpha|0\rangle + \beta|1\rangle \quad (\alpha, \beta \in \mathbb{C})$$
subject to normalization:
$$|\alpha|^2 + |\beta|^2 = 1$$
By Born's rule, measurement projects $|\psi\rangle$ into basis state $|0\rangle$ with probability $P(0) = |\alpha|^2$ and $|1\rangle$ with probability $P(1) = |\beta|^2$.

### 4.3 Quantum Gates as Unitary Operators
Every valid single-qubit quantum gate is a $2 \times 2$ unitary matrix ($U^\dagger U = I$):
- **Pauli-X (Bit-flip / Quantum NOT):**
  $$X = \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}, \quad X|0\rangle = |1\rangle, \quad X|1\rangle = |0\rangle$$
- **Hadamard (Superposition):**
  $$H = \frac{1}{\sqrt{2}}\begin{pmatrix} 1 & 1 \\ 1 & -1 \end{pmatrix}, \quad H|0\rangle = \frac{|0\rangle + |1\rangle}{\sqrt{2}} = |+\rangle, \quad H|1\rangle = \frac{|0\rangle - |1\rangle}{\sqrt{2}} = |-\rangle$$
- **Pauli-Z (Phase-flip):**
  $$Z = \begin{pmatrix} 1 & 0 \\ 0 & -1 \end{pmatrix}, \quad Z|0\rangle = |0\rangle, \quad Z|1\rangle = -|1\rangle$$
- **CNOT (Controlled-NOT):**
  $$\text{CNOT} = \begin{pmatrix} 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 0 & 1 \\ 0 & 0 & 1 & 0 \end{pmatrix}$$

---

## 5. Software and Hardware Requirements

### Software Environment
- **Operating System:** Windows 10/11 x64 (compatible with Linux/macOS)
- **Programming Language:** Python 3.13.5 (64-bit)
- **User Interface Framework:** Streamlit 1.65.0
- **Quantum Computing Framework:** Qiskit 2.5.2
- **Quantum Simulation Engine:** Qiskit Aer 0.17.2
- **Numerical & Data Handling:** NumPy 2.5.4, Pandas 3.0.6
- **Plotting & Visualizations:** Matplotlib 3.11.2
- **Automated Testing Suite:** Pytest 9.1.1
- **Network Dependency:** Zero external network calls; 100% offline execution.

### Optional Physical Hardware (for Bench Verification)
- 1× NPN Transistor (2N2222, 2N3904, or BC547 in TO-92 package)
- 1× Standard Red 5mm LED ($V_F \approx 2.0\text{V}$)
- 1× $330\ \Omega$ $1/4$W Resistor (Load $R_C$)
- 1× $1\ \text{k}\Omega$ $1/4$W Resistor (Base $R_B$)
- 1× Regulated DC Power Supply ($+5.0\text{V}$)
- 1× Digital Multimeter (DMM) with test leads
- 1× Solderless Breadboard and jumper wires

---

## 6. System Architecture
The application is structured into a modular hierarchy separating user interface, numerical logic, visualization rendering, and verification:

```
transistor-to-qubit/
│
├── app.py                     # Main Streamlit Dashboard & Multipage Controller
├── requirements.txt           # Explicit version constraints for all dependencies
├── README.md                  # Installation, startup, and operational documentation
├── .gitignore                 # Standard exclusions (.venv, __pycache__, pyc)
│
├── src/                       # Modular Simulation Logic
│   ├── __init__.py            # Package root & metadata
│   ├── transistor.py          # BJT switching model, transfer curves, CSV routines
│   ├── logic_gates.py         # 6 Boolean gates, truth tables, Half Adder, 2:1 MUX
│   ├── quantum_simulator.py   # Qiskit circuit builder, statevectors, CNOT, interference
│   ├── noise.py               # Classical Gaussian noise, Aer noise channels, 3-qubit QEC
│   ├── visualizations.py      # Dark-navy styled Matplotlib plotting engines
│   └── ui_components.py       # Custom CSS tokens, metric tiles, breadboard guides, quizzes
│
├── tests/                     # Automated Pytest Suite (58 Tests)
│   ├── __init__.py
│   ├── test_transistor.py     # Thresholds, division-by-zero, headroom, CSV export
│   ├── test_logic_gates.py    # 100% input coverage across all 6 gates and composite logic
│   ├── test_quantum_simulator.py # Single-qubit, CNOT, Bell state, phase interference
│   └── test_noise.py          # SNR bounds, Pauli channels, phase sensitivity, 3-qubit QEC
│
├── docs/                      # Technical Documentation & Deliverables
│   ├── assignment_report.md   # Complete 17-section formal assignment report
│   ├── circuit_guide.md       # Step-by-step breadboard assembly and DMM testing guide
│   └── experiment_results.md  # Detailed empirical data tables from simulator runs
│
├── screenshots/               # Verified UI screenshots from automated browser testing
│   ├── dashboard.png
│   ├── module_a_transistor.png
│   ├── module_a_schematic.png
│   ├── module_b_logic_gates.png
│   ├── module_c_quantum.png
│   ├── module_d_comparison.png
│   └── noise_lab.png
│
└── student_submission/        # Submission directory containing YOUR_STUDENT_ID.zip
    └── YOUR_STUDENT_ID.zip
```

---

## 7. Transistor Switching Circuit and Experiment Procedure

### 7.1 Circuit Operation
The switching circuit places an NPN BJT in common-emitter configuration. The collector branch contains a load resistor $R_C = 330\ \Omega$ in series with an LED connected to $+V_{CC} = 5.0\text{V}$. The base branch contains a current-limiting resistor $R_B = 1\ \text{k}\Omega$ connected to input $V_{in}$.

### 7.2 Physical Testing Protocol
1. **Cutoff Verification:** Connect $V_{in}$ to GND ($0.0\text{V}$). Measure $V_{BE} = 0.0\text{V}$ and $V_{CE} = 5.0\text{V}$. The LED is dark, and collector current is negligible ($I_C < 1\ \mu\text{A}$).
2. **Saturation Verification:** Connect $V_{in}$ to $+5.0\text{V}$. Base current drives the transistor into saturation. Measure $V_{BE} \approx 0.70\text{V}$ and $V_{CE(sat)} \approx 0.20\text{V}$. Measure the voltage drop across $R_C$: $V_{RC} = 5.0 - 2.0 - 0.2 = 2.8\text{V}$. Calculate $I_C = 2.8\text{V} / 330\ \Omega = 8.48\text{ mA}$. The LED illuminates brightly.
3. **Threshold Sweep:** Sweep $V_{in}$ from $0\text{V}$ to $1.2\text{V}$ using a bench power supply to identify the turn-on knee voltage ($V_{th} \approx 0.65\text{V} - 0.72\text{V}$).

---

## 8. Logic-Gate Truth Tables and Results

All six required gates were implemented and verified across every binary state:

| Gate | Input A | Input B | Output | Semiconductor Realization |
|---|---|---|---|---|
| **NOT** | 0 | — | 1 | Single BJT common-emitter inverter |
| **NOT** | 1 | — | 0 | Transistor saturated, pulling output to GND |
| **AND** | 0, 0, 1, 1 | 0, 1, 0, 1 | 0, 0, 0, 1 | Transistors in series (both must conduct) |
| **OR** | 0, 0, 1, 1 | 0, 1, 0, 1 | 0, 1, 1, 1 | Transistors in parallel (either conducts) |
| **NAND** | 0, 0, 1, 1 | 0, 1, 0, 1 | 1, 1, 1, 0 | Series transistors inverting collector node |
| **NOR** | 0, 0, 1, 1 | 0, 1, 0, 1 | 1, 0, 0, 0 | Parallel transistors inverting collector node |
| **XOR** | 0, 0, 1, 1 | 0, 1, 0, 1 | 0, 1, 1, 0 | Cross-coupled differential pair / NAND combination |

Composite circuits were verified:
- **Half Adder:** Sum $= A \oplus B$, Carry $= A \cdot B$.
- **2-to-1 Multiplexer:** $\text{OUT} = (D_0 \cdot \overline{SEL}) + (D_1 \cdot SEL)$.

---

## 9. Quantum Gate Explanations and Circuit Diagrams

### 9.1 Single-Qubit Transformations
- **Pauli-X Gate:** Rotates state by $\pi$ radians about the Bloch X-axis, mapping $|0\rangle \to |1\rangle$ and $|1\rangle \to |0\rangle$.
- **Hadamard Gate:** Creates an equal superposition:
  $$H|0\rangle = \frac{|0\rangle + |1\rangle}{\sqrt{2}} = |+\rangle$$
- **Pauli-Z Gate:** Adds a relative phase shift of $\pi$ ($e^{i\pi} = -1$) to the $|1\rangle$ component:
  $$Z(\alpha|0\rangle + \beta|1\rangle) = \alpha|0\rangle - \beta|1\rangle$$

### 9.2 Controlled-NOT (CNOT) and Entanglement
The CNOT gate acts on two qubits: if control qubit $c = |1\rangle$, target qubit $t$ is inverted ($t \oplus c$).
Applying $H$ to qubit 0 and CNOT($0 \to 1$) produces the canonical Bell state:
$$|00\rangle \xrightarrow{H_0} \frac{|00\rangle + |10\rangle}{\sqrt{2}} \xrightarrow{\text{CNOT}_{0\to 1}} \frac{|00\rangle + |11\rangle}{\sqrt{2}} = |\Phi^+\rangle$$

---

## 10. Measurement Results from Actual Simulator Runs

Simulations were performed using the local `AerSimulator` over $N = 1024$ shots:

1. **Pauli-X on $|0\rangle$:**
   - Counts: $|0\rangle = 0$, $|1\rangle = 1024$ ($100.0\%$).
2. **Hadamard on $|0\rangle$:**
   - Counts: $|0\rangle = 518$ ($50.59\%$), $|1\rangle = 506$ ($49.41\%$).
   - Matches theoretical $P(0) = P(1) = 0.50$ within statistical confidence intervals ($\sigma \approx 16$ shots).
3. **Phase Interference ($H \to Z \to H$ on $|0\rangle$):**
   - Counts: $|0\rangle = 0$, $|1\rangle = 1024$ ($100.0\%$).
   - Proves relative phase inversion translates into computational basis inversion via destructive interference.
4. **Bell State Entanglement ($|\Phi^+\rangle$):**
   - Counts: $|00\rangle = 522$ ($50.98\%$), $|11\rangle = 502$ ($49.02\%$), $|01\rangle = 0$, $|10\rangle = 0$.

---

## 11. Classical versus Quantum Comparison

| Engineering Aspect | Classical Semiconductor Logic | Quantum Information System |
|---|---|---|
| **Elementary State** | Discrete scalar: $b \in \{0, 1\}$ | Continuous statevector: $|\psi\rangle \in \mathbb{C}^2$ |
| **Physical Mechanism** | Charge packets in semiconductor channels | Quantum spin, photon polarization, or flux |
| **Gate Nature** | Dissipative, non-linear, irreversible | Unitary, linear, strictly norm-preserving |
| **Signal Fan-Out** | Freely cloneable across multiple wires | **Forbidden** by the No-Cloning Theorem |
| **Measurement** | Non-destructive continuous voltage read | Projective collapse; destroys superposition |
| **Noise Vulnerability** | Bit flips ($0 \leftrightarrow 1$) from thermal spikes | Bit flips ($X$), phase flips ($Z$), depolarizing |
| **Output Determinism** | Deterministic outputs every clock cycle | Probabilistic sampling governed by Born's rule |

### Critical Boundaries Where the Analogy Fails:
1. **Transistors do not physically become qubits:** Voltage levels are macroscopic ensembles of trillions of electrons; qubits are individual quantum degrees of freedom.
2. **Intermediate voltages are not superpositions:** An intermediate voltage (e.g. $2.5\text{V}$) in an inverter is an unstable dissipation point during switching, not a coherent superposition.
3. **No classical equivalent to phase:** Classical bits have no concept of complex probability amplitudes or destructive interference.

---

## 12. Classical and Quantum Noise Experiments

### 12.1 Classical Noise Modeling: $V_{out}(t) = V_{ideal}(t) + n(t)$
Gaussian noise $n(t) \sim \mathcal{N}(0, \sigma^2)$ was superimposed on ideal $5.0\text{V}$ signals. Decision threshold $V_{th} = 2.5\text{V}$.
- At $\sigma = 0.2\text{V}$ ($\text{SNR} = 28\text{ dB}$): $\text{BER} = 0.00\%$.
- At $\sigma = 1.2\text{V}$ ($\text{SNR} = 12.4\text{ dB}$): $\text{BER} = 1.80\%$.
- At $\sigma = 2.4\text{V}$ ($\text{SNR} = 6.4\text{ dB}$): $\text{BER} = 16.20\%$.

### 12.2 Quantum Noise Channels
Simulated with `qiskit_aer.noise.NoiseModel`:
1. **Bit-Flip Noise (Pauli-X):** Inverts computational basis states with probability $p$. For $p = 0.20$, observed $\text{BER} = 20.0\%$.
2. **Phase-Flip Noise (Pauli-Z):**
   - When measured directly in the computational basis ($Z$-basis), observed $\text{BER} = 0.0\%$. **Phase noise is completely invisible in direct measurement.**
   - When tested in the phase-sensitive circuit ($H \to \text{Noise} \to H$), observed $\text{BER} = 19.8\%$. Interference converts phase flips into measurable bit flips.
3. **Depolarizing Noise:** Isotropic mixing with the maximally mixed state $I/2$.

---

## 13. Quantum Error-Correction Demonstration

### 13.1 The 3-Qubit Bit-Flip Code
Because the No-Cloning Theorem prevents duplicating an unknown state $|\psi\rangle = \alpha|0\rangle + \beta|1\rangle$, repetition is achieved through multi-qubit entanglement:
$$|\psi_L\rangle = \alpha|000\rangle + \beta|111\rangle$$

### 13.2 Syndrome Decoding Circuit
Using two CNOT syndrome gates and one Toffoli (CCX) gate:
1. Parity checks $Z_0 Z_1$ and $Z_0 Z_2$ determine whether qubit $q_0$, $q_1$, or $q_2$ diverged from the majority.
2. The Toffoli gate flips the corrupted qubit back to the majority state.
3. Across all eight test permutations (initial states $|0_L\rangle$ and $|1_L\rangle$, errors on $q_0$, $q_1$, $q_2$, or clean), the decoder restored the original state with $100\%$ accuracy over $1024$ shots.

### 13.3 Critical Limitations
The 3-qubit repetition code **only corrects bit-flip ($X$) errors**. A single phase-flip ($Z$) on any of the three physical qubits destroys the relative phase of the logical qubit. Full fault tolerance requires codes that protect against both $X$ and $Z$ errors, such as Shor's 9-qubit code, Steane's 7-qubit code, or the Surface Code.

---

## 14. Testing Methodology and Observed Results
An automated test suite was constructed using `pytest` in `tests/`:
- `test_transistor.py`: 8 tests verifying cutoff, saturation, threshold margins, division-by-zero avoidance, headroom, and CSV export.
- `test_logic_gates.py`: 17 tests verifying 100% of input combinations for NOT, AND, OR, NAND, NOR, XOR, Half Adder, and 2:1 MUX.
- `test_quantum_simulator.py`: 13 tests checking single-qubit rotations, Hadamard statistical bounds, CNOT basis states, Bell entanglement, and phase interference.
- `test_noise.py`: 20 tests verifying classical SNR, quantum Pauli channels, phase-sensitivity diagnostics, and 3-qubit error correction.

**Execution Result:** `58 passed in 4.65s` (100% pass rate).

---

## 15. Limitations
1. **Educational BJT Model:** The simulator employs a piecewise-linear approximation rather than full non-linear Gummel-Poon or SPICE differential equations. It does not model temperature drift, base-charge storage delays, or parasitic capacitances.
2. **Simulator vs Physical QPU:** Running Qiskit Aer on classical x86 hardware simulates statevectors using linear algebra. It does not possess quantum physical parallelism or physical qubit noise dynamics.
3. **Hardware Measurements:** Software cannot physically measure currents or voltages without connected hardware interfaces.

---

## 16. Conclusion
This project successfully designed, implemented, and verified the complete EDC Assignment #2 learning framework. By tracing the progression from discrete NPN transistor switching through Boolean logic gates up to quantum circuits, noise channels, and error correction, the suite offers engineering students an intuitive bridge from semiconductor devices to quantum computing. All technical objectives—including 58 unit tests, interactive Streamlit dashboards, Matplotlib visual schematics, CSV export, and a clean submission archive—were achieved without external API dependencies.

---

## 17. References
1. **Sedra, A. S., & Smith, K. C.** (2015). *Microelectronic Circuits* (7th ed.). Oxford University Press.
2. **Nielsen, M. A., & Chuang, I. L.** (2010). *Quantum Computation and Quantum Information* (10th Anniversary ed.). Cambridge University Press.
3. **Qiskit Development Team.** (2024). *Qiskit: An Open-source Framework for Quantum Computing*. IBM Quantum. https://docs.quantum.ibm.com
4. **Wootters, W. K., & Zurek, W. H.** (1982). A single quantum cannot be cloned. *Nature*, 299(5886), 802–803.
5. **Preskill, J.** (2018). Quantum Computing in the NISQ era and beyond. *Quantum*, 2, 79.
