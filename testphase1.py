# test_phase1.py

from modules.encryption_module import load_image, split_HSB_LSB, additive_secret_sharing, block_scramble, save_image

img_path = "images/lena.png"
cover = load_image(img_path)

HSB, LSB = split_HSB_LSB(cover, n_bits=4)
share1, share2 = additive_secret_sharing(HSB, LSB)

scrambled1 = block_scramble(share1, block_size=2)
scrambled2 = block_scramble(share2, block_size=2)

save_image("output/share1.png", scrambled1)
save_image("output/share2.png", scrambled2)

print("✅ Phase 1 Test Passed: Scrambled shares saved to output/")
