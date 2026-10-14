# From Transistors to Qubits: A Hybrid Learning Framework
## Electronic Devices & Circuits (EDC) — Assignment #2

An interactive, offline, engineering-grade educational platform bridging semiconductor physics, digital electronics, and quantum information science.

Built with **Python 3.13**, **Streamlit**, **Qiskit 2.5**, **Qiskit Aer 0.17**, **NumPy**, **Pandas**, and **Matplotlib**.

---

## ⚡ Key Highlights
- **100% Offline & Free:** Zero external API keys, cloud services, databases, or subscriptions required.
- **Genuine Quantum Simulation:** Real unitary circuit simulations and noise models powered by Qiskit and Qiskit Aer.
- **Verified Software Engineering:** 58 passing automated tests covering all logic gates, transistor physics, quantum circuits, and noise channels.
- **Dark-Navy Aesthetic:** Designed with a professional engineering visual language, responsive cards, and dynamic Matplotlib schematics.
- **Practical Bench Guide:** Includes a complete step-by-step breadboard guide for physical NPN transistor switching experiments.

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- Python 3.10+ (Tested and certified on Python 3.13.5)
- Git (optional)

### 2. Activate the Environment
Navigate to the project root directory:
```powershell
cd C:\Users\Lenovo\.gemini\antigravity-ide\scratch\transistor-to-qubit
```

Activate the pre-configured virtual environment:
- **Windows (PowerShell):**
  ```powershell
  .\.venv\Scripts\Activate.ps1
  ```
- **Windows (CMD):**
  ```cmd
  .\.venv\Scripts\activate.bat
  ```
- **Linux / macOS:**
  ```bash
  source .venv/bin/activate
  ```

*(If creating a fresh virtual environment from scratch)*:
```powershell
python -m venv .venv
.\.venv\Scripts\pip install -r requirements.txt
```

### 3. Launch the Application
Run the Streamlit web dashboard:
```powershell
streamlit run app.py
```
Open your web browser and navigate to:
**`http://localhost:8501`**

### 4. Run the Automated Test Suite
Execute the full test suite with Pytest:
```powershell
pytest -v tests/
```
Expected output: **`58 passed in < 5s`**.

---

## 📚 Application Architecture & Modules

### 1. Dashboard
- Executive overview of semiconductor-to-quantum progression.
- Pedagogical 6-step pathway: BJT Switch ➔ Logic Gates ➔ Qubit State ➔ Unitary Gates ➔ Measurement ➔ Noise & QEC.
- Quick-access module cards and real-time engine status indicator.

### 2. Module A — Transistor Switch Simulator
- Piecewise-linear educational simulation of an NPN BJT driving an LED load.
- Interactive controls for $V_{in}$, $V_{th}$, $V_{CC}$, $R_{Load}$, $V_F$, and $V_{CE(sat)}$.
- Dynamic Matplotlib circuit schematic with illuminated LED state.
- Transfer curves ($V_{in}$ vs $I_C$ and $V_{out}$) with active operating point marker.
- Observation logger and CSV data export button.
- Comprehensive breadboard laboratory assembly guide.

### 3. Module B — Logic Gate Simulator
- Covers all six canonical Boolean gates: **NOT, AND, OR, NAND, NOR, XOR**.
- Interactive binary toggles with instant output calculation.
- Canonical truth tables with **active row highlighting**.
- Semiconductor circuit implementation explanations.
- Composite logic demonstrations: **1-Bit Half Adder** and **2-to-1 Multiplexer (MUX)**.

### 4. Module C — Quantum Simulator
- Genuine quantum circuit simulation using Qiskit and Qiskit Aer.
- Single-qubit circuit builder: Pauli-X, Hadamard, Pauli-Z, and custom gate sequences.
- Configurable measurement shots and bar charts of measurement counts.
- Displays exact Statevector complex amplitudes ($\alpha, \beta$) alongside empirical probabilities.
- Two-qubit CNOT demonstration with Bell State ($|\Phi^+\rangle$) entanglement preparation.
- Dedicated **Phase Interference** experiment proving how $H \to Z \to H$ converts invisible phase flips into measurable bit flips!

### 5. Module D — Classical vs Quantum Comparison
- 8 in-depth technical comparison cards covering state representation, gate irreversibility, no-cloning theorem, noise margins, and measurement collapse.
- Interactive side-by-side behavioral playground.
- Delineates exactly where the classical-quantum analogy breaks down.

### 6. Noise Lab & Error Correction
- **Classical Additive Noise:** Simulates $V_{out} = V_{ideal} + n(t)$ with Gaussian thermal noise. Plots waveform, calculates SNR (dB), and displays Bit Error Rate (BER).
- **Quantum Decoherence Channels:** Simulates Bit-flip ($X$), Phase-flip ($Z$), and Depolarizing channels with Qiskit Aer noise models. Demonstrates that phase-flip error is invisible in direct Z-measurement but visible in phase-sensitive circuits.
- **3-Qubit Repetition Code (QEC):** Interactive bit-flip code demonstrating syndrome decoding and Toffoli recovery on $|0_L\rangle$ and $|1_L\rangle$.

### 7. Learning Resources
- Eight comprehensive learning units with theory, worked mathematical examples, key takeaways, and self-scoring interactive quizzes.

### 8. About Project
- Project metadata, course details, complete software architecture, hardware vs simulation demarcation table, and academic literature citations.

---

## 📁 Repository Structure
```
transistor-to-qubit/
├── app.py                      # Streamlit application entry point
├── requirements.txt            # Python package dependencies
├── README.md                   # This documentation file
├── .gitignore                  # Git ignore rules
├── src/                        # Modular simulation engine
│   ├── __init__.py
│   ├── transistor.py           # Transistor physics & CSV export
│   ├── logic_gates.py          # Boolean logic & composite circuits
│   ├── quantum_simulator.py    # Qiskit circuit simulations
│   ├── noise.py                # Classical & quantum noise + QEC
│   ├── visualizations.py       # Matplotlib plotting routines
│   └── ui_components.py        # Streamlit design tokens & widgets
├── tests/                      # Automated test suite (58 tests)
│   ├── __init__.py
│   ├── test_transistor.py
│   ├── test_logic_gates.py
│   ├── test_quantum_simulator.py
│   └── test_noise.py
├── docs/                       # Technical reports & guides
│   ├── assignment_report.md    # 17-section formal assignment report
│   ├── circuit_guide.md        # Physical breadboard guide
│   └── experiment_results.md   # Simulated data records
├── screenshots/                # Browser-verified UI screenshots
│   ├── dashboard.png
│   ├── module_a_transistor.png
│   ├── module_a_schematic.png
│   ├── module_b_logic_gates.png
│   ├── module_c_quantum.png
│   ├── module_d_comparison.png
│   └── noise_lab.png
└── student_submission/         # Final submission bundle
    └── YOUR_STUDENT_ID.zip     # Clean submission archive
```

---

## 📦 Submission Archive & Renaming Instructions
The final submission archive has been prepared in:
`student_submission/YOUR_STUDENT_ID.zip`

### How to Rename the ZIP file:
To submit with your actual student roll number / ID (e.g., `21BCE1042`):
- **Windows (PowerShell):**
  ```powershell
  Rename-Item -Path "student_submission\YOUR_STUDENT_ID.zip" -NewName "21BCE1042.zip"
  ```
- **Windows File Explorer:**
  Navigate to `student_submission`, right-click `YOUR_STUDENT_ID.zip`, click **Rename**, and enter your Student ID.

The ZIP archive contains all source code, tests, documentation, circuit diagrams, and screenshots, while cleanly excluding `.venv`, `__pycache__`, and temporary build artifacts.

---

## 🔬 Hardware vs Simulation Demarcation
- **Simulated by Software:** All mathematical transistor transfer curves, Boolean gate logic tables, Qiskit quantum circuit simulations, Aer noise channels, and 3-qubit error correction routines.
- **Requires Physical Hardware:** Actual multimeter DC voltage/current measurements on physical silicon BJTs, breadboard wiring, oscilloscope waveform captures, and true physical quantum QPU execution.
