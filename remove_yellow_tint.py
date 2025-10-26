# standalone "no reference" color fix tuned toward the user's target look
# pipeline: (1) debias LAB b* toward mild warm target, (2) small a* magenta lift,
# (3) split-toned highlights/shadows, (4) soft S-curve, (5) slight chroma bump.
import cv2, numpy as np
from pathlib import Path

def smoothstep(x, e0, e1):
    t = np.clip((x - e0) / max(1e-6, (e1 - e0)), 0, 1)
    return t * t * (3 - 2 * t)

def fix_warm_cast_standalone(
        img_bgr,
        # global neutrality targets (lab space)
        target_b=+6.0,      # keep a touch of warmth after de-yellowing
        target_a=+2.0,      # slight magenta to avoid olive/green cast
        strength_b=0.85,    # how hard to push b* toward target
        strength_a=0.35,    # subtle on a*
        # split-toning (lab b* and a* tweaks by luminance)
        warm_highlights=+2.5,
        cool_shadows=-2.0,
        magenta_highlights=+0.8,
        # tone/contrast
        curve_amount=0.06,  # gentle S
        chroma_gain=1.06,   # mild saturation
):
    lab = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2LAB).astype(np.float32)
    L, A, B = cv2.split(lab)
    a, b = A - 128.0, B - 128.0

    # robust midtone stats for bias estimation
    w_mid = ((L > 50) & (L < 200)).astype(np.float32)
    mid_b = b[w_mid > 0]
    mid_a = a[w_mid > 0]
    if mid_b.size:
        lo, hi = np.percentile(mid_b, [10, 90]); mid_b = mid_b[(mid_b >= lo) & (mid_b <= hi)]
    if mid_a.size:
        lo2, hi2 = np.percentile(mid_a, [10, 90]); mid_a = mid_a[(mid_a >= lo2) & (mid_a <= hi2)]
    mean_b = float(mid_b.mean()) if mid_b.size else 0.0
    mean_a = float(mid_a.mean()) if mid_a.size else 0.0

    # move toward targets (global)
    b -= strength_b * (mean_b - target_b)
    a -= strength_a * (mean_a - target_a)

    # split-toning using smooth masks
    Ln = L / 255.0
    hmask = smoothstep(Ln, 0.58, 0.86)    # highlights
    smask = smoothstep(1.0 - Ln, 0.45, 0.82)  # shadows

    b += hmask * warm_highlights + smask * cool_shadows
    a += hmask * magenta_highlights

    # mild chroma scaling (preserves neutral grays)
    a *= chroma_gain
    b *= chroma_gain

    # soft S-curve on L
    x = np.arange(256, dtype=np.float32)/255.0
    y = x + curve_amount*(x-0.5)*(1.0 - (x-0.5)**2)
    lut = np.clip((y*255.0).round(), 0, 255).astype(np.uint8)
    L2 = cv2.LUT(L.astype(np.uint8), lut).astype(np.float32)

    out_lab = cv2.merge([L2, np.clip(a+128, 0, 255), np.clip(b+128, 0, 255)]).astype(np.uint8)
    return cv2.cvtColor(out_lab, cv2.COLOR_LAB2BGR)

if __name__ == "__main__":
    # Demo run: update path as needed
    before_path = Path("/mnt/data/477f0b9a-73b0-469c-a83f-a98e491d773f.png")
    img = cv2.imread(str(before_path), cv2.IMREAD_COLOR)
    out = fix_warm_cast_standalone(img)

