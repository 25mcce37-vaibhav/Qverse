"""
From Transistors to Qubits: A Hybrid Learning Framework
EDC Assignment #2 — Educational Engineering Suite
Main Streamlit Application
"""

import streamlit as st
import numpy as np
import pandas as pd
import io

# Local modular imports
from src.transistor import (
    TransistorParameters,
    simulate_transistor_switch,
    generate_transfer_curve,
    create_experiment_dataframe,
    export_experiment_csv
)
from src.logic_gates import (
    evaluate_gate,
    simulate_half_adder,
    simulate_2to1_mux,
    TRUTH_TABLES
)
from src.quantum_simulator import (
    run_single_qubit_circuit,
    run_two_qubit_cnot,
    run_z_interference_demo
)
from src.noise import (
    simulate_classical_noise,
    simulate_quantum_noise,
    simulate_3qubit_repetition_code
)
from src.visualizations import (
    plot_transistor_transfer,
    draw_transistor_schematic,
    plot_quantum_distribution,
    plot_classical_noise_waveform
)
from src.ui_components import (
    apply_custom_styles,
    render_header,
    render_metric_card,
    render_hardware_disclaimer,
    render_breadboard_guide,
    render_knowledge_check
)

# Page configuration
st.set_page_config(
    page_title="Transistor-to-Qubit Framework",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply Dark-Navy Design System
apply_custom_styles()

# Initialize session state for experiment observations
if "transistor_trials" not in st.session_state:
    st.session_state.transistor_trials = []
if "quantum_gates_sequence" not in st.session_state:
    st.session_state.quantum_gates_sequence = ["H"]

# Sidebar Navigation
st.sidebar.markdown("""
    <div style="text-align: center; padding: 12px 0 20px 0; border-bottom: 1px solid #1E2A4A;">
        <span style="font-size: 2.2rem;">⚡⚛️</span>
        <h3 style="margin: 6px 0 0 0; color: #00F5D4; font-size: 1.15rem; font-weight: 700;">
            TRANSISTOR → QUBIT
        </h3>
        <p style="margin: 0; color: #8D99AE; font-size: 0.75rem; letter-spacing: 0.05em;">
            EDC ASSIGNMENT #2 HYBRID FRAMEWORK
        </p>
    </div>
""", unsafe_allow_html=True)

nav_options = [
    "Dashboard",
    "Module A — Transistor Simulator",
    "Module B — Logic Gate Simulator",
    "Module C — Quantum Simulator",
    "Module D — Classical vs Quantum",
    "Noise Lab",
    "Learning Resources",
    "About Project"
]

selected_page = st.sidebar.radio("Navigation", nav_options, index=0)

st.sidebar.markdown("---")
st.sidebar.markdown("""
    <div style="font-size: 0.78rem; color: #8D99AE; padding: 0 8px;">
        <p style="margin: 0 0 4px 0;"><strong>Engine Status:</strong></p>
        <p style="margin: 0; color: #00F5D4;">● Qiskit 2.5.2 & Aer 0.17</p>
        <p style="margin: 0; color: #00F5D4;">● 58/58 Automated Tests Passing</p>
        <p style="margin: 6px 0 0 0; color: #8D99AE;">Local Execution • Zero External APIs</p>
    </div>
""", unsafe_allow_html=True)


# ==============================================================================
# 1. DASHBOARD
# ==============================================================================
if selected_page == "Dashboard":
    render_header(
        title="From Transistors to Qubits: A Hybrid Learning Framework",
        subtitle="A comprehensive interactive platform bridging semiconductor electronics and quantum computing concepts."
    )
    render_hardware_disclaimer()

    # Introduction Banner
    st.markdown("""
        <div class="eng-card">
            <div class="eng-card-title">🎯 Executive Project Overview</div>
            <p style="color: #D0E8F9; line-height: 1.6; margin: 0;">
                Classical computers derive their computational power from billions of microscopic silicon transistors acting as binary switches. 
                Quantum computers, by contrast, harness the fundamental physics of quantum mechanics—superposition, phase interference, and entanglement—to 
                process information in state spaces of exponentially greater capacity. 
                This platform provides an engineering journey from the unipolar cutoff/saturation regions of a bipolar junction transistor (BJT) 
                up to unitary operations on single and entangled multi-qubit systems.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # 4 Module Cards
    st.markdown("### 📚 Core Learning Modules")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
            <div class="eng-card">
                <div class="eng-card-title">⚡ Module A: Transistor Switch Simulator</div>
                <div class="eng-card-subtitle">Semiconductor Physics & Binary Logic Foundations</div>
                <p style="color: #8D99AE; font-size: 0.9rem; line-height: 1.5;">
                    Explore piecewise-linear NPN BJT switching behavior driving an LED load. 
                    Adjust base drive, switching threshold, and collector resistance. 
                    Analyze cutoff vs saturation regions, transfer characteristics, and download recorded laboratory trials.
                </p>
                <div style="margin-top: 12px;">
                    <span class="badge-quantum">V_th Thresholding</span>
                    <span class="badge-quantum">LED Load</span>
                    <span class="badge-quantum">CSV Export</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("""
            <div class="eng-card">
                <div class="eng-card-title">⚛️ Module C: Quantum Simulator</div>
                <div class="eng-card-subtitle">Genuine Qiskit & Aer Circuit Simulation</div>
                <p style="color: #8D99AE; font-size: 0.9rem; line-height: 1.5;">
                    Simulate real single and two-qubit quantum circuits. 
                    Apply Pauli-X (quantum NOT), Hadamard (superposition), Pauli-Z (phase-flip), and CNOT (entanglement). 
                    Inspect statevector complex amplitudes, measurement probabilities, and quantum interference.
                </p>
                <div style="margin-top: 12px;">
                    <span class="badge-quantum">Qiskit 2.5</span>
                    <span class="badge-quantum">Aer Simulator</span>
                    <span class="badge-quantum">Bell State</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div class="eng-card">
                <div class="eng-card-title">🔀 Module B: Logic Gate Simulator</div>
                <div class="eng-card-subtitle">Classical Boolean Gates & Composite Architectures</div>
                <p style="color: #8D99AE; font-size: 0.9rem; line-height: 1.5;">
                    Experiment with all six fundamental gates (NOT, AND, OR, NAND, NOR, XOR). 
                    Inspect dynamic truth tables with active row highlighting, schematic symbols, 
                    and explore composite arithmetic circuits like the Half Adder and 2-to-1 Multiplexer.
                </p>
                <div style="margin-top: 12px;">
                    <span class="badge-quantum">6 Canonical Gates</span>
                    <span class="badge-quantum">Active Highlighting</span>
                    <span class="badge-quantum">Half Adder</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("""
            <div class="eng-card">
                <div class="eng-card-title">⚖️ Module D: Classical vs Quantum Comparison</div>
                <div class="eng-card-subtitle">Systematic Conceptual Mapping & Limits of Analogy</div>
                <p style="color: #8D99AE; font-size: 0.9rem; line-height: 1.5;">
                    Eight rigorous engineering comparisons mapping voltage switches to statevectors, 
                    bits to qubits, and measurement collapse to non-destructive bus reads. 
                    Includes an interactive side-by-side gate playground highlighting where the analogy breaks down.
                </p>
                <div style="margin-top: 12px;">
                    <span class="badge-quantum">8 Core Mappings</span>
                    <span class="badge-quantum">Side-by-Side</span>
                    <span class="badge-quantum">Analogy Limits</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

    # Pathway & Noise Lab Row
    col3, col4 = st.columns([1, 1])
    with col3:
        st.markdown("""
            <div class="eng-card">
                <div class="eng-card-title">📡 Noise Lab & Error Correction</div>
                <p style="color: #8D99AE; font-size: 0.9rem; line-height: 1.5;">
                    Compare Gaussian electrical voltage noise ($V_{out} = V_{ideal} + n(t)$) against quantum decoherence 
                    (Bit-flip, Phase-flip, and Depolarizing channels). Witness why phase errors require phase-sensitive 
                    interference circuits to detect, and test the 3-Qubit Repetition Code.
                </p>
            </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
            <div class="eng-card">
                <div class="eng-card-title">📖 Theory & Knowledge Verification</div>
                <p style="color: #8D99AE; font-size: 0.9rem; line-height: 1.5;">
                    Eight modular learning units with theoretical explanations, worked mathematical examples, 
                    takeaways, and self-scoring knowledge checks designed for undergraduate engineering students.
                </p>
            </div>
        """, unsafe_allow_html=True)

    # Learning Pathway Diagram
    st.markdown("### 🗺️ The Transistor-to-Qubit Pedagogical Pathway")
    st.markdown("""
        <div style="background-color: #111C38; border: 1px solid #1E2A4A; border-radius: 8px; padding: 18px; margin-bottom: 24px;">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
                <div style="text-align: center; flex: 1; min-width: 120px;">
                    <div style="font-size: 1.4rem;">🔌</div>
                    <div style="font-weight: 700; color: #00F5D4; font-size: 0.85rem;">1. BJT Switch</div>
                    <div style="color: #8D99AE; font-size: 0.72rem;">V_in ≥ V_th Threshold</div>
                </div>
                <div style="color: #0077B6; font-size: 1.2rem;">➔</div>
                <div style="text-align: center; flex: 1; min-width: 120px;">
                    <div style="font-size: 1.4rem;">🔲</div>
                    <div style="font-weight: 700; color: #00F5D4; font-size: 0.85rem;">2. Logic Gates</div>
                    <div style="color: #8D99AE; font-size: 0.72rem;">Boolean Combinations</div>
                </div>
                <div style="color: #0077B6; font-size: 1.2rem;">➔</div>
                <div style="text-align: center; flex: 1; min-width: 120px;">
                    <div style="font-size: 1.4rem;">🌀</div>
                    <div style="font-weight: 700; color: #00F5D4; font-size: 0.85rem;">3. Qubit State</div>
                    <div style="color: #8D99AE; font-size: 0.72rem;">Complex Amplitudes</div>
                </div>
                <div style="color: #0077B6; font-size: 1.2rem;">➔</div>
                <div style="text-align: center; flex: 1; min-width: 120px;">
                    <div style="font-size: 1.4rem;">⚛️</div>
                    <div style="font-weight: 700; color: #00F5D4; font-size: 0.85rem;">4. Unitary Gates</div>
                    <div style="color: #8D99AE; font-size: 0.72rem;">X, H, Z, CNOT</div>
                </div>
                <div style="color: #0077B6; font-size: 1.2rem;">➔</div>
                <div style="text-align: center; flex: 1; min-width: 120px;">
                    <div style="font-size: 1.4rem;">🎲</div>
                    <div style="font-weight: 700; color: #00F5D4; font-size: 0.85rem;">5. Measurement</div>
                    <div style="color: #8D99AE; font-size: 0.72rem;">Collapse & Sampling</div>
                </div>
                <div style="color: #0077B6; font-size: 1.2rem;">➔</div>
                <div style="text-align: center; flex: 1; min-width: 120px;">
                    <div style="font-size: 1.4rem;">🛡️</div>
                    <div style="font-weight: 700; color: #00F5D4; font-size: 0.85rem;">6. Noise & QEC</div>
                    <div style="color: #8D99AE; font-size: 0.72rem;">Decoherence Protection</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)


# ==============================================================================
# 2. MODULE A — TRANSISTOR SIMULATOR
# ==============================================================================
elif selected_page == "Module A — Transistor Simulator":
    render_header(
        title="Module A: Educational Transistor Switching Simulator",
        subtitle="Explore bipolar junction transistor cutoff and saturation regions driving an LED load."
    )
    render_hardware_disclaimer()

    col_ctrl, col_view = st.columns([1, 2])

    with col_ctrl:
        st.markdown("### 🎛️ Circuit Controls")

        # Preset buttons
        st.markdown("**Quick Presets:**")
        preset_cols = st.columns(3)
        if preset_cols[0].button("Cutoff (0.2V)"):
            st.session_state.v_in_val = 0.2
        if preset_cols[1].button("Threshold (0.7V)"):
            st.session_state.v_in_val = 0.7
        if preset_cols[2].button("Sat (3.3V)"):
            st.session_state.v_in_val = 3.3

        v_in_default = getattr(st.session_state, "v_in_val", 0.80)

        v_in = st.slider("Base Input Voltage V_in (V)", 0.0, 5.0, float(v_in_default), 0.05, key="v_in_slider")
        v_th = st.slider("Switching Threshold V_th / V_BE(on) (V)", 0.4, 1.2, 0.70, 0.02)
        v_cc = st.slider("Supply Voltage V_CC (V)", 2.0, 10.0, 5.0, 0.5)
        r_load = st.number_input("Load Resistor R_Load (Ω)", min_value=50.0, max_value=5000.0, value=330.0, step=10.0)
        v_led_forward = st.slider("LED Forward Drop V_F (V)", 1.5, 3.2, 2.0, 0.1)
        v_ce_sat = st.slider("Transistor Saturation V_CE(sat) (V)", 0.05, 0.5, 0.20, 0.05)

        st.markdown("---")
        notes = st.text_input("Observation Notes (optional)", placeholder="e.g. Trial with 330 ohm resistor")
        if st.button("📝 Record Observation to Table"):
            params_temp = TransistorParameters(v_in=v_in, v_th=v_th, v_cc=v_cc, r_load=r_load, v_led_forward=v_led_forward, v_ce_sat=v_ce_sat)
            res_temp = simulate_transistor_switch(params_temp)
            st.session_state.transistor_trials.append({
                "Trial": len(st.session_state.transistor_trials) + 1,
                "V_in (V)": round(v_in, 2),
                "V_th (V)": round(v_th, 2),
                "V_cc (V)": round(v_cc, 1),
                "R_load (Ω)": round(r_load, 1),
                "Transistor State": res_temp.state_label,
                "I_c (mA)": round(res_temp.collector_current_ma, 2),
                "V_out (V)": round(res_temp.v_out_collector, 2),
                "LED State": res_temp.led_state_label,
                "Notes": notes or "Standard run"
            })
            st.success("Observation recorded!")

    with col_view:
        # Run simulation
        params = TransistorParameters(
            v_in=v_in,
            v_th=v_th,
            v_cc=v_cc,
            r_load=r_load,
            v_led_forward=v_led_forward,
            v_ce_sat=v_ce_sat
        )
        sim_res = simulate_transistor_switch(params)

        # Output Metric Cards
        mcol1, mcol2, mcol3, mcol4 = st.columns(4)
        with mcol1:
            render_metric_card("Transistor State", "SATURATED" if sim_res.is_on else "CUTOFF", "BJT Mode", "high" if sim_res.is_on else "low")
        with mcol2:
            render_metric_card("LED Status", "LIT" if sim_res.led_is_lit else "DARK", "Light Emission", "high" if sim_res.led_is_lit else "low")
        with mcol3:
            render_metric_card("Collector Current", f"{sim_res.collector_current_ma:.2f} mA", "I_C through LED", "neutral")
        with mcol4:
            render_metric_card("Collector V_out", f"{sim_res.v_out_collector:.2f} V", "Inverter Output", "neutral")

        # Switching Explanation
        st.markdown(f"""
            <div class="eng-card" style="margin-top: 14px; margin-bottom: 14px;">
                <div class="eng-card-title">💡 Switching Decision Analysis</div>
                <p style="color: #F8F9FA; margin: 0; line-height: 1.5;">{sim_res.explanation}</p>
                <p style="color: #8D99AE; font-size: 0.8rem; margin: 8px 0 0 0;"><em>{sim_res.disclaimer}</em></p>
            </div>
        """, unsafe_allow_html=True)

        # Tabs for Circuit Schematic vs Transfer Characteristic
        tab_sch, tab_curv = st.tabs(["📐 Circuit Schematic Diagram", "📈 V_in vs Transfer Characteristics"])
        with tab_sch:
            fig_sch = draw_transistor_schematic(v_in, v_th, sim_res.is_on, sim_res.led_is_lit, sim_res.collector_current_ma, v_cc)
            st.pyplot(fig_sch)

        with tab_curv:
            curves = generate_transfer_curve(params, v_in_max=5.0)
            fig_curv = plot_transistor_transfer(curves, v_in, v_th, sim_res.collector_current_ma, sim_res.v_out_collector)
            st.pyplot(fig_curv)

    # Observations Table & CSV Download Section
    st.markdown("### 📊 Recorded Laboratory Observations")
    df_trials = create_experiment_dataframe(st.session_state.transistor_trials)

    if not df_trials.empty:
        st.dataframe(df_trials, use_container_width=True)
        csv_data = export_experiment_csv(df_trials)
        dcol1, dcol2 = st.columns([1, 4])
        with dcol1:
            st.download_button(
                label="📥 Download Trials as CSV",
                data=csv_data,
                file_name="transistor_switching_trials.csv",
                mime="text/csv"
            )
        with dcol2:
            if st.button("🗑️ Clear Trials Table"):
                st.session_state.transistor_trials = []
                st.rerun()
    else:
        st.info("No experiment trials recorded yet. Use the 'Record Observation' button above to log data points.")

    # Practical Breadboard Guide
    render_breadboard_guide()


# ==============================================================================
# 3. MODULE B — LOGIC GATE SIMULATOR
# ==============================================================================
elif selected_page == "Module B — Logic Gate Simulator":
    render_header(
        title="Module B: Classical Logic Gate Simulator",
        subtitle="Interactive analysis of fundamental boolean gates, dynamic truth tables, and composite logic."
    )
    render_hardware_disclaimer()

    tab_single, tab_composite = st.tabs(["🔲 Individual Logic Gates", "🧩 Composite Logic Circuit Demonstrations"])

    with tab_single:
        gcol_left, gcol_right = st.columns([1, 2])

        with gcol_left:
            st.markdown("### ⚙️ Gate Configuration")
            gate_name = st.selectbox(
                "Select Logic Gate",
                ["NOT", "AND", "OR", "NAND", "NOR", "XOR"],
                index=0
            )

            st.markdown("**Binary Inputs:**")
            input_a = st.radio("Input A", [0, 1], index=0, horizontal=True)
            if gate_name != "NOT":
                input_b = st.radio("Input B", [0, 1], index=0, horizontal=True)
            else:
                input_b = 0
                st.caption("ℹ️ NOT gate operates on a single input.")

            gate_eval = evaluate_gate(gate_name, input_a, input_b)

        with gcol_right:
            st.markdown(f"### 📊 Evaluation: {gate_name} Gate")

            # Metrics
            m1, m2, m3 = st.columns(3)
            with m1:
                render_metric_card("Input A", str(input_a), "Binary Input", "high" if input_a else "low")
            with m2:
                if gate_name != "NOT":
                    render_metric_card("Input B", str(input_b), "Binary Input", "high" if input_b else "low")
                else:
                    render_metric_card("Input B", "N/A", "Single Input Gate", "neutral")
            with m3:
                render_metric_card("Output (OUT)", str(gate_eval.output), gate_eval.circuit_formula, "high" if gate_eval.output else "low")

            # Explanation
            st.markdown(f"""
                <div class="eng-card" style="margin-top: 14px; margin-bottom: 14px;">
                    <div class="eng-card-title">📖 Semiconductor & Boolean Logic Context</div>
                    <p style="color: #F8F9FA; margin: 0; line-height: 1.5;">{gate_eval.explanation}</p>
                </div>
            """, unsafe_allow_html=True)

            # Truth Table with Active Row Highlight
            st.markdown("#### Canonical Truth Table")
            table_rows = []
            for row in gate_eval.truth_table:
                # Check if this row matches active input
                if gate_name == "NOT":
                    is_active = (row["A"] == input_a)
                    active_tag = "👉 ACTIVE" if is_active else ""
                    table_rows.append({"A": row["A"], "OUT": row["OUT"], "Current State": active_tag})
                else:
                    is_active = (row["A"] == input_a and row["B"] == input_b)
                    active_tag = "👉 ACTIVE" if is_active else ""
                    table_rows.append({"A": row["A"], "B": row["B"], "OUT": row["OUT"], "Current State": active_tag})

            df_tt = pd.DataFrame(table_rows)

            # Style DataFrame so active row stands out
            def highlight_active_row(s):
                if s["Current State"] == "👉 ACTIVE":
                    return ['background-color: #0077B6; color: #FFFFFF; font-weight: bold'] * len(s)
                return [''] * len(s)

            styled_tt = df_tt.style.apply(highlight_active_row, axis=1)
            st.dataframe(styled_tt, use_container_width=True)

    with tab_composite:
        st.markdown("### 🧩 Composite Logic Demonstrations")
        comp_choice = st.radio("Choose Composite Circuit", ["1-Bit Half Adder", "2-to-1 Multiplexer (MUX)"], horizontal=True)

        if comp_choice == "1-Bit Half Adder":
            st.markdown(r"""
                A **Half Adder** performs binary addition of two 1-bit operands ($A$ and $B$).
                It produces a **Sum bit** ($S = A \oplus B$) and a **Carry bit** ($C = A \cdot B$).
            """)
            h_col1, h_col2 = st.columns([1, 2])
            with h_col1:
                ha_a = st.radio("Operand A", [0, 1], index=1, key="ha_a", horizontal=True)
                ha_b = st.radio("Operand B", [0, 1], index=1, key="ha_b", horizontal=True)
                res_ha = simulate_half_adder(ha_a, ha_b)

            with h_col2:
                mc1, mc2, mc3 = st.columns(3)
                with mc1:
                    render_metric_card("Sum (A ⊕ B)", str(res_ha["Sum"]), "XOR Gate", "high" if res_ha["Sum"] else "low")
                with mc2:
                    render_metric_card("Carry (A · B)", str(res_ha["Carry"]), "AND Gate", "high" if res_ha["Carry"] else "low")
                with mc3:
                    render_metric_card("Binary / Decimal", f"{res_ha['BinarySum']}₂ = {res_ha['DecimalSum']}₁₀", "Total Output", "neutral")
                st.info(f"Logic Formula: {res_ha['Formula']}")

        else:
            st.markdown("""
                A **2-to-1 Multiplexer (MUX)** steers one of two input lines ($D_0$ or $D_1$) to the output based on a **Select line** ($SEL$).
                Formula: $\\text{OUT} = (D_0 \\cdot \\overline{SEL}) + (D_1 \\cdot SEL)$.
            """)
            m_col1, m_col2 = st.columns([1, 2])
            with m_col1:
                mux_d0 = st.radio("Data 0 (D0)", [0, 1], index=0, key="mux_d0", horizontal=True)
                mux_d1 = st.radio("Data 1 (D1)", [0, 1], index=1, key="mux_d1", horizontal=True)
                mux_sel = st.radio("Select (SEL)", [0, 1], index=0, key="mux_sel", horizontal=True)
                res_mux = simulate_2to1_mux(mux_d0, mux_d1, mux_sel)

            with m_col2:
                mm1, mm2 = st.columns(2)
                with mm1:
                    render_metric_card("Multiplexer Output", str(res_mux["OUT"]), res_mux["Selected"], "high" if res_mux["OUT"] else "low")
                with mm2:
                    render_metric_card("Selected Input Line", f"Line D{mux_sel}", f"Value Routed: {res_mux['OUT']}", "neutral")
                st.info(f"Logic Formula: {res_mux['Formula']}")


# ==============================================================================
# 4. MODULE C — QUANTUM SIMULATOR
# ==============================================================================
elif selected_page == "Module C — Quantum Simulator":
    render_header(
        title="Module C: Quantum Circuit Simulator",
        subtitle="Genuine quantum state simulation and shot sampling using Qiskit and Qiskit Aer."
    )
    render_hardware_disclaimer()

    qtab_1q, qtab_2q, qtab_z = st.tabs(["⚛️ Single-Qubit Lab", "🔗 Two-Qubit CNOT & Entanglement", "🌈 Phase Interference (Z-Gate)"])

    # Single-Qubit Tab
    with qtab_1q:
        qcol_ctrl, qcol_res = st.columns([1, 2])

        with qcol_ctrl:
            st.markdown("### 🎛️ Circuit Controls")
            initial_state = st.radio("Initial Qubit State", ["0", "1"], index=0, horizontal=True)

            st.markdown("**Sequence Presets:**")
            pcols = st.columns(3)
            if pcols[0].button("Pauli-X"):
                st.session_state.quantum_gates_sequence = ["X"]
            if pcols[1].button("Hadamard"):
                st.session_state.quantum_gates_sequence = ["H"]
            if pcols[2].button("H → Z → H"):
                st.session_state.quantum_gates_sequence = ["H", "Z", "H"]

            gate_options = ["X", "H", "Z", "I"]
            selected_sequence = st.multiselect(
                "Gate Sequence (Applied Left-to-Right)",
                options=gate_options,
                default=st.session_state.quantum_gates_sequence
            )
            shots = st.slider("Measurement Shots", min_value=100, max_value=10000, value=1024, step=100)

            if st.button("🔄 Reset to Identity"):
                st.session_state.quantum_gates_sequence = []
                st.rerun()

        with qcol_res:
            # Run single qubit simulation
            q_out = run_single_qubit_circuit(initial_state=initial_state, gates=selected_sequence, shots=shots)

            # Metric tiles
            qm1, qm2, qm3 = st.columns(3)
            with qm1:
                render_metric_card("Count |0⟩", f"{q_out.counts.get('0', 0)} ({q_out.probabilities['0']*100:.1f}%)", "Observed 0s", "neutral")
            with qm2:
                render_metric_card("Count |1⟩", f"{q_out.counts.get('1', 0)} ({q_out.probabilities['1']*100:.1f}%)", "Observed 1s", "neutral")
            with qm3:
                render_metric_card("Total Shots", str(shots), "Aer Sampling", "neutral")

            # Circuit Representation & Bar Chart
            st.markdown("#### Generated Quantum Circuit")
            st.code(q_out.circuit_text, language="text")

            c_fig = plot_quantum_distribution(q_out.counts, shots, "Single-Qubit Measurement Distribution")
            st.pyplot(c_fig)

            # Statevector Complex Amplitudes vs Probabilities Table
            st.markdown("#### 📐 Statevector Complex Amplitudes vs Measurement Probabilities")
            alpha, beta = q_out.statevector[0], q_out.statevector[1]
            sv_data = [
                {"Basis State": "|0⟩", "Real Amplitude": f"{alpha.real:+.4f}", "Imag Amplitude": f"{alpha.imag:+.4f}", "|Amplitude|²": f"{abs(alpha)**2:.4f}", "Empirical Prob": f"{q_out.probabilities['0']:.4f}"},
                {"Basis State": "|1⟩", "Real Amplitude": f"{beta.real:+.4f}", "Imag Amplitude": f"{beta.imag:+.4f}", "|Amplitude|²": f"{abs(beta)**2:.4f}", "Empirical Prob": f"{q_out.probabilities['1']:.4f}"}
            ]
            st.table(pd.DataFrame(sv_data))

            # Narrative Explanation
            st.markdown(f"""
                <div class="eng-card">
                    <div class="eng-card-title">📖 Conceptual Quantum Analysis</div>
                    <pre style="color: #D0E8F9; font-family: monospace; white-space: pre-wrap; margin: 0;">{q_out.explanation}</pre>
                </div>
            """, unsafe_allow_html=True)

    # Two-Qubit CNOT Tab
    with qtab_2q:
        cnot_col1, cnot_col2 = st.columns([1, 2])
        with cnot_col1:
            st.markdown("### 🔗 CNOT Gate Configuration")
            init_q0 = st.radio("Initial State Qubit 0 (q0)", [0, 1], index=0, horizontal=True)
            init_q1 = st.radio("Initial State Qubit 1 (q1)", [0, 1], index=0, horizontal=True)
            ctrl = st.selectbox("Control Qubit", [0, 1], index=0)
            target = 1 if ctrl == 0 else 0
            st.caption(f"Target Qubit is automatically set to **q{target}**")

            bell_mode = st.checkbox("🌟 Prepare Bell State |Φ+⟩ (Apply H to Control)", value=False)
            shots_cnot = st.slider("CNOT Shots", 100, 5000, 1024, 100, key="shots_cnot")

        with cnot_col2:
            cnot_out = run_two_qubit_cnot(
                initial_q0=init_q0,
                initial_q1=init_q1,
                control_qubit=ctrl,
                target_qubit=target,
                apply_hadamard_to_control=bell_mode,
                shots=shots_cnot
            )

            st.markdown("#### Two-Qubit Circuit Diagram")
            st.code(cnot_out.circuit_text, language="text")

            fig_cnot = plot_quantum_distribution(cnot_out.counts, shots_cnot, "2-Qubit Measurement Distribution (|q1 q0⟩)")
            st.pyplot(fig_cnot)

            st.markdown(f"""
                <div class="eng-card">
                    <div class="eng-card-title">📖 Two-Qubit & Entanglement Analysis</div>
                    <p style="color: #D0E8F9; line-height: 1.5; margin: 0;">{cnot_out.explanation}</p>
                </div>
            """, unsafe_allow_html=True)

    # Phase Interference Tab
    with qtab_z:
        st.markdown("### 🌈 Quantum Phase Interference Demonstration")
        st.markdown(r"""
            A fundamental distinction between classical probabilities and quantum mechanics is **phase**.
            In the standard computational basis ($Z$-basis), measuring a state alone **cannot** reveal its relative phase 
            because $|e^{i\phi}|^2 = 1$. To reveal a phase flip, we must use quantum interference by sandwiching the phase gate between two Hadamard gates:
        """)

        if st.button("🚀 Run Interference Experiment (1024 Shots)"):
            z_demo = run_z_interference_demo(shots=1024)
            z_col1, z_col2 = st.columns(2)

            with z_col1:
                st.markdown("#### Experiment 1: Without Phase Flip (H → H)")
                st.code(z_demo["without_z"]["circuit_text"], language="text")
                fig_z1 = plot_quantum_distribution(z_demo["without_z"]["counts"], 1024, "Result: 100% |0⟩")
                st.pyplot(fig_z1)
                st.caption(z_demo["without_z"]["description"])

            with z_col2:
                st.markdown("#### Experiment 2: With Phase Flip (H → Z → H)")
                st.code(z_demo["with_z"]["circuit_text"], language="text")
                fig_z2 = plot_quantum_distribution(z_demo["with_z"]["counts"], 1024, "Result: 100% |1⟩ (Phase Converted to Bit Flip!)")
                st.pyplot(fig_z2)
                st.caption(z_demo["with_z"]["description"])

            st.markdown(f"""
                <div class="eng-card" style="margin-top: 14px;">
                    <div class="eng-card-title">💡 Physical Takeaway: Complex Amplitudes vs Probabilities</div>
                    <p style="color: #F8F9FA; line-height: 1.6; margin: 0;">{z_demo["explanation"]}</p>
                </div>
            """, unsafe_allow_html=True)


# ==============================================================================
# 5. MODULE D — CLASSICAL VS QUANTUM
# ==============================================================================
elif selected_page == "Module D — Classical vs Quantum":
    render_header(
        title="Module D: Classical vs Quantum Comparison",
        subtitle="Rigorous engineering mappings, side-by-side behavioral playground, and breakdown of analogies."
    )
    render_hardware_disclaimer()

    tab_mappings, tab_play = st.tabs(["📋 8 Conceptual Engineering Mappings", "🎮 Side-by-Side Behavioral Playground"])

    with tab_mappings:
        st.markdown("### 🔍 Systematic Comparison Framework")
        st.markdown("""
            The table below establishes direct technical analogies between semiconductor engineering 
            and quantum information science, alongside the exact boundaries where the analogies break down.
        """)

        mappings = [
            ("1. Transistor Switch vs State Manipulation",
             "Unipolar semiconductor switch driven between cutoff and saturation via base voltage threshold.",
             "Unitary matrix rotation of a statevector on the Bloch sphere driven by microwave/laser pulses.",
             "A transistor is an irreversible dissipative device; unitary quantum gates are strictly reversible and preserve norm."),
            
            ("2. Classical Bit vs Qubit",
             r"Deterministic scalar state: $b \in \{0, 1\}$. Defined by macroscopic charge on a capacitor.",
             r"Superposition state: $|\psi\rangle = \alpha|0\rangle + \beta|1\rangle$ with $\alpha, \beta \in \mathbb{C}$ and $|\alpha|^2 + |\beta|^2 = 1$.",
             "A qubit holds an infinite continuum of state amplitudes prior to measurement, but yields only 1 classical bit upon collapse."),

            ("3. Binary ON/OFF vs Quantum Amplitudes",
             r"Mutually exclusive macroscopic states (e.g. $0$V vs $5$V).",
             "Linear combination of basis states with complex probability amplitudes exhibiting relative phase.",
             "Classical logic has no concept of negative or complex interference."),

            ("4. Classical NOT vs Quantum Pauli-X",
             r"Boolean inverter ($0 \to 1, 1 \to 0$). Constructed from 1 BJT or CMOS inverter pair.",
             r"Pauli-X operator ($\sigma_x$). Rotates statevector by $\pi$ radians around the X-axis of the Bloch sphere.",
             r"Pauli-X acts on superpositions: $X(\alpha|0\rangle + \beta|1\rangle) = \beta|0\rangle + \alpha|1\rangle$."),

            ("5. Logic Circuits vs Quantum Circuits",
             "Network of dissipative gates (NAND, NOR, etc.). Fan-out (signal copying) is fundamental.",
             "Sequence of reversible unitary operations. Fan-out is strictly FORBIDDEN by the No-Cloning Theorem.",
             "Classical circuits can freely split and duplicate signals; quantum states cannot be duplicated without destruction."),

            ("6. Digital Bus Read vs Quantum Measurement",
             "Non-destructive voltage measurement. Reading a digital bus does not alter its stored logical state.",
             r"Von Neumann projective measurement. Forces the statevector to randomly collapse into $|0\rangle$ or $|1\rangle$.",
             "Quantum measurement fundamentally alters the system and irreversibly destroys coherent superpositions."),

            ("7. Electrical Noise vs Quantum Decoherence",
             r"Thermal Johnson-Nyquist noise, crosstalk, and ground bounce ($V_{out} = V_{ideal} + n(t)$). Resisted by noise margins.",
             r"Environmental coupling causing energy dissipation ($T_1$) and phase decoherence ($T_2$), plus bit-flips and phase-flips.",
             r"Classical bits only suffer bit flips ($0 \leftrightarrow 1$). Qubits also suffer phase errors ($Z$) with no classical analog."),

            ("8. Determinism vs Probabilistic Outcomes",
             "Strictly deterministic: ideal gates produce identical outputs every execution cycle.",
             r"Inherently probabilistic upon measurement according to Born's rule ($P(i) = |\langle i|\psi\rangle|^2$).",
             "Quantum computing is not random guessing; algorithms use interference to concentrate probability on correct solutions.")
        ]

        for title, cl_text, q_text, lim_text in mappings:
            st.markdown(f"""
                <div class="eng-card">
                    <div class="eng-card-title">{title}</div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin-top: 8px;">
                        <div style="background-color: #142145; padding: 12px; border-radius: 6px; border-left: 3px solid #00B4D8;">
                            <strong style="color: #00B4D8;">⚡ Classical Electronics:</strong><br>
                            <span style="color: #D0E8F9; font-size: 0.88rem;">{cl_text}</span>
                        </div>
                        <div style="background-color: #142145; padding: 12px; border-radius: 6px; border-left: 3px solid #00F5D4;">
                            <strong style="color: #00F5D4;">⚛️ Quantum Information:</strong><br>
                            <span style="color: #D0E8F9; font-size: 0.88rem;">{q_text}</span>
                        </div>
                    </div>
                    <div style="margin-top: 10px; background-color: #211933; padding: 10px 14px; border-radius: 6px; border-left: 3px solid #FFD166;">
                        <strong style="color: #FFD166;">⚠️ Where the Analogy Breaks Down:</strong><br>
                        <span style="color: #FFE699; font-size: 0.85rem;">{lim_text}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

    with tab_play:
        st.markdown("### 🎮 Side-by-Side Operational Playground")
        st.markdown("Execute a classical gate alongside a quantum gate to directly observe differences in behavior and measurement.")

        p_col_cl, p_col_qu = st.columns(2)

        with p_col_cl:
            st.markdown("#### ⚡ Classical System")
            c_in = st.radio("Classical Input Bit", [0, 1], index=0, horizontal=True, key="play_c_in")
            c_op = st.selectbox("Classical Operation", ["BUFFER (Identity)", "NOT (Inverter)"], index=1, key="play_c_op")

            c_out = c_in if "BUFFER" in c_op else (1 if c_in == 0 else 0)
            render_metric_card("Classical Output", f"Bit = {c_out}", f"V_out ≈ {'5.0V (HIGH)' if c_out else '0.2V (LOW)'}", "high" if c_out else "low")
            st.caption(f"Classical result is **100% deterministic**. Multiple reads yield identical bit {c_out} without disturbance.")

        with p_col_qu:
            st.markdown("#### ⚛️ Quantum System")
            q_in = st.radio("Quantum Input State", ["0", "1"], index=0, horizontal=True, key="play_q_in")
            q_gate = st.selectbox("Quantum Gate", ["Identity (I)", "Pauli-X (Quantum NOT)", "Hadamard (H)", "Pauli-Z"], index=1, key="play_q_gate")

            gate_code = "I" if "Identity" in q_gate else ("X" if "Pauli-X" in q_gate else ("H" if "Hadamard" in q_gate else "Z"))
            res_q_play = run_single_qubit_circuit(initial_state=q_in, gates=[gate_code], shots=500)

            render_metric_card(
                "Quantum Measurement (500 Shots)",
                f"P(0)={res_q_play.probabilities['0']:.2f} | P(1)={res_q_play.probabilities['1']:.2f}",
                f"Counts: |0⟩={res_q_play.counts.get('0',0)}, |1⟩={res_q_play.counts.get('1',0)}",
                "neutral"
            )
            st.caption("Quantum result requires **statistical sampling**. Measuring projects the superposition into an eigenstate.")

        st.markdown("---")
        st.markdown("""
            <div class="eng-card">
                <div class="eng-card-title">💡 Comparative Operational Summary</div>
                <ul style="color: #D0E8F9; margin: 0; padding-left: 20px; line-height: 1.6;">
                    <li><strong>When comparing Classical NOT vs Pauli-X:</strong> On computational basis inputs (|0⟩ or |1⟩), both produce inverted outputs. However, Pauli-X can act on superpositions, whereas classical NOT cannot.</li>
                    <li><strong>When comparing Classical Buffer vs Hadamard:</strong> A classical buffer merely preserves the bit. A Hadamard gate takes a deterministic bit and creates an equal superposition (|0⟩ + |1⟩)/√2 with zero classical equivalent!</li>
                    <li><strong>Crucial Physics Note:</strong> A transistor does <em>not</em> physically transform into a qubit. A classical voltage signal is an ensemble of trillions of electrons; a qubit is a two-level quantum mechanical degree of freedom.</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)


# ==============================================================================
# 6. NOISE LAB
# ==============================================================================
elif selected_page == "Noise Lab":
    render_header(
        title="Interactive Noise Lab & Error Correction",
        subtitle="Analyzing classical voltage noise, quantum decoherence channels, and the 3-qubit repetition code."
    )
    render_hardware_disclaimer()

    ntab_cl, ntab_qu, ntab_qec = st.tabs(["⚡ Classical Signal Noise", "⚛️ Quantum Decoherence Channels", "🛡️ 3-Qubit Repetition Code (QEC)"])

    # Classical Noise Tab
    with ntab_cl:
        st.markdown("### ⚡ Classical Additive Noise: $V_{out}(t) = V_{ideal}(t) + n(t)$")
        st.markdown("Observe how Gaussian thermal/electronic noise degrades noise margins and triggers logic errors.")

        cn_c1, cn_c2 = st.columns([1, 2])
        with cn_c1:
            st.markdown("#### Noise & Signal Controls")
            sig_type = st.radio("Signal Waveform", ["dc", "pulse"], format_func=lambda x: "DC High (+5V)" if x == "dc" else "Square Pulse Train")
            v_ideal = st.slider("Nominal HIGH Voltage (V)", 3.0, 6.0, 5.0, 0.5)
            noise_sigma = st.slider("Noise Standard Deviation σ (V)", 0.1, 2.5, 1.2, 0.1)
            v_thresh = st.slider("Decision Threshold V_th (V)", 1.0, 4.0, 2.5, 0.1)
            n_samples = st.slider("Sample Count", 50, 500, 200, 25)
            seed = st.number_input("Random Seed (for reproducibility)", value=42, step=1)

            cl_res = simulate_classical_noise(
                ideal_voltage=v_ideal,
                noise_std=noise_sigma,
                threshold=v_thresh,
                num_samples=n_samples,
                signal_type=sig_type,
                random_seed=int(seed)
            )

        with cn_c2:
            # Metrics
            nm1, nm2, nm3 = st.columns(3)
            with nm1:
                render_metric_card("Signal-to-Noise Ratio", f"{cl_res.snr_db:.1f} dB", "SNR", "neutral")
            with nm2:
                render_metric_card("Bit Error Rate (BER)", f"{cl_res.bit_error_rate*100:.2f}%", f"{cl_res.error_count}/{cl_res.total_samples} bit errors", "low" if cl_res.error_count > 0 else "high")
            with nm3:
                render_metric_card("Noise Margin Headroom", f"{v_ideal - v_thresh:.2f} V", "HIGH State Margin", "high" if (v_ideal - v_thresh) > 1.5 else "low")

            # Waveform Plot
            fig_cln = plot_classical_noise_waveform(
                cl_res.time_points,
                cl_res.ideal_signal,
                cl_res.noisy_signal,
                cl_res.threshold,
                cl_res.bit_errors,
                cl_res.bit_error_rate,
                cl_res.snr_db
            )
            st.pyplot(fig_cln)

            st.markdown(f"""
                <div class="eng-card" style="margin-top: 12px;">
                    <div class="eng-card-title">📖 Semiconductor Engineering Takeaway</div>
                    <p style="color: #D0E8F9; margin: 0; line-height: 1.5;">{cl_res.explanation}</p>
                </div>
            """, unsafe_allow_html=True)

    # Quantum Noise Tab
    with ntab_qu:
        st.markdown("### ⚛️ Quantum Noise Channels & Decoherence")
        st.markdown("Simulate genuine quantum noise models using Qiskit Aer. Discover why phase errors differ fundamentally from classical bit flips.")

        qn_c1, qn_c2 = st.columns([1, 2])
        with qn_c1:
            st.markdown("#### Quantum Noise Controls")
            noise_kind = st.selectbox(
                "Noise Channel Type",
                ["bit_flip", "phase_flip", "depolarizing"],
                format_func=lambda x: "Bit-Flip Error (X Noise)" if x == "bit_flip" else ("Phase-Flip Error (Z Noise)" if x == "phase_flip" else "Depolarizing Noise (Isotropic)")
            )
            error_prob = st.slider("Error Probability (p)", 0.0, 0.50, 0.20, 0.02)
            c_mode = st.radio(
                "Circuit Diagnostic Mode",
                ["standard", "phase_sensitive"],
                format_func=lambda x: "Standard Z-Basis Measurement (|0⟩ → Noise → Measure)" if x == "standard" else "Phase-Sensitive Interference Circuit (|0⟩ → H → Noise → H → Measure)"
            )
            q_shots = st.slider("Noise Simulation Shots", 500, 5000, 1024, 100, key="q_noise_shots")

        with qn_c2:
            q_noise_res = simulate_quantum_noise(
                noise_type=noise_kind,
                error_rate=error_prob,
                circuit_mode=c_mode,
                shots=q_shots
            )

            # Metric tiles
            qm1, qm2, qm3 = st.columns(3)
            with qm1:
                render_metric_card("Channel Error Rate", f"{error_prob*100:.1f}%", "Input Noise Parameter", "neutral")
            with qm2:
                render_metric_card("Observed Bit Error Rate", f"{q_noise_res.bit_error_rate*100:.1f}%", f"{q_noise_res.noisy_counts.get('1', 0)}/{q_shots} shots flipped", "low" if q_noise_res.bit_error_rate > 0.05 else "high")
            with qm3:
                render_metric_card("Diagnostic Mode", "Phase Sensitive" if q_noise_res.is_phase_sensitive else "Standard Z", "Circuit Type", "neutral")

            # Circuit display & Side-by-side bar chart
            st.markdown("#### Simulated Quantum Circuit with Noise Channel")
            st.code(q_noise_res.circuit_text, language="text")

            b_col1, b_col2 = st.columns(2)
            with b_col1:
                f_ideal = plot_quantum_distribution(q_noise_res.ideal_counts, q_shots, "Ideal (No Noise)")
                st.pyplot(f_ideal)
            with b_col2:
                f_noisy = plot_quantum_distribution(q_noise_res.noisy_counts, q_shots, f"Noisy Channel (p = {error_prob:.2f})")
                st.pyplot(f_noisy)

            st.markdown(f"""
                <div class="eng-card" style="margin-top: 12px;">
                    <div class="eng-card-title">📖 Quantum Noise Interpretation</div>
                    <p style="color: #D0E8F9; margin: 0; line-height: 1.5;">{q_noise_res.explanation}</p>
                </div>
            """, unsafe_allow_html=True)

    # 3-Qubit QEC Tab
    with ntab_qec:
        st.markdown("### 🛡️ 3-Qubit Bit-Flip Quantum Repetition Code")
        st.markdown("""
            Unlike classical bits which can be copied infinitely ($b \to bbb$), quantum states cannot be cloned 
            due to the **No-Cloning Theorem**. However, an unknown state $\\alpha|0\\rangle + \\beta|1\\rangle$ 
            can be entangled into an encoded logical subspace $\\alpha|000\\rangle + \\beta|111\\rangle$.
        """)

        qec_c1, qec_c2 = st.columns([1, 2])
        with qec_c1:
            st.markdown("#### Error Correction Controls")
            init_log = st.radio("Initial Logical Qubit State", [0, 1], index=0, horizontal=True, format_func=lambda x: f"|{x}_L⟩")
            err_target = st.selectbox(
                "Inject Bit-Flip (X) Error On:",
                ["none", "q0", "q1", "q2"],
                format_func=lambda x: "No Error (Clean Channel)" if x == "none" else f"Qubit {x} (Corrupt with Pauli-X)"
            )
            shots_qec = st.slider("QEC Evaluation Shots", 100, 2000, 1024, 100, key="shots_qec")

        with qec_c2:
            qec_result = simulate_3qubit_repetition_code(
                initial_logical_bit=init_log,
                error_qubit=err_target,
                shots=shots_qec
            )

            # Metric Cards
            ec1, ec2, ec3 = st.columns(3)
            with ec1:
                render_metric_card("Input Logical State", f"|{init_log}_L⟩", "Before Noise", "neutral")
            with ec2:
                render_metric_card("Decoded Output State", f"|{qec_result['measured_logical']}⟩", "After Correction", "high" if qec_result["success"] else "low")
            with ec3:
                render_metric_card("Syndrome Recovery", "SUCCESS (100%)" if qec_result["success"] else "FAILED", "Error Neutralized", "high" if qec_result["success"] else "low")

            st.markdown("#### Full Quantum Error Correction Circuit")
            st.code(qec_result["circuit_text"], language="text")

            fig_qec = plot_quantum_distribution(qec_result["counts"], shots_qec, "Decoded Logical Qubit Measurement")
            st.pyplot(fig_qec)

            st.markdown(f"""
                <div class="eng-card" style="margin-top: 12px;">
                    <div class="eng-card-title">📖 Quantum Error Correction Analysis & Fundamental Limits</div>
                    <pre style="color: #D0E8F9; font-family: monospace; white-space: pre-wrap; margin: 0;">{qec_result["explanation"]}</pre>
                </div>
            """, unsafe_allow_html=True)


# ==============================================================================
# 7. LEARNING RESOURCES
# ==============================================================================
elif selected_page == "Learning Resources":
    render_header(
        title="Learning Resources & Theory Modules",
        subtitle="Foundational theory, worked mathematical examples, key takeaways, and self-scoring knowledge checks."
    )
    render_hardware_disclaimer()

    resources = [
        {
            "id": "transistor_switching",
            "title": "1. Classical Bits and Transistor Switching",
            "explanation": (
                "Bipolar Junction Transistors (BJTs) operate as binary electronic switches by exploiting the non-linear "
                "conduction of the base-emitter PN junction. When the input voltage V_in is below the junction potential barrier "
                "(V_th ≈ 0.7V for silicon), the transistor rests in the CUTOFF region: base current is zero and the collector "
                "path acts as an open circuit (OFF state). When V_in exceeds V_th and sufficient base current is supplied, "
                "the transistor is driven into SATURATION: the collector-emitter voltage drops to V_CE(sat) ≈ 0.2V, conducting "
                "current through the load (ON state). This binary dichotomy forms the physical basis of classical bits."
            ),
            "example": (
                "Given V_CC = 5.0 V, R_load = 330 Ω, LED V_F = 2.0 V, V_CE(sat) = 0.2 V, and V_th = 0.7 V:\n"
                "• For V_in = 0.3 V (< V_th): Cutoff region. I_C = 0.0 mA, LED is DARK, V_out = 5.0 V.\n"
                "• For V_in = 2.5 V (≥ V_th): Saturation region. I_C = (5.0 - 2.0 - 0.2) / 330 = 2.8 / 330 = 8.48 mA. LED is LIT, V_out = 0.2 V."
            ),
            "takeaway": "Classical bits rely on macroscopic charge flow across a semiconductor barrier to establish deterministic 0 and 1 voltage rails.",
            "question": "What is the primary condition required to switch an NPN BJT from cutoff into saturation?",
            "options": [
                "Base voltage V_in must exceed threshold V_th (≈ 0.7V) and provide sufficient base current",
                "Collector voltage must be equal to 0V",
                "Load resistance must be reduced to 0 Ω",
                "The transistor must be cooled to absolute zero"
            ],
            "correct_idx": 0,
            "quiz_explanation": "Forward-biasing the base-emitter junction with V_in ≥ V_th injects minority carriers that trigger collector-emitter saturation conduction."
        },
        {
            "id": "logic_gates",
            "title": "2. Truth Tables and Logic Gates",
            "explanation": (
                "Boolean logic gates synthesize elementary switching operations into computational primitives. "
                "A NOT gate (inverter) flips a single bit; AND requires all inputs to be HIGH (transistors in series); "
                "OR requires at least one HIGH input (transistors in parallel). NAND and NOR are 'universal gates' because "
                "any arbitrary boolean function can be realized exclusively using combinations of either gate."
            ),
            "example": (
                "Constructing an XOR gate from NAND primitives:\n"
                "A ⊕ B = (A · ¬B) + (¬A · B) = ¬(¬(A · ¬(A·B)) · ¬(B · ¬(A·B))).\n"
                "Truth check for A=1, B=0: 1 ⊕ 0 = 1."
            ),
            "takeaway": "Classical digital architectures combine non-linear transistor switches to evaluate boolean truth tables deterministically.",
            "question": "Why are NAND and NOR classified as universal logic gates?",
            "options": [
                "Because they consume zero electrical power",
                "Because any boolean logic function can be constructed solely using that gate type",
                "Because they can simulate quantum superposition",
                "Because their truth tables are completely symmetrical"
            ],
            "correct_idx": 1,
            "quiz_explanation": "Universal gates form functionally complete sets capable of expressing NOT, AND, and OR operations."
        },
        {
            "id": "qubit_states",
            "title": "3. Qubit States and Probability Amplitudes",
            "explanation": (
                "A quantum bit (qubit) is a two-level quantum mechanical system represented as a normalized vector in a two-dimensional "
                "complex Hilbert space (ℂ²): |ψ⟩ = α|0⟩ + β|1⟩, where α, β ∈ ℂ. The complex coefficients α and β are called "
                "probability amplitudes. By Born's rule, the probability of measuring state |0⟩ is P(0) = |α|² and state |1⟩ is P(1) = |β|², "
                "subject to the normalization constraint |α|² + |β|² = 1. Unlike classical probabilities, amplitudes have complex phases "
                "that can constructively or destructively interfere."
            ),
            "example": (
                "Consider the state |ψ⟩ = (1/2)|0⟩ + (√3/2)|1⟩:\n"
                "• Amplitude for |0⟩: α = 0.5 → P(0) = |0.5|² = 0.25 (25%)\n"
                "• Amplitude for |1⟩: β = √3/2 ≈ 0.866 → P(1) = |√3/2|² = 3/4 = 0.75 (75%)\n"
                "• Normalization check: 0.25 + 0.75 = 1.0."
            ),
            "takeaway": "Qubits store continuous complex amplitudes prior to measurement, enabling interference and massive parallel state representation.",
            "question": "If a qubit has amplitude α = 1/√2 and β = -i/√2, what is the probability of measuring |1⟩?",
            "options": [
                "50% (0.50)",
                "-50% (-0.50)",
                "25% (0.25)",
                "100% (1.00)"
            ],
            "correct_idx": 0,
            "quiz_explanation": "By Born's rule, P(1) = |β|² = |-i/√2|² = |-i|² / (√2)² = 1 / 2 = 0.50 (50%)."
        },
        {
            "id": "quantum_gates",
            "title": "4. Quantum Gates: X, H, Z, and CNOT",
            "explanation": (
                "Quantum gates are represented by unitary matrices (U†U = I) that preserve the norm of the statevector. "
                "• Pauli-X (Quantum NOT): Inverts computational basis states: X|0⟩ = |1⟩, X|1⟩ = |0⟩.\n"
                "• Hadamard (H): Maps basis states into equal superpositions: H|0⟩ = (|0⟩ + |1⟩)/√2 = |+⟩, H|1⟩ = (|0⟩ - |1⟩)/√2 = |−⟩.\n"
                "• Pauli-Z (Phase-flip): Inverts the relative phase: Z|0⟩ = |0⟩, Z|1⟩ = -|1⟩.\n"
                "• CNOT (Controlled-NOT): 2-qubit entangling gate. Flips the target qubit if and only if the control qubit is |1⟩."
            ),
            "example": (
                "Bell State Entanglement Generation:\n"
                "|00⟩ ──H on q0──> (|00⟩ + |10⟩)/√2 ──CNOT(0→1)──> (|00⟩ + |11⟩)/√2 (|Φ+⟩).\n"
                "Measuring either qubit instantly correlates the state of the other!"
            ),
            "takeaway": "Quantum logic operations are norm-preserving unitary rotations, with CNOT providing the mechanism for non-local entanglement.",
            "question": "What is the output state when a Hadamard gate (H) is applied to state |1⟩?",
            "options": [
                "(|0⟩ − |1⟩) / √2",
                "(|0⟩ + |1⟩) / √2",
                "|0⟩",
                "−|1⟩"
            ],
            "correct_idx": 0,
            "quiz_explanation": "Applying H to |1⟩ yields the |−⟩ state: (|0⟩ − |1⟩)/√2, with relative phase π."
        },
        {
            "id": "measurement_shots",
            "title": "5. Quantum Measurement and Shot Counts",
            "explanation": (
                "In quantum mechanics, measurement is a non-unitary, irreversible projection (wavefunction collapse). "
                "When measuring a state |ψ⟩ = α|0⟩ + β|1⟩ in the computational basis, the superposition instantly collapses to |0⟩ "
                "with probability |α|² or |1⟩ with probability |β|². A single measurement yields exactly one classical bit. "
                "To reconstruct the underlying probability distribution, the quantum circuit must be prepared and measured "
                "repeatedly across hundreds or thousands of 'shots', yielding empirical binomial count distributions."
            ),
            "example": (
                "Measuring H|0⟩ over N = 1000 shots:\n"
                "Expected counts: N·P(0) = 500, N·P(1) = 500.\n"
                "Standard statistical deviation: σ = √(N·p·(1-p)) = √(1000·0.5·0.5) ≈ 15.8 shots.\n"
                "A trial yielding 488 zeros and 512 ones is well within the 95% confidence interval."
            ),
            "takeaway": "A single quantum measurement returns only classical bits; quantum amplitudes can only be estimated through repeated shot sampling.",
            "question": "Why does measuring a qubit in superposition (|0⟩ + |1⟩)/√2 not yield a value like '0.5'?",
            "options": [
                "Because quantum measurement forces projective collapse into an eigenstate (|0⟩ or |1⟩)",
                "Because our multimeters lack sufficient resolution",
                "Because classical bits cannot store fractions",
                "Because the qubit is destroyed by electrical current"
            ],
            "correct_idx": 0,
            "quiz_explanation": "By the projection postulate of quantum mechanics, measurement forces the system into one of the eigenstates of the measurement operator."
        },
        {
            "id": "noise_decoherence",
            "title": "6. Classical Noise vs Quantum Decoherence",
            "explanation": (
                "Classical noise consists of electrical voltage fluctuations (thermal Johnson-Nyquist noise, crosstalk) "
                "superimposed on signal wires: V(t) = V_ideal + n(t). Semiconductor logic buffers this using wide noise margins. "
                "Quantum noise (decoherence), by contrast, stems from environmental entanglement and energy dissipation. "
                "T₁ relaxation characterizes the time required for an excited state |1⟩ to decay to ground state |0⟩. "
                "T₂ dephasing characterizes the loss of coherent phase information between amplitudes."
            ),
            "example": (
                "Classical vs Quantum noise comparison:\n"
                "• Classical: A 0.2V spike on a 5V line leaves the digital logic unaffected (well inside noise margin).\n"
                "• Quantum: A tiny stray magnetic field shifts phase by e^{iθ}, destroying computational interference completely."
            ),
            "takeaway": "Classical digital logic relies on regenerative saturation margins; quantum computing requires strict physical isolation to prevent phase decay.",
            "question": "What is the physical meaning of the T₂ dephasing time in a quantum processor?",
            "options": [
                "The time scale over which relative quantum phase coherence is lost to the environment",
                "The time it takes to execute a CNOT gate",
                "The time required to compile a Qiskit circuit",
                "The clock cycle duration of the quantum CPU"
            ],
            "correct_idx": 0,
            "quiz_explanation": "T₂ measures transverse relaxation (pure dephasing + energy decay), after which quantum interference can no longer occur."
        },
        {
            "id": "quantum_error_types",
            "title": "7. Bit-Flip, Phase-Flip, and Depolarizing Errors",
            "explanation": (
                "Classical systems suffer only one discrete error type: bit flips (0 ↔ 1). Quantum channels suffer a continuous "
                "spectrum of errors, discretizable into three Pauli error types: "
                "1. Bit-flip error (Pauli-X): Inverts basis states (|0⟩ ↔ |1⟩).\n"
                "2. Phase-flip error (Pauli-Z): Inverts phase without changing population: Z(|0⟩ + |1⟩)/√2 = (|0⟩ - |1⟩)/√2.\n"
                "3. Combined bit-phase flip (Pauli-Y = iXZ).\n"
                "Depolarizing noise is an isotropic combination where the qubit decays into the maximally mixed state I/2."
            ),
            "example": (
                "Phase-flip error detection:\n"
                "Measuring Z|0⟩ directly in the computational basis yields 100% 0 (error is completely invisible!).\n"
                "Sandwiching with Hadamards: H · Z · H = X. The phase error becomes a measurable bit-flip: outcome is 100% 1."
            ),
            "takeaway": "Quantum noise includes phase-flip errors that have no classical analog and remain invisible to simple computational-basis measurements.",
            "question": "Why is a phase-flip error (Z) undetectable when measuring state |0⟩ directly in the Z-basis?",
            "options": [
                "Because Z|0⟩ = |0⟩, so the computational state and measurement probability are completely unaltered",
                "Because Z gates cannot execute on physical hardware",
                "Because phase flips only occur on two-qubit gates",
                "Because Qiskit Aer suppresses Z errors"
            ],
            "correct_idx": 0,
            "quiz_explanation": "Since |0⟩ is an eigenstate of Z with eigenvalue +1, Z|0⟩ = |0⟩. Phase errors only manifest when relative phase exists between superposition components."
        },
        {
            "id": "qec_intro",
            "title": "8. Introduction to Quantum Error Correction (QEC)",
            "explanation": (
                "Classical error correction uses simple duplication (repetition code: 0 → 000, majority voting). "
                "In quantum systems, the No-Cloning Theorem prevents copying unknown quantum states! "
                "Quantum Error Correction (QEC) overcomes this by entangling data into multi-qubit entangled states "
                "(e.g., 3-qubit bit-flip code: α|000⟩ + β|111⟩). Parity check operators (syndrome measurements) detect "
                "which qubit suffered an error WITHOUT measuring or collapsing the underlying stored data α and β."
            ),
            "example": (
                "Syndrome measurement in 3-qubit bit-flip code:\n"
                "If state is |100⟩ (q0 flipped):\n"
                "Parity check P₁ = Z₀Z₁ = -1 (mismatch on 0-1), P₂ = Z₁Z₂ = +1 (match on 1-2).\n"
                "Syndrome uniquely identifies qubit 0 as corrupted, triggering a corrective X gate on q0."
            ),
            "takeaway": "Quantum error correction measures multi-qubit parities to diagnose and fix errors without destroying the stored superposition.",
            "question": "Why can classical repetition (copying bit 3 times) not be directly applied to quantum states?",
            "options": [
                "The No-Cloning Theorem proves that an arbitrary unknown quantum state cannot be copied perfectly",
                "Quantum circuits do not have enough memory wires",
                "Qiskit Aer restricts circuit depth to 2 qubits",
                "Photons cannot travel across silicon substrates"
            ],
            "correct_idx": 0,
            "quiz_explanation": "Wootters and Zurek's No-Cloning Theorem (1982) proves that unitary linearity forbids creating an exact duplicate of an arbitrary unknown quantum state."
        }
    ]

    for topic in resources:
        with st.expander(f"📚 {topic['title']}", expanded=(topic["id"] == "transistor_switching")):
            st.markdown(f"**Theoretical Overview:**\n{topic['explanation']}")
            st.markdown(f"**Worked Engineering Example:**")
            st.code(topic["example"], language="text")
            st.markdown(f"""
                <div style="background-color: #142145; padding: 10px 14px; border-radius: 6px; border-left: 3px solid #00F5D4; margin: 12px 0;">
                    <strong style="color: #00F5D4;">📌 Key Takeaway:</strong> {topic['takeaway']}
                </div>
            """, unsafe_allow_html=True)
            render_knowledge_check(
                topic_id=topic["id"],
                question=topic["question"],
                options=topic["options"],
                correct_idx=topic["correct_idx"],
                explanation=topic["quiz_explanation"]
            )


# ==============================================================================
# 8. ABOUT PROJECT
# ==============================================================================
elif selected_page == "About Project":
    render_header(
        title="About Project: EDC Assignment #2",
        subtitle="Educational Engineering Software Architecture, Specifications, and Compliance Record."
    )
    render_hardware_disclaimer()

    st.markdown("""
        <div class="eng-card">
            <div class="eng-card-title">📋 Student & Course Metadata</div>
            <table style="width: 100%; color: #D0E8F9; border-collapse: collapse;">
                <tr><td style="padding: 6px; width: 220px;"><strong>Course:</strong></td><td>Electronic Devices and Circuits (EDC) — Assignment #2</td></tr>
                <tr><td style="padding: 6px;"><strong>Project Title:</strong></td><td>From Transistors to Qubits: A Hybrid Learning Framework</td></tr>
                <tr><td style="padding: 6px;"><strong>Student Name:</strong></td><td><code>[STUDENT_NAME_PLACEHOLDER]</code></td></tr>
                <tr><td style="padding: 6px;"><strong>Student ID / Roll No:</strong></td><td><code>[STUDENT_ID_PLACEHOLDER]</code></td></tr>
                <tr><td style="padding: 6px;"><strong>Instructor / Evaluator:</strong></td><td><code>[INSTRUCTOR_NAME_PLACEHOLDER]</code></td></tr>
                <tr><td style="padding: 6px;"><strong>Submission Date:</strong></td><td>October 2026</td></tr>
            </table>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("### 💻 System & Software Architecture")
    st.markdown("""
        - **Application Framework**: Streamlit (v1.65.0) with custom Dark-Navy and Electric-Cyan engineering CSS.
        - **Numerical & Plotting Engines**: NumPy (v2.5.4), Pandas (v3.0.6), Matplotlib (v3.11.2).
        - **Quantum Circuit Simulation**: Qiskit (v2.5.2) with Qiskit Aer (v0.17.2) for true unitary evolution and Aer noise channels.
        - **Automated Verification**: Pytest test suite (58 passing tests covering 100% of logic gates, transistor thresholds, quantum operators, noise channels, and CSV routines).
        - **Privacy & Connectivity**: 100% local offline execution. No paid APIs, external cloud databases, or subscriptions required.
    """)

    st.markdown("### 🔬 Laboratory & Hardware Demarcation")
    st.markdown("""
        | Learning Component | Execution Mode | Hardware vs Simulation Distinction |
        |---|---|---|
        | **Transistor Switching** | Simulated Software Model | Piecewise-linear simulation based on V_th, V_CC, and R_load. Physical measurements require real NPN BJT breadboard setup with DMM. |
        | **Logic Gates & Truth Tables** | Deterministic Boolean Logic | Fully validated mathematical models of NOT, AND, OR, NAND, NOR, XOR. Physical gates require 74xx series ICs or discrete BJT ladders. |
        | **Quantum Circuits & CNOT** | Qiskit Aer State Simulation | Genuine statevector evolution and shot sampling on local simulator. Physical qubits require cryogenic superconducting or trapped-ion QPUs. |
        | **Classical Noise Waveforms** | NumPy Gaussian Generator | Simulated additive noise model V_out = V_ideal + n(t). Real circuit noise requires bench oscilloscope sampling. |
        | **Quantum Noise Channels** | Aer Pauli & Depolarizing Models | Genuine simulated quantum open-system noise channels. Physical decoherence requires physical qubit pulse control. |
        | **3-Qubit Repetition Code** | Quantum Syndrome Decoding | Genuine Qiskit circuit with Toffoli correction. Physical fault tolerance requires physical quantum processor. |
    """)

    st.markdown("### 📚 Academic & Technical References")
    st.markdown("""
        1. **Sedra, A. S., & Smith, K. C.** (2015). *Microelectronic Circuits* (7th ed.). Oxford University Press. (BJT switching fundamentals, cutoff/saturation physics, inverter transfer curves).
        2. **Nielsen, M. A., & Chuang, I. L.** (2010). *Quantum Computation and Quantum Information* (10th Anniversary ed.). Cambridge University Press. (Qubit state spaces, unitary gates, Born's rule, quantum noise, 3-qubit repetition code).
        3. **Qiskit Development Team** (2024). *Qiskit: An Open-source Framework for Quantum Computing*. IBM Quantum. (Circuit transpilation, AerSimulator, Pauli and Depolarizing noise models).
        4. **Wootters, W. K., & Zurek, W. H.** (1982). *A single quantum cannot be cloned*. Nature, 299(5886), 802–803. (Theoretical basis for quantum error correction parities).
    """)
