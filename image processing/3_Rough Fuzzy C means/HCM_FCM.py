import numpy as np
import numpy.typing as npt
import os
from numba import njit
from Loader import Loader
from ANSI import *
from ImageGUI import getImg
from thirteen_features import Features
from Discriminant_Analysis_Initialisation import DAI
from loggingIn import loggingIn as lI

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_DIR, "loggs")
os.makedirs(LOG_DIR, exist_ok=True)

HCMFCMlog = lI(os.path.join(LOG_DIR, "HCM_FCM.log"))

@njit(cache=True,fastmath=True)
def _HCM(
    V:npt.NDArray[np.float32],      #centroids
    X:npt.NDArray[np.float32],      #features
    H:int,W:int,                    #dimensions
    max_iter:int = 100,
    n_classes = 4
):
    n = X.shape[0]
    n_features = X.shape[1]
    labels = np.empty(n, dtype=np.int32)
    V = V.copy()
    V_new = np.empty_like(V)
    sums = np.zeros_like(V)
    counts = np.zeros(n_classes, dtype=np.int32)

    for _ in range(max_iter):
        sums.fill(0.0)
        counts.fill(0)

        for idx in range(n):
            closest_class = 0
            closest_distance = np.inf
            for c in range(n_classes):
                distance = 0.0
                for feature in range(n_features):
                    difference = X[idx, feature] - V[c, feature]
                    distance += difference * difference
                if distance < closest_distance:
                    closest_distance = distance
                    closest_class = c

            labels[idx] = closest_class
            counts[closest_class] += 1
            for feature in range(n_features):
                sums[closest_class, feature] += X[idx, feature]

        max_change = 0.0
        for c in range(n_classes):
            for feature in range(n_features):
                if counts[c] == 0:
                    V_new[c, feature] = V[c, feature]
                else:
                    V_new[c, feature] = sums[c, feature] / counts[c]
                change = abs(V_new[c, feature] - V[c, feature])
                if change > max_change:
                    max_change = change

        V = V_new.copy()
        if max_change <= 0.01:
            break

    return labels.reshape(H, W), V
            
        
    
@njit(cache=True,fastmath=True,nogil=True)
def _FCM(
    V:npt.NDArray[np.float32],          #centroids  
    X:npt.NDArray[np.float32],          #features
    H:int,W:int,                
    epsilon:float=1e-5,
    max_iter=100,
    m_dash:float=2.0,
    c = 4
):
    n = X.shape[0]                      #number of pixels in total
    n_features = X.shape[1]
    if m_dash <= 1.0:
        raise ValueError("m_dash must be greater than 1")

    labels = np.empty(n, dtype=np.int32)
    V = V.copy()
    mu = np.zeros((n, c), dtype=np.float32)
    mu_prev = np.zeros_like(mu)
    exponent = 2.0 / (m_dash - 1.0)

    for iteration in range(max_iter):
        #----Membership Matrix------------------#
        for i in range(n):
            zero_distances = 0
            for j in range(c):
                distance_squared = 0.0
                for feature in range(n_features):
                    difference = X[i, feature] - V[j, feature]
                    distance_squared += difference * difference
                if distance_squared == 0.0:
                    zero_distances += 1

            if zero_distances > 0:
                for j in range(c):
                    distance_squared = 0.0
                    for feature in range(n_features):
                        difference = X[i, feature] - V[j, feature]
                        distance_squared += difference * difference
                    if distance_squared == 0.0:
                        mu[i, j] = 1.0 / zero_distances
                    else:
                        mu[i, j] = 0.0
            else:
                for j in range(c):
                    distance_j = 0.0
                    for feature in range(n_features):
                        difference = X[i, feature] - V[j, feature]
                        distance_j += difference * difference

                    sum_term = 0.0
                    for k in range(c):
                        distance_k = 0.0
                        for feature in range(n_features):
                            difference = X[i, feature] - V[k, feature]
                            distance_k += difference * difference
                        sum_term += (distance_j / distance_k) ** (exponent / 2.0)
                    mu[i, j] = 1.0 / sum_term

        #----Convergence Check------------------#
        max_change = 0.0
        if iteration > 0:
            for i in range(n):
                for j in range(c):
                    change = abs(mu[i, j] - mu_prev[i, j])
                    if change > max_change:
                        max_change = change
            if max_change <= epsilon:
                break

        #----Centroid Update--------------------#
        for i in range(c):
            numerator = np.zeros(n_features, dtype=np.float32)
            denominator = 0.0
            for j in range(n):
                weight = mu[j, i] ** m_dash
                for feature in range(n_features):
                    numerator[feature] += weight * X[j, feature]
                denominator += weight
            if denominator > 0.0:
                for feature in range(n_features):
                    numerator[feature] /= denominator
                    V[i, feature] = numerator[feature]

        mu_prev[:, :] = mu

    #----Hard Label Extraction------------------#
    for i in range(n):
        labels[i] = np.argmax(mu[i])

    #----Reshape Image--------------------------#
    return labels.reshape(H, W), V, mu


@HCMFCMlog()
def HCM(
    V: npt.NDArray[np.float32],
    img: Features,
    imageFile: str | os.PathLike[str],
    max_iter: int = 100,
    c = 4
):
    with Loader(f"Running Hard C-Means( cluster-count = {c} )"):
        labels, centroids = _HCM(
            V, 
            img.features, 
            img.height, 
            img.width, 
            max_iter,
            n_classes=c
        )

    infoHCMFCMlog(f"HCM clusters: {centroids.shape[0]}")  # type: ignore
    infoHCMFCMlog(f"HCM label shape: {labels.shape}")  # type: ignore
    return labels, centroids


@HCMFCMlog()
def FCM(
    V: npt.NDArray[np.float32],
    img: Features,
    imageFile: str | os.PathLike[str],
    epsilon: float = 1e-5,
    max_iter: int = 100,
    m_dash: float = 2.0,
    c = 4
):
    with Loader(f"Running Fuzzy C-Means( cluster-count = {c} )"):
        labels, centroids, membership = _FCM(
            V, 
            img.features, 
            img.height, 
            img.width, 
            epsilon, 
            max_iter, 
            m_dash,
            c = c
        )

    infoHCMFCMlog(f"FCM clusters: {centroids.shape[0]}")  # type: ignore
    infoHCMFCMlog(f"FCM label shape: {labels.shape}")  # type: ignore
    infoHCMFCMlog(f"FCM membership shape: {membership.shape}")  # type: ignore
    return labels, centroids, membership
        
if __name__ == "__main__":
    with Loader("Fetching Image",font = [ANSI.BOLD,ANSI.BRIGHT_RED]):
        imgPath = getImg()
    img = Features(imgPath)
    centroids = np.asarray(DAI(img, imageFile=imgPath), dtype=np.float32)
    HCM(centroids, img, imageFile=imgPath)
    FCM(centroids, img, imageFile=imgPath)
    
