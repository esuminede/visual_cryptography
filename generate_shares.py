import cv2
import numpy as np
import os
from PIL import Image

# Üç pay için kullanılan şablonlar
def generate_shares_for_three():
    return [[[[1, 1], [0, 0]], [[0, 0], [1, 1]]],  # Şablon 1
            [[[1, 0], [0, 1]], [[0, 1], [1, 0]]],  # Şablon 2
            [[[1, 0], [1, 0]], [[0, 1], [0, 1]]]]  # Şablon 3


def process_image(image):
    shares = generate_shares_for_three()

    # Görüntüyü ikili (binary) forma dönüştürme
    if isinstance(image, str):
        img = cv2.imread(image, cv2.IMREAD_GRAYSCALE)
    elif isinstance(image, Image.Image):
        img = np.array(image.convert('L'))
    else:
        raise ValueError("Input must be a file path or a PIL Image object")

    (thresh, imbw) = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    # Yeni transparanlar oluşturma
    new_rows = 2 * len(imbw)
    new_cols = 2 * len(imbw[0])
    transparency1 = np.zeros((new_rows, new_cols), dtype=np.uint8)
    transparency2 = np.zeros((new_rows, new_cols), dtype=np.uint8)
    transparency3 = np.zeros((new_rows, new_cols), dtype=np.uint8)

    # Piksel bazında şifreleme
    for i in range(len(imbw)):
        for j in range(len(imbw[0])):
            randInt = int.from_bytes(os.urandom(1), byteorder="big") % 3  # Şablon seçimi
            k, l = 2 * i, 2 * j

            if imbw[i, j] == 255:  # Beyaz piksel için (1)
                transparency1[k:k+2, l:l+2] = shares[randInt][0]
                transparency2[k:k+2, l:l+2] = shares[randInt][0]
                transparency3[k:k+2, l:l+2] = shares[randInt][0]

            elif imbw[i, j] == 0:  # Siyah piksel için (0)
                transparency1[k:k+2, l:l+2] = shares[randInt][0]
                transparency2[k:k+2, l:l+2] = shares[randInt][1]
                transparency3[k:k+2, l:l+2] = shares[randInt][(randInt + 1) % 2]

    return imbw, transparency1, transparency2, transparency3

def combine_shares(transparency1, transparency2, transparency3):
    # Üç payın üst üste birleştirilmesi
    combined = cv2.bitwise_and(transparency1, transparency2)
    combined = cv2.bitwise_and(combined, transparency3)
    return combined

def save_and_show_images(imbw, transparency1, transparency2, transparency3, combined):
    # Görüntülerin kaydedilmesi
    cv2.imwrite('transparency1.png', transparency1 * 255)
    cv2.imwrite('transparency2.png', transparency2 * 255)
    cv2.imwrite('transparency3.png', transparency3 * 255)
    cv2.imwrite('combined.png', combined * 255)

    # Görüntülerin gösterimi
    cv2.imshow('Original Binary Image', imbw)
    cv2.imshow('Transparency 1', transparency1 * 255)
    cv2.imshow('Transparency 2', transparency2 * 255)
    cv2.imshow('Transparency 3', transparency3 * 255)
    cv2.imshow('Decrypted Image', combined * 255)
    cv2.waitKey(0)
    cv2.destroyAllWindows()