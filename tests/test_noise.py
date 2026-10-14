"""
Unit tests for Noise Lab Module.
Tests classical Gaussian noise, quantum noise models, phase-sensitive interference, and 3-qubit QEC.
"""

import pytest
import numpy as np
from src.noise import (
    simulate_classical_noise,
    simulate_quantum_noise,
    simulate_3qubit_repetition_code
)


def test_classical_noise_dc_validity():
    """Test classical noise on a DC HIGH signal with valid error rates and SNR."""
    res = simulate_classical_noise(
        ideal_voltage=5.0,
        noise_std=1.0,
        threshold=2.5,
        num_samples=500,
        signal_type="dc",
        random_seed=123
    )
    assert res.total_samples == 500
    assert 0.0 <= res.bit_error_rate <= 1.0
    assert res.snr_db > 0.0
    assert len(res.noisy_signal) == 500
    assert len(res.bit_errors) == 500


def test_classical_noise_pulse_validity():
    """Test classical noise on a square pulse signal."""
    res = simulate_classical_noise(
        ideal_voltage=5.0,
        noise_std=0.5,
        threshold=2.5,
        num_samples=200,
        signal_type="pulse",
        random_seed=456
    )
    assert res.total_samples == 200
    assert 0.0 <= res.bit_error_rate <= 0.1  # Low noise should result in low BER


def test_quantum_noise_bit_flip():
    """Test quantum bit-flip noise channel."""
    shots = 1000
    error_rate = 0.20
    res = simulate_quantum_noise(
        noise_type="bit_flip",
        error_rate=error_rate,
        circuit_mode="standard",
        shots=shots
    )
    total_counts = sum(res.noisy_counts.values())
    assert total_counts == shots
    assert 0.0 <= res.bit_error_rate <= 1.0
    # For error rate 0.20, observed BER should be close to 0.20 (+/- 0.06)
    assert 0.14 <= res.bit_error_rate <= 0.26


def test_quantum_noise_phase_flip_hidden_in_standard():
    """
    Test that phase-flip error (Z) is INVISIBLE in standard computational basis measurement.
    Initial state is |0>, Z|0> = |0>. Measurement yields 0% bit error!
    """
    shots = 1000
    error_rate = 0.30
    res = simulate_quantum_noise(
        noise_type="phase_flip",
        error_rate=error_rate,
        circuit_mode="standard",
        shots=shots
    )
    assert res.bit_error_rate == 0.0
    assert res.noisy_counts.get("0", 0) == shots


def test_quantum_noise_phase_flip_revealed_in_phase_sensitive():
    """
    Test that phase-flip error (Z) IS REVEALED when using phase-sensitive circuit (H -> Noise -> H).
    H · Z · H = X, so phase flips become bit flips with probability equal to error_rate.
    """
    shots = 1000
    error_rate = 0.30
    res = simulate_quantum_noise(
        noise_type="phase_flip",
        error_rate=error_rate,
        circuit_mode="phase_sensitive",
        shots=shots
    )
    assert 0.23 <= res.bit_error_rate <= 0.37


def test_quantum_noise_invalid_error_rate():
    """Test that invalid error rates (> 1.0 or < 0.0) are rejected."""
    with pytest.raises(ValueError, match="between 0.0 and 1.0"):
        simulate_quantum_noise(noise_type="bit_flip", error_rate=1.5)
    with pytest.raises(ValueError, match="between 0.0 and 1.0"):
        simulate_quantum_noise(noise_type="bit_flip", error_rate=-0.1)


@pytest.mark.parametrize("error_qubit", ["none", "q0", "q1", "q2"])
@pytest.mark.parametrize("initial_bit", [0, 1])
def test_3qubit_repetition_code_correction(error_qubit, initial_bit):
    """
    Test 3-qubit repetition code successfully corrects single bit-flip error
    on any of the three physical qubits for both logical |0> and |1>.
    """
    res = simulate_3qubit_repetition_code(
        initial_logical_bit=initial_bit,
        error_qubit=error_qubit,
        shots=500
    )
    assert res["success"] is True
    assert res["measured_logical"] == initial_bit
