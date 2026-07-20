#1. paths -> typehint: str | os.PathLike[str]
#2. to get the image pixels as pixel -> img = Image.open(filename).convert("L")


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

offsets = [[-1,-1],[-1, 0],[-1, 1],
           [ 0,-1],        [ 0, 1],
           [ 1,-1],[ 1, 0],[ 1, 1]]

    
class features:
    def __init__(self,filename:str|os.PathLike[str]):
        if not os.path.isfile(filename):
            raise FileNotFoundError(f"'{filename}' does not exist")
        try:
            img = Image.open(filename).convert("L")
        except Exception as e:
            raise ValueError(f"Could not read Image '{filename}'.") from e
        self.img: npt.NDArray[np.uint8] = np.array(img)
        self.height = img.height
        self.width = img.width
        
    @property
    def features(self):
        glcm_dtype = ([
            ('0_deg',np.float32),
            ('45_deg',np.float32),
            ('90_deg',np.float32),
            ('135_deg',np.float32)
        ])
        pixel_dtype = np.dtype([
            ('GLCM',glcm_dtype),
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
        features = np.zeros(self.img.shape,dtype=pixel_dtype)
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
        GLCM = features['GLCM']
        
                
                
        
        
        
        
        
        
        
        


if __name__ == '__main__':
    img1 = features(r'E:\python\image processing\4_RFCM/Images\1_090.pgm')
    print(img1.img.shape[0])
    print(img1.img[20,100])
    
        