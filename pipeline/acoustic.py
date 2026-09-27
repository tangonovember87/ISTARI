"""
ISTARI Acoustic Pipeline
AmbiX B-format processing: beamforming, PSD, resonance detection.
INTERNAL -- Not for distribution.
"""

import numpy as np
import soundfile as sf
from scipy import signal
from scipy.ndimage import uniform_filter1d


def load_ambix(filepath):
    """Load AmbiX B-format WAV. Returns (data, samplerate). Expects 4-channel file."""
    data, sr = sf.read(filepath, always_2d=True)
    if data.shape[1] < 4:
        raise ValueError(f"Expected 4-channel AmbiX, got {data.shape[1]} channels.")
    return data, sr


def beamform(data, azimuth_deg=0.0, elevation_deg=0.0):
    """
    AmbiX first-order beamforming.
    Steers a virtual cardioid microphone toward (azimuth, elevation).

    Formula: P(az,el) = W + X*cos(az)*cos(el) + Y*sin(az)*cos(el) + Z*sin(el)
    AmbiX channel order: W=0, Y=1, Z=2, X=3

    Args:
        data: (N, 4) array in AmbiX channel order [W, Y, Z, X]
        azimuth_deg: horizontal angle (0=front, 90=left, 180=back)
        elevation_deg: vertical angle (0=horizon, 90=above)

    Returns: (N,) beamformed mono signal
    """
    az = np.radians(azimuth_deg)
    el = np.radians(elevation_deg)

    W = data[:, 0]
    Y = data[:, 1]
    Z = data[:, 2]
    X = data[:, 3]

    # First-order pressure-velocity beamformer (cardioid pattern)
    beam = W + X * np.cos(az) * np.cos(el) \
             + Y * np.sin(az) * np.cos(el) \
             + Z * np.sin(el)
    return beam


def compute_psd(signal_data, sr, window_seconds=4):
    """Welch PSD. Returns (frequencies, psd_linear, psd_db)."""
    nperseg = int(sr * window_seconds)
    nperseg = min(nperseg, len(signal_data) // 4)
    freq, psd = signal.welch(signal_data, fs=sr, nperseg=nperseg,
                              noverlap=nperseg // 2, window='hann')
    psd_db = 10 * np.log10(psd + 1e-20)
    return freq, psd, psd_db


def compute_fdd_psd(data, sr, window_seconds=4):
    """
    Frequency Domain Decomposition (OMA).
    Computes cross-spectral density matrix across all 4 channels,
    takes SVD at each frequency bin, returns first singular value vector.
    First SV peaks correspond to structural natural frequencies.
    """
    n_ch = data.shape[1]
    nperseg = int(sr * window_seconds)
    nperseg = min(nperseg, data.shape[0] // 4)

    # Compute cross-spectral density matrix [n_freq, n_ch, n_ch]
    freq = None
    G = None
    for i in range(n_ch):
        for j in range(n_ch):
            f, csd = signal.csd(data[:, i], data[:, j], fs=sr,
                                nperseg=nperseg, noverlap=nperseg // 2)
            if G is None:
                G = np.zeros((len(f), n_ch, n_ch), dtype=complex)
                freq = f
            G[:, i, j] = csd

    # SVD at each frequency, extract first singular value
    sv1 = np.array([np.linalg.svd(G[k], compute_uv=False)[0] for k in range(len(freq))])
    sv1_db = 10 * np.log10(sv1 + 1e-20)
    return freq, sv1_db


def detect_peaks(freq, psd_db, f_min=1.0, f_max=2000.0, top_n=8):
    """Detect structural resonance peaks. Returns list of dicts."""
    mask = (freq >= f_min) & (freq <= f_max)
    f = freq[mask]
    p = psd_db[mask]
    p_smooth = uniform_filter1d(p, size=20)

    peaks_idx, props = signal.find_peaks(
        p_smooth,
        height=np.percentile(p_smooth, 60),
        distance=30,
        prominence=1.5
    )
    if len(peaks_idx) == 0:
        return []

    order = np.argsort(props['prominences'])[::-1][:top_n]
    results = []
    for i in order:
        # Half-power bandwidth for damping ratio: zeta = (f2-f1)/(2*fn)
        fn = f[peaks_idx[i]]
        amp_peak = p[peaks_idx[i]]
        amp_3db = amp_peak - 3.0
        # Find -3dB crossings around peak
        left_idx = peaks_idx[i]
        right_idx = peaks_idx[i]
        while left_idx > 0 and p_smooth[left_idx] > amp_3db:
            left_idx -= 1
        while right_idx < len(p_smooth) - 1 and p_smooth[right_idx] > amp_3db:
            right_idx += 1
        f1 = f[left_idx]
        f2 = f[right_idx]
        zeta = (f2 - f1) / (2 * fn) if fn > 0 else None

        results.append({
            'freq_hz': round(float(fn), 2),
            'amplitude_db': round(float(amp_peak), 2),
            'prominence': round(float(props['prominences'][i]), 2),
            'damping_ratio': round(float(zeta), 4) if zeta is not None else None,
            'bandwidth_hz': round(float(f2 - f1), 2),
        })

    return sorted(results, key=lambda x: x['freq_hz'])


def acoustic_health_score(peaks, fundamental_range=(10, 30)):
    """
    Acoustic health score 0.0-1.0.
    Higher prominence fundamental = stiffer structure = healthier.
    Higher damping ratio = energy dissipation = damage indicator.
    """
    if not peaks:
        return 0.5, "Insufficient spectral data"

    fund_peaks = [p for p in peaks if fundamental_range[0] <= p['freq_hz'] <= fundamental_range[1]]

    if fund_peaks:
        best = max(fund_peaks, key=lambda x: x['prominence'])
        prominence_score = min(best['prominence'] / 10.0, 1.0)

        # Damping penalty: high damping ratio indicates damage
        zeta = best.get('damping_ratio') or 0.02
        damping_penalty = min(zeta / 0.10, 0.3)  # max 30% penalty at zeta=0.10
        score = 0.4 + 0.6 * prominence_score - damping_penalty
        score = max(0.0, min(1.0, score))

        damping_str = f", zeta={zeta:.3f}" if best.get('damping_ratio') else ""
        interp = (f"Fundamental at {best['freq_hz']} Hz "
                  f"(prominence: {best['prominence']:.1f} dB{damping_str})")
    else:
        score = 0.35
        interp = "No clear fundamental in 10-30 Hz band -- possible stiffness reduction"

    high_freq = [p for p in peaks if p['freq_hz'] > 500]
    if len(high_freq) > 3:
        score = max(score - 0.1, 0.0)
        interp += " | High-frequency peak dominance"

    return round(score, 3), interp


def analyze_acoustic(filepath, label="Acoustic", az_deg=0.0, el_deg=0.0):
    """
    Full acoustic pipeline: beamform + PSD + FDD-OMA + peak detection + health score.
    """
    data, sr = load_ambix(filepath)
    duration = data.shape[0] / sr

    # Beamformed signal toward structure
    beam = beamform(data, azimuth_deg=az_deg, elevation_deg=el_deg)

    # Standard PSD on beamformed signal
    freq, psd_lin, psd_db = compute_psd(beam, sr)

    # FDD-OMA on all 4 channels
    freq_fdd, sv1_db = compute_fdd_psd(data, sr)

    # Peak detection on beamformed PSD
    peaks = detect_peaks(freq, psd_db)

    # Also find OMA peaks
    oma_peaks = detect_peaks(freq_fdd, sv1_db, top_n=5)

    score, interpretation = acoustic_health_score(peaks)

    return {
        'label': label,
        'duration_s': round(duration, 1),
        'sample_rate': sr,
        'channels': data.shape[1],
        'beamform_az': az_deg,
        'beamform_el': el_deg,
        'freq': freq,
        'psd_db': psd_db,
        'freq_fdd': freq_fdd,
        'sv1_db': sv1_db,
        'peaks': peaks,
        'oma_peaks': oma_peaks,
        'acoustic_score': score,
        'interpretation': interpretation,
    }
