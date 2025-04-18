import numpy as np
import cv2
from modules.evaluation_module import calculate_psnr, calculate_ssim, calculate_ber, calculate_npcr

# Load images (prefer .npy for accuracy)
try:
    original_image = np.load("output/original_image.npy")
except FileNotFoundError:
    print("⚠️ original_image.npy not found. Loading 'images/lena.png' instead.")
    original_image = cv2.imread("images/lena.png", cv2.IMREAD_GRAYSCALE)

recovered_image = np.load("output/recovered_image.npy")
marked_image = np.load("output/marked_share1.npy")
scrambled_image = np.load("output/share1.npy")

# Load watermark bits
original_watermark_bits = np.load("output/original_watermark_bits.npy")
extracted_watermark_bits = np.load("output/extracted_watermark_bits.npy")

# ✅ Ensure equal length before BER calculation
min_len = min(len(original_watermark_bits), len(extracted_watermark_bits))
original_bits_trimmed = original_watermark_bits[:min_len]
extracted_bits_trimmed = extracted_watermark_bits[:min_len]

# Evaluate metrics
psnr_score = calculate_psnr(original_image, recovered_image)
ssim_score = calculate_ssim(original_image, recovered_image)
ber_score = calculate_ber(original_bits_trimmed, extracted_bits_trimmed)
npcr_score = calculate_npcr(scrambled_image, marked_image)

# Display results
print(f"🔍 Evaluation Metrics:")
print(f"📏 PSNR: {psnr_score:.2f} dB")
print(f"🧠 SSIM: {ssim_score:.4f}")
print(f"❌ Bit Error Rate (BER): {ber_score:.4f}")
print(f"📊 NPCR: {npcr_score * 100:.2f}%")
