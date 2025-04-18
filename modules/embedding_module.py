import cv2
import numpy as np
import os
from modules.encryption_module import load_image, save_image

def load_watermark(watermark_path):
    """
    Load a binary watermark image and flatten to 1D bit array.
    """
    watermark = cv2.imread(watermark_path, cv2.IMREAD_GRAYSCALE)
    if watermark is None:
        raise FileNotFoundError(f"Watermark not found at {watermark_path}")
    _, binary_wm = cv2.threshold(watermark, 127, 1, cv2.THRESH_BINARY)
    return binary_wm.flatten()

def block_predictor(block):
    """
    Predict the bottom-right pixel of a 2x2 block using average of other 3.
    """
    a, b, c, _ = block.flatten()
    prediction = (int(a) + int(b) + int(c)) // 3
    return prediction

def calculate_prediction_error(image):
    """
    For each 2x2 block, compute prediction error at (i+1,j+1).
    Returns:
        errors: list of tuples (i, j, error)
    """
    h, w = image.shape
    errors = []
    for i in range(0, h - 1, 2):
        for j in range(0, w - 1, 2):
            block = image[i:i+2, j:j+2]
            if block.shape == (2, 2):
                pred = block_predictor(block)
                actual = int(block[1, 1])
                error = actual - pred
                errors.append((i+1, j+1, error))
    return errors

def embed_watermark_bits(image, watermark_bits):
    """
    Embed watermark bits into image using histogram shifting.
    Returns watermarked image and embedding positions.
    """
    marked = image.copy()
    errors = calculate_prediction_error(image)
    histogram = {}

    for _, _, e in errors:
        histogram[e] = histogram.get(e, 0) + 1

    # Most frequent error (ME)
    if not histogram:
        raise ValueError("No prediction errors calculated.")
    ME = max(histogram, key=histogram.get)

    embedded_positions = []
    bit_idx = 0

    for i, j, e in errors:
        if bit_idx >= len(watermark_bits):
            break

        if e == ME:
            bit = watermark_bits[bit_idx]
            pixel = int(marked[i, j])
            marked[i, j] = np.clip(pixel + bit, 0, 255)
            embedded_positions.append((i, j))
            bit_idx += 1
        elif e > ME:
            # Histogram shifting
            marked[i, j] = np.clip(marked[i, j] + 1, 0, 255)

    return marked, embedded_positions

# 🔵 Example test driver
if __name__ == "__main__":
    # Load encrypted scrambled share
    share1_path = "../output/share1.png"
    watermark_path = "../images/watermark.png"

    encrypted_share = load_image(share1_path)
    watermark_bits = load_watermark(watermark_path)

    marked_share, embedded_pos = embed_watermark_bits(encrypted_share, watermark_bits)

    # Save output
    save_image("../output/marked_share1.png", marked_share)

    print(f"Watermark embedded in {len(embedded_pos)} positions.")
