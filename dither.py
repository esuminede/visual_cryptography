import numpy as np
from PIL import Image


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
    if isinstance(image_file, str):  # Eğer dosya yolu ise
        new_img = Image.open(image_file).convert('L')
    elif isinstance(image_file, Image.Image):  # Eğer zaten bir Image nesnesi ise
        new_img = image_file.convert('L')
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
