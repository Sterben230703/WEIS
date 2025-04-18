import numpy as np
import cv2

def combine_shares(share1, share2):
    """
    Combine two encrypted shares to get marked encrypted image.
    """
    return (share1.astype(np.uint16) + share2.astype(np.uint16)) % 256


def inverse_scramble(scrambled_image, block_size, seed=None):
    """
    Reverse block scrambling. Requires known block shuffle order (use same seed).
    """
    if seed is not None:
        np.random.seed(seed)

    image = scrambled_image.copy()
    h, w = image.shape
    num_blocks_h = h // block_size
    num_blocks_w = w // block_size

    indices = [(i, j) for i in range(num_blocks_h) for j in range(num_blocks_w)]
    shuffled = indices.copy()
    np.random.shuffle(shuffled)

    reverse_map = {v: k for k, v in zip(indices, shuffled)}

    unscrambled_image = image.copy()
    for (i, j), (orig_i, orig_j) in reverse_map.items():
        block = image[i*block_size:(i+1)*block_size, j*block_size:(j+1)*block_size]
        unscrambled_image[orig_i*block_size:(orig_i+1)*block_size, orig_j*block_size:(orig_j+1)*block_size] = block

    return unscrambled_image


def extract_watermark(marked_image, max_bits=1024):
    """
    Extract watermark bits from the marked image using inverse PEE.
    Assumes 2x2 block structure.
    """
    h, w = marked_image.shape
    watermark_bits = []
    embedded_positions = []

    for i in range(0, h - 1, 2):
        for j in range(0, w - 1, 2):
            block = marked_image[i:i+2, j:j+2]
            a, b = block[0, 0], block[0, 1]
            c, d = block[1, 0], block[1, 1]

            predicted = int((int(a) + int(b) + int(c)) / 3)
            e = int(d) - predicted

            if e == 0:
                watermark_bits.append(0)
                embedded_positions.append((i+1, j+1))
            elif e == 1:
                watermark_bits.append(1)
                embedded_positions.append((i+1, j+1))

            if len(watermark_bits) >= max_bits:
                return np.array(watermark_bits), embedded_positions

    return np.array(watermark_bits), embedded_positions

def recover_image(marked_image, watermark_bits, embedded_positions):
    """
    Recovers the original image by subtracting watermark bits from the marked image at the embedding positions.
    This reverses the histogram shifting-based embedding.
    """
    recovered = marked_image.copy()
    
    for (bit, (i, j)) in zip(watermark_bits, embedded_positions):
        recovered[i, j] = np.clip(recovered[i, j] - bit, 0, 255)

    return recovered


def reconstruct_image(HSB, LSB, n_bits):
    """
    Reconstruct the original image from HSB and LSB.
    """
    return (HSB | LSB).astype(np.uint8)
