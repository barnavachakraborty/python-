from numba import njit
from numba.core import types
from numba.typed.typedlist import List
import math
import numpy as np
import numpy.typing as npt
import os
from Loader import Loader
from ImageGUI import  getImg

from loggingIn import loggingIn as lI
from thirteen_features import Features
from ANSI import ANSI

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR  = os.path.join(BASE_DIR, 'loggs')
os.makedirs(LOG_DIR, exist_ok=True)

DAIlog = lI(os.path.join(LOG_DIR, 'Discriminant_Analysis_Initialisation.log'))

@njit(cache=True, fastmath=True,nogil=True)
def DISCRETISE(feature_matrix: npt.NDArray[np.float32], N: int):
    L = 101
    disc = np.zeros((N, 13), dtype=np.float32)
    for m in range(13):
        f_min = feature_matrix[:, m].min()
        f_max = feature_matrix[:, m].max()
        if f_max == f_min:
            for j in range(N):
                disc[j, m] = np.float32(0)
        else:
            diff = f_max - f_min
            for j in range(N):
                val = np.float32(feature_matrix[j, m])
                disc[j, m] = round((L - 1) * (val - f_min) / diff)
    return disc

@njit(cache=True, fastmath=True)
def BUILD_HISTOGRAM(disc: npt.NDArray[np.float32], N: int):
    h = np.zeros((13, 101), dtype=np.float32)
    for m in range(13):
        for j in range(N):
            z = int(disc[j, m])
            h[m, z] += 1
        h[m, :] = h[m, :] / N
    return h

@njit(cache=True, fastmath=True)
def FIND_THRESHOLDS(h):
    Tm = np.zeros(13, dtype=np.float32)
    z_idx = np.arange(101, dtype=np.float32)
    
    for m in range(13):
        best_J = -math.inf
        best_T = 0
        
        for T in range(100):
            p1 = np.float32(np.sum(h[m, :T+1]))
            p2 = np.float32(1.0 - p1)
            
            if p1 == 0 or p2 == 0:
                continue
            
            m1 = (1.0 / p1) * np.sum(z_idx[:T+1] * h[m, :T+1])
            m2 = (1.0 / p2) * np.sum(z_idx[T+1:101] * h[m, T+1:101])
            
            s1 = (1.0 / p1) * np.sum(((z_idx[:T+1] - m1) ** 2) * h[m, :T+1])
            s2 = (1.0 / p2) * np.sum(((z_idx[T+1:101] - m2) ** 2) * h[m, T+1:101])
            
            denom = p1 * s1 + p2 * s2
            if denom == 0:
                J = 0
            else:
                J = (p1 * p2 * (m1 - m2) ** 2) / denom
                
            if J > best_J:
                best_J = J
                best_T = T
        Tm[m] = best_T
    return Tm 

@njit(cache=True, fastmath=True)
def BINARISE(disc: npt.NDArray[np.float32], Tm: npt.NDArray[np.float32], N: int):
    binary = np.zeros((N, 13), dtype=np.float32)
    for j in range(N):
        for m in range(13):
            if disc[j, m] >= Tm[m]:
                binary[j, m] = 1
            else:
                binary[j, m] = 0
    return binary

@njit(cache=True, fastmath=True)
def GROUP_PATTERNS(binary: npt.NDArray[np.float32], feature_matrix: npt.NDArray[np.float32], N: int):
    pattern_map = np.zeros((8192, 14), np.float32)
    for j in range(N):
        pattern = 0
        for n in range(13):
            pattern |= int(binary[j, n]) << n
        pattern_map[pattern, 0] += 1
        pattern_map[pattern, 1:] += feature_matrix[j, :]
    
    for p in range(8192):
        if pattern_map[p, 0] > 0:
            pattern_map[p, 1:] /= pattern_map[p, 0]
            
    return pattern_map

@njit(cache=True, fastmath=True)
def SORT_AND_DEDUPLICATE(pairs: npt.NDArray[np.float32]):
    
    count = 0
    for p in range(8192):
        if pairs[p, 0] > 0:
            count += 1
            
    non_zero = np.empty((count, 14), dtype=np.float32)
    idx = 0
    for p in range(8192):
        if pairs[p, 0] > 0:
            non_zero[idx] = pairs[p]
            idx += 1

    # sort descending by count                                    
    non_zero = non_zero[np.argsort(non_zero[:, 0])[::-1]]

    reduced = List.empty_list(types.float32[::1])
    reduced.append(non_zero[0])
    for i in range(1, len(non_zero)):                            
        if np.all(non_zero[i] == non_zero[i-1]):                
            continue
        reduced.append(non_zero[i])                              

    out = np.empty((len(reduced), 14), dtype=np.float32)
    for i in range(len(reduced)):
        out[i] = reduced[i]
    return out

@njit(cache=True, fastmath=True)
def SELECT_CENTROIDS(reduced_pairs: npt.NDArray[np.float32]):
    n_ = len(reduced_pairs)
    epsilon_tilde = np.float32(0.5)                              
    R = np.float32(0.0)                                          
    for i in range(n_ - 1):
        N_curr = reduced_pairs[i, 0]
        N_next = reduced_pairs[i+1, 0]
        if N_curr == N_next:
            continue
        R += np.float32(1.0) / (N_curr - N_next)               
    
    Tr = R / epsilon_tilde
    
    centroids = List.empty_list(types.float32[::1])
    for i in range(n_):
        if reduced_pairs[i, 0] > Tr:
            centroids.append(reduced_pairs[i, 1:])
            
    return centroids

@DAIlog()
def DAI(img: Features, imageFile: str | os.PathLike[str]):
    with Loader("Calculating Centroids"):
        N = int(img.height * img.width)
        feature_matrix = img.features
        disc      = DISCRETISE(feature_matrix, N)
        h         = BUILD_HISTOGRAM(disc, N)
        Tm        = FIND_THRESHOLDS(h)
        binary    = BINARISE(disc, Tm, N)
        pairs     = GROUP_PATTERNS(binary, feature_matrix, N)
        pairs     = SORT_AND_DEDUPLICATE(pairs)
        centroids = SELECT_CENTROIDS(pairs)
        infoDAIlog(f"Centroids: {len(centroids)}")          #type:ignore       
        for i, c in enumerate(centroids):                        
            infoDAIlog(f"  centroid {i}: \n{c[:2]}")      #type:ignore
    return centroids

if __name__ == "__main__":
    with Loader("Fetching Image",font = [ANSI.BOLD,ANSI.BRIGHT_RED]):
        imgPath = getImg()
    feature_matrix = Features(imgPath)
    DAI(feature_matrix, imageFile=imgPath)