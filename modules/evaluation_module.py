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
def evaluate_all(original, recovered, encrypted, extracted_watermark, original_watermark):
    """
    Evaluate image and watermark quality using PSNR, SSIM, BER, and NPCR.
    """
    print("\n📈 Evaluation Results:\n" + "-" * 60)

    # PSNR and SSIM between original and recovered
    psnr_val = calculate_psnr(original, recovered)
    ssim_val = calculate_ssim(original, recovered)
    print(f"🖼️ Image Quality:\n  PSNR: {psnr_val:.2f} dB\n  SSIM: {ssim_val:.4f}")

    # NPCR between original and encrypted
    npcr_val = calculate_npcr(original, encrypted)
    print(f"🔐 Encryption Strength:\n  NPCR: {npcr_val*100:.2f}%")

    # BER for watermark (convert images to bits)
    wm_bits_original = (original_watermark > 127).astype(np.uint8).flatten()
    wm_bits_extracted = (extracted_watermark > 127).astype(np.uint8).flatten()

    min_len = min(len(wm_bits_original), len(wm_bits_extracted))
    ber_val = calculate_ber(wm_bits_original[:min_len], wm_bits_extracted[:min_len])
    print(f"💧 Watermark Integrity:\n  BER: {ber_val*100:.2f}%")
