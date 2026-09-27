"""
ISTARI Weighted Fusion Algorithm
Combines acoustic, vibration, and visual scores into a single structural health index.

Weights: Acoustic 45% | Vibration 30% | Visual 25%
health_index = 100 - (0.45 x acoustic_score x 100 + 0.30 x vibration_score x 100 + 0.25 x visual_score x 100)

INTERNAL -- Not for distribution.
"""

# Health tier thresholds
TIER_CRITICAL = 40
TIER_WARNING = 65


def compute_health_index(acoustic_score, vibration_score, visual_score=0.5):
    """
    Compute structural health index from individual modality scores.

    Args:
        acoustic_score: float 0.0-1.0 (1.0 = healthy)
        vibration_score: float 0.0-1.0 (1.0 = healthy)
        visual_score: float 0.0-1.0 (1.0 = healthy), default 0.5 if no CV data

    Returns:
        dict with health_index (0-100), tier, confidence, breakdown
    """
    acoustic_score = float(np.clip(acoustic_score, 0, 1))
    vibration_score = float(np.clip(vibration_score, 0, 1))
    visual_score = float(np.clip(visual_score, 0, 1))

    # Weighted damage contribution (higher score = less damage)
    damage_index = (
        0.45 * (1 - acoustic_score) +
        0.30 * (1 - vibration_score) +
        0.25 * (1 - visual_score)
    )
    health_index = round(100 - (damage_index * 100), 1)
    health_index = max(0.0, min(100.0, health_index))

    # Tier classification
    if health_index < TIER_CRITICAL:
        tier = "CRITICAL"
        tier_color = "#C0392B"
        recommendation = "Immediate structural inspection recommended. Do not delay."
    elif health_index < TIER_WARNING:
        tier = "WARNING"
        tier_color = "#E67E22"
        recommendation = "Schedule inspection within 30 days. Monitor closely."
    else:
        tier = "HEALTHY"
        tier_color = "#27AE60"
        recommendation = "No immediate action required. Continue periodic monitoring."

    # Confidence: lower if visual score is default (no CV data)
    visual_is_default = abs(visual_score - 0.5) < 0.01
    confidence = "Medium" if visual_is_default else "High"
    confidence_note = "Visual modality using default value (no CV input)" if visual_is_default else "All three modalities active"

    return {
        'health_index': health_index,
        'tier': tier,
        'tier_color': tier_color,
        'recommendation': recommendation,
        'confidence': confidence,
        'confidence_note': confidence_note,
        'breakdown': {
            'acoustic': {'score': round(acoustic_score, 3), 'weight': 0.45,
                         'contribution': round(acoustic_score * 0.45 * 100, 1)},
            'vibration': {'score': round(vibration_score, 3), 'weight': 0.30,
                          'contribution': round(vibration_score * 0.30 * 100, 1)},
            'visual': {'score': round(visual_score, 3), 'weight': 0.25,
                       'contribution': round(visual_score * 0.25 * 100, 1)},
        }
    }


import numpy as np
