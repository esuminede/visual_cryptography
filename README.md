# visual_cryptography

This project uses Python code for visual cryptography. The first step is to get an image and convert it to grayscale with Floyd-Steinberg dithering.
The second step the dithered image split into three shares. Finally, these shares will be getting together and reconstructing the original image.

Input can be RGB or Grayscale. Dithering function works for both. 
In this project there are two different functin for dithering. Jarvis Judice Ninke dithering method give more accurate outputs. So this function choosen
for use in the main function.


