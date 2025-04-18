# import numpy as np

# def apply_patchwork_watermark(image, watermark_bits, strength=5, seed=42):
#     """
#     Apply patchwork-based watermark to an image by modifying region pairs.
#     Args:
#         image: HSB plane of image (numpy.ndarray)
#         watermark_bits: list/array of bits to embed
#         strength: intensity to modify between patch pairs
#     Returns:
#         watermarked_image
#     """
#     np.random.seed(seed)
#     watermarked_image = image.copy()
#     h, w = image.shape
#     for idx, bit in enumerate(watermark_bits):
#         # Random A and B patches (1x1 pixels for simplicity; can generalize)
#         ax, ay = np.random.randint(0, h), np.random.randint(0, w)
#         bx, by = np.random.randint(0, h), np.random.randint(0, w)

#         if bit == 1:
#             watermarked_image[ax, ay] = min(255, watermarked_image[ax, ay] + strength)
#             watermarked_image[bx, by] = max(0,   watermarked_image[bx, by] - strength)
#         else:
#             watermarked_image[ax, ay] = max(0,   watermarked_image[ax, ay] - strength)
#             watermarked_image[bx, by] = min(255, watermarked_image[bx, by] + strength)

#     return watermarked_image


# def embed_side_info_with_pee(image, side_bits):
#     """
#     Embed side information using Prediction Error Expansion (PEE) on image.
#     Args:
#         image: LSB plane or full image
#         side_bits: list of bits to embed
#     Returns:
#         marked_image: image with side info embedded
#     """
#     h, w = image.shape
#     marked_image = image.copy()
#     bit_idx = 0

#     for i in range(0, h - 1, 2):
#         for j in range(0, w - 1, 2):
#             if bit_idx >= len(side_bits):
#                 return marked_image

#             block = image[i:i+2, j:j+2]
#             a, b = block[0, 0], block[0, 1]
#             c, d = block[1, 0], block[1, 1]
#             pred = int((a + b + c) / 3)
#             e = int(d) - pred

#             if e == 0 and side_bits[bit_idx] == 0:
#                 bit_idx += 1
#             elif e == 0 and side_bits[bit_idx] == 1:
#                 marked_image[i+1, j+1] = (pred + 1)
#                 bit_idx += 1

#     return marked_image


# def extract_patchwork_watermark(image, num_bits, strength=5, seed=42):
#     """
#     Extract watermark bits from patchwork-embedded image.
#     Args:
#         image: watermarked HSB image
#         num_bits: number of bits to extract
#     Returns:
#         watermark_bits: list of bits
#     """
#     np.random.seed(seed)
#     h, w = image.shape
#     bits = []

#     for _ in range(num_bits):
#         ax, ay = np.random.randint(0, h), np.random.randint(0, w)
#         bx, by = np.random.randint(0, h), np.random.randint(0, w)

#         a = image[ax, ay]
#         b = image[bx, by]

#         bit = 1 if a > b else 0
#         bits.append(bit)

#     return bits


# def extract_side_info_with_pee(image, num_bits=1024):
#     """
#     Extract side information embedded via PEE.
#     Returns:
#         side_bits: list of bits
#     """
#     h, w = image.shape
#     bits = []
#     for i in range(0, h - 1, 2):
#         for j in range(0, w - 1, 2):
#             if len(bits) >= num_bits:
#                 return bits

#             block = image[i:i+2, j:j+2]
#             a, b = block[0, 0], block[0, 1]
#             c, d = block[1, 0], block[1, 1]
#             pred = int((a + b + c) / 3)
#             e = int(d) - pred

#             if e == 0:
#                 bits.append(0)
#             elif e == 1:
#                 bits.append(1)

#     return bits
import numpy as np
import cv2

def adaptive_prediction(block):
    """
    Predict a pixel value in a block using a better adaptive model.
    Currently: average of surrounding 3 pixels (improvable).
    """
    a, b = block[0, 0], block[0, 1]
    c, _ = block[1, 0], block[1, 1]  # d is target
    return int((int(a) + int(b) + int(c)) / 3)


def robust_embed(image, watermark_bits):
    """
    Embed watermark with more redundancy & prediction error shifting.
    Returns watermarked image + map of embedded positions.
    """
    marked = image.copy()
    h, w = image.shape
    embedded = []
    idx = 0

    for i in range(0, h - 1, 2):
        for j in range(0, w - 1, 2):
            if idx >= len(watermark_bits):
                break

            block = marked[i:i+2, j:j+2]
            pred = adaptive_prediction(block)
            pixel = int(block[1, 1])
            e = pixel - pred

            if e in (0, 1):  # can embed
                bit = watermark_bits[idx]
                marked[i+1, j+1] = np.clip(pixel + bit, 0, 255)
                embedded.append((i+1, j+1))
                idx += 1
            elif e > 1:
                marked[i+1, j+1] = np.clip(pixel + 1, 0, 255)  # shift

    return marked, embedded


def robust_extract(image, max_bits=1024):
    """
    Extract watermark using adaptive prediction.
    Returns extracted bits and their positions.
    """
    h, w = image.shape
    bits = []
    positions = []

    for i in range(0, h - 1, 2):
        for j in range(0, w - 1, 2):
            block = image[i:i+2, j:j+2]
            pred = adaptive_prediction(block)
            pixel = int(block[1, 1])
            e = pixel - pred

            if e == 0:
                bits.append(0)
                positions.append((i+1, j+1))
            elif e == 1:
                bits.append(1)
                positions.append((i+1, j+1))

            if len(bits) >= max_bits:
                return np.array(bits), positions

    return np.array(bits), positions


def recover_original(marked_image, embedded_positions, watermark_bits):
    """
    Restore original image by subtracting watermark bits.
    """
    recovered = marked_image.copy()
    for (i, j), bit in zip(embedded_positions, watermark_bits):
        recovered[i, j] = np.clip(recovered[i, j] - bit, 0, 255)
    return recovered
def apply_modified_rrwei(image, watermark_image):
    """
    High-level function to embed watermark using the modified RRWEI-SM method.
    Converts watermark to bit array, embeds it, and returns the marked image and side info.
    """
    # Convert watermark image to bit array (assuming binary watermark)
    watermark_bits = (watermark_image > 127).astype(np.uint8).flatten()

    # Embed watermark
    marked_image, embedded_positions = robust_embed(image, watermark_bits)

    # Store side info (positions & bits) if needed for full reversibility
    side_info = {
        "positions": embedded_positions,
        "watermark_bits": watermark_bits
    }

    return marked_image, side_info
