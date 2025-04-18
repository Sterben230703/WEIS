# import cv2
# import numpy as np
# from modules.encryption_module import load_image
# from modules.embedding_module import embed_watermark_bits

# # Load one of the scrambled shares from Phase 1
# image = load_image("output/share1.png")

# # Generate dummy binary watermark (e.g. 100 bits)
# np.random.seed(42)
# watermark_bits = np.random.randint(0, 2, 100).tolist()

# # Embed the watermark
# marked_image, positions = embed_watermark_bits(image, watermark_bits)

# # Save output
# cv2.imwrite("output/marked_share1.png", marked_image)

# print(f"✅ Phase 2 Test Passed: Watermark embedded in {len(positions)} positions.")

import cv2
import numpy as np
from modules.encryption_module import load_image, save_image
from modules.embedding_module import load_watermark, embed_watermark_bits

# Load one of the scrambled encrypted shares from Phase 1
image = load_image("output/share1.png")

# Load actual watermark bits from watermark image
watermark_bits = load_watermark("images/watermark.png")

# Embed the watermark into the share
marked_image, positions = embed_watermark_bits(image, watermark_bits)

# Save marked share as image and .npy
save_image("output/marked_share1.png", marked_image)
np.save("output/marked_share1.npy", marked_image)

# Save the original watermark bits for evaluation later
np.save("output/original_watermark_bits.npy", watermark_bits)

# Display summary
print(f"✅ Phase 2 Test Passed: Watermark embedded in {len(positions)} positions.")
print(f"🧩 Embedded positions preview: {positions[:10]}...")
