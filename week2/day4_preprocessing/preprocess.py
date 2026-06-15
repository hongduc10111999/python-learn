from pathlib import Path

import cv2
import numpy as np

OUTPUT_DIR = Path(__file__).parent.parent / "output" / "preprocess"


def to_grayscale(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


def denoise(gray):
    return cv2.fastNlMeansDenoising(gray, h=20)


def threshold(gray):
    return cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 15
    )


def _detect_angle(gray):
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    lines = cv2.HoughLinesP(
        edges, 1, np.pi / 180, threshold=100, minLineLength=gray.shape[1] // 3,
        maxLineGap=20,
    )
    if lines is None:
        return 0.0
    angles = []
    for x1, y1, x2, y2 in lines[:, 0]:
        angle = np.degrees(np.arctan2(y2 - y1, x2 - x1))
        if abs(angle) <= 45:
            angles.append(angle)
    if not angles:
        return 0.0
    return float(np.median(angles))


def deskew(gray):
    angle = _detect_angle(gray)
    if abs(angle) < 0.5:
        return gray
    h, w = gray.shape
    matrix = cv2.getRotationMatrix2D((w // 2, h // 2), angle, 1.0)
    return cv2.warpAffine(
        gray, matrix, (w, h), flags=cv2.INTER_CUBIC,
        borderMode=cv2.BORDER_REPLICATE, borderValue=255,
    )


def full_pipeline(path, save=False):
    img = cv2.imread(str(path))
    gray = to_grayscale(img)
    clean = denoise(gray)
    straight = deskew(clean)
    binary = threshold(straight)

    if save:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        stem = Path(path).stem
        cv2.imwrite(str(OUTPUT_DIR / f"{stem}_1_gray.png"), gray)
        cv2.imwrite(str(OUTPUT_DIR / f"{stem}_2_denoise.png"), clean)
        cv2.imwrite(str(OUTPUT_DIR / f"{stem}_3_deskew.png"), straight)
        cv2.imwrite(str(OUTPUT_DIR / f"{stem}_4_binary.png"), binary)
    return binary


if __name__ == "__main__":
    SAMPLE_DIR = Path(__file__).parent.parent / "data" / "samples"
    sample = SAMPLE_DIR / "skewed_noisy.png"
    full_pipeline(sample, save=True)
    print("Đã xử lý và lưu các bước vào", OUTPUT_DIR)
    for f in sorted(OUTPUT_DIR.glob(f"{sample.stem}_*.png")):
        print(" -", f.name)
