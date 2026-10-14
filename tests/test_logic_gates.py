"""
Unit tests for Classical Logic Gate Simulator Module.
Tests every classical logic gate across every possible input combination.
"""

import pytest
from src.logic_gates import evaluate_gate, simulate_half_adder, simulate_2to1_mux, TRUTH_TABLES


@pytest.mark.parametrize("a,expected", [
    (0, 1),
    (1, 0),
])
def test_not_gate_all_combinations(a, expected):
    """Test NOT gate across all possible inputs (0, 1)."""
    res = evaluate_gate("NOT", a)
    assert res.output == expected
    assert res.inputs == (a,)
    assert res.gate_name == "NOT"


@pytest.mark.parametrize("a,b,expected", [
    (0, 0, 0),
    (0, 1, 0),
    (1, 0, 0),
    (1, 1, 1),
])
def test_and_gate_all_combinations(a, b, expected):
    """Test AND gate across all 4 input combinations."""
    res = evaluate_gate("AND", a, b)
    assert res.output == expected
    assert res.inputs == (a, b)


@pytest.mark.parametrize("a,b,expected", [
    (0, 0, 0),
    (0, 1, 1),
    (1, 0, 1),
    (1, 1, 1),
])
def test_or_gate_all_combinations(a, b, expected):
    """Test OR gate across all 4 input combinations."""
    res = evaluate_gate("OR", a, b)
    assert res.output == expected
    assert res.inputs == (a, b)


@pytest.mark.parametrize("a,b,expected", [
    (0, 0, 1),
    (0, 1, 1),
    (1, 0, 1),
    (1, 1, 0),
])
def test_nand_gate_all_combinations(a, b, expected):
    """Test NAND gate across all 4 input combinations."""
    res = evaluate_gate("NAND", a, b)
    assert res.output == expected
    assert res.inputs == (a, b)


@pytest.mark.parametrize("a,b,expected", [
    (0, 0, 1),
    (0, 1, 0),
    (1, 0, 0),
    (1, 1, 0),
])
def test_nor_gate_all_combinations(a, b, expected):
    """Test NOR gate across all 4 input combinations."""
    res = evaluate_gate("NOR", a, b)
    assert res.output == expected
    assert res.inputs == (a, b)


@pytest.mark.parametrize("a,b,expected", [
    (0, 0, 0),
    (0, 1, 1),
    (1, 0, 1),
    (1, 1, 0),
])
def test_xor_gate_all_combinations(a, b, expected):
    """Test XOR gate across all 4 input combinations."""
    res = evaluate_gate("XOR", a, b)
    assert res.output == expected
    assert res.inputs == (a, b)


def test_invalid_gate_inputs():
    """Test that non-binary inputs raise ValueError."""
    with pytest.raises(ValueError, match="Input A must be binary"):
        evaluate_gate("AND", 2, 0)
    with pytest.raises(ValueError, match="Input B must be binary"):
        evaluate_gate("AND", 0, -1)
    with pytest.raises(ValueError, match="Unsupported gate"):
        evaluate_gate("INVALID_GATE", 0, 0)


def test_half_adder_all_combinations():
    """Test half adder composite circuit across all 4 binary additions."""
    add_00 = simulate_half_adder(0, 0)
    assert add_00["Sum"] == 0 and add_00["Carry"] == 0 and add_00["DecimalSum"] == 0

    add_01 = simulate_half_adder(0, 1)
    assert add_01["Sum"] == 1 and add_01["Carry"] == 0 and add_01["DecimalSum"] == 1

    add_10 = simulate_half_adder(1, 0)
    assert add_10["Sum"] == 1 and add_10["Carry"] == 0 and add_10["DecimalSum"] == 1

    add_11 = simulate_half_adder(1, 1)
    assert add_11["Sum"] == 0 and add_11["Carry"] == 1 and add_11["DecimalSum"] == 2


def test_2to1_mux_all_combinations():
    """Test 2-to-1 Multiplexer for SEL=0 and SEL=1 routing."""
    # When SEL=0, OUT should equal D0
    mux_sel0 = simulate_2to1_mux(d0=1, d1=0, sel=0)
    assert mux_sel0["OUT"] == 1

    mux_sel0_b = simulate_2to1_mux(d0=0, d1=1, sel=0)
    assert mux_sel0_b["OUT"] == 0

    # When SEL=1, OUT should equal D1
    mux_sel1 = simulate_2to1_mux(d0=0, d1=1, sel=1)
    assert mux_sel1["OUT"] == 1

    mux_sel1_b = simulate_2to1_mux(d0=1, d1=0, sel=1)
    assert mux_sel1_b["OUT"] == 0
