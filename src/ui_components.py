"""
UI Components Module
Reusable Streamlit components, styled cards, status indicators,
and custom CSS for the dark-navy and electric-blue engineering theme.
"""

import streamlit as st
from typing import List, Dict, Any, Optional


CUSTOM_CSS = """
<style>
/* Main Background and Text */
[data-testid="stAppViewContainer"] {
    background-color: #0A1128;
    color: #F8F9FA;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
}

[data-testid="stSidebar"] {
    background-color: #080D21;
    border-right: 1px solid #1E2A4A;
}

[data-testid="stHeader"] {
    background-color: rgba(10, 17, 40, 0.85);
    backdrop-filter: blur(8px);
}

/* Engineering Dashboard Card */
.eng-card {
    background-color: #111C38;
    border: 1px solid #1E2A4A;
    border-radius: 10px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0 4px 14px rgba(0, 0, 0, 0.3);
    transition: transform 0.2s ease, border-color 0.2s ease;
}

.eng-card:hover {
    border-color: #0077B6;
}

.eng-card-title {
    font-size: 1.15rem;
    font-weight: 700;
    color: #00F5D4;
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    gap: 8px;
}

.eng-card-subtitle {
    font-size: 0.85rem;
    color: #8D99AE;
    margin-bottom: 12px;
}

/* Metric Display Tile */
.metric-tile {
    background-color: #142145;
    border: 1px solid #23345E;
    border-radius: 8px;
    padding: 14px;
    text-align: center;
}

.metric-value-high {
    font-size: 1.6rem;
    font-weight: 800;
    color: #00F5D4;
}

.metric-value-low {
    font-size: 1.6rem;
    font-weight: 800;
    color: #FF6B6B;
}

.metric-value-neutral {
    font-size: 1.6rem;
    font-weight: 800;
    color: #48CAE4;
}

.metric-label {
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #8D99AE;
    margin-top: 4px;
}

/* Status Badges */
.badge-on {
    display: inline-block;
    padding: 4px 10px;
    background-color: rgba(0, 245, 212, 0.15);
    border: 1px solid #00F5D4;
    color: #00F5D4;
    font-size: 0.8rem;
    font-weight: 700;
    border-radius: 6px;
}

.badge-off {
    display: inline-block;
    padding: 4px 10px;
    background-color: rgba(255, 107, 107, 0.15);
    border: 1px solid #FF6B6B;
    color: #FF6B6B;
    font-size: 0.8rem;
    font-weight: 700;
    border-radius: 6px;
}

.badge-quantum {
    display: inline-block;
    padding: 4px 10px;
    background-color: rgba(0, 180, 216, 0.15);
    border: 1px solid #00B4D8;
    color: #00B4D8;
    font-size: 0.8rem;
    font-weight: 700;
    border-radius: 6px;
}

/* Disclaimer / Warning Box */
.eng-alert-warning {
    background-color: #262214;
    border-left: 4px solid #FFD166;
    border-radius: 4px;
    padding: 12px 16px;
    color: #FFE699;
    font-size: 0.88rem;
    margin-bottom: 16px;
}

.eng-alert-info {
    background-color: #10243C;
    border-left: 4px solid #00B4D8;
    border-radius: 4px;
    padding: 12px 16px;
    color: #D0E8F9;
    font-size: 0.88rem;
    margin-bottom: 16px;
}

/* Styled Table */
.dataframe {
    background-color: #111C38 !important;
    color: #FFFFFF !important;
    border: 1px solid #1E2A4A !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #0077B6 0%, #0096C7 100%);
    color: #FFFFFF;
    font-weight: 600;
    border: 1px solid #00B4D8;
    border-radius: 6px;
    padding: 8px 18px;
    transition: all 0.2s ease;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #0096C7 0%, #00F5D4 100%);
    color: #0A1128;
    border-color: #00F5D4;
    box-shadow: 0 0 12px rgba(0, 245, 212, 0.4);
}
</style>
"""


def apply_custom_styles():
    """Injects custom CSS styles into the Streamlit session."""
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def render_header(title: str, subtitle: str, badge_text: str = "EDC ASSIGNMENT #2"):
    """Renders a standard, professional engineering dashboard header."""
    badge_html = f'<span class="badge-quantum">{badge_text}</span>'
    st.markdown(f"""
        <div style="margin-bottom: 24px; padding-bottom: 12px; border-bottom: 1px solid #1E2A4A;">
            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                <div>
                    <h1 style="margin: 0; color: #FFFFFF; font-size: 2.1rem; font-weight: 800; letter-spacing: -0.02em;">
                        {title}
                    </h1>
                    <p style="margin: 6px 0 0 0; color: #8D99AE; font-size: 1.05rem;">
                        {subtitle}
                    </p>
                </div>
                <div>
                    {badge_html}
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)


def render_metric_card(label: str, value: str, subtext: str = "", status: str = "neutral"):
    """Renders a metric card with status-tailored coloring."""
    val_class = f"metric-value-{status}"
    st.markdown(f"""
        <div class="metric-tile">
            <div class="{val_class}">{value}</div>
            <div class="metric-label">{label}</div>
            {f'<div style="font-size: 0.72rem; color: #8D99AE; margin-top: 4px;">{subtext}</div>' if subtext else ''}
        </div>
    """, unsafe_allow_html=True)


def render_hardware_disclaimer():
    """Displays mandatory educational disclaimer distinguishing simulations from hardware."""
    st.markdown("""
        <div class="eng-alert-warning">
            <strong>⚠️ Educational Simulation Notice & Measurement Disclaimer:</strong><br>
            All calculations, switching curves, and quantum circuit outcomes displayed here are 
            <strong>mathematical simulations</strong> generated locally (via piecewise models and Qiskit Aer). 
            This software does <strong>not</strong> perform real-time physical bench measurements. 
            Physical current, voltage, and gate fidelity measurements require actual laboratory hardware 
            (multimeters, oscilloscopes, DC power supplies, or physical quantum QPUs).
        </div>
    """, unsafe_allow_html=True)


def render_breadboard_guide():
    """Renders practical step-by-step breadboard guide for physical circuit experiment."""
    with st.expander("🛠️ Practical Bench Experiment Guide: NPN Transistor Switch Assembly", expanded=False):
        st.markdown("""
        ### Laboratory Guide: Constructing the NPN BJT Switching Circuit
        
        #### 1. Components Required
        - **Transistor**: NPN BJT (e.g., 2N2222, 2N3904, or BC547).
        - **LED**: Standard 5mm Red LED ($V_F \approx 1.8 - 2.0$ V).
        - **Load Resistor ($R_C$)**: $330\ \Omega$ (or $470\ \Omega$), $1/4$ W (limits LED current to safe $\sim 10$ mA).
        - **Base Resistor ($R_B$)**: $1\ \text{k}\Omega$ to $10\ \text{k}\Omega$ (limits base drive current).
        - **Power Source**: Regulated DC Bench Power Supply or 5.0 V USB/Battery source.
        - **Measurement Tools**: Digital Multimeter (DMM) for DC voltage and current.
        - **Prototyping**: Solderless breadboard and jumper wires.

        #### 2. Transistor Pinout (TO-92 Package: Flat face facing you)
        - **2N2222 / 2N3904**: Pin 1 = Emitter (E), Pin 2 = Base (B), Pin 3 = Collector (C).
        - **BC547**: Pin 1 = Collector (C), Pin 2 = Base (B), Pin 3 = Emitter (E).
        *(Always verify with component datasheet or DMM diode test before powering on).*

        #### 3. Step-by-Step Breadboard Wiring
        1. **Common Ground**: Connect the negative terminal of the 5V DC supply to the breadboard blue/negative rail (**GND**).
        2. **Emitter Connection**: Connect the **Emitter (E)** pin directly to **GND**.
        3. **Collector & LED Wiring**:
           - Connect the positive 5V supply rail to one leg of the **$330\ \Omega$ resistor ($R_C$)**.
           - Connect the other leg of $R_C$ to the **Anode** (longer lead) of the LED.
           - Connect the **Cathode** (flat rim/shorter lead) of the LED to the **Collector (C)** pin.
        4. **Base Drive**:
           - Connect one leg of the **$1\ \text{k}\Omega$ resistor ($R_B$)** to the **Base (B)** pin.
           - Connect the other leg of $R_B$ to your variable input voltage terminal ($V_{in}$) or a switched 5V/0V jumper.

        #### 4. Physical Testing Procedure & Multimeter Checkpoints
        - **Test A: Cutoff State ($V_{in} = 0\text{V}$)**:
          - Tie $V_{in}$ to GND ($0$ V).
          - Measure $V_{BE}$: should read $\approx 0.0$ V.
          - Measure $V_{CE}$: should read $\approx 5.0$ V (supply level).
          - Observe LED: Completely DARK ($I_C < 1\ \mu\text{A}$).
        - **Test B: Saturation State ($V_{in} = 5\text{V}$)**:
          - Connect $V_{in}$ to $+5$ V rail through $R_B$.
          - Measure $V_{BE}$: should clamp to $\approx 0.65 - 0.72$ V (diode drop).
          - Measure $V_{CE}$: should drop to $\approx 0.1 - 0.25$ V (saturation).
          - Measure voltage across $R_C$: $V_{RC} = V_{CC} - V_F - V_{CE} \approx 5.0 - 1.9 - 0.2 = 2.9$ V.
          - Calculate actual current: $I_C = 2.9\text{V} / 330\ \Omega = 8.8\text{ mA}$.
          - Observe LED: Brightly ILLUMINATED.
        
        #### 5. Laboratory Safety Precautions
        - Never connect the base directly to $+5$V without $R_B$; excessive base current will destroy the base-emitter junction.
        - Ensure correct LED polarity. Reversing LED prevents conduction but will not switch.
        """)


def render_knowledge_check(
    topic_id: str,
    question: str,
    options: List[str],
    correct_idx: int,
    explanation: str
):
    """Renders an interactive quiz widget with immediate feedback."""
    st.markdown(f"**Knowledge Check:** {question}")
    user_choice = st.radio(
        "Select your answer:",
        options,
        key=f"quiz_{topic_id}",
        index=None
    )
    if user_choice is not None:
        selected_idx = options.index(user_choice)
        if selected_idx == correct_idx:
            st.success(f"✅ **Correct!** {explanation}")
        else:
            st.error(f"❌ **Incorrect.** {explanation}")
