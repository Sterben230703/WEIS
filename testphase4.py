import cv2
import numpy as np
from modules.modified_rrwei_module import robust_extract, recover_original
from modules.encryption_module import save_image

# Load marked image
marked_image = np.load('output/marked_share1.npy')

# Extract watermark bits
watermark_bits, positions = robust_extract(marked_image, max_bits=1024)
print(f"✅ Extracted {len(watermark_bits)} watermark bits.")

# ✅ Save extracted bits
np.save("output/extracted_watermark_bits.npy", watermark_bits)

# Recover original image
recovered_image = recover_original(marked_image, positions, watermark_bits)

# Save recovered image as .png and .npy
save_image('output/recovered_image.png', recovered_image)
np.save('output/recovered_image.npy', recovered_image)
print("📦 Recovered image saved as 'output/recovered_image.png'.")

# Preview
print("🧩 Preview of extracted watermark bits:", watermark_bits[:20])
