"""
ISTARI -- Integrated Structural Testing and Acoustic Resonance Intelligence
Streamlit Demo App

Structural health monitoring via Acoustics + Vibration + Computer Vision.
Origin Weekend Fall 2026 | Team ISTARI | Mithrandir Dynamics
"""

import streamlit as st
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import tempfile, os

from pipeline.acoustic import analyze_acoustic
from pipeline.vibration import analyze_vibration
from pipeline.fusion import compute_health_index
from pipeline.demo_data import get_demo_results

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ISTARI | Structural Health Monitor",
    page_icon="🔊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ──────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #0D1117; color: #E6EDF3; }
    .stApp { background-color: #0D1117; }
    h1, h2, h3 { color: #58A6FF; }
    .metric-box {
        background: #161B22; border: 1px solid #30363D;
        border-radius: 8px; padding: 16px; text-align: center; margin: 4px;
    }
    .health-score {
        font-size: 64px; font-weight: 800; line-height: 1;
    }
    .tier-badge {
        font-size: 20px; font-weight: 700; padding: 4px 16px;
        border-radius: 20px; display: inline-block; margin-top: 8px;
    }
    .stButton>button {
        background-color: #1F6FEB; color: white; border: none;
        border-radius: 6px; font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)


# ── Sidebar ─────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.image("https://raw.githubusercontent.com/tariqnazar/ISTARI/main/assets/logo.png",
             use_column_width=True) if False else None
    st.markdown("## ISTARI")
    st.markdown("**I**ntegrated **S**tructural **T**esting and **A**coustic **R**esonance **I**ntelligence")
    st.markdown("---")
    st.markdown("**Three-Modality Platform**")
    st.markdown("- Acoustics (45%)")
    st.markdown("- Vibrations (30%)")
    st.markdown("- Computer Vision (25%)")
    st.markdown("---")
    st.markdown("**Team ISTARI**")
    st.markdown("Tariq Nazar | Ishan Bhakta")
    st.markdown("Adolfo Balderas | Amogh Skanda")
    st.markdown("Solal Chasques")
    st.markdown("---")
    st.markdown("*Origin Weekend Fall 2026*")
    st.markdown("*Mithrandir Dynamics*")

    demo_mode = st.checkbox("Use Figueroa Overpass Sample Data", value=True,
                             help="Pre-loaded field recordings from I-110 Figueroa St overpass (Sep 27, 2026)")


# ── Main content ────────────────────────────────────────────────────────────────
st.title("ISTARI Structural Health Monitor")
st.markdown("Upload AmbiX field recordings to assess structural health using acoustic resonance and vibration analysis.")

tab1, tab2, tab3 = st.tabs(["Upload & Analyze", "Results & Health Score", "About ISTARI"])


# ── Tab 1: Upload ───────────────────────────────────────────────────────────────
with tab1:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Contact Recording (Vibration)")
        st.caption("H3-VR taped directly to structure -- captures structure-borne vibration via acoustic coupling")
        if demo_mode:
            st.info("Using sample: Figueroa Overpass Pillar 01 contact recording (8 min)")
            contact_file = "data/sample/260927_001.WAV"
        else:
            contact_upload = st.file_uploader("Upload contact WAV (AmbiX 4-channel)", type=["wav", "WAV"],
                                               key="contact")
            contact_file = None
            if contact_upload:
                with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
                    tmp.write(contact_upload.read())
                    contact_file = tmp.name

    with col2:
        st.subheader("Acoustic Recordings (Standoff)")
        st.caption("H3-VR on tripod at measured distances -- captures airborne structural radiation")
        if demo_mode:
            st.info("Using sample: 0.3m, 1m, 3m standoff recordings from same pillar")
            acoustic_files = [
                ("data/sample/260927_002.WAV", "Acoustic 0.3m"),
                ("data/sample/260927_003.WAV", "Acoustic 1m"),
                ("data/sample/260927_004.WAV", "Acoustic 3m"),
            ]
        else:
            acoustic_uploads = st.file_uploader("Upload acoustic WAVs (AmbiX 4-channel)",
                                                 type=["wav", "WAV"], accept_multiple_files=True,
                                                 key="acoustic")
            acoustic_files = []
            if acoustic_uploads:
                for i, f in enumerate(acoustic_uploads):
                    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
                        tmp.write(f.read())
                        acoustic_files.append((tmp.name, f.name))

    st.markdown("---")

    visual_score_input = st.slider(
        "Visual / CV Score (0 = severe cracking, 1 = no visible damage)",
        min_value=0.0, max_value=1.0, value=0.5, step=0.05,
        help="Manual input until CV pipeline is fully integrated. 0.5 = no visual data available."
    )

    run_btn = st.button("Run ISTARI Analysis", use_container_width=True)


# ── Analysis logic ──────────────────────────────────────────────────────────────
if run_btn or (demo_mode and not st.session_state.get('ready')):
    if demo_mode:
        with st.spinner("Loading Figueroa Overpass field data..."):
            vib_result, acoustic_results = get_demo_results()
    else:
        if not contact_file:
            st.warning("Please upload a contact recording to proceed.")
            st.stop()

        with st.spinner("Running acoustic pipeline..."):
            try:
                vib_result = analyze_vibration(contact_file, label="Contact (Vibration)")
            except Exception as e:
                st.error(f"Vibration analysis failed: {e}")
                st.stop()

        acoustic_results = []
        for fpath, flabel in acoustic_files:
            with st.spinner(f"Analyzing {flabel}..."):
                try:
                    res = analyze_acoustic(fpath, label=flabel)
                    acoustic_results.append(res)
                except Exception as e:
                    st.warning(f"Could not analyze {flabel}: {e}")

        if not acoustic_results:
            st.error("No acoustic recordings could be analyzed.")
            st.stop()

    # Average acoustic score across standoff distances
    avg_acoustic_score = np.mean([r['acoustic_score'] for r in acoustic_results])

    # Fusion
    fusion = compute_health_index(
        acoustic_score=avg_acoustic_score,
        vibration_score=vib_result['vibration_score'],
        visual_score=visual_score_input
    )

    # Store in session state
    st.session_state['fusion'] = fusion
    st.session_state['vib_result'] = vib_result
    st.session_state['acoustic_results'] = acoustic_results
    st.session_state['ready'] = True


# ── Tab 2: Results ──────────────────────────────────────────────────────────────
with tab2:
    if not st.session_state.get('ready'):
        st.info("Run the analysis first in the Upload tab.")
    else:
        fusion = st.session_state['fusion']
        vib_result = st.session_state['vib_result']
        acoustic_results = st.session_state['acoustic_results']

        # Health score display
        tier_colors = {'HEALTHY': '#27AE60', 'WARNING': '#E67E22', 'CRITICAL': '#C0392B'}
        color = tier_colors[fusion['tier']]

        st.markdown(f"""
        <div style="text-align:center; padding: 32px; background:#161B22;
                    border-radius:12px; border:2px solid {color}; margin-bottom:24px;">
            <div style="color:#8B949E; font-size:14px; text-transform:uppercase;
                        letter-spacing:2px; margin-bottom:8px;">Structural Health Index</div>
            <div style="font-size:80px; font-weight:800; color:{color}; line-height:1;">
                {fusion['health_index']}</div>
            <div style="font-size:11px; color:#8B949E;">/ 100</div>
            <div style="margin-top:12px;">
                <span style="background:{color}; color:white; font-size:18px; font-weight:700;
                             padding:6px 24px; border-radius:20px;">{fusion['tier']}</span>
            </div>
            <div style="color:#8B949E; font-size:13px; margin-top:12px;">
                {fusion['recommendation']}</div>
        </div>
        """, unsafe_allow_html=True)

        # Score breakdown
        st.subheader("Score Breakdown")
        c1, c2, c3 = st.columns(3)
        bd = fusion['breakdown']
        with c1:
            st.metric("Acoustic Score", f"{bd['acoustic']['score']:.2f}",
                      help=f"Weight: {int(bd['acoustic']['weight']*100)}%")
        with c2:
            st.metric("Vibration Score", f"{bd['vibration']['score']:.2f}",
                      help=f"Weight: {int(bd['vibration']['weight']*100)}%")
        with c3:
            st.metric("Visual Score", f"{bd['visual']['score']:.2f}",
                      help=f"Weight: {int(bd['visual']['weight']*100)}%  |  {fusion['confidence_note']}")

        st.caption(f"Confidence: **{fusion['confidence']}** -- {fusion['confidence_note']}")

        st.markdown("---")

        # PSD Plots
        st.subheader("Power Spectral Density Analysis")

        all_results = [vib_result] + acoustic_results
        colors_list = ["#C0392B", "#2980B9", "#27AE60", "#8E44AD"]
        n = len(all_results)

        fig, axes = plt.subplots(n, 1, figsize=(12, 4 * n))
        fig.patch.set_facecolor('#0D1117')
        if n == 1:
            axes = [axes]

        for ax, res, col in zip(axes, all_results, colors_list):
            freq = res['freq']
            psd_db = res['psd_db']
            mask = (freq >= 1) & (freq <= 2000)

            ax.set_facecolor('#161B22')
            ax.plot(freq[mask], psd_db[mask], color=col, linewidth=0.8, alpha=0.9)

            # Mark detected peaks
            for pk in res.get('peaks', []):
                ax.axvline(x=pk['freq_hz'], color=col, alpha=0.4, linewidth=0.8, linestyle='--')
                ax.text(pk['freq_hz'], ax.get_ylim()[1] if ax.get_ylim()[1] != 1.0 else -25,
                        f"{pk['freq_hz']} Hz", fontsize=7, color='white', rotation=90,
                        va='top', ha='right')

            score_key = 'vibration_score' if 'vibration_score' in res else 'acoustic_score'
            score_val = res[score_key]
            ax.set_title(f"  {res['label']}  |  Score: {score_val:.2f}  |  {res['duration_s']/60:.1f} min",
                         color='white', fontsize=10, loc='left')
            ax.set_xscale('log')
            ax.set_xlim(1, 2000)
            ax.set_xlabel('Frequency (Hz)', color='#8B949E', fontsize=8)
            ax.set_ylabel('PSD [dB(Z)]', color='#8B949E', fontsize=8)
            ax.tick_params(colors='#8B949E', labelsize=7)
            ax.spines[:].set_color('#30363D')
            ax.grid(True, alpha=0.12, color='#8B949E', linewidth=0.3)
            ax.axvspan(1, 20, alpha=0.04, color='yellow')
            ax.axvspan(20, 500, alpha=0.04, color='cyan')

        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

        # Resonance frequency table
        st.subheader("Detected Resonance Frequencies")
        all_peaks = []
        for res in all_results:
            for pk in res.get('peaks', []):
                all_peaks.append({
                    'Source': res['label'],
                    'Frequency (Hz)': pk['freq_hz'],
                    'Amplitude (dB)': pk['amplitude_db'],
                    'Prominence (dB)': pk['prominence']
                })
        if all_peaks:
            import pandas as pd
            df = pd.DataFrame(all_peaks).sort_values('Frequency (Hz)')
            st.dataframe(df, use_container_width=True, hide_index=True)

        # Interpretation
        st.subheader("Interpretation")
        st.info(f"**Vibration:** {vib_result['interpretation']}")
        for res in acoustic_results:
            st.info(f"**{res['label']}:** {res['interpretation']}")


# ── Tab 3: About ────────────────────────────────────────────────────────────────
with tab3:
    st.subheader("What is ISTARI?")
    st.markdown("""
    ISTARI is a three-modality structural health monitoring platform that uses a single
    consumer-grade ambisonic microphone (Zoom H3-VR) to assess the structural integrity
    of bridges, columns, and infrastructure without contact sensors or expensive equipment.

    **The Problem**

    Current structural inspection methods are expensive, infrequent, and reactive.
    Piezoelectric sensor arrays cost $50k-$500k per installation. Visual inspections
    miss micro-cracks. The US has over 45,000 structurally deficient bridges.

    **The Solution**

    ISTARI captures three complementary signals from a single $350 device:

    | Modality | Method | What It Detects |
    |---|---|---|
    | Acoustics (45%) | AmbiX B-format PSD analysis | Resonance shifts from stiffness loss |
    | Vibrations (30%) | Contact-mode structure-borne sensing | Natural frequency drift, damping changes |
    | Computer Vision (25%) | YOLOv8 crack detection on video | Surface defects, spalling, corrosion |

    **Fusion Algorithm**

    ```
    health_index = 100 - (0.45 x acoustic_score x 100
                        + 0.30 x vibration_score x 100
                        + 0.25 x visual_score x 100)
    ```

    **Field Data**

    Today's demo uses real recordings captured at the Figueroa Street overpass
    over Interstate 110, Los Angeles (September 27, 2026).

    **Team**

    Tariq Nazar (Founder, Mithrandir Dynamics) | Ishan Bhakta | Adolfo Balderas |
    Amogh Skanda | Solal Chasques

    *Origin Weekend Fall 2026 -- USC Tiehub*
    """)
