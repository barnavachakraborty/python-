import numpy as np
import numpy.typing as npt
import argparse
import os
from ImageData import imgdata

def sobelFilter(sobel:imgdata) -> npt.NDArray[np.int32]:
    pixels = sobel.pixels.reshape(sobel.height,sobel.width).astype(np.uint8)
    output = np.zeros_like(pixels,dtype=np.uint8)
    sobelX= np.array([
    [-1,0,1],
    [-2,0,2],
    [-1,0,1]
    ])
    sobelY = sobelX.T
    for i in range(1,sobel.height-1):
        for j in range(1,sobel.width-1):
            Gx = np.sum(pixels[i-1:i+2,j-1:j+2]*sobelX)
            Gy = np.sum(pixels[i-1:i+2,j-1:j+2]*sobelY)
            G = np.sqrt(Gx**2+Gy**2)
            output[i,j]=G
    output=np.clip(output,0,255)
    return output.astype(np.int32).flatten()
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip",type = str, required = True)
    args = parser.parse_args()
    ip = args.ip
    sobel = imgdata(ip,['Sobel'])
    sobel.writeOP(sobelFilter(sobel))
    print('Execution Complete')
    