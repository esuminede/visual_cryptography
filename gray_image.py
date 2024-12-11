# This page for learning how Floyd Steinberg dithering works. It is written in main file (visual-cryptography.py)
import numpy as np
from PIL import Image

def floyd_steinberg_dithering(image):
    img = np.array(image, dtype=np.float32)
    height, width = map(int, img.shape)

    error_matrix = [
        (1, 0, 7 / 16),
        (-1, 1, 3 / 16),
        (0, 1, 5 / 16), 
        (1, 1, 1 / 16)
    ]

    for y in range(int(height)):
        for x in range(int(width)):
            old_pixel = img[y,x]
            new_pixel = 255.0 if old_pixel > 127.0 else 0
            img[y, x] = new_pixel
            quant_error = old_pixel - new_pixel

            for dx, dy, width in error_matrix:
                nx, ny = x + dx, y + dy
                if 0 <= nx < width and 0 <= ny < height:
                    img[ny, nx] += quant_error * width

    return Image.fromarray(img.clip(0, 255).astype(np.uint8))

if __name__ == "__main__":
    input_image = Image.open(r"C:\Users\EmineSudeAslan\Desktop\secret_sharing\images\flowers.jpeg").convert("L")
    output_image = floyd_steinberg_dithering(input_image)

    output_image.show()
    output_image.save("output_dithered.jpg")
