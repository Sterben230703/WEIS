import numpy as np
import cv2
from skimage.metrics import structural_similarity as ssim

def calculate_psnr(original, test):
    """
    Compute Peak Signal-to-Noise Ratio between two images.
    """
    mse = np.mean((original.astype(np.float32) - test.astype(np.float32)) ** 2)
    if mse == 0:
        return float('inf')
    PIXEL_MAX = 255.0
    return 20 * np.log10(PIXEL_MAX / np.sqrt(mse))


def calculate_ssim(original, test):
    """
    Compute Structural Similarity Index between two images.
    """
    score, _ = ssim(original, test, full=True)
    return score


def calculate_ber(original_bits, extracted_bits):
    """
    Compute Bit Error Rate (BER) between watermark bits.
    """
    original_bits = np.array(original_bits)
    extracted_bits = np.array(extracted_bits)

    if len(original_bits) != len(extracted_bits):
        raise ValueError("Length mismatch in BER calculation.")

    errors = np.sum(original_bits != extracted_bits)
    return errors / len(original_bits)


def calculate_npcr(original, test):
    """
    Compute Number of Pixel Change Rate (NPCR).
    """
    assert original.shape == test.shape, "Image dimensions must match."

    diff = original != test
    changed_pixels = np.sum(diff)
    total_pixels = original.size

    return changed_pixels / total_pixels
