import numpy as np
import numpy.typing as npt
import argparse
import os
import random
from pathlib import Path


def kMeansSegment(height:int, width:int, pixels:npt.NDArray[np.uint8], k:int) -> npt.NDArray[np.uint8]:
    
    centroids = np.array(random.sample(range(256), k=k), dtype='uint8')

    label = np.empty(256, dtype=object)
    label.fill(None)

    for _ in range(10):
        intmd = np.zeros((k, 2))

        for i, pixel in enumerate(pixels):
            min_val = float('inf')
            idx = None

            for j, centroid in enumerate(centroids):
                t = abs(int(pixel) - int(centroid))
                if min_val > t:
                    min_val = t
                    idx = j

            if label[pixel] is None:
                label[pixel] = idx

            intmd[idx][0] += pixel
            intmd[idx][1] += 1

        ssum = intmd[:, 0]
        count = intmd[:, 1]

        avg_intmd = np.divide(ssum, count, out=np.zeros_like(ssum), where=count != 0)
        centroids = avg_intmd.astype(np.uint8)

    # mapping pixels using label
    segmented = label[pixels]

    # replace label indices with centroid values
    output = np.array([centroids[idx] for idx in segmented], dtype=np.uint8)

    return output


def main(ip:str, op:str, k:int):

    # ASSIGNMENT OF VALUES
    pixels, height, width = None, None, None

    try:
        with open(ip, "r") as f_ip:
            if f_ip.readline().strip() != 'P2':
                raise Exception("Not a proper file...")

            pos = f_ip.tell()
            comment = f_ip.readline()
            if not comment.startswith('#'):
                f_ip.seek(pos)

            width, height = map(int, f_ip.readline().split())
            maxval = int(f_ip.readline())

            data = list(map(int, f_ip.read().split()))
            pixels = np.array(data, dtype="uint8")

            if pixels.size != height * width:
                raise ValueError("The pixel data does not match")

    except FileNotFoundError:
        print(f"{ip} not found")
        exit(1)

    # KMEANS OUTPUT
    pixels = kMeansSegment(height=height, width=width, pixels=pixels, k=k)

    # CREATION OF UNIQUE FILENAME AND WRITING
    c = 0
    if pixels is None:
        raise ValueError("Image loading failed")

    while True:
        splitt = os.path.splitext(op)
        op_name = f"{splitt[0]}-{k}-centroids{splitt[1]}"

        filename = op_name
        if c != 0:
            name, ext = os.path.splitext(op_name)
            filename = f"{name}({c}){ext}"

        try:
            with open(filename, "x") as f_op:
                print(f"{filename} opened")

                f_op.write(f"P2\n{width} {height}\n{maxval}\n")

                for i in range(height):
                    for j in range(width):
                        f_op.write(f"{pixels[i*width + j]} ")
                    f_op.write("\n")

                break

        except:
            c += 1

    print("Execution Complete.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--k", type=int, required=True)
    parser.add_argument("--ip", type=str, required=True)

    args = parser.parse_args()
    op = Path(args.ip).name
    
    main(args.ip, op, args.k)