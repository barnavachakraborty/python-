import cv2 as cv
from PIL import Image
import numpy as np

brain = np.array(Image.open('1_095[KSeg(4)].pgm'))
coloured = cv.applyColorMap(brain,cv.COLORMAP_HSV)
cv.imshow('colured',coloured)
cv.waitKey(0)