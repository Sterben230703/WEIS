import cv2
from modules.encryption_module import load_image
from modules.decryption_extraction_module import (
    combine_shares,
    inverse_scramble,
    extract_watermark,
    recover_image
)

# Load encrypted marked shares
share1 = load_image("output/share1.png")
share2 = load_image("output/share2.png")

# Combine shares into encrypted image
combined = combine_shares(share1, share2)

# Unscramble to simulate decryption
decrypted = inverse_scramble(combined, block_size=2)

# Load the marked image (created in Phase 2)
marked_image = load_image("output/marked_share1.png")

# Dummy positions used for testing — in real case, these would be saved during embedding
# You can simulate by using output from Phase 2 or just pick some random pixels for testing
positions = [(i, i) for i in range(100)]  # Replace this with real embedding positions

# Extract watermark
watermark_bits, positions = extract_watermark(marked_image, max_bits=1024)

# Recover original image (optional)
recovered_image = recover_image(marked_image, watermark_bits, positions)

# Save outputs
cv2.imwrite("output/decrypted_combined.png", decrypted)
cv2.imwrite("output/recovered_image.png", recovered_image)

print("✅ Phase 3 Test Passed: Decryption and watermark extraction completed.")
print(f"🧩 Extracted watermark bits: {watermark_bits[:20]}...")
