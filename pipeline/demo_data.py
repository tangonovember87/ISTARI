"""
Pre-computed analysis results from ISTARI field recording session.
Location: Figueroa Street overpass over I-110, Los Angeles, CA
Date: September 27, 2026
Equipment: Zoom H3-VR ambisonic microphone (AmbiX B-format, 48kHz/24-bit)

This module provides hardcoded demo results so the app can run without
loading the raw WAV files (which are 850MB total).
"""

import numpy as np

# Simulated PSD curves based on actual field measurements
# These reproduce the spectral shape observed in the Figueroa recordings

def _make_psd_curve(sr=48000, duration_s=300, dominant_hz=20.0, seed=42):
    """Generate a realistic structural PSD curve matching field observations."""
    rng = np.random.default_rng(seed)
    freq = np.linspace(1, 24000, 8000)

    # 1/f^2 background (typical urban vibration noise floor)
    base = -20 - 20 * np.log10(freq / 10.0 + 1e-6)

    # Add structural resonance peaks
    def add_peak(f_arr, psd, f0, amplitude, width=2.0):
        psd = psd + amplitude * np.exp(-((np.log(f_arr + 1e-6) - np.log(f0)) ** 2) / (2 * (width / f0) ** 2))
        return psd

    psd = base.copy()
    psd = add_peak(freq, psd, dominant_hz, 8.0, 3.0)        # Primary structural mode
    psd = add_peak(freq, psd, dominant_hz * 5.5, 4.0, 5.0)  # Higher mode
    psd = add_peak(freq, psd, dominant_hz * 20, 3.0, 8.0)   # High-freq mode

    # Add noise
    psd += rng.normal(0, 1.0, len(freq))
    return freq, psd


DEMO_CONTACT = {
    'label': 'Contact (Vibration) -- Figueroa Overpass Pillar 01',
    'duration_s': 478.0,
    'sample_rate': 48000,
    'peaks': [
        {'freq_hz': 20.2, 'amplitude_db': -24.8, 'prominence': 7.1},
    ],
    'vibration_score': 0.74,
    'interpretation': 'Primary mode at 20.2 Hz -- within expected structural band (5-50 Hz) | 1 mode identified',
    '_freq_seed': 42,
    '_dominant_hz': 20.2,
}

DEMO_ACOUSTIC_03 = {
    'label': 'Acoustic 0.3m -- Figueroa Overpass Pillar 01',
    'duration_s': 322.1,
    'sample_rate': 48000,
    'peaks': [
        {'freq_hz': 17.5, 'amplitude_db': -30.1, 'prominence': 6.3},
        {'freq_hz': 112.5, 'amplitude_db': -36.2, 'prominence': 3.8},
        {'freq_hz': 408.5, 'amplitude_db': -48.1, 'prominence': 2.1},
    ],
    'acoustic_score': 0.71,
    'interpretation': 'Fundamental mode detected at 17.5 Hz (prominence: 6.3 dB)',
    '_freq_seed': 43,
    '_dominant_hz': 17.5,
}

DEMO_ACOUSTIC_1 = {
    'label': 'Acoustic 1m -- Figueroa Overpass Pillar 01',
    'duration_s': 342.8,
    'sample_rate': 48000,
    'peaks': [
        {'freq_hz': 21.2, 'amplitude_db': -27.4, 'prominence': 5.9},
        {'freq_hz': 202.2, 'amplitude_db': -40.8, 'prominence': 3.1},
        {'freq_hz': 454.8, 'amplitude_db': -49.2, 'prominence': 2.4},
    ],
    'acoustic_score': 0.69,
    'interpretation': 'Fundamental mode detected at 21.2 Hz (prominence: 5.9 dB)',
    '_freq_seed': 44,
    '_dominant_hz': 21.2,
}

DEMO_ACOUSTIC_3 = {
    'label': 'Acoustic 3m -- Figueroa Overpass Pillar 01',
    'duration_s': 331.4,
    'sample_rate': 48000,
    'peaks': [
        {'freq_hz': 21.5, 'amplitude_db': -29.3, 'prominence': 5.4},
        {'freq_hz': 422.5, 'amplitude_db': -51.0, 'prominence': 2.0},
    ],
    'acoustic_score': 0.66,
    'interpretation': 'Fundamental mode detected at 21.5 Hz (prominence: 5.4 dB)',
    '_freq_seed': 45,
    '_dominant_hz': 21.5,
}


def get_demo_results():
    """Return pre-computed demo results with synthetic PSD curves."""
    results = []
    for rec in [DEMO_CONTACT, DEMO_ACOUSTIC_03, DEMO_ACOUSTIC_1, DEMO_ACOUSTIC_3]:
        r = dict(rec)
        freq, psd_db = _make_psd_curve(
            dominant_hz=rec['_dominant_hz'],
            seed=rec['_freq_seed']
        )
        r['freq'] = freq
        r['psd_db'] = psd_db
        results.append(r)

    vib_result = results[0]
    acoustic_results = results[1:]
    return vib_result, acoustic_results
