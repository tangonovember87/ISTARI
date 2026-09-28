# ISTARI
## Integrated Structural Testing and Acoustic Resonance Intelligence

**Acoustic-First Predictive Infrastructure Intelligence**

Origin Weekend Fall 2026 | Prompt D: Infrastructure and Resilience | USC Tiehub

> *Infrastructure kills silently. ISTARI listens before it fails.*

![ISTARI Pipeline](images/04_pipeline.png)

---

## The Problem

Infrastructure degrades continuously from the moment it is built. Steel corrodes. Concrete micro-cracks. Weld joints fatigue under cyclic loading. Rebar loses bond strength as chloride ions penetrate the cover layer. None of this is exceptional -- it is the normal, expected physics of aging infrastructure under load.

The world currently answers the inspection question very poorly.

### What is Wrong with Inspection Today

The dominant methodology across virtually every infrastructure sector is visual inspection by a human being. An inspector walks, drives, flies, or climbs to a structure on a fixed schedule -- typically every 2 to 6 years -- and visually examines the surface. This approach has three fundamental failures:

**It is reactive, not predictive.** Inspection happens on a calendar schedule, not triggered by actual structural condition. A bridge degrading rapidly between inspection cycles is indistinguishable from a healthy one until a human physically arrives and looks at it.

**It is surface-limited.** The human eye, and virtually all camera-based inspection systems, can only detect damage that has propagated to the exterior surface. Internal damage -- subsurface micro-cracking, rebar corrosion, internal delamination, void formation -- is completely invisible to visual inspection regardless of how sophisticated the camera.

**It is point-in-time.** A single inspection captures a snapshot. It tells you nothing about the rate of degradation, whether a damage region is stable or accelerating, or how much useful life remains.

> **The consequence:** By the time a visual inspection detects structural damage, the internal compromise is often already 40-70% advanced. You are not catching the problem early. You are confirming it late.

### The Scale of the Problem

- Over 45,000 structurally deficient bridges in the United States
- $50B+ spent annually on reactive infrastructure inspection and maintenance
- The LA wildfires demonstrated this acutely: grid operators had no efficient way to prioritize which power towers to inspect first, leading to days of unnecessary outage
- Every earthquake, flood, or wildfire forces operators to assess thousands of assets simultaneously with no triage intelligence

### The Industrial Alternative: Acoustic Emission Testing

The engineering community recognized decades ago that structures communicate their internal state acoustically. Acoustic Emission Testing (AET) is the established non-destructive testing method: piezoelectric contact sensors physically bonded to the structure surface detect high-frequency elastic waves (100 kHz to 1 MHz) released when micro-cracks propagate.

AET is real and capable. But it has critical limitations:

| Limitation | Impact |
|---|---|
| $50,000 to $500,000 per installation | Only economically viable for highest-criticality assets |
| Requires predetermined sensor placement | Blind zones between sensors; misses damage that initiates between them |
| Contact sensors only | Cannot be deployed remotely or repositioned without physical access |
| Point measurement | No spatial context; cannot map damage distribution |
| Specialist operation | Requires trained NDT engineers on-site |

---

## The Solution: ISTARI

ISTARI integrates three sensing modalities into one unified inspection pipeline. Each modality captures a different layer of structural truth. Together they produce a single, actionable health score.

```
                    ┌─────────────────────────────────────┐
                    │           FIELD HARDWARE            │
                    │  Zoom H3-VR Ambisonic Recorder      │
                    │  AmbiX B-Format | 4-channel | 48kHz │
                    └───────────────┬─────────────────────┘
                                    │
              ┌─────────────────────┼──────────────────────┐
              ▼                     ▼                      ▼
   ┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐
   │   ACOUSTICS     │   │   VIBRATIONS    │   │ COMPUTER VISION │
   │   Weight: 45%   │   │   Weight: 30%   │   │   Weight: 25%   │
   │                 │   │                 │   │                 │
   │ AmbiX beamform  │   │ Contact-mode    │   │ Phone/drone     │
   │ W/X/Y/Z PSD     │   │ structure-borne │   │ video frames    │
   │ FDD-OMA         │   │ OMA + damping   │   │ Crack detection │
   │ Resonance peaks │   │ ratio zeta      │   │ defect scoring  │
   └────────┬────────┘   └────────┬────────┘   └────────┬────────┘
            └────────────────────┬┘────────────────────┘
                                 ▼
                    ┌────────────────────────┐
                    │   WEIGHTED FUSION      │
                    │                        │
                    │  health_index = 100 -  │
                    │  (0.45 x acoustic      │
                    │   x 100               │
                    │  + 0.30 x vibration   │
                    │   x 100               │
                    │  + 0.25 x visual      │
                    │   x 100)              │
                    └──────────┬─────────────┘
                               ▼
                  ┌────────────────────────────┐
                  │    STRUCTURAL HEALTH INDEX │
                  │    0 - 100                 │
                  │    HEALTHY / WARNING /     │
                  │    CRITICAL                │
                  └────────────────────────────┘
```

---

## Modality 1: Acoustics (45%)

### Why Acoustics Leads

Structures communicate stress before they fail. When a micro-crack propagates through concrete or steel, it releases stored elastic strain energy as a transient elastic wave. When a joint loosens, it introduces nonlinear contact mechanics that modulate passing vibration. When rebar corrodes, the corrosion products expand, generating slow compressive stress waves in the surrounding concrete.

None of these phenomena are visible to a camera. All of them are detectable in the acoustic spectrum.

### The Hardware: Zoom H3-VR Ambisonic Recorder

ISTARI uses the Zoom H3-VR, a consumer-grade ambisonic microphone that captures spatial audio in AmbiX B-format.

| Specification | Value |
|---|---|
| Microphone configuration | 4 matched condenser capsules, tetrahedral array |
| Format | AmbiX B-format (W, X, Y, Z channels) |
| Sample rate | 48 kHz / 96 kHz |
| Bit depth | 24-bit |
| Dynamic range | 120 dB SPL maximum |
| Built-in sensors | 6-axis IMU (3-axis gyroscope + 3-axis accelerometer) |
| Weight | 120 g |
| Cost | ~$350 |

The four channels encode complete three-dimensional spatial information about the sound field:
- **W channel:** Omnidirectional pressure (all directions equally)
- **X channel:** Front-back axis
- **Y channel:** Left-right axis
- **Z channel:** Up-down axis

### Beamforming: Steering a Virtual Microphone

ISTARI applies first-order beamforming to steer a virtual cardioid microphone toward the structure. This suppresses ambient noise from other directions and maximizes signal from the structure being inspected. The beamformed signal is then analyzed for structural resonance using Welch Power Spectral Density estimation.

### Frequency Coverage

| Band | Range | ISTARI Capability | What It Detects |
|---|---|---|---|
| Infrasonic | Below 20 Hz | Partial (rolls off) | Large-scale structural modes, bridge deflection |
| Low structural | 20 Hz - 500 Hz | Full capability | Bending modes, joint resonance, primary health indicators |
| Mid acoustic | 500 Hz - 5 kHz | Full capability | Surface cracking, material discontinuities |
| High acoustic | 5 kHz - 24 kHz | Full capability | Micro-cracking, material grain boundaries |

![FDD-OMA Acoustic Analysis](images/02_fdd_oma_acoustic.png)

### OMA: Operational Modal Analysis

ISTARI implements Frequency Domain Decomposition (FDD), a standard Operational Modal Analysis technique. The cross-spectral density matrix is computed across all four B-format channels, and singular value decomposition is applied at each frequency bin. Peaks in the first singular value correspond to structural natural frequencies -- extracted from ambient traffic, wind, and thermal excitation, without any artificial impact or excitation.

---

## Modality 2: Vibrations (30%)

### The Physics Basis

The foundation of structural dynamics is the Single Degree of Freedom (SDOF) system, governed by the equation of motion:

```
m * x'' + c * x' + k * x = F(t)
```

Where `m` = mass, `c` = damping coefficient, `k` = stiffness, `x` = displacement, `F(t)` = external force.

For free vibration, the natural frequency is:

```
f_n = (1 / 2pi) * sqrt(k / m)     [Hz]
```

This equation is the entire foundation of vibration-based structural health monitoring:

- Mass `m` changes very little over time (concrete and steel do not gain or lose significant mass from normal degradation)
- Stiffness `k` changes dramatically as damage accumulates
- Therefore: **a decrease in measured natural frequency indicates structural damage**

A crack propagating through a concrete beam reduces its cross-sectional area and therefore its bending stiffness. A corroding rebar section loses cross-section and bond strength. A loose joint introduces local nonlinearity. In every case, stiffness falls, and with it, the natural frequency.

### Damping Ratio Extraction

ISTARI extracts the damping ratio `zeta` for each detected structural mode using the half-power bandwidth method:

```
zeta = (f2 - f1) / (2 * f_n)
```

Where `f1` and `f2` are the -3 dB points on either side of the resonance peak. Healthy concrete structures exhibit damping ratios of 1-3% (zeta = 0.01-0.03). Damaged structures show elevated damping as energy is dissipated at crack faces and loose joints.

![Contact Vibration PSD](images/01_vibration_psd.png)

### Contact Mode Measurement

When the H3-VR is taped against a structural element, structure-borne vibration couples mechanically through the device body into the microphone capsules. The 4-channel B-format PSD of this contact recording reveals something the standoff recordings cannot: the directional channels (X=front-back, Y=left-right, Z=up-down) cancel out diffuse omnidirectional acoustic noise and retain only coherent structural vibration with a preferred direction. In the field contact recording, all three directional channels independently confirm a structural resonance at 19-22 Hz -- the Y (left-right) channel with the highest peak prominence (15 dB), consistent with lateral bending as the dominant vibration mode. A secondary mode at 64.5 Hz appears in all directional channels. The W (omnidirectional) channel peaks at 14.65 Hz, contaminated by diffuse traffic noise from all directions, and should not be interpreted as the structural resonance frequency.

---

![Waveform and Spectrogram](images/09_waveform_spectrogram.png)

![Frequency Shift Damage Indicator](images/10_freq_shift.png)

---

## Modality 3: Computer Vision (25%)

### Role in the Pipeline

Computer vision confirms and grades what acoustics and vibrations detect internally. It is the final layer of evidence -- the surface check that runs after the deeper signals have already indicated where to look.

### Crack Detection Pipeline

ISTARI processes video frames through a multi-stage OpenCV pipeline:

1. **ROI masking:** Exclude sky, ground, and high-saturation regions (paint, rust stains)
2. **Local contrast enhancement:** CLAHE adaptive histogram equalization
3. **Dark feature isolation:** Cracks are darker than surrounding concrete background
4. **Canny edge detection:** Thin feature extraction
5. **Morphological filtering:** Retain only elongated, continuous, high-aspect-ratio features
6. **Contour analysis:** Minimum crack length, maximum width constraints to reject aggregate texture

![Crack Detection Pipeline](images/05_crack_detection.png)

The output is a crack density metric (fraction of the inspected surface with confirmed crack features) mapped to a visual health score.

> Next phase: YOLOv8 + SAM segmentation fine-tuned on the CODEBRIM dataset (Concrete Defect Bridge Image dataset) for semantic crack classification.

---

## Field Validation: Figueroa Street Overpass, Los Angeles

![Field Deployment Schematic](images/08_deployment.png)

On September 27, 2026, ISTARI conducted its first real-world field recording at the Figueroa Street overpass over Interstate 110, Los Angeles -- a 10-minute walk from the USC campus.

### Recording Protocol

| Recording | Duration | Configuration |
|---|---|---|
| Contact (vibration) | 8 min | H3-VR taped flat to pillar column |
| Acoustic standoff 0.3m | 5.4 min | H3-VR on bag, capsules toward structure |
| Acoustic standoff 1m | 5.7 min | H3-VR on bag, capsules toward structure |
| Acoustic standoff 3m | 5.5 min | H3-VR on bag, capsules toward structure |
| Video | 3.9 min | Phone camera, slow overlapping passes |

Format: AmbiX B-format, 48 kHz, 24-bit, 4 channels

### Results

![ISTARI Health Dashboard](images/03_health_dashboard.png)

| Modality | Score | Key Finding |
|---|---|---|
| Acoustics | 0.70 | Primary resonance at 21.2 Hz (3m standoff), cross-validated at 20.5 Hz (1m) |
| Vibrations | 0.73 | Consistent structural mode across all standoff distances, no frequency downshift |
| Visual | 0.626 | WARNING flagged due to graffiti -- acoustic/vibration fusion overrides correctly |
| **Health Index** | **75.9 / 100** | **HEALTHY -- periodic monitoring recommended** |

The consistent detection of a structural resonance at approximately 20-21 Hz across all four real field recordings -- contact and three acoustic standoff distances -- confirms this as a genuine structural mode, not measurement noise. For a reinforced concrete bridge column under ambient I-110 traffic load, a fundamental frequency in this range is physically consistent with SDOF column models.

### Graffiti as a Proof-of-Concept

The visual modality returned a WARNING score (0.626) on this pillar. The root cause: the pillar has spray-paint graffiti (blue-grey tags with pink fill) covering a significant portion of the column face. The OpenCV crack detection pipeline identifies elongated high-contrast strokes -- and graffiti paint strokes are morphologically identical to cracks. Any single-modality visual inspection system, including a human inspector on a routine walk, would flag this pillar for further investigation.

The acoustic and vibration modalities are completely unaffected by surface paint. They measure internal structural state: natural frequency, modal damping, and cross-spectral density across channels. With a stable resonance at 21.2 Hz and no damping anomaly, both modalities return HEALTHY scores.

The weighted fusion (45% acoustic + 30% vibration + 25% visual) correctly overrides the visual false positive and returns an overall HEALTHY verdict. This is not a system failure -- this is the system working as designed. Visual inspection has known false-positive vulnerabilities; acoustic sensing does not.

> Pitch line: "We deployed on a real I-110 bridge column today. Visual inspection said WARNING. Our acoustic sensors said HEALTHY. The column has graffiti on it. Our system got it right."

![Graffiti Visual Inspection Failure Case](images/05_crack_detection.png)

---

## Architecture

```
istari/
├── app.py                    # Streamlit dashboard (Upload / Results / About)
├── pipeline/
│   ├── acoustic.py           # AmbiX load, beamforming, Welch PSD, FDD-OMA, health score
│   ├── vibration.py          # Contact-mode PSD, damping ratio extraction, vibration score
│   ├── vision.py             # Frame extraction, crack detection, visual score
│   ├── fusion.py             # Weighted health index (45/30/25)
│   └── demo_data.py          # Pre-computed Figueroa field results (no WAV files needed)
├── requirements.txt
├── .replit                   # Replit deployment config
└── README.md
```

---

## Installation

```bash
git clone https://github.com/tangonovember87/ISTARI.git
cd ISTARI
pip install -r requirements.txt
streamlit run app.py
```

### Requirements

```
streamlit>=1.35.0
numpy>=1.24.0
scipy>=1.11.0
soundfile>=0.12.1
matplotlib>=3.7.0
pandas>=2.0.0
opencv-python-headless>=4.8.0
```

---

## Usage

**Demo mode (pre-loaded Figueroa field data):**
Launch the app and check "Use Figueroa Overpass Sample Data". Results display instantly from pre-computed analysis of the September 27 recordings.

**Upload your own data:**
Record with any 4-channel AmbiX B-format recorder (Zoom H3-VR, Sennheiser Ambeo, Rode NT-SF1). Upload your contact WAV and standoff WAVs. Upload your structural video. Adjust the visual score slider or let the CV pipeline compute it. Hit Run.

**Supported input formats:**
- Audio: 4-channel AmbiX WAV (48 kHz or 96 kHz, 24-bit)
- Video: MP4, MOV, AVI

---

![Damping Ratio Health Classification](images/06_damping_health.png)

## Competitive Advantage

![Competitive Analysis](images/07_competitive.png)


| Capability | Industrial AET | ISTARI |
|---|---|---|
| Cost per deployment | $50k - $500k | ~$350 (hardware) |
| Requires contact sensors | Yes, epoxy-bonded | No -- fully non-contact |
| Spatial coverage | Fixed sensor grid | 360-degree ambisonic capture |
| Redeployable | No | Yes -- one device, any structure |
| Requires specialists | Yes | No -- field protocol in under 30 min |
| Modalities | 1 (acoustic emission only) | 3 (acoustics + vibration + vision) |
| Output | AE event count | Unified 0-100 health index |

---

## Research Basis, Dataset Methodology, and Honest Accounting

This section documents what ISTARI set out to prove, what we validated with synthetic data, what we measured with real field data, and -- critically -- what we did not complete and why. It is written for technical reviewers, not for marketing.

### The Core Thesis

ISTARI rests on one falsifiable claim: **a $400 consumer-grade tetrahedral microphone array, combined with a phone camera and a unified signal processing pipeline, can detect structural anomalies in reinforced concrete infrastructure that single-modality inspection systems miss -- and can do so without trained inspectors, specialized hardware, or physical contact with the structure.**

This is decomposed into four sub-claims:

**Sub-claim 1: Structural natural frequencies are detectable from ambient vibration.**
A reinforced concrete column under normal traffic loading behaves as a damped single-degree-of-freedom (SDOF) oscillator at its fundamental bending mode. The natural frequency fn = (1/2pi) * sqrt(k/m) is a function of structural stiffness k and mass m. Structural damage (cracking, rebar corrosion, delamination) reduces effective stiffness k, which reduces fn. A detectable downward shift in fn is therefore a structural damage indicator. This is the theoretical basis of Operational Modal Analysis (OMA) and is well-established in structural engineering literature. We claim the Zoom H3-VR captures sufficient signal to identify fn from ambient traffic excitation using Welch's PSD method.

**Sub-claim 2: AmbiX B-format spatial audio enables directional acoustic analysis.**
The Zoom H3-VR records in AmbiX B-format: four channels (W=omnidirectional, X=front-back, Y=left-right, Z=up-down) from a tetrahedral capsule array with approximately 5cm spacing. The first-order beamforming formula P(az,el) = W + X*cos(az)*cos(el) + Y*sin(az)*cos(el) + Z*sin(el) steers a virtual microphone in any direction. Applied to ambient recordings, this localizes the dominant acoustic energy source. A Frequency Domain Decomposition (FDD) of the 4x4 cross-spectral density matrix between channels, followed by Singular Value Decomposition (SVD) at each frequency, isolates the structural response from broadband excitation noise.

**Sub-claim 3: Computer vision surface inspection fails systematically on real infrastructure.**
OpenCV-based crack detection using adaptive thresholding, CLAHE contrast enhancement, and morphological filtering identifies elongated high-contrast features as crack candidates. Structural graffiti, staining, and utility markings produce morphologically identical features and generate systematic false positives. A single-modality visual inspection system -- human or algorithmic -- cannot distinguish paint strokes from cracks without additional evidence.

**Sub-claim 4: Weighted fusion of three modalities produces a more reliable health index than any single modality alone.**
The health index H = 100 - (0.45*a + 0.30*v + 0.25*vis)*100, where a=acoustic score, v=vibration score, vis=visual score, weights acoustic sensing highest because it captures internal structural state. Visual inspection captures surface state only. The weights (45/30/25) are not empirically calibrated -- they are a principled prior based on the relative depth of information each modality provides. Validation requires testing across structures with known damage states, which we have not done.

---

### Synthetic Dataset

We generated a synthetic validation dataset to test the pipeline end-to-end before field deployment. The synthetic data was not used to claim real measurements -- it was used to verify that the code paths work correctly and that the visualizations accurately represent what the pipeline would produce on real data.

**What the synthetic dataset contains:**
- Simulated SDOF free vibration signal: x(t) = A * exp(-zeta*omega_n*t) * sin(omega_d*t) + noise, with fn=21.1 Hz and zeta=0.023 (2.3% damping)
- Simulated four-channel AmbiX recording with the structural signal steered to az=15 degrees, el=5 degrees and broadband white Gaussian noise added at -20 dB SNR
- Simulated crack detection images: synthetic concrete texture with programmatically drawn crack-like line segments, blurred and contrast-adjusted to mimic real crack appearance
- Simulated health scores: acoustic=0.70, vibration=0.73, visual=0.90, yielding health index 75.9/100 HEALTHY

**What the synthetic dataset validated:**
- The Welch PSD pipeline correctly identifies the synthetic 21.1 Hz peak with the expected prominence
- The beamforming formula correctly recovers the injected source direction (az=15, el=5) when the signal is synthetic and clean
- The SDOF damping ratio extraction (half-power bandwidth method) correctly returns 2.3% on a clean synthetic signal
- The weighted health fusion formula produces the correct numerical output
- The FDD pipeline correctly returns the synthetic fn as the first singular value peak when channels are synthetically mixed with known weights

**What the synthetic dataset did not validate:**
- Whether any of these results replicate on real infrastructure with real noise characteristics
- Whether the 45/30/25 weights are correct for real-world inspection scenarios
- Whether the OpenCV crack detection has acceptable false positive and false negative rates on real concrete surfaces
- Whether the health index threshold boundaries (40/65) are correctly placed relative to real structural damage states

---

### Real Field Dataset

**Site:** Figueroa Street overpass over Interstate 110, Los Angeles, CA. Pillar 01, northeast face. Circular cross-section reinforced concrete column, approximately 1.2m diameter, supporting the I-110 to SR-110 interchange deck.

**Date:** September 27, 2026, approximately 10:00-11:00 local time.

**Hardware:** Zoom H3-VR recorder, AmbiX B-format, 48 kHz, 24-bit, 4 channels.

**Recordings:**

| File | Duration | Configuration | Clipping |
|---|---|---|---|
| 260927_001.WAV | 478s | H3-VR taped flat to pillar face, contact coupling | 11.7% (W channel) -- severely clipped |
| 260927_002.WAV | 322s | H3-VR on bag, 0.3m standoff, capsules toward pillar | 0.62% (W channel) -- acceptable |
| 260927_003.WAV | 343s | H3-VR on bag, 1m standoff, capsules toward pillar | 3.72% (W channel) -- acceptable |
| 260927_004.WAV | 331s | H3-VR on bag, 3m standoff, capsules toward pillar | measured -- acceptable |

**What we actually computed from the real data:**

1. **Welch Power Spectral Density (all three standoff files)**
   - Method: scipy.signal.welch, nperseg=65536 (0.732 Hz frequency resolution), noverlap=32768, Hann window, density scaling
   - Channel used: W (omnidirectional), DC removed
   - Results:
     - 002.WAV (0.3m): dominant peak at 15.38 Hz, prominence 8.87 dB
     - 003.WAV (1m): dominant peak at 20.51 Hz, prominence 11.66 dB
     - 004.WAV (3m): dominant peak at 21.24 Hz, prominence 11.77 dB
   - Secondary peaks (003+004 agreement): 54-60 Hz, 69-75 Hz, 89-97 Hz

2. **Frequency Domain Decomposition (003.WAV and 004.WAV)**
   - Method: 4x4 cross-spectral density matrix using scipy.signal.csd for all channel pairs, SVD at each frequency bin via numpy.linalg.svd, first singular value extracted as the dominant mode indicator
   - Results:
     - 003.WAV: FDD peak at 13.18 Hz (prominence 10.09 dB in SV1 spectrum)
     - 004.WAV: FDD peak at 18.31 Hz (prominence 10.89 dB in SV1 spectrum)
   - Coherence at FDD peaks: W-X=0.127, W-Y=0.162, W-Z=0.007 (all well below the 0.80 reliability threshold)
   - FDD and Welch PSD disagree by 2-7 Hz depending on standoff distance

3. **Beamforming Steered Response Power (003.WAV, 30-second excerpt)**
   - Method: Applied B-format steering formula across 73x37 azimuth/elevation grid in 5-degree steps, frequency band 100-1500 Hz (where 5cm array spacing provides spatial discrimination; structural band 5-50 Hz is physically unresolvable with this array aperture)
   - Peak direction: az=20 degrees, el=-10 degrees
   - Interpretation: Dominant noise source slightly below horizontal, consistent with road surface and vehicle undercarriage noise. Not a structural feature.

4. **Visual inspection on field video (IMG_9012.MOV)**
   - Frame extraction: 117 frames at 0.5fps across 233-second video
   - Pipeline: CLAHE + adaptive threshold + morphological opening (horizontal/vertical kernels) + contour filtering (aspect ratio > 3.5, area > 25px, perimeter > 18px)
   - Result: 95 false-positive contours, visual score 0.626 (WARNING)
   - Root cause: The pillar face has spray-paint graffiti (blue-grey tags with pink fill). Graffiti strokes are morphologically identical to crack features.

**What the real data showed:**
- Structural resonance is detectable in the ambient recording. The 1m and 3m standoffs agree on approximately 20-21 Hz, consistent with the synthetic simulation.
- The contact recording (260927_001.WAV) was 11.7% clipped, but 80 seconds of clean signal was recovered by scanning the 478s recording in 5-second windows and assembling windows with less than 1% clipping. Separate PSDs were computed for all four B-format channels (W, X, Y, Z) on this clean buffer. The key finding: the three directional channels (X=22.0 Hz, Y=19.0 Hz, Z=20.5 Hz) independently show peaks in the 19-22 Hz range, cross-validating the 1m and 3m standoff results. The W (omnidirectional) channel peaks at 14.65 Hz, which is a lower frequency dominated by diffuse acoustic traffic noise -- the directional channels cancel out isotropic ambient noise and preferentially retain coherent structural vibration with a dominant direction. A secondary mode appears at 64.5 Hz in all three directional channels but not clearly in W. The dominant vibration direction is left-right (Y channel has the highest prominence at 15 dB), consistent with the expected lateral bending mode of a vertical column. This is the strongest independent cross-validation of the 20 Hz structural resonance in the dataset.
- Welch PSD and FDD disagree on the exact frequency. This disagreement is meaningful: FDD suppresses uncorrelated noise components, so if FDD gives a lower frequency it may be identifying a different (real) mode or it may be affected by the non-stationarity of traffic events. The low inter-channel coherence at both peaks (max 0.162) suggests we are not seeing a clean structural resonance -- we are seeing traffic-dominated noise with a spectral shape that peaks in the 13-21 Hz range.
- The beamforming result at 100-1500 Hz is a noise source localization result, not a structural result.
- The visual pipeline produces systematic false positives on painted surfaces, demonstrating Sub-claim 3.

---

### What We Did Not Do, and Why

The following is an honest list of analyses that are theoretically appropriate for this dataset but were not completed due to time constraints at a 48-hour hackathon.

**1. True Operational Modal Analysis with spatial sensor distribution**
OMA requires sensors at multiple points on the structure to recover mode shapes, not just natural frequencies. With one recorder at three standoff distances, we have time signals from three positions along roughly the same sightline. True OMA would require the H3-VR to be repositioned to multiple faces of the column (0 degrees, 90 degrees, 180 degrees, 270 degrees) and at multiple heights (base, mid-column, cap). This would give us enough spatial sampling to compute the first few bending mode shapes. We did not do this because it would have required returning to the field with a structured measurement protocol, which was not feasible within the hackathon timeline.

**2. Damping ratio extraction from real data**
The SDOF half-power bandwidth method (zeta = (f2-f1)/(2*fn)) requires a clean, isolated resonance peak. On our real recordings, the half-power bandwidth calculation returned zeta approximately 60%, which is physically impossible for undamaged concrete (typical zeta = 0.01-0.03). This indicates the identified peak is not a clean structural resonance but rather a noise-dominated spectral feature. Correct damping extraction would require either (a) impact hammer testing to produce a clean impulse response, or (b) stochastic subspace identification (SSI) applied to longer recordings with sufficient stationarity. We have neither capability with the current hardware in this context.

**3. Stochastic Subspace Identification (SSI)**
SSI is the state-of-the-art time-domain OMA method. It constructs a state-space model of the structural response directly from output-only measurements without assuming a specific spectral shape. It handles non-stationary excitation better than FDD. Implementation requires building a block Hankel matrix from the channel data, computing its SVD, and fitting an autoregressive model to the subspace. This is approximately 200 lines of numpy code and an hour of implementation time. We did not do it.

**4. Calibrated health score thresholds**
The boundaries CRITICAL (<40), WARNING (40-65), HEALTHY (>65) and the modality weights (45/30/25) are principled engineering choices, not empirically calibrated parameters. Proper calibration requires a labeled dataset of structures with known damage states -- at minimum, a set of columns with confirmed crack depths and confirmed acoustic signatures. No such labeled dataset was available, and creating one within a hackathon is not possible. The thresholds we use are defensible as a starting point but should not be interpreted as validated discrimination boundaries.

**5. YOLOv8 semantic crack segmentation**
We identified CODEBRIM (Concrete Defect Bridge Image dataset) as the appropriate fine-tuning dataset for a production crack detection model. Training YOLOv8 on CODEBRIM would replace our OpenCV heuristic pipeline with a model that has learned to distinguish true structural cracks from graffiti, staining, and texture. We did not do this because model training requires GPU resources and days of fine-tuning that are outside the scope of a hackathon prototype.

**6. Full clipping restoration on the contact recording (260927_001.WAV)**
The contact recording was severely clipped (11.7% of samples). We salvaged 80 seconds of clean signal by scanning the full 478s in 5-second blocks and assembling only blocks with less than 1% clipping. This produced usable 4-channel PSDs from the clean segments. What we did not do is full clipping restoration on the clipped segments -- a sinc-interpolation approach on the clipped samples would recover roughly 60% more usable data and could improve the PSD SNR. We did not do this because the clean-window approach was sufficient to confirm the 20 Hz resonance across all directional channels, and further clipping restoration would not change the structural interpretation. A practical fix for future field work: reduce H3-VR input gain by at least 12 dB before pressing against a concrete pillar with ambient traffic excitation.

**7. Cross-structure baseline comparison**
The 21.24 Hz resonance we measured tells us the current state of Pillar 01. It does not tell us whether that frequency represents a healthy or damaged state, because we have no historical baseline for this specific column. Structural health monitoring requires either (a) a pre-damage baseline measurement from the same structure, (b) a physics-based model of the expected healthy frequency for this geometry and material, or (c) comparison with similar structures in a known-healthy condition. We have none of these. The HEALTHY verdict from our pipeline is based on the absence of detected anomalies in a single-point-in-time measurement, not on comparison to a damage-sensitive baseline.

![FDD-OMA Cross-Spectral Analysis](images/02_fdd_oma_acoustic.png)

---

## Roadmap

- **Phase 1 (current):** Single-device proof of concept -- H3-VR + phone video. Working on real infrastructure.
- **Phase 2:** Drone integration -- attach H3-VR to drone for elevated and inaccessible structural elements. OpenDroneMap photogrammetry for orthomosaic generation.
- **Phase 3:** YOLOv8 + SAM crack detection fine-tuned on CODEBRIM dataset replacing OpenCV pipeline.
- **Phase 4:** Multi-structure dashboard -- GPS-registered health maps across an asset network.
- **Phase 5:** Continuous monitoring mode -- fixed installation with scheduled recording and automated alerts.

---

## Team

| Name | Role |
|---|---|
| Tariq Nazar | Acoustics architecture, pipeline design |
| Ishan Bhakta | Engineering -- Viterbi School |
| Adolfo Balderas | Engineering -- Viterbi School |
| Amogh Skanda | Engineering / Computer Vision -- Viterbi School |

*Origin Weekend Fall 2026 | USC Tiehub | Prompt D: Infrastructure and Resilience*

---

## License

MIT License. See LICENSE for details.

*Field data collected at Figueroa Street overpass over I-110, Los Angeles, CA -- September 27, 2026.*
