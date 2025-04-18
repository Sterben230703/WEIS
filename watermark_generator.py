# watermark_generator.py

import cv2
import numpy as np
import os

def generate_watermark(output_path="images/watermark.png", text="WMARK", size=(64, 64), font_scale=0.6):
    """
    Generates a binary watermark image with custom text.
    
    Args:
        output_path (str): Path to save the generated watermark.
        text (str): Text to embed in the watermark.
        size (tuple): Size of the watermark image (width, height).
        font_scale (float): Size of the text.
    """
    width, height = size
    watermark = np.ones((height, width), dtype=np.uint8) * 255  # White background

    font = cv2.FONT_HERSHEY_SIMPLEX
    thickness = 1

    text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
    text_x = (width - text_size[0]) // 2
    text_y = (height + text_size[1]) // 2

    cv2.putText(watermark, text, (text_x, text_y), font, font_scale, (0,), thickness, cv2.LINE_AA)

    # Convert to binary (black and white only)
    _, binary_watermark = cv2.threshold(watermark, 128, 255, cv2.THRESH_BINARY)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    cv2.imwrite(output_path, binary_watermark)
    print(f"✅ Generated watermark at: {output_path}")

if __name__ == "__main__":
    generate_watermark()
