"""
Visualizations Module
Generates high-quality Matplotlib figures for the Transistor-to-Qubit learning framework.
Uses a professional dark-navy engineering palette matching the dashboard design.
"""

from typing import Dict, List, Any, Optional
import matplotlib
matplotlib.use("Agg")  # Non-interactive backend for server environments
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# Theme palette
PALETTE = {
    "bg_navy": "#0B132B",
    "card_navy": "#1C2541",
    "electric_blue": "#0077B6",
    "cyan": "#00F5D4",
    "bright_blue": "#00B4D8",
    "accent_coral": "#FF6B6B",
    "accent_amber": "#FFD166",
    "accent_green": "#06D6A0",
    "text_white": "#FFFFFF",
    "text_muted": "#8D99AE",
    "grid_color": "#2B3A67",
}


def _apply_dark_style(fig, ax):
    """Applies engineering dark-mode styling to matplotlib axes."""
    fig.patch.set_facecolor(PALETTE["bg_navy"])
    ax.set_facecolor(PALETTE["card_navy"])
    ax.tick_params(colors=PALETTE["text_white"], labelsize=10)
    for spine in ax.spines.values():
        spine.set_color(PALETTE["grid_color"])
        spine.set_linewidth(1.2)
    ax.grid(True, linestyle="--", alpha=0.35, color=PALETTE["grid_color"])


def plot_transistor_transfer(
    transfer_data: Dict[str, np.ndarray],
    current_v_in: float,
    v_th: float,
    current_ic_ma: float,
    current_vout: float
) -> plt.Figure:
    """Plots V_in vs I_C and V_out transfer characteristics with operating point markers."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.2), dpi=120)
    _apply_dark_style(fig, ax1)
    _apply_dark_style(fig, ax2)

    v_in = transfer_data["v_in"]
    i_c = transfer_data["i_c_ma"]
    v_out = transfer_data["v_out"]

    # Ax 1: Collector Current vs V_in
    ax1.plot(v_in, i_c, color=PALETTE["cyan"], lw=2.5, label="I_C (mA)")
    ax1.axvline(v_th, color=PALETTE["accent_amber"], ls="--", lw=1.8, label=f"V_th ({v_th:.2f}V)")
    ax1.scatter([current_v_in], [current_ic_ma], color=PALETTE["accent_coral"], s=100, zorder=5, label=f"Operating Point ({current_v_in:.2f}V, {current_ic_ma:.1f}mA)")
    ax1.set_title("Input Voltage vs Collector Current", color=PALETTE["text_white"], fontsize=11, fontweight="bold", pad=10)
    ax1.set_xlabel("V_in (V)", color=PALETTE["text_white"], fontsize=10)
    ax1.set_ylabel("I_C (mA)", color=PALETTE["cyan"], fontsize=10)
    ax1.legend(facecolor=PALETTE["card_navy"], edgecolor=PALETTE["grid_color"], labelcolor=PALETTE["text_white"], fontsize=8)

    # Ax 2: Output Voltage vs V_in (Inverter characteristic)
    ax2.plot(v_in, v_out, color=PALETTE["bright_blue"], lw=2.5, label="V_out (Collector)")
    ax2.axvline(v_th, color=PALETTE["accent_amber"], ls="--", lw=1.8, label=f"V_th ({v_th:.2f}V)")
    ax2.scatter([current_v_in], [current_vout], color=PALETTE["accent_coral"], s=100, zorder=5, label=f"Operating Point ({current_v_in:.2f}V, {current_vout:.2f}V)")
    ax2.set_title("Input vs Output Voltage (Inverter Action)", color=PALETTE["text_white"], fontsize=11, fontweight="bold", pad=10)
    ax2.set_xlabel("V_in (V)", color=PALETTE["text_white"], fontsize=10)
    ax2.set_ylabel("V_out (V)", color=PALETTE["bright_blue"], fontsize=10)
    ax2.legend(facecolor=PALETTE["card_navy"], edgecolor=PALETTE["grid_color"], labelcolor=PALETTE["text_white"], fontsize=8)

    plt.tight_layout()
    return fig


def draw_transistor_schematic(
    v_in: float,
    v_th: float,
    is_on: bool,
    led_lit: bool,
    i_c_ma: float,
    v_cc: float
) -> plt.Figure:
    """Draws a clean schematic diagram of the NPN transistor switching circuit with LED."""
    fig, ax = plt.subplots(figsize=(8, 4.5), dpi=120)
    fig.patch.set_facecolor(PALETTE["bg_navy"])
    ax.set_facecolor(PALETTE["card_navy"])
    ax.axis("off")
    ax.set_xlim(-1, 11)
    ax.set_ylim(-1, 8)

    # Wire styles
    wire_color = PALETTE["cyan"] if is_on else PALETTE["text_muted"]
    wire_kw = {"color": wire_color, "lw": 2.2}

    # 1. Supply Rail (+Vcc)
    ax.plot([4, 6], [7, 7], color=PALETTE["accent_amber"], lw=3)
    ax.text(5, 7.3, f"+V_CC = {v_cc:.1f} V", color=PALETTE["accent_amber"], fontsize=11, fontweight="bold", ha="center")

    # 2. Wire down to Load Resistor
    ax.plot([5, 5], [7, 5.8], **wire_kw)

    # 3. Load Resistor R_C
    rect_rc = patches.Rectangle((4.6, 5.0), 0.8, 0.8, facecolor=PALETTE["card_navy"], edgecolor=PALETTE["bright_blue"], lw=2)
    ax.add_patch(rect_rc)
    ax.text(5.6, 5.4, "R_Load (R_C)", color=PALETTE["text_white"], fontsize=9, va="center")

    # 4. Wire from R_C down to LED
    ax.plot([5, 5], [5.0, 4.2], **wire_kw)

    # 5. LED Symbol
    led_fill = PALETTE["accent_amber"] if led_lit else PALETTE["grid_color"]
    led_edge = PALETTE["accent_amber"] if led_lit else PALETTE["text_muted"]
    triangle = patches.Polygon([[4.6, 4.2], [5.4, 4.2], [5.0, 3.5]], closed=True, facecolor=led_fill, edgecolor=led_edge, lw=2)
    ax.add_patch(triangle)
    ax.plot([4.6, 5.4], [3.5, 3.5], color=led_edge, lw=2.5)  # Cathode bar

    # LED light rays if lit
    if led_lit:
        ax.annotate("", xy=(5.7, 4.3), xytext=(5.3, 3.9), arrowprops=dict(arrowstyle="->", color=PALETTE["accent_amber"], lw=2))
        ax.annotate("", xy=(5.9, 4.0), xytext=(5.4, 3.7), arrowprops=dict(arrowstyle="->", color=PALETTE["accent_amber"], lw=2))
        ax.text(6.1, 4.1, f"LIT ({i_c_ma:.1f} mA)", color=PALETTE["accent_amber"], fontsize=10, fontweight="bold")
    else:
        ax.text(5.7, 3.8, "DARK (0 mA)", color=PALETTE["text_muted"], fontsize=9)

    # 6. Wire from LED down to Transistor Collector
    ax.plot([5, 5], [3.5, 2.5], **wire_kw)

    # 7. NPN Transistor Symbol
    # Base bar
    b_color = PALETTE["cyan"] if is_on else PALETTE["text_muted"]
    ax.plot([4.4, 4.4], [1.8, 2.6], color=b_color, lw=3.5)
    # Collector wire
    ax.plot([4.4, 5.0], [2.4, 2.5], color=b_color, lw=2)
    # Emitter wire with NPN arrow
    ax.plot([4.4, 5.0], [2.0, 1.5], color=b_color, lw=2)
    # Arrow on emitter pointing outward
    ax.annotate("", xy=(4.95, 1.55), xytext=(4.65, 1.8), arrowprops=dict(arrowstyle="->", color=b_color, lw=2))

    # Transistor label
    t_state_text = "SATURATED (ON)" if is_on else "CUTOFF (OFF)"
    t_state_color = PALETTE["accent_green"] if is_on else PALETTE["accent_coral"]
    ax.text(5.6, 2.0, f"NPN BJT\n[{t_state_text}]", color=t_state_color, fontsize=10, fontweight="bold")

    # 8. Emitter to Ground
    ax.plot([5.0, 5.0], [1.5, 0.5], color=PALETTE["bright_blue"], lw=2)
    # Ground symbol
    ax.plot([4.6, 5.4], [0.5, 0.5], color=PALETTE["bright_blue"], lw=2.5)
    ax.plot([4.75, 5.25], [0.35, 0.35], color=PALETTE["bright_blue"], lw=2)
    ax.plot([4.9, 5.1], [0.2, 0.2], color=PALETTE["bright_blue"], lw=1.5)
    ax.text(5.0, -0.2, "GND (0V)", color=PALETTE["text_muted"], fontsize=8, ha="center")

    # 9. Base Drive (V_in and R_Base)
    ax.plot([1.0, 2.0], [2.2, 2.2], color=b_color, lw=2)
    rect_rb = patches.Rectangle((2.0, 1.9), 1.4, 0.6, facecolor=PALETTE["card_navy"], edgecolor=PALETTE["bright_blue"], lw=1.8)
    ax.add_patch(rect_rb)
    ax.text(2.7, 2.2, "R_Base", color=PALETTE["text_white"], fontsize=8, ha="center", va="center")
    ax.plot([3.4, 4.4], [2.2, 2.2], color=b_color, lw=2)

    # Input Terminal
    ax.scatter([1.0], [2.2], color=PALETTE["accent_amber"], s=80, zorder=5)
    ax.text(1.0, 2.7, f"V_in = {v_in:.2f} V\n(V_th = {v_th:.2f} V)", color=PALETTE["text_white"], fontsize=9, ha="center", fontweight="bold")

    # Overall Status Banner
    banner_bg = PALETTE["accent_green"] if is_on else PALETTE["accent_coral"]
    ax.text(5.0, 0.0, f"CIRCUIT STATUS: {'SWITCH CLOSED (LOGIC 1 / CONDUCTING)' if is_on else 'SWITCH OPEN (LOGIC 0 / CUTOFF)'}",
            color=banner_bg, fontsize=10, fontweight="bold", ha="center")

    plt.tight_layout()
    return fig


def plot_quantum_distribution(counts: Dict[str, int], shots: int, title: str = "Quantum Measurement Distribution") -> plt.Figure:
    """Plots a clean, beautifully styled bar chart of measurement counts and probabilities."""
    fig, ax = plt.subplots(figsize=(6.5, 3.8), dpi=120)
    _apply_dark_style(fig, ax)

    states = sorted(counts.keys())
    values = [counts[s] for s in states]
    probs = [counts[s] / shots for s in states]

    bars = ax.bar(states, values, color=PALETTE["cyan"], edgecolor=PALETTE["electric_blue"], width=0.45, lw=1.5)
    
    # Value annotations on bars
    for bar, p, val in zip(bars, probs, values):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2.0, height + (shots * 0.02),
                f"{val} ({p * 100:.1f}%)", ha="center", va="bottom",
                color=PALETTE["text_white"], fontsize=9, fontweight="bold")

    ax.set_ylim(0, max(values) * 1.25 if values else 100)
    ax.set_title(title, color=PALETTE["text_white"], fontsize=11, fontweight="bold", pad=12)
    ax.set_xlabel("Basis State (|bitstring⟩)", color=PALETTE["text_white"], fontsize=10)
    ax.set_ylabel("Shot Counts", color=PALETTE["text_white"], fontsize=10)

    plt.tight_layout()
    return fig


def plot_classical_noise_waveform(
    time_pts: np.ndarray,
    ideal_sig: np.ndarray,
    noisy_sig: np.ndarray,
    v_th: float,
    bit_errors: np.ndarray,
    ber: float,
    snr_db: float
) -> plt.Figure:
    """Plots ideal vs noisy waveform with threshold line and highlighted bit errors."""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9.5, 5.0), dpi=120, sharex=True)
    _apply_dark_style(fig, ax1)
    _apply_dark_style(fig, ax2)

    # Upper subplot: Continuous voltage waveform
    ax1.plot(time_pts, ideal_sig, color=PALETTE["cyan"], lw=2.2, label="Ideal V_ideal(t)")
    ax1.plot(time_pts, noisy_sig, color=PALETTE["bright_blue"], lw=1.2, alpha=0.85, label="Noisy V_out(t)")
    ax1.axhline(v_th, color=PALETTE["accent_amber"], ls="--", lw=1.8, label=f"Threshold V_th ({v_th:.2f}V)")

    # Error points where noise causes incorrect decision
    err_indices = np.where(bit_errors)[0]
    if len(err_indices) > 0:
        ax1.scatter(time_pts[err_indices], noisy_sig[err_indices], color=PALETTE["accent_coral"], s=35, zorder=6,
                    label=f"Bit Flip Errors ({len(err_indices)})")

    ax1.set_title(f"Classical Signal with Gaussian Noise (SNR: {snr_db:.1f} dB, BER: {ber*100:.2f}%)",
                  color=PALETTE["text_white"], fontsize=11, fontweight="bold")
    ax1.set_ylabel("Voltage (V)", color=PALETTE["text_white"], fontsize=10)
    ax1.legend(facecolor=PALETTE["card_navy"], edgecolor=PALETTE["grid_color"], labelcolor=PALETTE["text_white"], fontsize=8, loc="upper right")

    # Lower subplot: Interpreted Digital Logic (0 / 1)
    detected_bits = (noisy_sig >= v_th).astype(int)
    ideal_bits = (ideal_sig >= v_th).astype(int)
    ax2.step(time_pts, ideal_bits, color=PALETTE["cyan"], where="mid", lw=2, label="Ideal Digital Bit")
    ax2.step(time_pts, detected_bits, color=PALETTE["accent_coral"], where="mid", lw=1.2, alpha=0.7, label="Decoded Bit (Thresholded)")
    ax2.set_yticks([0, 1])
    ax2.set_yticklabels(["LOW (0)", "HIGH (1)"])
    ax2.set_xlabel("Sample Time Index", color=PALETTE["text_white"], fontsize=10)
    ax2.set_ylabel("Digital Logic", color=PALETTE["text_white"], fontsize=10)
    ax2.legend(facecolor=PALETTE["card_navy"], edgecolor=PALETTE["grid_color"], labelcolor=PALETTE["text_white"], fontsize=8, loc="upper right")

    plt.tight_layout()
    return fig
