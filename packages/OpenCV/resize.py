import cv2 as cv

img = cv.imread('E:/python/image processing/k_means_segementation/girl.pgm',cv.IMREAD_GRAYSCALE)
if img is not None:
    cv.imshow('Girl',cv.resize(img,(img.shape[1]*7,img.shape[0]*7),interpolation=cv.INTER_CUBIC))
    cv.waitKey(0)
else:
    raise ValueError("img not found")
