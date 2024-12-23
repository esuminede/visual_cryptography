import numpy as np
from PIL import Image
import os
import cv2
from math import floor


def floyd_steinberg_dithering(image):
    img = np.array(image, dtype=np.uint8)
    height, width = img.shape
    
    error_matrix = [
        (1, 0, 7 / 16),
        (-1, 1, 3 / 16),
        (0, 1, 5 / 16), 
        (1, 1, 1 / 16)
    ]
    for y in range(height):
            for x in range(width):
                old_pixel = img[y, x]
                new_pixel = 0 if old_pixel < 128 else 255  # Threshold: 128
                img[y, x] = new_pixel

                quant_error = old_pixel - new_pixel  # Kuantizasyon hatası

                # Komşu piksellere hatayı yay
                for dx, dy, factor in error_matrix:
                    nx, ny = x + dx, y + dy  # Komşu piksel koordinatları
                    if 0 <= nx < width and 0 <= ny < height:  # Sınır kontrolü
                        img[ny, nx] += quant_error * factor

        # Piksel değerlerini 0-255 aralığına çek
    return Image.fromarray(img.clip(0, 255).astype(np.uint8))


def jarvis_judice_ninke_dither(image_file):
        # Görüntüyü yükle ve gri tonlamaya dönüştür
    if isinstance(input_image, str):  # Eğer dosya yolu ise
        new_img = Image.open(input_image).convert('L')
    elif isinstance(input_image, Image.Image):  # Eğer zaten bir Image nesnesi ise
        new_img = input_image.convert('L')
    else:
        raise ValueError("input_image must be a file path or an Image object")   
    
    pixel = np.array(new_img, dtype=np.int32)

    height, width = pixel.shape
    
    # Adaptif threshold: Görüntünün ortalama değeri
    threshold = np.mean(pixel)

    # Jarvis-Judice-Ninke hata yayma matrisi
    diffusion_matrix = [
        (1, 0, 7 / 48), (2, 0, 5 / 48),
        (-2, 1, 3 / 48), (-1, 1, 5 / 48), (0, 1, 7 / 48), (1, 1, 5 / 48), (2, 1, 3 / 48),
        (-2, 2, 1 / 48), (-1, 2, 3 / 48), (0, 2, 5 / 48), (1, 2, 3 / 48), (2, 2, 1 / 48)
    ]

    # Her piksel üzerinde dolaşarak dithering uygula
    for y in range(height):
        for x in range(width):
            old_pixel = pixel[y, x]
            new_pixel = 0 if old_pixel < threshold else 255
            pixel[y, x] = new_pixel
            quant_error = old_pixel - new_pixel
            
            # Hata yayma matrisi
            for dx, dy, weight in diffusion_matrix:
                nx, ny = x + dx, y + dy
                if 0 <= nx < width and 0 <= ny < height:
                    pixel[ny, nx] += int(quant_error * weight)
    
    # Değerleri sınırlandır ve uint8 tipine çevir
    pixel = np.clip(pixel, 0, 255).astype(np.uint8)
    
    return Image.fromarray(pixel)

def generate_shares_with_random(image, num_shares):
    height, width = image.shape
    shares = [np.random.randint(0, 256, (height, width), dtype=np.uint8) for _ in range(num_shares - 1)]

    final_share = image.copy()
    for share in shares:
        final_share = (final_share - share) % 255
    
    shares.append(final_share)
    return shares

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

def save_shares(shares, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    for i, share in enumerate(shares):
        img = Image.fromarray((share * 255).astype(np.uint8))
        img.save(os.path.join(output_dir, f"share_{i+1}.png"))

def reconstruct_image_for_random(shares):
    # İlk paylaşımı temel olarak alın.
    combined = shares[0].copy()
    for share in shares[1:]:
        combined += share  # Toplama işlemi yapılır.

    # Piksel değerlerini 0-255 aralığına normalize et.
    combined = np.clip(combined, 0, 255)
    return combined.astype(np.uint8)  # Uygun veri tipine dönüştür.

def reconstruct_image_for_xor(shares):
    # İlk paylaşımı temel olarak alın.
    combined = shares[0].copy()
    for share in shares[1:]:
        combined = np.bitwise_xor(combined, share)  # XOR işlemi yapılır.

    return combined.astype(np.uint8)  # Uygun veri tipine dönüştür.

if __name__ == "__main__":
    input_image = Image.open(r"C:\Users\EmineSudeAslan\Desktop\secret_sharing\images\woman.png").convert("L")
    output_image = jarvis_judice_ninke_dither(input_image)

    output_image.save("output_dithered.jpg")

    output_dir = "shares"
    #image = load_image(output_image)
    
    output_image_array = np.array(output_image)
    
    shares = generate_shares_with_xor(output_image_array, num_shares=3)

    save_shares(shares, output_dir)

    reconstructed = reconstruct_image_for_xor(shares)
    reconstruct_image = Image.fromarray(reconstructed)
    reconstruct_image.save("reconstructed.png")
