import numpy as np
from PIL import Image

def floyd_steinberg_dithering(input_path):
    # Resmi yükleyip grayscale'e dönüştürme
    img = Image.open(input_path).convert('L')

    # Görüntüyü numpy dizisine dönüştürme
    img_array = np.array(img, dtype=np.float32) / 255.0  # 0-1 aralığına normalleştirme

    # Resmin boyutlarını alalım
    height, width = img_array.shape

    # Floyd-Steinberg Dithering uygulaması
    for y in range(height):
        for x in range(width):
            old_pixel = img_array[y, x]
            new_pixel = np.round(old_pixel)
            img_array[y, x] = new_pixel
            quant_error = old_pixel - new_pixel

            if x < width - 1:
                img_array[y, x + 1] += quant_error * 7 / 16
            if y < height - 1 and x > 0:
                img_array[y + 1, x - 1] += quant_error * 3 / 16
            if y < height - 1:
                img_array[y + 1, x] += quant_error * 5 / 16
            if y < height - 1 and x < width - 1:
                img_array[y + 1, x + 1] += quant_error * 1 / 16

            # Piksel değerlerini 0 ile 1 arasında tutalım
            img_array = np.clip(img_array, 0.0, 1.0)

    # Dithered görüntüyü oluşturma
    dithered_img = (img_array * 255).astype(np.uint8)

    # Sonucu kaydetme
    dithered_image = Image.fromarray(dithered_img)
    #dithered_image.save("dithered_image.png")
    return dithered_image


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
