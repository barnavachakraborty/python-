from ImageData import imgdata
from kSeg import kMeansSegment
from sobel import sobelFilter
from Otsu import OtsuThresholding
import numpy as np
import numpy.typing as npt
from heapq import heappush as push ,heappop as pop
import argparse



NEIGHBORS = [(-1, -1), (-1, 0), (-1,1),
             ( 0, -1),          (0, 1),
             ( 1, -1), ( 1, 0), (1, 1)]
    

def generateMarkers(KSeg: dict) -> npt.NDArray[np.int32]:
    minarea = 50
    clusters = KSeg["centroids"]
    image = KSeg["image"]
    height = image.height
    width = image.width
    pixels = image.pixels.reshape([height, width])
    M = np.zeros_like(pixels, dtype=np.int32)

    markerId = 1
    
    for cluster in clusters:
        cluster_mask = (pixels == cluster)
        if not cluster_mask.any():
            continue
        
        visited = np.zeros_like(pixels, dtype=bool)
        
        def connectedComponents(start_i: int, start_j: int) -> list | None:
            pack = []
            stack = [(start_i, start_j)]
            
            while stack:
                ii, jj = stack.pop()
                if not (0 <= ii < height and 0 <= jj < width):
                    continue
                if not cluster_mask[ii, jj] or visited[ii, jj]:
                    continue
                    
                pack.append((ii, jj))
                visited[ii, jj] = True
                
                for di, dj in NEIGHBORS:
                    stack.append((ii + di, jj + dj))
            
            return pack if len(pack) >= minarea else None
        
        components = []
        for i in range(height):
            for j in range(width):
                if cluster_mask[i, j] and not visited[i, j]:
                    blob = connectedComponents(i, j)
                    if blob is not None:
                        components.append(blob)
        
        for blob in components:
            blobset = set(blob)
            border = set()
            
            for ii, jj in blobset:
                for di, dj in NEIGHBORS:
                    ni, nj = ii + di, jj + dj
                    # Pixel is border if neighbor is out of image bounds OR not in blob
                    if not (0 <= ni < height and 0 <= nj < width) or (ni, nj) not in blobset:
                        border.add((ii, jj))
                        break
            
            blobset -= border
            
            if not blobset:      # <-- GUARD: skip edge-only blobs
                continue
            
            rows, columns = zip(*blobset)
            M[rows, columns] = markerId
            markerId += 1
    
    return M

def watershedTransform(image:imgdata)->npt.NDArray:
    height = image.height
    width = image.width
    maxval = image.maxval
    K = kMeansSegment(image.dataform,4)
    S = sobelFilter(
        imgdata(
            pixels=K["image"].pixels,
            height=height,
            width=image.width,
            maxval=image.maxval)).reshape([height,width])
    T= OtsuThresholding(imgdata(pixels=S.flatten(),height=height,width=width,maxval=maxval))
    S = np.where(S>T,S,0)
    M = generateMarkers(K)
    W = M.copy()
    BOUNDARY = -1
    UNKNOWN = 0
    Q = []
    queued = np.zeros_like(M, dtype=bool)  # track what's in queue to avoid duplicates
    for i in range(height):
        for j in range(width):
            if M[i,j] > 0:
                for ni,nj in NEIGHBORS:
                    if not(0<=ni<height and 0<=nj<width):
                        continue
                    if M[ni,nj] == UNKNOWN and not queued[ni,nj]:
                        push(Q,(S[ni,nj],ni,nj))
                        queued[ni,nj] = True
    while Q:
        (priority,x,y) = pop(Q)
        if W[x,y] != UNKNOWN:  # skip if already labeled by another path
            continue
        foundLabels = set()
        for ni,nj in NEIGHBORS:
            if not(0<=ni<height and 0<=nj<width):
                continue
            if W[ni,nj] != UNKNOWN and W[ni,nj] != BOUNDARY:  # exclude boundaries from label competition
                foundLabels.add(W[ni,nj])
        match len(foundLabels):
            case 0: 
                continue
            case 1: 
                W[x,y] = foundLabels.pop()
                for ni,nj in NEIGHBORS:
                    if not(0<=ni<height and 0<=nj<width):
                        continue
                    if W[ni,nj] == UNKNOWN and not queued[ni,nj]:
                        push(Q,(S[ni,nj],ni,nj))
                        queued[ni,nj] = True
            case _:
                W[x,y] = BOUNDARY
    W = np.where(W == UNKNOWN, BOUNDARY, W)  # assign result back to W
            
    return W.flatten()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip",required=True,type=str)
    ip = parser.parse_args().ip
    watershed = imgdata(ip,['KSeg','Sobel','Otsu','Watershed'])
    outpix = watershedTransform(watershed.dataform)
    maxoutpix = max(outpix)
    outpix = (outpix.astype(np.float32)/maxoutpix *255).astype(np.uint8)
    
    watershed.writeOP(outpix)
    