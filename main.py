from PIL import Image
import numpy as np
from dither import jarvis_judice_ninke_dither
from generate_shares import *



if __name__ == "__main__":
    input_image_path = "/home/esa/Desktop/visual_cryptography/images/chessboard.jpeg"
    input_image = Image.open(input_image_path).convert("L")
    image = cv2.imread(input_image_path, cv2.IMREAD_GRAYSCALE)  # Read image in grayscale
    _, img_array = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY)  # Convert to binary image
    height, width = img_array.shape
    output_image = jarvis_judice_ninke_dither(input_image)
    output_image.save("output_dithered.jpg")

    # output_dir = "shares"
    # output_image_array = np.array(output_image)

    # shares = generate_shares_for_three(output_image_array)
    # save_shares(shares, output_dir)

    # reconstructed = reconstruct_image_for_xor(shares)
    # reconstructed_image = Image.fromarray(reconstructed)
    # reconstructed_image.save("reconstructed.png")

    # image_path = r"C:\Users\EmineSudeAslan\Desktop\secret_sharing\images\lena-bw.jpeg"
    imbw, transparency1, transparency2, transparency3 = process_image(output_image)
    combined = combine_shares(transparency1, transparency2, transparency3)
    save_and_show_images(imbw, transparency1, transparency2, transparency3, combined)