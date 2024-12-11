import numpy as np
from PIL import Image
import os
import cv2

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

#def load_image(image):
 #   if isinstance(image, Image.Image):
  #      img = image.convert("1") 
   # else:
    #    img = Image.open(image).convert("1")

    #return np.array(img)

def generate_shares(image, num_shares):
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
        img = Image.fromarray((share * 255).astype(np.uint8))
        img.save(os.path.join(output_dir, f"share_{i+1}.png"))

def reconstruct_image(shares):
    combined = shares[0].copy()
    for share in shares[1:]:
        combined = (combined + share) % 255
    return combined


if __name__ == "__main__":
    input_image = Image.open(r"C:\Users\EmineSudeAslan\Desktop\secret_sharing\images\flowers.jpeg").convert("L")
    output_image = floyd_steinberg_dithering(input_image)

    output_image.show()
    output_image.save("output_dithered.jpg")

    output_dir = "shares"
    #image = load_image(output_image)
    
    output_image_array = np.array(output_image)
    
    shares = generate_shares(output_image_array, num_shares=3)

    save_shares(shares, output_dir)

    reconstructed = reconstruct_image(shares)
    reconstruct_image = Image.fromarray(reconstructed)
    reconstruct_image.save("reconstructed.png")
    reconstruct_image.show()
