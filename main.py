from PIL import Image
import numpy as np
from dither import jarvis_judice_ninke_dither
from shares import generate_shares_with_xor, save_shares, reconstruct_image_for_xor

if __name__ == "__main__":
    input_image = Image.open(r"C:\Users\EmineSudeAslan\Desktop\secret_sharing\images\woman.png").convert("L")
    output_image = jarvis_judice_ninke_dither(input_image)
    output_image.save("output_dithered.jpg")

    output_dir = "shares"
    output_image_array = np.array(output_image)

    shares = generate_shares_with_xor(output_image_array, num_shares=3)
    save_shares(shares, output_dir)

    reconstructed = reconstruct_image_for_xor(shares)
    reconstructed_image = Image.fromarray(reconstructed)
    reconstructed_image.save("reconstructed.png")