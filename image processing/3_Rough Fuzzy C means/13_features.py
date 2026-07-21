#1. paths -> typehint: str | os.PathLike[str]
#2. to get the image pixels as pixel -> img = Image.open(filename).convert("L")

from numba import njit
from PIL import Image
import logging
import numpy as np
import os 
import random
import re
import inspect
import sys
import argparse
import numpy.typing as npt


@njit(cache=True, fastmath=True)
def cal_glcm(img:npt.NDArray)-> npt.NDArray:
    pixel_dtype = np.dtype([
            ('homogeneity',np.float32),
            ('edge',np.float32),
            ('asm',np.float32),
            ('contrast',np.float32),
            ('correlation',np.float32),
            ('idm',np.float32),
            ('sum_avg',np.float32),
            ('sum_var',np.float32),
            ('sum_entropy',np.float32),
            ('entropy',np.float32),
            ('diff_var',np.float32),
            ('diff_entropy',np.float32),
        ])
    features = np.zeros(img.shape,dtype=pixel_dtype)
    homogeneity = features['homogeneity']
    edge = features['edge']
    asm = features['asm']
    contrast = features['contrast']
    correlation = features['correlation']
    idm = features['idm']
    sum_avg = features['sum_avg']
    sum_var = features['sum_var']
    sum_entropy = features['sum_entropy']
    entropy = features['entropy']
    diff_var = features['diff_var']
    diff_entropy = features['diff_entropy']
    GLCM = np.empty((4,16,16),dtype=np.float32)
    for i in range(1,img.shape[0]-1):
        for j in range(1,img.shape[1]-1):
            GLCM.fill(0)
            # a b c
            # d e f
            # g h i
            a = img[i-1, j-1] >> 4
            b = img[i-1, j  ] >> 4
            c = img[i-1, j+1] >> 4

            d = img[i  , j-1] >> 4
            e = img[i  , j  ] >> 4
            f = img[i  , j+1] >> 4

            g = img[i+1, j-1] >> 4
            h = img[i+1, j  ] >> 4
            i_ = img[i+1, j+1] >> 4

            # 0° (6 pairs)
            GLCM[0, a, b] += 1
            GLCM[0, b, c] += 1
            GLCM[0, d, e] += 1
            GLCM[0, e, f] += 1
            GLCM[0, g, h] += 1
            GLCM[0, h, i_] += 1

            # 45° (4 pairs)
            GLCM[1, d, b] += 1
            GLCM[1, g, e] += 1
            GLCM[1, e, c] += 1
            GLCM[1, h, f] += 1

            # 90° (6 pairs)
            GLCM[2, d, a] += 1
            GLCM[2, g, d] += 1
            GLCM[2, e, b] += 1
            GLCM[2, h, e] += 1
            GLCM[2, f, c] += 1
            GLCM[2, i_, f] += 1

            # 135° (4 pairs)
            GLCM[3, e, a] += 1
            GLCM[3, h, d] += 1
            GLCM[3, f, b] += 1
            GLCM[3, i_, e] += 1

            # ------------ Normalize ------------

            GLCM[0] *= (1.0 / 6.0)   # 0°
            GLCM[1] *= (1.0 / 4.0)   # 45°
            GLCM[2] *= (1.0 / 6.0)   # 90°
            GLCM[3] *= (1.0 / 4.0)   # 135°
            
                    
    return features
            

    
class features:
    def __init__(self,filename:str|os.PathLike[str]):
        if not os.path.isfile(filename):
            raise FileNotFoundError(f"'{filename}' does not exist")
        try:
            _img = Image.open(filename).convert("L")
        except Exception as e:
            raise ValueError(f"Could not read Image '{filename}'.") from e
        self.img: npt.NDArray[np.uint8] = np.array(_img)
        self.height = _img.height
        self.width = _img.width
    
                
        
    
    @property
    def features(self):
        pass
    
    
        
        
        

if __name__ == '__main__':
    img1 = features(r'E:\python\image processing\4_RFCM/Images\1_090.pgm')
    print(img1.img.shape[0])
    print(img1.img[20,100])
    
    
        