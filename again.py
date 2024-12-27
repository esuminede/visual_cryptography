import numpy as np
from PIL import Image
import random

def generate_shares(image_path, num_shares):
    image = Image.open(image_path).convert('1')  # Convert image to black and white
    img_array = np.array(image)
    height, width = img_array.shape

    shares = np.zeros((num_shares, height, width), dtype=np.uint8)

    for y in range(height):
        for x in range(width):
            pixel = img_array[y, x]
            if pixel == 0:  # Black pixel
                perm = np.random.permutation(num_shares)
                for i in range(num_shares):
                    shares[perm[i], y, x] = 0 if i < num_shares // 2 else 255
            else:  # White pixel
                for i in range(num_shares):
                    shares[i, y, x] = 255

    return [Image.fromarray(share) for share in shares]

# Example usage
shares = generate_shares('path_to_image.png', 3)
for i, share in enumerate(shares):
    share.save(f'share_{i + 1}.png')
