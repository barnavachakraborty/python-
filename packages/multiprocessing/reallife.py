from PIL import Image, ImageFilter
import time
import os
from glob import glob

directory = r"E:\python\packages\threading"

jpg_files = glob(os.path.join(directory, "**", "*.jpg"), recursive=True)

size = (1200, 1200)

os.makedirs("processed", exist_ok=True)

t1 = time.perf_counter()

for img_name in jpg_files:
    try:
        with Image.open(img_name) as img:
            img = img.filter(ImageFilter.GaussianBlur(12))
            img.thumbnail(size)

            output_path = os.path.join(
                "processed",
                os.path.basename(img_name)
            )

            img.save(output_path)
            print(f'{img_name}')

        print(f"{img_name} saved")

    except Exception as e:
        print(f"Invalid image: {img_name}")
        print(e)

t2 = time.perf_counter()

print(f"Took {round(t2 - t1, 2)} seconds")