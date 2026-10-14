"""
Unit tests for Transistor Simulation Module.
"""

import pytest
import pandas as pd
from src.transistor import (
    TransistorParameters,
    simulate_transistor_switch,
    validate_parameters,
    generate_transfer_curve,
    create_experiment_dataframe,
    export_experiment_csv
)


def test_transistor_switching_below_threshold():
    """Test switching immediately below the threshold."""
    v_th = 0.7
    params = TransistorParameters(
        v_in=v_th - 0.05,  # 0.65 V
        v_th=v_th,
        v_cc=5.0,
        r_load=330.0,
        v_led_forward=2.0,
        v_ce_sat=0.2
    )
    result = simulate_transistor_switch(params)
    assert not result.is_on
    assert result.collector_current_ma == 0.0
    assert not result.led_is_lit
    assert result.v_out_collector == 5.0
    assert "CUTOFF" in result.state_label.upper()


def test_transistor_switching_at_threshold():
    """Test switching exactly at the threshold."""
    v_th = 0.7
    params = TransistorParameters(
        v_in=v_th,  # 0.70 V
        v_th=v_th,
        v_cc=5.0,
        r_load=330.0,
        v_led_forward=2.0,
        v_ce_sat=0.2
    )
    result = simulate_transistor_switch(params)
    assert result.is_on
    # Expected I_C = (5.0 - 2.0 - 0.2) / 330 = 2.8 / 330 ≈ 0.00848 A = 8.48 mA
    assert result.collector_current_ma > 0.0
    assert pytest.approx(result.collector_current_ma, 0.01) == 8.48
    assert result.led_is_lit
    assert result.v_out_collector == 0.2
    assert "SATURATION" in result.state_label or "Saturated" in result.state_label


def test_transistor_switching_above_threshold():
    """Test switching well above the threshold."""
    v_th = 0.7
    params = TransistorParameters(
        v_in=3.3,
        v_th=v_th,
        v_cc=5.0,
        r_load=330.0,
        v_led_forward=2.0,
        v_ce_sat=0.2
    )
    result = simulate_transistor_switch(params)
    assert result.is_on
    assert result.led_is_lit
    assert result.collector_current_ma > 8.0


def test_transistor_resistance_validation():
    """Test that non-positive load resistance is rejected to avoid division by zero."""
    params_zero = TransistorParameters(
        v_in=2.0, v_th=0.7, v_cc=5.0, r_load=0.0, v_led_forward=2.0, v_ce_sat=0.2
    )
    errors = validate_parameters(params_zero)
    assert any("strictly greater than 0" in e for e in errors)
    with pytest.raises(ValueError, match="strictly greater than 0"):
        simulate_transistor_switch(params_zero)

    params_negative = TransistorParameters(
        v_in=2.0, v_th=0.7, v_cc=5.0, r_load=-100.0, v_led_forward=2.0, v_ce_sat=0.2
    )
    with pytest.raises(ValueError):
        simulate_transistor_switch(params_negative)


def test_transistor_voltage_validation():
    """Test that invalid voltages are caught."""
    # Negative input voltage
    params_neg_vin = TransistorParameters(
        v_in=-1.0, v_th=0.7, v_cc=5.0, r_load=330.0, v_led_forward=2.0, v_ce_sat=0.2
    )
    with pytest.raises(ValueError, match="cannot be negative"):
        simulate_transistor_switch(params_neg_vin)

    # Negative V_cc
    params_neg_vcc = TransistorParameters(
        v_in=1.0, v_th=0.7, v_cc=-5.0, r_load=330.0, v_led_forward=2.0, v_ce_sat=0.2
    )
    with pytest.raises(ValueError, match="cannot be negative"):
        simulate_transistor_switch(params_neg_vcc)

    # Zero or negative V_th
    params_zero_th = TransistorParameters(
        v_in=1.0, v_th=0.0, v_cc=5.0, r_load=330.0, v_led_forward=2.0, v_ce_sat=0.2
    )
    with pytest.raises(ValueError, match="greater than 0"):
        simulate_transistor_switch(params_zero_th)


def test_transistor_insufficient_headroom():
    """Test behavior when V_cc is lower than LED forward drop + V_ce(sat)."""
    params = TransistorParameters(
        v_in=2.0, v_th=0.7, v_cc=1.5, r_load=330.0, v_led_forward=2.0, v_ce_sat=0.2
    )
    result = simulate_transistor_switch(params)
    assert result.is_on  # base is forward biased
    assert not result.led_is_lit  # but supply cannot drive LED
    assert result.collector_current_ma == 0.0


def test_transfer_curve_generation():
    """Test that transfer characteristic curves are generated correctly."""
    params = TransistorParameters(
        v_in=1.0, v_th=0.7, v_cc=5.0, r_load=330.0, v_led_forward=2.0, v_ce_sat=0.2
    )
    curves = generate_transfer_curve(params, steps=50)
    assert len(curves["v_in"]) == 50
    assert len(curves["i_c_ma"]) == 50
    assert len(curves["v_out"]) == 50
    # First point at V_in = 0 should have I_c = 0
    assert curves["i_c_ma"][0] == 0.0
    # Last point at V_in = 5 should have I_c > 0
    assert curves["i_c_ma"][-1] > 0.0


def test_csv_export():
    """Test structured observation table creation and CSV export."""
    records = [
        {"Trial": 1, "V_in (V)": 0.2, "V_th (V)": 0.7, "V_cc (V)": 5.0, "R_load (Ω)": 330.0, "Transistor State": "OFF", "I_c (mA)": 0.0, "LED State": "DARK", "Notes": "Cutoff test"},
        {"Trial": 2, "V_in (V)": 2.5, "V_th (V)": 0.7, "V_cc (V)": 5.0, "R_load (Ω)": 330.0, "Transistor State": "ON", "I_c (mA)": 8.48, "LED State": "LIT", "Notes": "Saturation test"}
    ]
    df = create_experiment_dataframe(records)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2
    
    csv_str = export_experiment_csv(df)
    assert "Trial" in csv_str
    assert "8.48" in csv_str
    assert "Cutoff test" in csv_str
