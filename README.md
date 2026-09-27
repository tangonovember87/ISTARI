# ISTARI
**Integrated Structural Testing and Acoustic Resonance Intelligence**

A three-modality structural health monitoring platform using a single consumer-grade ambisonic microphone.

## What It Does

ISTARI assesses bridge and infrastructure integrity without expensive contact sensor arrays. Using a Zoom H3-VR ambisonic recorder, it captures:

| Modality | Method | Weight |
|---|---|---|
| Acoustics | AmbiX B-format PSD -- resonance shift detection | 45% |
| Vibrations | Contact-mode structure-borne sensing via W-channel | 30% |
| Computer Vision | YOLOv8 crack detection on video frames | 25% |

These feed into a weighted fusion algorithm:

```
health_index = 100 - (0.45 x acoustic_score x 100
                    + 0.30 x vibration_score x 100
                    + 0.25 x visual_score x 100)
```

Output: health score 0-100 with HEALTHY / WARNING / CRITICAL classification.

## Demo

The app includes pre-loaded field recordings captured at the **Figueroa Street overpass over I-110, Los Angeles** (September 27, 2026). Consistent structural resonance detected at ~20 Hz across all four measurement positions.

## Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Run on Replit

Import this repo into Replit. The `.replit` file configures the run command automatically.

## Upload Your Own Data

The app accepts 4-channel AmbiX WAV files (recorded with Zoom H3-VR or any compatible ambisonic recorder). Upload your contact recording and standoff recordings via the interface.

## Team

- Tariq Nazar -- Founder, Mithrandir Dynamics
- Ishan Bhakta
- Adolfo Balderas
- Amogh Skanda
- Solal Chasques

*Origin Weekend Fall 2026 -- USC Tiehub*
*Prompt D: Infrastructure and Resilience*
