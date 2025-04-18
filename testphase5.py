# testphase5.py
import cv2
import numpy as np
from modules.evaluation_module import calculate_psnr, calculate_ssim, calculate_ber, calculate_npcr
from utils import load_watermark_bits  # If you have saved original bits

# Load images
original_image = cv2.imread("images/lena.png", cv2.IMREAD_GRAYSCALE)
recovered_image = cv2.imread("output/recovered_image.png", cv2.IMREAD_GRAYSCALE)
marked_image = cv2.imread("output/marked_encrypted.png", cv2.IMREAD_GRAYSCALE)
scrambled_image = cv2.imread("output/scrambled_image.png", cv2.IMREAD_GRAYSCALE)

# Load watermark bits
original_watermark_bits = np.load("output/original_watermark_bits.npy")
extracted_watermark_bits = np.load("output/extracted_watermark_bits.npy")

# Evaluate metrics
psnr_score = calculate_psnr(original_image, recovered_image)
ssim_score = calculate_ssim(original_image, recovered_image)
ber_score = calculate_ber(original_watermark_bits, extracted_watermark_bits)
npcr_score = calculate_npcr(scrambled_image, marked_image)

# Display results
print(f"🔍 Evaluation Metrics:")
print(f"📏 PSNR: {psnr_score:.2f} dB")
print(f"🧠 SSIM: {ssim_score:.4f}")
print(f"❌ Bit Error Rate (BER): {ber_score:.4f}")
print(f"📊 NPCR: {npcr_score * 100:.2f}%")
