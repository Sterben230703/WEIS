import cv2
import numpy as np
import os

def load_image(image_path):
    """
    Load a grayscale image from the given path.
    Returns:
        image: numpy.ndarray (dtype: uint8)
    """
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise FileNotFoundError(f"Image not found at {image_path}")
    return image


def split_HSB_LSB(image, n_bits):
    """
    Split image pixels into HSB (Higher Significant Bits) and LSB (Lower Significant Bits).
    Args:
        image: numpy.ndarray
        n_bits: Number of LSB bits (1-8)
    Returns:
        HSB: numpy.ndarray
        LSB: numpy.ndarray
    """
    HSB = (image >> n_bits) << n_bits
    LSB = image & ((1 << n_bits) - 1)
    return HSB, LSB


def additive_secret_sharing(HSB, LSB):
    """
    Perform additive secret sharing on both HSB and LSB.
    Args:
        HSB: numpy.ndarray
        LSB: numpy.ndarray
    Returns:
        share1, share2: Two secret shares as numpy.ndarrays
    """
    shape = HSB.shape
    # Random values for HSB and LSB shares
    rand_HSB = np.random.randint(0, 256, shape, dtype=np.uint8)
    rand_LSB = np.random.randint(0, 256, shape, dtype=np.uint8)

    share1 = ((rand_HSB & 0xF0) | (rand_LSB & 0x0F))
    share2 = ((HSB + LSB - share1) % 256).astype(np.uint8)

    return share1, share2


def block_scramble(image, block_size):
    """
    Apply block-level scrambling to the given image.
    Args:
        image: numpy.ndarray
        block_size: size of the block (eg. 2 for 2x2)
    Returns:
        scrambled_image: numpy.ndarray
    """
    scrambled_image = image.copy()
    h, w = image.shape
    num_blocks_h = h // block_size
    num_blocks_w = w // block_size

    indices = [(i, j) for i in range(num_blocks_h) for j in range(num_blocks_w)]
    np.random.shuffle(indices)

    for idx, (i, j) in enumerate(indices):
        target_i, target_j = divmod(idx, num_blocks_w)
        if (target_i, target_j) != (i, j):
            # swap blocks
            block1 = image[i*block_size:(i+1)*block_size, j*block_size:(j+1)*block_size].copy()
            block2 = image[target_i*block_size:(target_i+1)*block_size, target_j*block_size:(target_j+1)*block_size].copy()

            scrambled_image[i*block_size:(i+1)*block_size, j*block_size:(j+1)*block_size] = block2
            scrambled_image[target_i*block_size:(target_i+1)*block_size, target_j*block_size:(target_j+1)*block_size] = block1

    return scrambled_image


def save_image(output_path, image):
    """
    Save an image to disk.
    Args:
        output_path: str
        image: numpy.ndarray
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    cv2.imwrite(output_path, image)


# 🔵 Example test driver
if __name__ == "__main__":
    image_path = "../images/lena.png"
    cover_image = load_image(image_path)

    n_bits = 4       # number of LSB bits
    block_size = 2   # scrambling block size

    HSB, LSB = split_HSB_LSB(cover_image, n_bits)
    share1, share2 = additive_secret_sharing(HSB, LSB)

    scrambled_share1 = block_scramble(share1, block_size)
    scrambled_share2 = block_scramble(share2, block_size)

    save_image("../output/share1.png", scrambled_share1)
    save_image("../output/share2.png", scrambled_share2)

    print("Phase 1 complete. Encrypted and scrambled shares saved.")
