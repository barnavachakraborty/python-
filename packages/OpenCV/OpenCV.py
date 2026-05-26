import cv2 as cv
import numpy as np
import sys
"""blank = np.zeros((500,500,3),dtype = 'uint8')
cv.imshow('blank',blank)

blank[0:50,0:10] = 255,255,0
blank[40:150,0:255] = 255,255,255
cv.imshow('blank-paint',blank)


cv.rectangle(blank,(250,250),(300,400),color=(35,46,100),thickness=cv.FILLED)
cv.imshow('rectangle',blank)
cv.waitKey(0)"""

'''blank = np.zeros((500,500,3),dtype = 'uint8')
cv.imshow('blank',blank)

cv.rectangle(blank,(0,0),(blank.shape[1]//2,blank.shape[0]//2),(0,200,255),thickness=-1)
cv.imshow('blank-rectangle',blank)

cv.circle(blank,(blank.shape[1]//2,blank.shape[0]//2),40,(255,0,0),thickness=-1)
cv.imshow('blank-rectangle+circle',blank)

cv.line(blank,(0,0),(blank.shape[1]//2,blank.shape[0]//2),(0,45,255),thickness=4)
cv.imshow('blank-rectangle+cicle+line',blank)'''

'''img = cv.imread("E:/python/image processing/k_means_segementation/girl.pgm",cv.IMREAD_GRAYSCALE)
if img is not None:
    blur = cv.GaussianBlur(img,(5,5),cv.BORDER_DEFAULT)
    sobel = cv.Sobel(blur,cv.CV_64F,1,0,ksize=7,scale=1,delta = 45,borderType=cv.BORDER_DEFAULT)
    cv.imshow("original",img)
    cv.imshow("original-edged",sobel)
    cv.waitKey(0)
    cv.destroyAllWindows()
else:
    raise ValueError("Image not found")'''
    
'''img = cv.imread("photos/cat.jpg")
def rotate(img,angle,rotPoint = None):
    (height,width) = img.shape[:2]
    if rotPoint == None:
        rotPoint = (width//2,height//2)
        rotMat = cv.getRotationMatrix2D(rotPoint,angle,1.0)
        print(rotMat)
        dimensions = (width,height)
        return cv.warpAffine(img,rotMat,dimensions)
rotated = rotate(img,60)
if rotated is not None:
    cv.imshow("rotated",rotated)
'''

'''img = cv.imread("photos/cats.jpg")
if img is None:
    print("Error: Image not loaded")
    sys.exit(1)
cv.imshow("cats",img)

gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
cv.imshow("cats-gray",gray)

blur = cv.GaussianBlur(gray,(5,5),cv.BORDER_DEFAULT)
cv.imshow("cats-blurred(5,5)",blur)

canny = cv.Canny(blur,125,175)
cv.imshow("cats-blurred(5,5)-canny",canny)

# ret,thresh = cv.threshold(gray,125,175,cv.THRESH_BINARY)
# cv.imshow("cats-gray-thresholded",thresh)

blank = np.ones((img.shape[0],img.shape[1],3),dtype = np.uint8)
cv.imshow("blank",blank)

contours,hierarchy = cv.findContours(canny,cv.RETR_LIST,cv.CHAIN_APPROX_SIMPLE)
print(f"{len(contours)} countour(s)")

cv.drawContours(blank,contours,-1,(0,200,125),thickness=1)
cv.imshow("blank-contoured",blank)

if not cv.imwrite("photos/catsContoured.png",blank):
    print("Could not write the image")
else:
    print("Image written successfully")'''

'''img = cv.imread("photos/park.jpg")
if img is None:
    print("Error: Image not loaded")
    sys.exit(1)
cv.imshow("park",img)

blank = np.zeros((img.shape[:2]),dtype = np.uint8)

b,g,r = cv.split(img)
cv.imshow("park-binary-blue",b)
cv.imshow("park-binary-green",g)
cv.imshow("park-binary-red",r)

blue = cv.merge([b,blank,blank])
cv.imshow("park-blue",blue)

green = cv.merge([blank,g,blank])
cv.imshow("park-green",green)

red = cv.merge([blank,blank,r])
cv.imshow("park-red",red)'''

'''img = cv.imread("photos/cats.jpg")
if img is None:
    print("Error: Image not loaded")
    sys.exit(1)
cv.imshow("cats",img)

bilateral = cv.bilateralFilter(img,241,120,1000)
cv.imshow("cats-bilateral",bilateral)'''

'''blank = np.zeros((400,400),dtype='uint8')

rectangle = cv.rectangle(blank.copy(),(30,30),(370,370),255,-1)
circle = cv.circle(blank.copy(),(200,200),200,255,-1)

cv.imshow('rectangle',rectangle)
cv.imshow('circle',circle)

RectangleAndCircle = cv.bitwise_and(rectangle,circle)
cv.imshow("rectangle . circle",RectangleAndCircle)

RectangleOrCircle = cv.bitwise_or(rectangle,circle)
cv.imshow("rectangle + circle",RectangleOrCircle)

NotRectangle = cv.bitwise_not(rectangle)
cv.imshow("~rectangle",NotRectangle)


RectangleXorCircle = cv.bitwise_xor(rectangle,circle)
cv.imshow("rectangle xor circle",RectangleXorCircle)'''

'''img = cv.imread("photos/cats.jpg")
if img is None:
    print("Error: Image not loaded")
    sys.exit(1)
cv.imshow("cats",img)

blur = cv.GaussianBlur(img,(31,31),0)
cv.imshow("blur mask",blur)

mask = np.zeros((img.shape[0],img.shape[1]),dtype='uint8')
cv.circle(mask,( mask.shape[1]//2+45,mask.shape[0]//2),40,255,thickness=-1)


blurred = cv.bitwise_and(blur,blur,mask=cv.bitwise_not(mask))
cv.imshow('blurred mask',blurred)

mask2 = cv.bitwise_and(img,img,mask=mask)
cv.imshow('cutout',mask2)

masked_img = cv.add(blurred,mask2)
cv.imshow('img',masked_img)'''



cv.waitKey(0)
cv.destroyAllWindows()




