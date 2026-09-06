import subprocess
import numpy as np
from pathlib import Path
from PIL import Image
from thirteen_features import Features
from Discriminant_Analysis_Initialisation import DAI
from HCM_FCM import HCM, FCM
from ANSI import *
from ImageGUI import getImg
from Loader import Loader

IRFANVIEW = r"E:\c_files\image_processing\IrfanView\i_view64.exe"

def labels_to_pgm(labels: np.ndarray, c: int, out_path: Path):
    with Loader("Converting from label to image", [ANSI.BOLD]):
        labels = labels.astype(np.float32)
        min_val, max_val = labels.min(), labels.max()
        if max_val > min_val:
            intensity = np.round((labels - min_val) * (255.0 / (max_val - min_val))).astype(np.uint8)
        else:
            intensity = np.full_like(labels, 128, dtype=np.uint8)
        with open(out_path, 'w') as f:
            f.write(f"P2\n{intensity.shape[1]} {intensity.shape[0]}\n255\n")
            for row in intensity:
                f.write(' '.join(map(str, row)) + '\n')

def get_unique_output_path(out_dir: Path, base_name: str, c: int, method: str) -> Path:
    pattern = f"{base_name}_Rough_Fuzzy_C_Means_{method}_c{c}_*.pgm"
    existing = list(out_dir.glob(pattern))
    count = len(existing) + 1
    out_name = f"{base_name}_Rough_Fuzzy_C_Means_{method}_c{c}_{count}.pgm"
    return out_dir / out_name

def save_and_open(labels: np.ndarray, c, img_path: str, method: str):
    with Loader(f"Saving and Opening for {method}", [ANSI.BOLD]):
        in_path = Path(img_path)
        out_dir = Path("output")
        out_dir.mkdir(exist_ok=True)
        out_path = get_unique_output_path(out_dir, in_path.stem, c, method)
        labels_to_pgm(labels, c, out_path)
        subprocess.Popen([IRFANVIEW, str(out_path.resolve())])

print(f"\033[{ANSI.BRIGHT_MAGENTA_BACKGROUND};{ANSI.BOLD}m   -----  Rough Fuzzy C-Means  -----------------   \033[0m")
with Loader("Fetching Image",font = [ANSI.BOLD,ANSI.BRIGHT_RED]):
    imgPath = getImg()
img = Features(imgPath)
centroids = np.asarray(DAI(img, imageFile=imgPath), dtype=np.float32)
c_in = input(
    f"\033[{ANSI.BOLD};{ANSI.BRIGHT_BLUE}m\n"
    "Enter the number of clusters( Default = 4 | c = candidate clusters ): "
)
if c_in == "":
    c = 4
elif c_in == "c":
    c = centroids.shape[0]
else:
    c = int(c_in)
if c > centroids.shape[0]:
    raise ValueError("Cluster count value more than Candidate centroids")
hcm_labels, hcm_centroids = HCM(centroids, img, imageFile=imgPath, c = c)
fcm_labels, fcm_centroids, _ = FCM(centroids, img, imageFile=imgPath, c = c)

save_and_open(hcm_labels, c, imgPath, "HCM")
save_and_open(fcm_labels, c, imgPath, "FCM")





