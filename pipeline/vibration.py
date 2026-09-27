"""
ISTARI Vibration Pipeline
Contact-mode AmbiX processing: OMA, damping ratio extraction, structural health scoring.
INTERNAL -- Not for distribution.
"""

import numpy as np
import soundfile as sf
from scipy import signal
from scipy.ndimage import uniform_filter1d


def analyze_vibration(filepath, label="Contact (Vibration)"):
    """
    Full vibration pipeline for contact-mode recording.
    Implements:
    - Structure-borne vibration via W-channel acoustic coupling
    - OMA peak picking in structural band (1-500 Hz)
    - Damping ratio extraction via half-power bandwidth
    - Modal health scoring based on stiffness indicators
    """
    data, sr = sf.read(filepath, always_2d=True)
    w = data[:, 0]
    duration = len(w) / sr

    # Long windows for low-frequency resolution (SDOF physics: fn = 1/2pi * sqrt(k/m))
    nperseg = int(sr * 8)
    nperseg = min(nperseg, len(w) // 4)
    freq, psd = signal.welch(w, fs=sr, nperseg=nperseg,
                              noverlap=nperseg // 2, window='hann')
    psd_db = 10 * np.log10(psd + 1e-20)

    # Structural band
    mask = (freq >= 1) & (freq <= 500)
    f_struct = freq[mask]
    p_struct = psd_db[mask]
    p_smooth = uniform_filter1d(p_struct, size=15)

    peaks_idx, props = signal.find_peaks(
        p_smooth,
        height=np.percentile(p_smooth, 65),
        distance=20,
        prominence=1.0
    )

    peaks = []
    if len(peaks_idx) > 0:
        order = np.argsort(props['prominences'])[::-1][:6]
        for i in order:
            fn = f_struct[peaks_idx[i]]
            amp_peak = p_struct[peaks_idx[i]]

            # Half-power bandwidth: damping ratio zeta = (f2-f1)/(2*fn)
            # Limit search to fn/2 on each side to avoid noise floor contamination
            amp_3db = amp_peak - 3.0
            max_search = int((fn / 2) / (f_struct[1] - f_struct[0])) if len(f_struct) > 1 else 50
            max_search = max(5, min(max_search, 200))
            li = peaks_idx[i]
            ri = peaks_idx[i]
            for _ in range(max_search):
                if li <= 0 or p_smooth[li] <= amp_3db:
                    break
                li -= 1
            for _ in range(max_search):
                if ri >= len(p_smooth) - 1 or p_smooth[ri] <= amp_3db:
                    break
                ri += 1
            f1 = f_struct[li]
            f2 = f_struct[ri]
            bandwidth = float(f2 - f1)
            zeta = min(bandwidth / (2 * fn), 0.20) if fn > 0 else 0.02  # cap at 20%

            peaks.append({
                'freq_hz': round(float(fn), 2),
                'amplitude_db': round(float(amp_peak), 2),
                'prominence': round(float(props['prominences'][i]), 2),
                'damping_ratio': round(float(zeta), 4),
                'bandwidth_hz': round(bandwidth, 2),
                'interpretation': _mode_interpretation(fn, zeta),
            })
        peaks = sorted(peaks, key=lambda x: x['freq_hz'])

    score, interpretation = vibration_health_score(peaks)

    return {
        'label': label,
        'duration_s': round(duration, 1),
        'sample_rate': sr,
        'freq': freq,
        'psd_db': psd_db,
        'freq_struct': f_struct,
        'psd_struct': p_struct,
        'peaks': peaks,
        'vibration_score': score,
        'interpretation': interpretation,
    }


def _mode_interpretation(fn, zeta):
    """Human-readable interpretation of a single mode."""
    health = "Healthy" if zeta < 0.03 else ("Moderate" if zeta < 0.06 else "Elevated damping -- inspect")
    return f"fn={fn:.1f} Hz, zeta={zeta:.3f} ({health})"


def vibration_health_score(peaks, target_band=(5, 50)):
    """
    Vibration health score (0.0=damaged, 1.0=healthy).

    Physics basis (from SDOF: mẍ + cẋ + kx = F(t)):
    - fn = (1/2pi)*sqrt(k/m): damage reduces k, lowering fn
    - zeta = c/(2*sqrt(km)): damage increases c (energy dissipation), raising zeta
    - Healthy: sharp peaks (low zeta), fn in expected range
    - Damaged: broadened peaks (high zeta), fn shifted down
    """
    if not peaks:
        return 0.4, "No structural modes detected in contact recording"

    primary = max(peaks, key=lambda x: x['prominence'])
    fn = primary['freq_hz']
    zeta = primary.get('damping_ratio', 0.02)
    prominence = primary['prominence']

    # Prominence score (sharpness of resonance = low damping = healthy)
    prominence_score = min(prominence / 8.0, 1.0)

    # Damping score: healthy concrete zeta < 0.02-0.03
    # Damaged: zeta > 0.05-0.08
    if zeta < 0.025:
        damping_score = 1.0
        damping_note = "Low damping -- healthy"
    elif zeta < 0.05:
        damping_score = 0.7
        damping_note = "Moderate damping"
    elif zeta < 0.08:
        damping_score = 0.4
        damping_note = "Elevated damping -- possible damage"
    else:
        damping_score = 0.2
        damping_note = "High damping -- inspect urgently"

    # Frequency score: is fn in expected range for this element?
    if target_band[0] <= fn <= target_band[1]:
        freq_score = 1.0
        freq_note = f"fn={fn:.1f} Hz in expected band"
    elif fn < target_band[0]:
        freq_score = 0.6
        freq_note = f"fn={fn:.1f} Hz below expected band (possible stiffness loss)"
    else:
        freq_score = 0.8
        freq_note = f"fn={fn:.1f} Hz above expected band"

    # Combined score
    score = 0.4 * prominence_score + 0.4 * damping_score + 0.2 * freq_score
    score = max(0.0, min(1.0, score))

    if len(peaks) >= 3:
        score = min(score + 0.05, 1.0)

    interp = f"{freq_note} | {damping_note} | {len(peaks)} mode(s) identified"
    return round(score, 3), interp
