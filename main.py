from dither import jarvis_judice_ninke_dither, floyd_steinberg_dithering
from generate_shares import *



if __name__ == "__main__":
    input_image = "/home/esa/Desktop/visual_cryptography/images/chessboard.jpeg"
    
    output_image = jarvis_judice_ninke_dither(input_image)
    output_image.save("output_dithered.jpg")

    imbw, transparency1, transparency2, transparency3 = process_image(output_image)
    combined = combine_shares(transparency1, transparency2, transparency3)
    save_and_show_images(imbw, transparency1, transparency2, transparency3, combined)
