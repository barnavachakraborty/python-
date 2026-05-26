import numpy as np
import numpy.typing as npt
import argparse
import os
import random
from ImageData import imgdata


def kMeansSegment(kSeg:imgdata, k:int) -> dict:
    if k<=1:
        raise ValueError('K should be more than 1')
    centroids = np.array([255*i // (k-1) for i in range(k)], dtype='uint8')

    label = np.empty(256, dtype=object)
    label.fill(None)

    while True:
        intmd = np.zeros((k, 2))

        for i, pixel in enumerate(kSeg.pixels):
            min_val = float('inf')
            idx = None

            for j, centroid in enumerate(centroids):
                t = abs(int(pixel) - int(centroid))
                if min_val > t:
                    min_val = t
                    idx = j

            label[pixel] = idx

            intmd[idx,0] += pixel
            intmd[idx,1] += 1

        ssum = intmd[:, 0]
        count = intmd[:, 1]

        avg_intmd = np.divide(ssum, count, out=np.zeros_like(ssum), where=count != 0)
        if np.all(np.abs(avg_intmd-centroids) <2):
            break
        
        centroids = avg_intmd.astype(np.uint8)

    # mapping pixels using label
    segmented = label[kSeg.pixels].astype(np.intp)

    # replace label indices with centroid values
    # output = np.array([centroids[idx] for idx in segmented], dtype=np.uint8)
    output = centroids[segmented].astype(np.uint8)


    
    return {
        "image" :imgdata(pixels=output,height=kSeg.height,width = kSeg.width,maxval=kSeg.maxval),
        "centroids":centroids
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--k", type=int, required=True)
    parser.add_argument("--ip", type=str, required=True)

    args = parser.parse_args()
    kSeg = imgdata(args.ip,[f'KSeg({args.k})'])
    kSeg.writeOP(kMeansSegment(kSeg,args.k)["image"].pixels)
    print('Execution Complete')