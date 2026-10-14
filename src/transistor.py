"""
Transistor Switching Simulator Module
Implements educational simulation of an NPN BJT switching circuit with LED load.

IMPORTANT DISCLAIMER:
This model is a simplified piecewise-linear educational approximation
designed to demonstrate binary switching behavior (cutoff vs saturation),
not a full non-linear semiconductor physics model (such as Ebers-Moll or SPICE).
All results are SIMULATED and do not constitute actual physical measurements.
"""

from dataclasses import dataclass
from typing import Dict, Any, List, Optional
import pandas as pd
import numpy as np


@dataclass
class TransistorParameters:
    v_in: float           # Base / Input voltage (V)
    v_th: float           # Switching threshold / V_BE(on) (V) (default: 0.7V)
    v_cc: float           # Supply voltage (V) (default: 5.0V)
    r_load: float         # Collector / Load resistor R_C (Ohms) (default: 330.0)
    v_led_forward: float  # LED forward voltage drop V_F (V) (default: 2.0V)
    v_ce_sat: float       # Transistor saturation voltage V_CE(sat) (V) (default: 0.2V)
    r_base: float = 1000.0  # Base resistor R_B (Ohms) (default: 1000.0)


@dataclass
class SimulationResult:
    is_on: bool
    state_label: str
    collector_current_ma: float
    collector_current_a: float
    v_out_collector: float
    led_is_lit: bool
    led_state_label: str
    explanation: str
    disclaimer: str


def validate_parameters(params: TransistorParameters) -> List[str]:
    """Validate transistor parameters to prevent division by zero or non-physical values."""
    errors = []
    if params.r_load <= 0:
        errors.append("Load resistance (R_load) must be strictly greater than 0 Ω to prevent division by zero.")
    if params.r_base <= 0:
        errors.append("Base resistance (R_base) must be strictly greater than 0 Ω.")
    if params.v_in < 0:
        errors.append("Input voltage (V_in) cannot be negative in this unipolar model.")
    if params.v_cc < 0:
        errors.append("Supply voltage (V_cc) cannot be negative.")
    if params.v_th <= 0:
        errors.append("Switching threshold (V_th) must be greater than 0 V.")
    if params.v_ce_sat < 0:
        errors.append("Saturation voltage (V_ce_sat) cannot be negative.")
    if params.v_led_forward < 0:
        errors.append("LED forward voltage cannot be negative.")
    return errors


def simulate_transistor_switch(params: TransistorParameters) -> SimulationResult:
    """
    Simulates the NPN switching circuit.
    
    Logic:
    - If V_in < V_th: The base-emitter junction is not forward biased.
      Transistor is in CUTOFF (OFF).
      Collector current I_C = 0 mA.
      LED is OFF.
      Output voltage at collector V_out ≈ V_cc.
    - If V_in >= V_th: The base-emitter junction conducts.
      Transistor is driven into SATURATION (ON) in a properly designed switch.
      Collector current:
        I_C = max(0, (V_cc - V_led_forward - V_ce_sat) / R_load)
      LED is ON if I_C > 0 mA.
      Output voltage at collector V_out ≈ V_ce_sat (Logic LOW output / Inverter behavior).
    """
    errors = validate_parameters(params)
    if errors:
        raise ValueError("; ".join(errors))

    is_on = params.v_in >= params.v_th

    disclaimer = (
        "Simulated educational approximation. Not a physical hardware measurement. "
        "Real semiconductor devices exhibit continuous exponential diode characteristics, "
        "temperature dependency, and parasitic capacitances."
    )

    if not is_on:
        i_c_a = 0.0
        i_c_ma = 0.0
        v_out = params.v_cc
        led_lit = False
        explanation = (
            f"Input voltage ({params.v_in:.3f} V) is BELOW switching threshold "
            f"({params.v_th:.3f} V). The base-emitter junction remains reverse/un-biased. "
            f"Transistor is in CUTOFF (OFF state). No collector current flows (I_C = 0.0 mA). "
            f"The LED does not emit light. Collector node rests at pull-up supply voltage ({params.v_cc:.2f} V)."
        )
    else:
        # Check if supply is sufficient to overcome LED forward drop + V_ce_sat
        voltage_headroom = params.v_cc - params.v_led_forward - params.v_ce_sat
        if voltage_headroom > 0:
            i_c_a = voltage_headroom / params.r_load
            i_c_ma = i_c_a * 1000.0
            led_lit = True
            v_out = params.v_ce_sat
            explanation = (
                f"Input voltage ({params.v_in:.3f} V) is AT OR ABOVE threshold "
                f"({params.v_th:.3f} V). Base current drives transistor into SATURATION (ON state). "
                f"Collector-emitter junction conducts with V_CE(sat) ≈ {params.v_ce_sat:.2f} V. "
                f"Collector current of {i_c_ma:.2f} mA flows through the load resistor and LED, "
                f"lighting up the LED."
            )
        else:
            i_c_a = 0.0
            i_c_ma = 0.0
            led_lit = False
            v_out = params.v_cc
            explanation = (
                f"Transistor base is forward biased (V_in = {params.v_in:.3f} V >= V_th = {params.v_th:.3f} V), "
                f"but supply voltage V_CC ({params.v_cc:.2f} V) is INSUFFICIENT to overcome the LED forward "
                f"drop ({params.v_led_forward:.2f} V) + V_CE(sat) ({params.v_ce_sat:.2f} V). "
                f"No collector current can flow (I_C = 0.0 mA)."
            )

    return SimulationResult(
        is_on=is_on,
        state_label="ON (Saturated)" if is_on else "OFF (Cutoff)",
        collector_current_ma=i_c_ma,
        collector_current_a=i_c_a,
        v_out_collector=v_out,
        led_is_lit=led_lit,
        led_state_label="LIT (Illuminated)" if led_lit else "UNLIT (Dark)",
        explanation=explanation,
        disclaimer=disclaimer
    )


def generate_transfer_curve(params: TransistorParameters, v_in_max: float = 5.0, steps: int = 200) -> Dict[str, np.ndarray]:
    """Generates the V_in vs I_c and V_out transfer characteristics."""
    v_in_range = np.linspace(0.0, max(v_in_max, params.v_th * 1.5, 3.0), steps)
    i_c_vals = []
    v_out_vals = []
    
    for v in v_in_range:
        temp_params = TransistorParameters(
            v_in=v,
            v_th=params.v_th,
            v_cc=params.v_cc,
            r_load=params.r_load,
            v_led_forward=params.v_led_forward,
            v_ce_sat=params.v_ce_sat,
            r_base=params.r_base
        )
        res = simulate_transistor_switch(temp_params)
        i_c_vals.append(res.collector_current_ma)
        v_out_vals.append(res.v_out_collector)
        
    return {
        "v_in": v_in_range,
        "i_c_ma": np.array(i_c_vals),
        "v_out": np.array(v_out_vals)
    }


def create_experiment_dataframe(records: List[Dict[str, Any]]) -> pd.DataFrame:
    """Converts a list of experiment observations into a structured Pandas DataFrame."""
    if not records:
        return pd.DataFrame(columns=[
            "Trial", "V_in (V)", "V_th (V)", "V_cc (V)", "R_load (Ω)",
            "Transistor State", "I_c (mA)", "LED State", "Notes"
        ])
    return pd.DataFrame(records)


def export_experiment_csv(df: pd.DataFrame) -> str:
    """Exports the experiment DataFrame to a CSV string."""
    return df.to_csv(index=False)
