import cv2 as cv
from PIL import Image
import numpy as np

ip_img = str(input("Enter the imege-filepath:  "))
brain = np.array(Image.open(ip_img))
coloured = cv.applyColorMap(brain,cv.COLORMAP_HSV)
cv.imshow('coloured',coloured)
cv.waitKey(0)