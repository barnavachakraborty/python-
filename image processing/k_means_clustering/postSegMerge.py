from watershed import watershedTransform
from ImageData import imgdata
import numpy as np
from numpy import typing as npt
from Otsu import OtsuThresholding
from loggingIn import loggingIn

workingImage = []
logger = loggingIn('logs.log')

def dictToStr(dictionary:dict)->str:
    dictionaryStr = 'Dictionary String\n'
    for i,(key,val) in enumerate(dictionary.items()):
        dictionaryStr+=f"\t{i+1}. {key}: {val}\n"
    return dictionaryStr

def neighbourSegments(watersheded:imgdata)->dict[frozenset,list]:
    height = watersheded.height
    width = watersheded.width
    pixels = watersheded.pixels.reshape(height,width)
    boundaryMap: dict[frozenset,list] = {}
    for i in range(height):                 #looping through whole image
        for j in range(width):
            if pixels[i,j] != -1:           #excluding pixels with values without BOUNDARY
                continue
            offsets = (((-1,-1),( 1, 1)),   #checking nieghbours of BOUNDARY
                       ((-1, 0),( 1, 0)),
                       ((-1, 1),( 1,-1)),
                       (( 0,-1),( 0, 1))) 
            for offset in offsets:          #loop for all the 8 neighbours
                pairs = set()               #pairs thats to be added inside the main set of unordered paires
                nij = list()
                for ii,jj in offset:        #loop for each oposite pair of neighbours 
                    ni = i+ii
                    nj = j+jj
                    rep=1
                    while (
                        0<=ni<height        and
                        0<=nj<width         and 
                        pixels[ni,nj] == -1 and 
                        rep<=5
                    ):
                        rep+=1              #getting the non-boundary pair of pixels
                        ni+=ii
                        nj+=jj
                    if not (0<=ni<height and 0<=nj<width):
                        continue            #out of the image range
                    if pixels[ni,nj] == -1: #if still a boundary
                        continue            
                    pairs.add(pixels[ni,nj])
                    nij.append((ni,nj))
                if len(pairs) == 2:         #adding as an unordered list
                    boundaryMap.setdefault(frozenset(pairs),[[],[]])
                    pairslist = list(pairs)
                    for n in nij:
                        if pixels[n[0],n[1]] == pairslist[0]:
                            boundaryMap[frozenset(pairs)][0].append(n)
                        else:
                            boundaryMap[frozenset(pairs)][1].append(n)
    return boundaryMap
                        
@logger(workingImage)
def postSegMerg(watersheded:imgdata,original:npt.NDArray[np.float32])->npt.NDArray[np.uint8]:
    height = watersheded.height
    width = watersheded.width
    W = watersheded.pixels.reshape(height,width).astype(int)
    I = original.reshape(height,width).astype(int)
    borderMap = neighbourSegments(watersheded)
    
    uniqueLabels = np.unique(W)
    uniqueLabels = uniqueLabels[uniqueLabels!=-1]
    
    M = {
        int(label) : float(np.mean(I[W==label]))
        for label in uniqueLabels           #found the means of the segmented pixels but from the original image
    }
    C = {}
    for segs in borderMap.keys():           #found the mean of each border pixels seperating each neighbour segments
        seg1,seg2 = segs
        Mij = abs(M[seg1] - M[seg2])
        former,later  = borderMap[segs]     
        former,later = float(np.mean(I[former])),float(np.mean(I[later]))
        Bij= abs(former-later)
        C[segs] = 0.5*(Bij+Mij)
    _,Cij = zip(*C.items())
    Tc = OtsuThresholding(np.array(Cij,dtype=np.int32))
        # Merge neighbouring regions whose similarity is below threshold
    for segs, cij in C.items():
        if cij < Tc:
            seg1, seg2 = tuple(segs)

            # merge seg2 into seg1
            W[W == seg2] = seg1


    # Sequential relabeling
    uniqueLabels = np.unique(W)
    infologger(str(uniqueLabels))       #type:ignore
    uniqueLabels = uniqueLabels[uniqueLabels != -1]

    labelMap = {
        oldLabel: newLabel
        for newLabel, oldLabel in enumerate(uniqueLabels, start=1)
    }

    F = W.copy()

    for oldLabel, newLabel in labelMap.items():

        F[F == oldLabel] = newLabel
    uniqueLabels = np.unique(F)
    infologger(str(uniqueLabels))       #type:ignore
    uniquel = np.unique(F)
    uniquel = uniquel[uniquel!=-1]
    
    uniqueno = len(uniquel)
    if uniqueno!=0:
        step = 255 // uniqueno
        labelMapIntensity = {
            label : (i+1)*step
            for i,label in enumerate(uniquel)
        }
        for label,intensity in labelMapIntensity.items():
            F[F == label] = intensity
    unique = np.unique(F)
    infologger(str(unique))     #type:ignore
    return F.astype(np.uint8).flatten()
        
        


        
        
workingImage.append('1_095.pgm')    
watershed = imgdata('images/1_095.pgm',['Kseg','Sobel','Otsu','Watershed','PostSegMerge'])
watershed.pixels = watershedTransform(watershed.dataform)
original = imgdata('images/1_095.pgm')
# postSegMerg(watershed.dataform,original.pixels.astype(np.float32))
watershed.writeOP(postSegMerg(watershed.dataform,original.pixels.astype(np.float32)))