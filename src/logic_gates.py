"""
Logic Gate Simulator Module
Implements classical boolean logic gates (NOT, AND, OR, NAND, NOR, XOR)
along with truth tables, validation, and composite logic demonstrations.
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple, Any


@dataclass
class GateEvaluation:
    gate_name: str
    inputs: Tuple[int, ...]
    output: int
    truth_table: List[Dict[str, Any]]
    explanation: str
    circuit_formula: str


# Truth table definitions for all 6 gates
TRUTH_TABLES: Dict[str, List[Dict[str, int]]] = {
    "NOT": [
        {"A": 0, "OUT": 1},
        {"A": 1, "OUT": 0},
    ],
    "AND": [
        {"A": 0, "B": 0, "OUT": 0},
        {"A": 0, "B": 1, "OUT": 0},
        {"A": 1, "B": 0, "OUT": 0},
        {"A": 1, "B": 1, "OUT": 1},
    ],
    "OR": [
        {"A": 0, "B": 0, "OUT": 0},
        {"A": 0, "B": 1, "OUT": 1},
        {"A": 1, "B": 0, "OUT": 1},
        {"A": 1, "B": 1, "OUT": 1},
    ],
    "NAND": [
        {"A": 0, "B": 0, "OUT": 1},
        {"A": 0, "B": 1, "OUT": 1},
        {"A": 1, "B": 0, "OUT": 1},
        {"A": 1, "B": 1, "OUT": 0},
    ],
    "NOR": [
        {"A": 0, "B": 0, "OUT": 1},
        {"A": 0, "B": 1, "OUT": 0},
        {"A": 1, "B": 0, "OUT": 0},
        {"A": 1, "B": 1, "OUT": 0},
    ],
    "XOR": [
        {"A": 0, "B": 0, "OUT": 0},
        {"A": 0, "B": 1, "OUT": 1},
        {"A": 1, "B": 0, "OUT": 1},
        {"A": 1, "B": 1, "OUT": 0},
    ],
}


def evaluate_gate(gate_name: str, a: int, b: int = 0) -> GateEvaluation:
    """
    Evaluates a logic gate given input A (and optional B).
    Validates inputs and returns full evaluation details.
    """
    gate = gate_name.upper()
    if a not in (0, 1):
        raise ValueError(f"Input A must be binary (0 or 1), got {a}")
    if gate != "NOT" and b not in (0, 1):
        raise ValueError(f"Input B must be binary (0 or 1), got {b}")

    if gate == "NOT":
        out = 1 if a == 0 else 0
        inputs = (a,)
        explanation = (
            f"NOT Inverter: Inverts the single input. "
            f"Given input A={a}, output is {out}. "
            f"Implemented classically with a single NPN transistor switch in common-emitter mode."
        )
        formula = f"OUT = NOT({a}) = {out}"

    elif gate == "AND":
        out = 1 if (a == 1 and b == 1) else 0
        inputs = (a, b)
        explanation = (
            f"AND Gate: Output is HIGH (1) if and only if BOTH inputs are HIGH (1). "
            f"Since A={a} and B={b}, output is {out}. "
            f"In semiconductor logic, requires transistors in series."
        )
        formula = f"OUT = {a} AND {b} = {out}"

    elif gate == "OR":
        out = 1 if (a == 1 or b == 1) else 0
        inputs = (a, b)
        explanation = (
            f"OR Gate: Output is HIGH (1) if AT LEAST ONE input is HIGH (1). "
            f"Since A={a} and B={b}, output is {out}. "
            f"In semiconductor logic, constructed with transistors in parallel."
        )
        formula = f"OUT = {a} OR {b} = {out}"

    elif gate == "NAND":
        out = 0 if (a == 1 and b == 1) else 1
        inputs = (a, b)
        explanation = (
            f"NAND Gate (NOT-AND): Universal gate. Output is LOW (0) ONLY when both inputs are HIGH (1). "
            f"Since A={a} and B={b}, output is {out}. "
            f"Any boolean circuit can be constructed using solely NAND gates."
        )
        formula = f"OUT = NOT({a} AND {b}) = {out}"

    elif gate == "NOR":
        out = 1 if (a == 0 and b == 0) else 0
        inputs = (a, b)
        explanation = (
            f"NOR Gate (NOT-OR): Universal gate. Output is HIGH (1) ONLY when both inputs are LOW (0). "
            f"Since A={a} and B={b}, output is {out}. "
            f"Like NAND, NOR is functionally complete."
        )
        formula = f"OUT = NOT({a} OR {b}) = {out}"

    elif gate == "XOR":
        out = 1 if a != b else 0
        inputs = (a, b)
        explanation = (
            f"XOR Gate (Exclusive-OR): Output is HIGH (1) when inputs are DIFFERENT (one 0 and one 1). "
            f"Since A={a} and B={b}, output is {out}. "
            f"Crucial in binary arithmetic, parity checking, and reversible computing."
        )
        formula = f"OUT = {a} XOR {b} = {out}"

    else:
        raise ValueError(f"Unsupported gate: '{gate_name}'. Choose from NOT, AND, OR, NAND, NOR, XOR.")

    table = TRUTH_TABLES[gate]
    
    # Self-validation against canonical truth table
    match_found = False
    for row in table:
        if gate == "NOT":
            if row["A"] == a and row["OUT"] == out:
                match_found = True
                break
        else:
            if row["A"] == a and row["B"] == b and row["OUT"] == out:
                match_found = True
                break
    
    if not match_found:
        raise RuntimeError(f"Internal validation failed for {gate} with inputs {inputs}")

    return GateEvaluation(
        gate_name=gate,
        inputs=inputs,
        output=out,
        truth_table=table,
        explanation=explanation,
        circuit_formula=formula
    )


def simulate_half_adder(a: int, b: int) -> Dict[str, Any]:
    """
    Combined logic demonstration: Half Adder.
    Sum = A XOR B
    Carry = A AND B
    """
    sum_val = evaluate_gate("XOR", a, b).output
    carry_val = evaluate_gate("AND", a, b).output
    return {
        "A": a,
        "B": b,
        "Sum": sum_val,
        "Carry": carry_val,
        "BinarySum": f"{carry_val}{sum_val}",
        "DecimalSum": a + b,
        "Formula": f"Sum = {a} ⊕ {b} = {sum_val}; Carry = {a} · {b} = {carry_val}"
    }


def simulate_2to1_mux(d0: int, d1: int, sel: int) -> Dict[str, Any]:
    """
    Combined logic demonstration: 2-to-1 Multiplexer.
    OUT = (D0 AND NOT(SEL)) OR (D1 AND SEL)
    """
    not_sel = evaluate_gate("NOT", sel).output
    term0 = evaluate_gate("AND", d0, not_sel).output
    term1 = evaluate_gate("AND", d1, sel).output
    out = evaluate_gate("OR", term0, term1).output
    return {
        "D0": d0,
        "D1": d1,
        "SEL": sel,
        "OUT": out,
        "Selected": f"D{sel} (value: {d1 if sel == 1 else d0})",
        "Formula": f"OUT = ({d0} · ¬{sel}) + ({d1} · {sel}) = {out}"
    }
