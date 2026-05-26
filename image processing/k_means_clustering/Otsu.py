import argparse
import numpy as np
import numpy.typing as npt
import os
from sobel import sobelFilter
from ImageData import imgdata

def OtsuThresholding(Otsu:imgdata|npt.NDArray) ->int:
    if type(Otsu) == imgdata:
        totalPixels = Otsu.height*Otsu.width
        histogram = np.bincount(Otsu.pixels,minlength=256)
    elif isinstance(Otsu,np.ndarray):
        totalPixels = len(Otsu)
        histogram = np.bincount(Otsu,minlength=256)
    else:
        raise ValueError('Not matching the datatype')
    p = histogram.astype(np.float64)/totalPixels
    muTotal = np.sum(np.arange(256)*p)
    w0= 0
    mu0=0
    max_variance = 0
    best_threshold = 0
    
    for T in range(256):
        w0 = w0 + p[T]
        mu0 = mu0 + T * p[T]
        if(w0 == 0):
            continue
        
        w1 = 1 -w0
        if w1 == 0:
            break
        
        mu0Current = mu0/w0
        mu1 = (muTotal-mu0)/w1
        #between-class variance
        
        btClsVar = w0*w1*(mu0Current-mu1)**2
        if btClsVar > max_variance :
            max_variance = btClsVar
            best_threshold = T
    
    return best_threshold

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, required=True)

    args = parser.parse_args()
    Otsu = imgdata(args.ip,['Sobel','Otsu'])
    Otsu.pixels = sobelFilter(Otsu)
    T = OtsuThresholding(Otsu)
    output = np.where(Otsu.pixels < T,0,Otsu.pixels)
    Otsu.writeOP(output)
    print("Execution Complete")
