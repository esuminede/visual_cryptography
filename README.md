# visual_cryptography

This project uses Python code for visual cryptography. The first step is to get an image and convert it to grayscale with Floyd-Steinberg dithering.
The second step the dithered image split into three shares. Finally, these shares will be getting together and reconstructing the original image.

Input can be RGB or Grayscale. At dither.py file image turn into grayscale anyway. So dithering function works for both. 
In this project there are two different function for dithering. Jarvis Judice Ninke dithering method created more easily. So this function choosen one 
for use in the main function.

For the modularity, created dither.py and shares.py files.
    * dither.py file just does the dithering part as you can understand looking file' name. 
    
    * generate_shares.py file does the generates shares, saves shares and reconstructs the original image using shares

    * main.py file is just main file. We run all functions in it.

Thats all. Thank you. :)