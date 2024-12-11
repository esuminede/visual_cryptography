#this file is just training. It probably will not use in main file.

import cv2
import numpy as np

def combine_images(image_path):
    # Resimleri yükle
    images = [cv2.imread(path, cv2.IMREAD_GRAYSCALE) for path in image_paths]
    
    # Resimlerin aynı boyutta olduğundan emin olun
    for i in range(1, len(images)):
        if images[i].shape != images[0].shape:
            raise ValueError("Tüm resimler aynı boyutta olmalı!")

    # İlk resmi başlangıç olarak alın
    combined_image = images[0]
    
    # Her bir resmi üst üste bindir
    for img in images[1:]:
        # Piksel bazında bitwise AND veya OR işlemi
        combined_image = cv2.bitwise_and(combined_image, img)
    
    return combined_image

# Resim dosyalarının yolları
image_paths = [r'C:\Users\EmineSudeAslan\Desktop\secret_sharing\share_1.png', r'C:\Users\EmineSudeAslan\Desktop\secret_sharing\share_2.png', r'C:\Users\EmineSudeAslan\Desktop\secret_sharing\share_3.png']

# Resimleri birleştir
result = combine_images(image_paths)

# Sonucu göster ve kaydet
cv2.imshow("Combined Image", result)
cv2.imwrite("combined_result.png", result)
cv2.waitKey(0)
cv2.destroyAllWindows()
