"""
ISTARI Computer Vision Pipeline
Crack and defect detection from structural video using OpenCV.
Designed for phone/drone footage of bridge columns, beams, and decks.

Next phase: YOLOv8 + SAM fine-tuned on CODEBRIM dataset.
Current implementation: edge-density and morphological crack detection.
INTERNAL -- Not for distribution.
"""

import cv2
import numpy as np
import os


def extract_frames(video_path, n_frames=20, skip_start_s=2, skip_end_s=2):
    """
    Extract evenly-spaced frames from video, skipping first/last N seconds.
    Returns list of BGR frames.
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise IOError(f"Cannot open video: {video_path}")

    fps = cap.get(cv2.CAP_PROP_FPS)
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration_s = total / fps if fps > 0 else 0

    start_frame = int(skip_start_s * fps)
    end_frame = max(start_frame + 1, total - int(skip_end_s * fps))
    usable = end_frame - start_frame

    step = max(1, usable // n_frames)
    frame_indices = list(range(start_frame, end_frame, step))[:n_frames]

    frames = []
    for idx in frame_indices:
        cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
        ret, frame = cap.read()
        if ret:
            frames.append(frame)
    cap.release()
    return frames, fps, duration_s


def detect_cracks_frame(frame):
    """
    Detect crack-like features in a single frame.
    Strategy: cracks are DARK, THIN, ELONGATED features on a lighter concrete background.
    Rejects: aggregate texture (small blobs), paint marks (high saturation), shadows (large uniform dark areas).

    Returns:
        crack_mask: binary mask
        crack_density: fraction of USABLE frame covered by confirmed cracks
        annotated: BGR frame with detections overlaid
    """
    h, w = frame.shape[:2]
    scale = min(1.0, 1280 / max(h, w))
    if scale < 1.0:
        frame = cv2.resize(frame, (int(w * scale), int(h * scale)))
    h, w = frame.shape[:2]

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # --- 1. Exclude non-concrete regions ---
    # Exclude top 15% (often sky/bridge deck overhang/shadow transition)
    # Exclude high-saturation pixels (paint, rust stains)
    roi_mask = np.ones((h, w), dtype=np.uint8) * 255
    roi_mask[:int(h * 0.15), :] = 0  # exclude top 15%
    roi_mask[int(h * 0.92):, :] = 0  # exclude bottom (ground/dirt)
    high_sat = hsv[:, :, 1] > 60      # paint and colored marks
    roi_mask[high_sat] = 0

    # --- 2. Local contrast: cracks are darker than their neighborhood ---
    blur_local = cv2.GaussianBlur(gray, (31, 31), 0)
    local_contrast = blur_local.astype(np.int16) - gray.astype(np.int16)
    # Dark features: local_contrast > threshold
    dark_mask = (local_contrast > 12).astype(np.uint8) * 255
    dark_mask = cv2.bitwise_and(dark_mask, roi_mask)

    # --- 3. Edge detection (thin features only) ---
    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    edges = cv2.Canny(blur, 40, 100)
    edges = cv2.bitwise_and(edges, roi_mask)

    # Combine: must be both dark AND an edge
    candidate = cv2.bitwise_and(dark_mask, edges)

    # Dilate slightly to connect nearby edge pixels
    k_connect = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    candidate = cv2.dilate(candidate, k_connect, iterations=1)

    # --- 4. Contour filtering: elongated (high aspect ratio) + minimum length ---
    crack_mask = np.zeros((h, w), dtype=np.uint8)
    crack_contours = []
    contours, _ = cv2.findContours(candidate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    min_length_px = max(30, w // 25)  # minimum crack length scales with image width

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < 15:
            continue
        rect = cv2.minAreaRect(cnt)
        rw, rh = rect[1]
        if min(rw, rh) < 1e-6:
            continue
        length = max(rw, rh)
        width = min(rw, rh)
        aspect = length / width

        # Crack criteria: elongated (aspect > 5), minimum length, not too wide (not a shadow)
        if aspect > 5 and length > min_length_px and width < 15:
            cv2.drawContours(crack_mask, [cnt], -1, 255, thickness=cv2.FILLED)
            crack_contours.append(cnt)

    # Crack density over usable ROI only
    roi_area = max(1, np.count_nonzero(roi_mask))
    crack_density = np.count_nonzero(crack_mask) / roi_area

    # Annotate
    annotated = frame.copy()
    if crack_contours:
        overlay = annotated.copy()
        cv2.drawContours(overlay, crack_contours, -1, (0, 0, 220), 2)
        cv2.addWeighted(overlay, 0.55, annotated, 0.45, 0, annotated)
    # Draw ROI boundary
    cv2.rectangle(annotated, (0, int(h * 0.15)), (w - 1, int(h * 0.92)),
                  (0, 200, 0), 1)

    return crack_mask, crack_density, annotated


def analyze_video(video_path, n_frames=20, output_dir=None):
    """
    Full CV pipeline for structural video.
    Extracts frames, detects cracks, computes visual health score.

    Returns dict with visual_score and analysis details.
    """
    frames, fps, duration_s = extract_frames(video_path, n_frames=n_frames)

    if not frames:
        return {
            'visual_score': 0.5,
            'interpretation': 'No frames could be extracted from video',
            'n_frames_analyzed': 0,
            'crack_densities': [],
            'mean_crack_density': 0.0,
            'annotated_frames': [],
        }

    densities = []
    annotated_frames = []

    for frame in frames:
        _, density, annotated = detect_cracks_frame(frame)
        densities.append(density)
        annotated_frames.append(annotated)

    mean_density = float(np.mean(densities))
    max_density = float(np.max(densities))
    crack_frame_fraction = sum(1 for d in densities if d > 0.005) / len(densities)

    # Visual health score
    # Dense crack network -> low score; clean surface -> high score
    # Calibrated thresholds for concrete surface video:
    # <0.5% crack density per frame = healthy
    # 0.5-2% = minor surface cracking
    # 2-5% = moderate cracking
    # >5% = severe, needs immediate inspection
    if mean_density < 0.005:
        visual_score = 0.90
        condition = "No significant surface cracking detected"
    elif mean_density < 0.015:
        visual_score = 0.70
        condition = "Minor surface features detected -- possible hairline cracks"
    elif mean_density < 0.035:
        visual_score = 0.50
        condition = "Moderate crack density -- surface cracking present"
    elif mean_density < 0.06:
        visual_score = 0.30
        condition = "Significant cracking -- structural inspection recommended"
    else:
        visual_score = 0.10
        condition = "Severe surface deterioration detected"

    # Save sample annotated frames
    saved_paths = []
    if output_dir and annotated_frames:
        os.makedirs(output_dir, exist_ok=True)
        step = max(1, len(annotated_frames) // 4)
        for i, f in enumerate(annotated_frames[::step][:4]):
            path = os.path.join(output_dir, f'crack_frame_{i:02d}.jpg')
            cv2.imwrite(path, f)
            saved_paths.append(path)

    interp = (f"{condition} | Mean crack density: {mean_density*100:.2f}% "
              f"| {int(crack_frame_fraction*100)}% of frames show features "
              f"| {len(frames)} frames analyzed from {duration_s:.0f}s video")

    return {
        'visual_score': round(visual_score, 3),
        'interpretation': interp,
        'n_frames_analyzed': len(frames),
        'crack_densities': [round(d, 5) for d in densities],
        'mean_crack_density': round(mean_density, 5),
        'max_crack_density': round(max_density, 5),
        'crack_frame_fraction': round(crack_frame_fraction, 3),
        'annotated_frame_paths': saved_paths,
        'annotated_frames': annotated_frames[:4],  # Keep first 4 for display
    }
