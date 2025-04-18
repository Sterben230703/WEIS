# import cv2
# import numpy as np
# from modules.modified_rrwei_module import robust_extract, recover_original

# # Load marked image generated in Phase 2 or 3
# marked_image = cv2.imread('output/marked_share1.png', cv2.IMREAD_GRAYSCALE)

# if marked_image is None:
#     raise FileNotFoundError("❌ 'marked_share1.png' not found in /output/. Make sure Phase 2 was run.")

# # Extract watermark bits
# watermark_bits, positions = robust_extract(marked_image, max_bits=1024)
# print(f"✅ Extracted {len(watermark_bits)} watermark bits.")

# # Recover original image
# recovered_image = recover_original(marked_image, positions, watermark_bits)
# cv2.imwrite('output/recovered_image.png', recovered_image)
# print("📦 Recovered image saved as 'output/recovered_image.png'.")

# # Optionally visualize watermark bits (preview only)
# print("🧩 Preview of extracted watermark bits:", watermark_bits[:20])

# testphase4.py
import numpy as np
import cv2
from modules.decryption_extraction_module import reconstruct_image
from modules.evaluation_module import calculate_psnr, calculate_ssim, calculate_ber, calculate_npcr
from utils import load_watermark_bits

# Load images
marked_share1 = cv2.imread("output/marked_share1.png", cv2.IMREAD_GRAYSCALE)
marked_share2 = cv2.imread("output/marked_share2.png", cv2.IMREAD_GRAYSCALE)

# Reconstruct the image
recovered_image = reconstruct_image(marked_share1, marked_share2, n_bits=4)

# Save recovered image
save_image("output/recovered_image.png", recovered_image)

# Load watermark bits (original and extracted)
original_watermark_bits = np.load("output/original_watermark_bits.npy")
extracted_watermark_bits = np.load("output/extracted_watermark_bits.npy")

# Evaluate metrics
psnr_score = calculate_psnr(marked_share1, recovered_image)
ssim_score = calculate_ssim(marked_share1, recovered_image)
ber_score = calculate_ber(original_watermark_bits, extracted_watermark_bits)
npcr_score = calculate_npcr(marked_share1, recovered_image)

# Display results
print(f"✅ Extracted {len(extracted_watermark_bits)} watermark bits.")
print(f"📦 Recovered image saved as 'output/recovered_image.png'.")
print(f"🧩 Preview of extracted watermark bits: {extracted_watermark_bits[:20]}...")
print(f"🔍 Evaluation Metrics:")
print(f"📏 PSNR: {psnr_score:.2f} dB")
print(f"🧠 SSIM: {ssim_score:.4f}")
print(f"❌ Bit Error Rate (BER): {ber_score:.4f}")
print(f"📊 NPCR: {npcr_score * 100:.2f}%")
