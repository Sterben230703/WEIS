from modules.encryption_module import load_image, split_HSB_LSB, additive_secret_sharing, block_scramble, save_image
import numpy as np

img_path = "images/lena.png"
cover = load_image(img_path)

# ✅ Save original image as .npy for evaluation in later phases
np.save("output/original_image.npy", cover)

HSB, LSB = split_HSB_LSB(cover, n_bits=4)
share1, share2 = additive_secret_sharing(HSB, LSB)

scrambled1 = block_scramble(share1, block_size=2)
scrambled2 = block_scramble(share2, block_size=2)

save_image("output/share1.png", scrambled1)
save_image("output/share2.png", scrambled2)

# ✅ Save scrambled images as .npy too (for consistent NPCR / PSNR eval)
np.save("output/share1.npy", scrambled1)
np.save("output/share2.npy", scrambled2)

print("✅ Phase 1 Test Passed: Scrambled shares and original image saved to output/")
