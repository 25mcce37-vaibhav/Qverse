"""
Quantum Simulator Module
Genuine quantum circuit creation and simulation using Qiskit and Qiskit Aer.

Provides:
- 1-qubit circuits (X, H, Z, sequence execution, statevector, phase interference)
- 2-qubit circuits (CNOT, Bell State entanglement)
- Configurable shots, measurement counts, probabilities
- Statevector amplitudes, Bloch-sphere angle calculations, and circuit diagrams
- Explanations of bitstring ordering and quantum concepts
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple, Any, Optional
import numpy as np

# Qiskit imports
from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import Statevector
try:
    from qiskit_aer import AerSimulator
    AER_AVAILABLE = True
except ImportError:
    AER_AVAILABLE = False


@dataclass
class SimulationOutput:
    circuit: QuantumCircuit
    circuit_text: str
    shots: int
    counts: Dict[str, int]
    probabilities: Dict[str, float]
    statevector: Optional[List[complex]] = None
    statevector_labels: Optional[List[str]] = None
    explanation: str = ""
    gate_sequence: Optional[List[str]] = None


def get_simulator():
    """Returns an AerSimulator backend if available, or fallback info."""
    if AER_AVAILABLE:
        return AerSimulator()
    return None


def run_single_qubit_circuit(
    initial_state: str = "0",
    gates: Optional[List[str]] = None,
    shots: int = 1024,
    measure: bool = True
) -> SimulationOutput:
    """
    Constructs and simulates a single-qubit quantum circuit.
    
    Parameters:
    - initial_state: "0" or "1"
    - gates: list of gate names e.g. ["X", "H", "Z"]
    - shots: number of measurement shots (1 to 100000)
    - measure: whether to append measurement to a classical register
    """
    if initial_state not in ("0", "1"):
        raise ValueError(f"Initial state must be '0' or '1', got '{initial_state}'")
    if shots < 1:
        raise ValueError("Shots must be at least 1.")

    gates = gates or []
    qc = QuantumCircuit(1, 1 if measure else 0)

    # Initialize state
    if initial_state == "1":
        qc.x(0)  # Prepare |1> from |0>

    # Apply gates in order
    for g in gates:
        g_upper = g.strip().upper()
        if g_upper == "X":
            qc.x(0)
        elif g_upper == "H":
            qc.h(0)
        elif g_upper == "Z":
            qc.z(0)
        elif g_upper == "I" or g_upper == "IDENTITY":
            qc.id(0)
        else:
            raise ValueError(f"Unsupported 1-qubit gate '{g}'. Supported: X, H, Z, I.")

    # Calculate exact statevector before measurement
    sv = Statevector.from_instruction(qc)
    amplitudes = [complex(sv.data[0]), complex(sv.data[1])]
    sv_labels = ["|0⟩", "|1⟩"]

    # Measure
    if measure:
        qc.measure(0, 0)

    # Run simulation
    counts = {}
    backend = get_simulator()
    if backend and measure:
        compiled_circuit = transpile(qc, backend)
        result = backend.run(compiled_circuit, shots=shots).result()
        counts = result.get_counts()
    elif measure:
        # Fallback exact sampling from Statevector
        probs = sv.probabilities()
        samples = np.random.choice([0, 1], size=shots, p=probs)
        c0 = int(np.sum(samples == 0))
        c1 = int(np.sum(samples == 1))
        if c0 > 0:
            counts["0"] = c0
        if c1 > 0:
            counts["1"] = c1

    # Ensure all states exist in dictionary for consistent reporting
    total_shots = sum(counts.values()) if counts else shots
    probabilities = {
        "0": counts.get("0", 0) / total_shots if total_shots > 0 else 0.0,
        "1": counts.get("1", 0) / total_shots if total_shots > 0 else 0.0
    }

    # Generate explanation
    explanation = _generate_1qubit_explanation(initial_state, gates, amplitudes, probabilities)

    return SimulationOutput(
        circuit=qc,
        circuit_text=str(qc.draw(output="text")),
        shots=shots,
        counts=counts,
        probabilities=probabilities,
        statevector=amplitudes,
        statevector_labels=sv_labels,
        explanation=explanation,
        gate_sequence=gates
    )


def run_z_interference_demo(shots: int = 1024) -> Dict[str, Any]:
    """
    Demonstrates quantum phase interference for Pauli-Z.
    
    The computational basis (|0>, |1>) alone cannot directly detect a phase flip
    because |alpha|^2 is unchanged.
    By creating superposition with H, applying Z, and then applying H again:
    |0> -> H -> |+> = (|0> + |1>)/sqrt(2)
        -> Z -> |-> = (|0> - |1>)/sqrt(2)
        -> H -> |1>
    
    Without the Z gate:
    |0> -> H -> H -> |0> (100% |0>)
    
    With the Z gate:
    |0> -> H -> Z -> H -> |1> (100% |1>)!
    """
    # Circuit 1: H -> H (Identity)
    qc_no_z = QuantumCircuit(1, 1)
    qc_no_z.h(0)
    qc_no_z.h(0)
    qc_no_z.measure(0, 0)
    
    # Circuit 2: H -> Z -> H (Phase interference converts phase flip into bit flip)
    qc_with_z = QuantumCircuit(1, 1)
    qc_with_z.h(0)
    qc_with_z.z(0)
    qc_with_z.h(0)
    qc_with_z.measure(0, 0)

    backend = get_simulator()
    if backend:
        res_no_z = backend.run(transpile(qc_no_z, backend), shots=shots).result().get_counts()
        res_with_z = backend.run(transpile(qc_with_z, backend), shots=shots).result().get_counts()
    else:
        res_no_z = {"0": shots}
        res_with_z = {"1": shots}

    return {
        "without_z": {
            "circuit_text": str(qc_no_z.draw(output="text")),
            "counts": res_no_z,
            "description": "Sequence: H → H. Constructive interference on |0⟩, destructive on |1⟩. Output is 100% |0⟩."
        },
        "with_z": {
            "circuit_text": str(qc_with_z.draw(output="text")),
            "counts": res_with_z,
            "description": "Sequence: H → Z → H. The Z-gate flips the relative phase of |1⟩ to -|1⟩. The second Hadamard causes destructive interference on |0⟩ and constructive interference on |1⟩! Output is 100% |1⟩."
        },
        "explanation": (
            "Phase Interference Principle: Quantum gates operate on complex probability amplitudes, "
            "not classical probabilities. A Z gate maps (|0⟩ + |1⟩)/√2 into (|0⟩ - |1⟩)/√2. "
            "Although both states have identical 50/50 measurement probabilities in the Z-basis, "
            "their relative phase differs by π radians (180°). Interference created by the second "
            "Hadamard gate maps this relative phase into a measurable computational-basis difference."
        )
    }


def run_two_qubit_cnot(
    initial_q0: int = 0,
    initial_q1: int = 0,
    control_qubit: int = 0,
    target_qubit: int = 1,
    apply_hadamard_to_control: bool = False,
    shots: int = 1024
) -> SimulationOutput:
    """
    Simulates a 2-qubit CNOT circuit.
    
    Parameters:
    - initial_q0, initial_q1: binary (0 or 1)
    - control_qubit: 0 or 1
    - target_qubit: 0 or 1 (must differ from control_qubit)
    - apply_hadamard_to_control: If True, creates Bell State |Phi+> = (|00> + |11>)/sqrt(2)
    """
    if control_qubit == target_qubit:
        raise ValueError("Control and Target qubits must be distinct.")
    if initial_q0 not in (0, 1) or initial_q1 not in (0, 1):
        raise ValueError("Initial qubit states must be 0 or 1.")

    qc = QuantumCircuit(2, 2)

    # Initialize states
    if initial_q0 == 1:
        qc.x(0)
    if initial_q1 == 1:
        qc.x(1)

    # Optional Hadamard for entanglement
    if apply_hadamard_to_control:
        qc.h(control_qubit)

    # Apply CNOT
    qc.cx(control_qubit, target_qubit)

    # Calculate Statevector
    sv = Statevector.from_instruction(qc)
    amplitudes = [complex(sv.data[i]) for i in range(4)]
    # Little-endian label ordering in Qiskit: |q1 q0>
    sv_labels = ["|00⟩", "|01⟩", "|10⟩", "|11⟩"]

    # Measure both qubits: q0 -> c0, q1 -> c1
    qc.measure([0, 1], [0, 1])

    # Run simulation
    backend = get_simulator()
    if backend:
        compiled = transpile(qc, backend)
        result = backend.run(compiled, shots=shots).result()
        counts = result.get_counts()
    else:
        probs = sv.probabilities()
        bitstrings = ["00", "01", "10", "11"]
        samples = np.random.choice(bitstrings, size=shots, p=probs)
        counts = {b: int(np.sum(samples == b)) for b in bitstrings if np.sum(samples == b) > 0}

    total_shots = sum(counts.values()) if counts else shots
    all_states = ["00", "01", "10", "11"]
    probabilities = {s: counts.get(s, 0) / total_shots for s in all_states}

    # Generate explanation
    ctrl_val = initial_q0 if control_qubit == 0 else initial_q1
    tgt_val = initial_q1 if target_qubit == 1 else initial_q0

    if apply_hadamard_to_control:
        explanation = (
            f"Bell State Generation (Entanglement): Applying H to control q{control_qubit} puts it into "
            f"superposition (|0⟩ + |1⟩)/√2. The subsequent CNOT(q{control_qubit} → q{target_qubit}) "
            f"entangles both qubits into the Bell state (|00⟩ + |11⟩)/√2. "
            f"Notice that the measurement yields either '00' or '11' with ~50% probability each, "
            f"and never '01' or '10'. Measuring one qubit immediately determines the other! "
            f"Note on Qiskit bit ordering: Qiskit displays bitstrings as 'q1 q0' (rightmost is q0)."
        )
    else:
        new_tgt_val = tgt_val ^ ctrl_val
        expected_q0 = ctrl_val if control_qubit == 0 else new_tgt_val
        expected_q1 = new_tgt_val if target_qubit == 1 else ctrl_val
        expected_bitstring = f"{expected_q1}{expected_q0}"
        
        explanation = (
            f"Deterministic CNOT Operation: Control is q{control_qubit} (value: {ctrl_val}), "
            f"Target is q{target_qubit} (initial: {tgt_val}). "
            f"Since control is {ctrl_val}, target {'flips to ' + str(new_tgt_val) if ctrl_val == 1 else 'remains ' + str(tgt_val)}. "
            f"Final state is |q1={expected_q1}, q0={expected_q0}⟩ = |{expected_bitstring}⟩. "
            f"In Qiskit's standard little-endian notation, the bitstring is '{expected_bitstring}'."
        )

    return SimulationOutput(
        circuit=qc,
        circuit_text=str(qc.draw(output="text")),
        shots=shots,
        counts=counts,
        probabilities=probabilities,
        statevector=amplitudes,
        statevector_labels=sv_labels,
        explanation=explanation
    )


def _generate_1qubit_explanation(
    initial_state: str,
    gates: List[str],
    amplitudes: List[complex],
    probabilities: Dict[str, float]
) -> str:
    """Generates educational narrative for single-qubit transformations."""
    alpha, beta = amplitudes[0], amplitudes[1]
    mag_alpha_sq = abs(alpha) ** 2
    mag_beta_sq = abs(beta) ** 2

    seq_str = " → ".join(gates) if gates else "None (Identity)"
    lines = [
        f"Initial State: |{initial_state}⟩",
        f"Applied Gate Sequence: {seq_str}",
        f"Final Statevector: |ψ⟩ = ({alpha.real:+.3f}{alpha.imag:+.3f}j)|0⟩ + ({beta.real:+.3f}{beta.imag:+.3f}j)|1⟩",
        f"Theoretical Probabilities: P(0) = |α|² = {mag_alpha_sq:.3f}, P(1) = |β|² = {mag_beta_sq:.3f}",
        f"Observed Measurement Probabilities (over simulated shots): P(0) = {probabilities['0']:.3f}, P(1) = {probabilities['1']:.3f}",
    ]

    # Specific conceptual insights
    if not gates:
        lines.append("No gates applied: Qubit remains in its basis state.")
    elif gates == ["X"]:
        lines.append("Pauli-X (Quantum NOT): Rotates state by π around X-axis. Inverts computational basis: X|0⟩ = |1⟩, X|1⟩ = |0⟩.")
    elif gates == ["H"]:
        lines.append("Hadamard Gate: Creates an equal superposition with zero relative phase: H|0⟩ = (|0⟩ + |1⟩)/√2 = |+⟩. Measurement yields ~50% '0' and ~50% '1'.")
    elif gates == ["Z"]:
        lines.append("Pauli-Z (Phase-Flip): Multiplies the |1⟩ component by -1 (adds π phase shift). Z|0⟩ = |0⟩. Measurement in Z-basis is identical to |0⟩, demonstrating why phase requires interference to observe.")
    elif gates == ["X", "H"]:
        lines.append("X followed by H: Prepares |1⟩ then applies H, yielding |−⟩ = (|0⟩ − |1⟩)/√2. Probabilities are 50/50, but relative phase is π.")
    elif gates == ["H", "Z", "H"]:
        lines.append("H → Z → H: Superposition is created, phase is flipped, and second Hadamard causes interference that steers the state deterministically to |1⟩!")

    return "\n".join(lines)
