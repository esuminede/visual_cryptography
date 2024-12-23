import numpy as np
from PIL import Image
import os

def generate_shares_with_xor(image, num_shares=2):
    height, width = image.shape
    shares = [np.zeros((height, width), dtype=np.uint8) for _ in range(num_shares)]

    for y in range(height):
        for x in range(width):
            pixel_value = 1 if image[y, x] > 127 else 0  # Piksel değerini 0 veya 1 yap
            random_bits = np.random.randint(0, 2, num_shares - 1)
            last_bit = pixel_value ^ np.bitwise_xor.reduce(random_bits)
            bits = np.append(random_bits, last_bit)

            for i in range(num_shares):
                shares[i][y, x] = bits[i] * 255  # 0 veya 255 değerini ata

    return shares

def generate_shares_with_random(image, num_shares):
    height, width = image.shape
    shares = [np.random.randint(0, 256, (height, width), dtype=np.uint8) for _ in range(num_shares - 1)]

    final_share = image.copy()
    for share in shares:
        final_share = (final_share - share) % 255
    
    shares.append(final_share)
    return shares

def save_shares(shares, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    for i, share in enumerate(shares):
        img = Image.fromarray(share)
        img.save(os.path.join(output_dir, f"share_{i+1}.png"))

def reconstruct_image_for_xor(shares):
    combined = shares[0].copy()
    for share in shares[1:]:
        combined = np.bitwise_xor(combined, share)  # XOR işlemi yapılır.

    return combined.astype(np.uint8)  # Uygun veri tipine dönüştür.

def reconstruct_image_for_random(shares):
    # İlk paylaşımı temel olarak alın.
    combined = shares[0].copy()
    for share in shares[1:]:
        combined += share  # Toplama işlemi yapılır.

    # Piksel değerlerini 0-255 aralığına normalize et.
    combined = np.clip(combined, 0, 255)
    return combined.astype(np.uint8)  # Uygun veri tipine dönüştür.
