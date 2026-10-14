"""
Noise Lab Simulation Module
Implements classical signal noise models, quantum noise channels (Bit-flip, Phase-flip, Depolarizing),
phase-sensitive interference diagnostics, and the 3-qubit quantum repetition error correction code.
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple, Any, Optional
import numpy as np

# Qiskit imports
from qiskit import QuantumCircuit, transpile
try:
    from qiskit_aer import AerSimulator
    from qiskit_aer.noise import NoiseModel, pauli_error, depolarizing_error
    AER_NOISE_AVAILABLE = True
except ImportError:
    AER_NOISE_AVAILABLE = False


@dataclass
class ClassicalNoiseResult:
    time_points: np.ndarray
    ideal_signal: np.ndarray
    noise: np.ndarray
    noisy_signal: np.ndarray
    threshold: float
    detected_bits: np.ndarray
    ideal_bits: np.ndarray
    bit_errors: np.ndarray
    total_samples: int
    error_count: int
    bit_error_rate: float
    snr_db: float
    explanation: str


@dataclass
class QuantumNoiseResult:
    noise_type: str
    error_rate: float
    ideal_counts: Dict[str, int]
    noisy_counts: Dict[str, int]
    circuit_text: str
    shots: int
    bit_error_rate: float
    explanation: str
    is_phase_sensitive: bool


def simulate_classical_noise(
    ideal_voltage: float = 5.0,
    noise_std: float = 1.2,
    threshold: float = 2.5,
    num_samples: int = 200,
    signal_type: str = "dc",
    random_seed: Optional[int] = 42
) -> ClassicalNoiseResult:
    """
    Simulates classical noise: V_out(t) = V_ideal(t) + n(t)
    where n(t) ~ Normal(0, noise_std^2).
    
    Parameters:
    - ideal_voltage: nominal HIGH voltage (e.g. 5.0V)
    - noise_std: standard deviation of Gaussian thermal/electronic noise
    - threshold: decision switching threshold (V_th)
    - num_samples: number of discrete time observations
    - signal_type: "dc" (constant HIGH) or "pulse" (alternating square wave)
    """
    if random_seed is not None:
        np.random.seed(random_seed)

    t = np.arange(num_samples)
    
    if signal_type == "pulse":
        # Square wave pulse train alternating between 0V and ideal_voltage every 20 samples
        period = 40
        ideal_signal = np.where((t % period) < (period // 2), ideal_voltage, 0.0)
    else:
        ideal_signal = np.full(num_samples, ideal_voltage)

    noise = np.random.normal(0, noise_std, size=num_samples)
    noisy_signal = ideal_signal + noise

    # Threshold detection: V >= V_th is interpreted as Logic 1, else Logic 0
    detected_bits = (noisy_signal >= threshold).astype(int)
    ideal_bits = (ideal_signal >= threshold).astype(int)

    bit_errors = detected_bits != ideal_bits
    error_count = int(np.sum(bit_errors))
    ber = error_count / num_samples

    # Signal to Noise Ratio (SNR) in dB
    signal_power = np.mean(ideal_signal ** 2)
    noise_power = noise_std ** 2
    snr_db = 10 * np.log10(signal_power / noise_power) if (noise_power > 0 and signal_power > 0) else 0.0

    explanation = (
        f"Classical Noise Analysis: V_out = V_ideal + n(t). "
        f"With an ideal signal of {ideal_voltage:.1f} V, switching threshold of {threshold:.1f} V, "
        f"and Gaussian noise standard deviation σ = {noise_std:.2f} V (SNR = {snr_db:.1f} dB), "
        f"{error_count} out of {num_samples} samples crossed the logic threshold erroneously "
        f"(Bit Error Rate: {ber * 100:.2f}%). This directly illustrates why semiconductor logic "
        f"requires wide noise margins (V_OH - V_IH and V_IL - V_OL)."
    )

    return ClassicalNoiseResult(
        time_points=t,
        ideal_signal=ideal_signal,
        noise=noise,
        noisy_signal=noisy_signal,
        threshold=threshold,
        detected_bits=detected_bits,
        ideal_bits=ideal_bits,
        bit_errors=bit_errors,
        total_samples=num_samples,
        error_count=error_count,
        bit_error_rate=ber,
        snr_db=snr_db,
        explanation=explanation
    )


def simulate_quantum_noise(
    noise_type: str = "bit_flip",
    error_rate: float = 0.15,
    circuit_mode: str = "standard",
    shots: int = 1024
) -> QuantumNoiseResult:
    """
    Simulates quantum channel noise using Qiskit Aer noise models.
    
    Supported noise types:
    - 'bit_flip': Pauli-X error with probability p
    - 'phase_flip': Pauli-Z error with probability p
    - 'depolarizing': Depolarizing error with probability p
    
    Circuit modes:
    - 'standard': |0> -> [Noise on ID] -> Measure (measures in Z-basis)
    - 'phase_sensitive': |0> -> H -> [Noise on ID] -> H -> Measure (reveals phase flips via interference)
    """
    if not (0.0 <= error_rate <= 1.0):
        raise ValueError("Error rate must be between 0.0 and 1.0")

    qc = QuantumCircuit(1, 1)
    is_phase = (circuit_mode == "phase_sensitive")

    if is_phase:
        qc.h(0)
        qc.id(0)
        qc.h(0)
    else:
        qc.id(0)

    qc.measure(0, 0)

    # Ideal outcomes:
    # In standard mode on |0>, ideal is '0'
    # In phase-sensitive mode (H -> Id -> H) on |0>, ideal is also '0' (H^2 = I)
    ideal_counts = {"0": shots, "1": 0}

    # Simulate with Qiskit Aer NoiseModel
    noisy_counts = {}
    if AER_NOISE_AVAILABLE and error_rate > 0.0:
        noise_model = NoiseModel()
        
        if noise_type == "bit_flip":
            err = pauli_error([('X', error_rate), ('I', 1 - error_rate)])
            noise_model.add_all_qubit_quantum_error(err, ['id'])
        elif noise_type == "phase_flip":
            err = pauli_error([('Z', error_rate), ('I', 1 - error_rate)])
            noise_model.add_all_qubit_quantum_error(err, ['id'])
        elif noise_type == "depolarizing":
            err = depolarizing_error(error_rate, 1)
            noise_model.add_all_qubit_quantum_error(err, ['id'])

        sim_noise = AerSimulator(noise_model=noise_model)
        # optimization_level=0 prevents transpile from removing the 'id' instruction
        compiled = transpile(qc, sim_noise, optimization_level=0)
        res = sim_noise.run(compiled, shots=shots).result()
        raw_counts = res.get_counts()
        noisy_counts = {"0": raw_counts.get("0", 0), "1": raw_counts.get("1", 0)}
    else:
        # Fallback simulation
        if noise_type == "bit_flip":
            p1 = error_rate if not is_phase else 0.0
        elif noise_type == "phase_flip":
            p1 = 0.0 if not is_phase else error_rate
        elif noise_type == "depolarizing":
            p1 = (2.0 / 3.0) * error_rate
        else:
            p1 = 0.0

        n1 = int(np.random.binomial(shots, p1))
        noisy_counts = {"0": shots - n1, "1": n1}

    if "0" not in noisy_counts:
        noisy_counts["0"] = 0
    if "1" not in noisy_counts:
        noisy_counts["1"] = 0

    ber = noisy_counts["1"] / shots

    # Educational narrative
    if noise_type == "bit_flip" and not is_phase:
        explanation = (
            f"Bit-Flip Error (X-Noise): Causes state inversion |0⟩ ↔ |1⟩ with probability p = {error_rate:.2f}. "
            f"Observed bit error rate: {ber * 100:.1f}%. This directly mimics classical voltage spike bit flips."
        )
    elif noise_type == "bit_flip" and is_phase:
        explanation = (
            f"Bit-Flip Error in Hadamard Basis: In the Hadamard basis (|+⟩, |−⟩), an X gate preserves |+⟩ (since X|+⟩ = |+⟩) "
            f"and inverts |−⟩ into -|−⟩. Thus, after the second Hadamard, the measurement yields '0' with virtually 0 bit errors. "
            f"This illustrates the dual relationship between bit flips and phase flips under Fourier/Hadamard transformation."
        )
    elif noise_type == "phase_flip" and not is_phase:
        explanation = (
            f"Phase-Flip Error (Z-Noise) in Computational Basis: Z|0⟩ = |0⟩ and Z|1⟩ = -|1⟩. "
            f"Notice that the measured BER is 0.0% ({ber * 100:.1f}%)! "
            f"Standard computational basis measurement alone CANNOT detect phase noise, "
            f"because relative phase shifts do not alter |α|² or |β|² without interference. "
            f"Switch to 'Phase-Sensitive Circuit (H-Noise-H)' to see how this phase error is revealed!"
        )
    elif noise_type == "phase_flip" and is_phase:
        explanation = (
            f"Phase-Flip Error in Phase-Sensitive Circuit: Applying H before and after creates quantum interference. "
            f"Because H · Z · H = X, a phase flip in the computational basis becomes a bit flip in the Hadamard basis! "
            f"Observed error rate: {ber * 100:.1f}%. This proves that quantum phase noise is physically real, destructive, "
            f"and requires specialized quantum error correction (unlike classical circuits which only suffer bit flips)."
        )
    elif noise_type == "depolarizing":
        explanation = (
            f"Depolarizing Noise: Represents isotropic decoherence where the qubit decays into the maximally "
            f"mixed state I/2 with probability p = {error_rate:.2f}. "
            f"It combines bit-flip, phase-flip, and combined bit-phase (Y) errors. "
            f"Observed error rate: {ber * 100:.1f}%."
        )
    else:
        explanation = f"Quantum noise simulation complete with error rate {error_rate:.2f}."

    return QuantumNoiseResult(
        noise_type=noise_type,
        error_rate=error_rate,
        ideal_counts=ideal_counts,
        noisy_counts=noisy_counts,
        circuit_text=str(qc.draw(output="text")),
        shots=shots,
        bit_error_rate=ber,
        explanation=explanation,
        is_phase_sensitive=is_phase
    )


def simulate_3qubit_repetition_code(
    initial_logical_bit: int = 0,
    error_qubit: str = "q1",
    shots: int = 1024
) -> Dict[str, Any]:
    """
    Demonstrates the 3-Qubit Bit-Flip Repetition Code (Quantum Error Correction).
    
    Process:
    1. Encode:
       |0>_L = |000>
       |1>_L = |111>
       Encoding circuit: CNOT(0->1), CNOT(0->2)
    2. Channel / Error Injection:
       Apply Pauli-X to one of the physical qubits (q0, q1, q2, or none)
    3. Syndrome Extraction & Correction:
       Majority voting decoding using standard Toffoli / CNOT logic:
       - Parity check and conditional flip of corrupted qubit
       - Decodes back to logical state on qubit 0
    """
    if initial_logical_bit not in (0, 1):
        raise ValueError("Initial logical bit must be 0 or 1.")

    qc = QuantumCircuit(3, 1)

    # Step 1: Initialize logical state on qubit 0
    if initial_logical_bit == 1:
        qc.x(0)

    # Step 2: Encode into 3-qubit repetition code
    qc.cx(0, 1)
    qc.cx(0, 2)
    qc.barrier()

    # Step 3: Error injection
    if error_qubit == "q0":
        qc.x(0)
    elif error_qubit == "q1":
        qc.x(1)
    elif error_qubit == "q2":
        qc.x(2)
    qc.barrier()

    # Step 4: Majority-vote syndrome decoding and error correction
    qc.cx(0, 1)
    qc.cx(0, 2)
    qc.ccx(2, 1, 0)
    qc.barrier()

    # Measure logical output on qubit 0
    qc.measure(0, 0)

    backend = None
    if AER_NOISE_AVAILABLE:
        backend = AerSimulator()

    if backend:
        compiled = transpile(qc, backend, optimization_level=0)
        counts = backend.run(compiled, shots=shots).result().get_counts()
    else:
        counts = {str(initial_logical_bit): shots}

    c0 = counts.get("0", 0)
    c1 = counts.get("1", 0)
    measured_logical = 0 if c0 > c1 else 1
    success = (measured_logical == initial_logical_bit)

    explanation = (
        f"3-Qubit Repetition Code Analysis:\n"
        f"• Initial Logical State: |{initial_logical_bit}_L⟩ (encoded as |{initial_logical_bit}{initial_logical_bit}{initial_logical_bit}⟩).\n"
        f"• Injected Error: {f'Bit-flip (X) on {error_qubit}' if error_qubit != 'none' else 'None (Clean channel)'}.\n"
        f"• Syndrome & Correction: The parity syndrome checks detect which qubit diverged. "
        f"The Toffoli (CCX) gate restores the corrupted qubit to match the majority.\n"
        f"• Decoded Output: |{measured_logical}⟩ with {counts.get(str(measured_logical), 0)}/{shots} shots (Success: {success}).\n\n"
        f"IMPORTANT LIMITATIONS:\n"
        f"1. This code ONLY corrects a single BIT-FLIP (X) error. It does NOT protect against PHASE-FLIP (Z) errors. "
        f"In fact, a single Z error on any of the three qubits corrupts the relative phase of the entire logical state!\n"
        f"2. To correct both bit-flips and phase-flips, a full code such as Shor's 9-qubit code, the 7-qubit Steane code, "
        f"or the Surface Code with fault-tolerant stabilizer measurements is required."
    )

    return {
        "circuit_text": str(qc.draw(output="text")),
        "initial_logical": initial_logical_bit,
        "error_qubit": error_qubit,
        "counts": counts,
        "measured_logical": measured_logical,
        "success": success,
        "explanation": explanation
    }
