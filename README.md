# visual_cryptography

This project uses Python code for visual cryptography. The first step is to get an image and convert it to grayscale with Floyd-Steinberg dithering.
The second step the dithered image split into three shares. Finally, these shares will be getting together and reconstructing the original image.

Input can be RGB or Grayscale. Dithering function works for both. 
In this project there are two different functin for dithering. Jarvis Judice Ninke dithering method give more accurate outputs. So this function choosen
for use in the main function.

visual_cryptography.py file is the all files in on file. The project coded one file at first. But,

For the modularity, created dither.py and shares.py files.
    * dither.py file just does the dithering part as you can understand looking file' name. 
    
    * shares.py file does the generating shares, saving shares to the shares directory and reconstructing the dithered image.

    * main.py file is just main file. We run all functions in it.

Thats all. Thank you.