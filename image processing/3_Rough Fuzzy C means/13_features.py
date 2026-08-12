#1. paths -> typehint: str | os.PathLike[str]
#2. to get the image pixels as pixel -> img = Image.open(filename).convert("L")

from numba import njit
from PIL import Image
import numpy as np
import os
import numpy.typing as npt
import logging




@njit(cache=True, fastmath=True)
def cal_glcm(img: npt.NDArray) -> npt.NDArray:
    features = np.zeros((12, img.shape[0], img.shape[1]), dtype=np.float32)
    homogeneity = features[0]
    asm         = features[1]
    edge        = features[2]
    contrast    = features[3]
    correlation = features[4]
    idm         = features[5]
    sum_avg     = features[6]
    sum_var     = features[7]
    sum_entropy = features[8]
    entropy     = features[9]
    diff_var    = features[10]
    diff_entropy= features[11]

    GLCM     = np.empty((4, 16, 16), dtype=np.float32)
    GLCM_sum = np.empty((16, 16),    dtype=np.float32)
    px       = np.empty(16, dtype=np.float32)
    py       = np.empty(16, dtype=np.float32)
    p_xpy    = np.zeros(31, dtype=np.float32)
    p_xmy    = np.zeros(16, dtype=np.float32)

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):

            # ── clamp neighbor coordinates ──────────────────────
            im1 = i - 1 if i - 1 >= 0 else 0
            ip1 = i + 1 if i + 1 < img.shape[0] else img.shape[0] - 1
            ip2 = i + 2 if i + 2 < img.shape[0] else img.shape[0] - 1
            jm1 = j - 1 if j - 1 >= 0 else 0
            jp1 = j + 1 if j + 1 < img.shape[1] else img.shape[1] - 1
            jp2 = j + 2 if j + 2 < img.shape[1] else img.shape[1] - 1

            # ── 3x3 window (quantized to 16 levels) ─────────────
            # a b c
            # d e f
            # g h k
            a = img[im1, jm1] >> 4
            b = img[im1, j  ] >> 4
            c = img[im1, jp1] >> 4
            d = img[i  , jm1] >> 4
            e = img[i  , j  ] >> 4
            f = img[i  , jp1] >> 4
            g = img[ip1, jm1] >> 4
            h = img[ip1, j  ] >> 4
            k = img[ip1, jp1] >> 4

            # ── build GLCM ───────────────────────────────────────
            GLCM.fill(0)

            # 0° — horizontal pairs
            GLCM[0, a, b] += 1; GLCM[0, b, a] += 1
            GLCM[0, b, c] += 1; GLCM[0, c, b] += 1
            GLCM[0, d, e] += 1; GLCM[0, e, d] += 1
            GLCM[0, e, f] += 1; GLCM[0, f, e] += 1
            GLCM[0, g, h] += 1; GLCM[0, h, g] += 1
            GLCM[0, h, k] += 1; GLCM[0, k, h] += 1

            # 45° — diagonal pairs
            GLCM[1, d, b] += 1; GLCM[1, b, d] += 1
            GLCM[1, g, e] += 1; GLCM[1, e, g] += 1
            GLCM[1, e, c] += 1; GLCM[1, c, e] += 1
            GLCM[1, h, f] += 1; GLCM[1, f, h] += 1

            # 90° — vertical pairs
            GLCM[2, d, a] += 1; GLCM[2, a, d] += 1
            GLCM[2, g, d] += 1; GLCM[2, d, g] += 1
            GLCM[2, e, b] += 1; GLCM[2, b, e] += 1
            GLCM[2, h, e] += 1; GLCM[2, e, h] += 1
            GLCM[2, f, c] += 1; GLCM[2, c, f] += 1
            GLCM[2, k, f] += 1; GLCM[2, f, k] += 1

            # 135° — anti-diagonal pairs
            GLCM[3, e, a] += 1; GLCM[3, a, e] += 1
            GLCM[3, h, d] += 1; GLCM[3, d, h] += 1
            GLCM[3, f, b] += 1; GLCM[3, b, f] += 1
            GLCM[3, k, e] += 1; GLCM[3, e, k] += 1

            # ── average and normalize ────────────────────────────
            GLCM_sum.fill(0)
            for dir_ in range(4):
                for r in range(16):
                    for c_ in range(16):
                        GLCM_sum[r, c_] += GLCM[dir_, r, c_]

            P = GLCM_sum / GLCM_sum.sum()

            # ── marginal distributions + sum/diff dist ───────────
            px.fill(0)
            py.fill(0)
            p_xpy.fill(0)
            p_xmy.fill(0)

            for x in range(16):
                for y in range(16):
                    px[x]        += P[x, y]
                    py[y]        += P[x, y]
                    p_xpy[x + y] += P[x, y]
                    diff = x - y
                    if diff < 0:
                        diff = -diff
                    p_xmy[diff]  += P[x, y]

            # ── mean (reset each pixel) ──────────────────────────
            mu_x = np.float32(0)
            mu_y = np.float32(0)
            for x in range(16):
                mu_x += x * px[x]
                mu_y += x * py[x]

            # ── variance (reset each pixel) ──────────────────────
            var_x = np.float32(0)
            var_y = np.float32(0)
            for x in range(16):
                var_x += ((x - mu_x) ** 2) * px[x]
                var_y += ((x - mu_y) ** 2) * py[x]

            # ── Feature 1: Homogeneity ───────────────────────────
            I_max = max(a, b, c, d, e, f, g, h, k)
            I_min = min(a, b, c, d, e, f, g, h, k)
            if I_max == I_min:
                homogeneity[i, j] = np.float32(1.0)
            else:
                term1 = abs(a + k - c - g)
                term2 = abs(a + 2*d + g - c - 2*f - k)   # fixed: 2*d+g not 2*d+2*g
                homogeneity[i, j] = np.float32(1.0) - (np.float32(1.0) / (6 * (I_max - I_min))) * (term1 + term2)

            # ── Feature 2: Edge Value ────────────────────────────
            horiz = abs(img[im1, j ] + img[im1, jp1] + img[i,   j ] + img[i,   jp1]
                      - img[ip1, j ] - img[ip1, jp1] - img[ip2, j ] - img[ip2, jp1])
            vert  = abs(img[i,   jm1] + img[i,   j ] + img[ip1, jm1] + img[ip1, j ]
                      - img[i,   jp1] - img[i,   jp2] - img[ip1, jp1] - img[ip1, jp2])
            edge[i, j] = np.float32(0.25) * max(horiz, vert)

            # ── Features 3-6: ASM, Contrast, Correlation, IDM ───
            asm_val  = np.float32(0)
            con_val  = np.float32(0)
            corr_val = np.float32(0)
            idm_val  = np.float32(0)
            for x in range(16):
                for y in range(16):
                    asm_val  += P[x, y] ** 2
                    con_val  += (x - y) ** 2 * P[x, y]
                    corr_val += x * y * P[x, y]
                    idm_val  += P[x, y] / (np.float32(1.0) + (x - y) ** 2)

            asm[i, j]         = asm_val
            contrast[i, j]    = con_val
            correlation[i, j] = (corr_val - mu_x * mu_y) / (var_x ** 0.5 * var_y ** 0.5 + np.float32(1e-10))
            idm[i, j]         = idm_val

            # ── Feature 7: Sum Average ───────────────────────────
            sum_avg_val = np.float32(0)
            for kk in range(31):
                sum_avg_val += kk * p_xpy[kk]
            sum_avg[i, j] = sum_avg_val

            # ── Feature 8: Sum Variance ──────────────────────────
            sum_var_val = np.float32(0)
            for kk in range(31):
                sum_var_val += (kk - sum_avg_val) ** 2 * p_xpy[kk]
            sum_var[i, j] = sum_var_val

            # ── Feature 9: Sum Entropy ───────────────────────────
            sum_ent_val = np.float32(0)
            for kk in range(31):
                sum_ent_val += p_xpy[kk] * np.log(p_xpy[kk] + np.float32(1e-10))
            sum_entropy[i, j] = -sum_ent_val

            # ── Feature 10: Entropy (Second-Order) ──────────────
            ent_val = np.float32(0)
            for x in range(16):
                for y in range(16):
                    ent_val += P[x, y] * np.log(P[x, y] + np.float32(1e-10))
            entropy[i, j] = -ent_val

            # ── Feature 11: Difference Variance ─────────────────
            mu_xmy = np.float32(0)
            for kk in range(16):
                mu_xmy += kk * p_xmy[kk]
            diff_var_val = np.float32(0)
            for kk in range(16):
                diff_var_val += (kk - mu_xmy) ** 2 * p_xmy[kk]
            diff_var[i, j] = diff_var_val

            # ── Feature 12: Difference Entropy ──────────────────
            diff_ent_val = np.float32(0)
            for kk in range(16):
                diff_ent_val += p_xmy[kk] * np.log(p_xmy[kk] + np.float32(1e-10))
            diff_entropy[i, j] = -diff_ent_val

    return features


class Features:
    def __init__(self, filename: str | os.PathLike[str]):
        if not os.path.isfile(filename):
            raise FileNotFoundError(f"'{filename}' does not exist")
        try:
            _img = Image.open(filename).convert("L")
        except Exception as e:
            raise ValueError(f"Could not read Image '{filename}'.") from e
        self.img: npt.NDArray[np.uint8] = np.array(_img)
        self.height = _img.height
        self.width  = _img.width

    @property
    def features(self) -> npt.NDArray[np.float32]:
        return cal_glcm(self.img)


if __name__ == '__main__':
    img1 = Features(r'E:\python\image processing\4_RFCM/Images\1_090.pgm')
    print(img1.img.shape[0])
    print(img1.img[20, 100])
    f = img1.features
    print("Features shape:", f.shape)   # (12, H, W)