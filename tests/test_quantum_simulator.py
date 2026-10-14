"""
Unit tests for Quantum Simulator Module.
Tests single-qubit gates, superposition statistics, CNOT logic, Bell states, and phase interference.
"""

import pytest
import numpy as np
from src.quantum_simulator import (
    run_single_qubit_circuit,
    run_two_qubit_cnot,
    run_z_interference_demo
)


def test_x_gate_on_zero():
    """Test X|0⟩ = |1⟩ with 100% deterministic measurement."""
    shots = 500
    res = run_single_qubit_circuit(initial_state="0", gates=["X"], shots=shots)
    assert res.counts.get("1", 0) == shots
    assert res.counts.get("0", 0) == 0
    assert res.probabilities["1"] == 1.0
    # Statevector check: alpha=0, beta=1
    assert abs(res.statevector[0]) < 1e-6
    assert pytest.approx(abs(res.statevector[1]), 1e-5) == 1.0


def test_x_gate_on_one():
    """Test X|1⟩ = |0⟩ with 100% deterministic measurement."""
    shots = 500
    res = run_single_qubit_circuit(initial_state="1", gates=["X"], shots=shots)
    assert res.counts.get("0", 0) == shots
    assert res.counts.get("1", 0) == 0
    assert res.probabilities["0"] == 1.0
    # Statevector check: alpha=1, beta=0
    assert pytest.approx(abs(res.statevector[0]), 1e-5) == 1.0
    assert abs(res.statevector[1]) < 1e-6


def test_hadamard_superposition_distribution():
    """
    Test H|0⟩ over 2000 shots.
    Expectation: P(0) ≈ 0.50, P(1) ≈ 0.50 within binomial sampling tolerance (3 sigma ~ +/- 0.035).
    """
    shots = 2000
    res = run_single_qubit_circuit(initial_state="0", gates=["H"], shots=shots)
    p0 = res.probabilities["0"]
    p1 = res.probabilities["1"]
    
    assert 0.43 <= p0 <= 0.57, f"Observed P(0)={p0} outside statistical tolerance [0.43, 0.57]"
    assert 0.43 <= p1 <= 0.57, f"Observed P(1)={p1} outside statistical tolerance [0.43, 0.57]"
    assert p0 + p1 == pytest.approx(1.0, 1e-6)

    # Statevector check: alpha = 1/sqrt(2), beta = 1/sqrt(2)
    expected_amp = 1.0 / np.sqrt(2)
    assert pytest.approx(abs(res.statevector[0]), 1e-4) == expected_amp
    assert pytest.approx(abs(res.statevector[1]), 1e-4) == expected_amp


@pytest.mark.parametrize("q0,q1,ctrl,tgt,expected_bitstring", [
    (0, 0, 0, 1, "00"),  # ctrl q0=0, tgt q1=0 -> no flip -> "00"
    (0, 1, 0, 1, "10"),  # ctrl q0=0, tgt q1=1 -> no flip -> "10"
    (1, 0, 0, 1, "11"),  # ctrl q0=1, tgt q1=0 -> flip tgt to 1 -> "11"
    (1, 1, 0, 1, "01"),  # ctrl q0=1, tgt q1=1 -> flip tgt to 0 -> "01"
    (0, 1, 1, 0, "11"),  # ctrl q1=1, tgt q0=0 -> flip tgt to 1 -> "11"
    (0, 0, 1, 0, "00"),  # ctrl q1=0, tgt q0=0 -> no flip -> "00"
])
def test_cnot_computational_basis(q0, q1, ctrl, tgt, expected_bitstring):
    """
    Test CNOT gate across computational basis inputs.
    Note Qiskit bitstring ordering is 'q1 q0'.
    """
    shots = 400
    res = run_two_qubit_cnot(
        initial_q0=q0,
        initial_q1=q1,
        control_qubit=ctrl,
        target_qubit=tgt,
        apply_hadamard_to_control=False,
        shots=shots
    )
    assert res.counts.get(expected_bitstring, 0) == shots


def test_cnot_bell_state_entanglement():
    """
    Test Bell State (|00⟩ + |11⟩)/sqrt(2) preparation using H and CNOT.
    Correlations: should only measure '00' or '11', zero '01' or '10'.
    """
    shots = 2000
    res = run_two_qubit_cnot(
        initial_q0=0,
        initial_q1=0,
        control_qubit=0,
        target_qubit=1,
        apply_hadamard_to_control=True,
        shots=shots
    )
    assert res.counts.get("01", 0) == 0
    assert res.counts.get("10", 0) == 0
    p00 = res.probabilities["00"]
    p11 = res.probabilities["11"]
    assert 0.43 <= p00 <= 0.57
    assert 0.43 <= p11 <= 0.57


def test_z_gate_phase_interference():
    """
    Test phase interference demonstration:
    H -> H gives 100% |0>
    H -> Z -> H gives 100% |1>
    """
    demo = run_z_interference_demo(shots=500)
    assert demo["without_z"]["counts"].get("0", 0) == 500
    assert demo["with_z"]["counts"].get("1", 0) == 500
