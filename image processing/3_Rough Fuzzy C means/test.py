# import cv2 as iio

# img = iio.imread(r"E:\python\image processing\4_RFCM\Images\1_090.pgm")

# print(img)
# # print(img.shape)
# # print(img.dtype)
# # print(img[20, 100])

# offsets = [[-1,-1],[-1, 0],[-1, 1],
#            [ 0,-1],[ 0, 0],[ 0, 1],
#            [ 1,-1],[ 1, 0],[ 1, 1]]

# print(offsets[2*3+1])

# for i in range(4):
#     print(i)

# from numba import njit
# import numpy as np

# @njit(cache=True,fastmath=True)
# def add(upto:int):
#     list_ = np.sum(np.array([x for x in range(upto+1)]))
#     return list_

# print(add(10))

# from numba import njit
# import numpy as np
# import numpy.typing as npt

# @njit(cache=True,fastmath=True)
# def GROUP_PATTERNS(
#     binary:npt.NDArray[np.float32],
#     feature_matrix:npt.NDArray[np.float32],
#     N:int
# ):
#     pattern_map = np.zeros((8192,14),np.float32)
#     for j in range(N):
#         pattern = 0
#         for n in range(13):
#             pattern |= int(binary[j,n]) << n
#         pattern_map[pattern,0]+=1
#         pattern_map[pattern,1:] += feature_matrix[j,:]
#     mask = pattern_map[:,0] > 0
#     pattern_map[mask,1:] /= pattern_map[mask,0,None]
#     return pattern_map
# result = GROUP_PATTERNS(np.array([
#     [1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0],   # pixel 0
#     [1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0],   # pixel 1 — same as 0
#     [0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1],   # pixel 2 — different
#     [0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1],   # pixel 3 — same as 2
#     [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],   # pixel 4 — unique
# ], dtype=np.float32),np.array([
#     [162.0, 0.88, 12.4, 0.45, 0.02, 0.77, 8.3, 1.6, 0.78, 1.12, 0.54, 0.58, 0.03],
#     [158.0, 0.91, 11.8, 0.48, 0.03, 0.75, 8.1, 1.5, 0.76, 1.10, 0.52, 0.56, 0.02],
#     [ 45.0, 0.65,  8.1, 0.30, 0.10, 0.50, 5.2, 0.8, 0.45, 0.80, 0.30, 0.35, 0.01],
#     [ 48.0, 0.68,  8.5, 0.32, 0.11, 0.52, 5.4, 0.9, 0.47, 0.82, 0.32, 0.37, 0.01],
#     [ 12.0, 0.95,  2.1, 0.90, 0.01, 0.10, 1.2, 0.2, 0.10, 0.30, 0.05, 0.08, 0.00],
# ], dtype=np.float32),5)

# for i in range(8192):
#     if result[i,0] > 0:
#         print(f"{i}) {result[i,0]} [{result[i,1:]}]")

# print(";".join(["36","0"]))







import tkinter as tk
import numpy as np

from PIL import Image, ImageTk


class PGMViewer:

    def __init__(self, root: tk.Tk, filepath: str):

        self.root = root
        self.filepath = filepath

        self.root.title("PGM Image Viewer")
        self.root.geometry("1200x700")

        # =====================================================
        # IMAGE
        # =====================================================

        self.image = Image.open(filepath).convert("L")

        self.photo = None

        self.zoom = 1.0

        # =====================================================
        # PAN
        # =====================================================

        self.pan_x = 0
        self.pan_y = 0

        self.drag_start_x = 0
        self.drag_start_y = 0

        # =====================================================
        # MAIN FRAME
        # =====================================================

        self.main_frame = tk.Frame(
            self.root
        )

        self.main_frame.pack(
            fill="both",
            expand=True
        )

        # =====================================================
        # IMAGE FRAME
        # =====================================================

        self.image_frame = tk.Frame(
            self.main_frame
        )

        self.image_frame.pack(
            side="left",
            fill="both",
            expand=True
        )

        # =====================================================
        # HISTOGRAM FRAME
        # =====================================================

        self.histogram_frame = tk.Frame(
            self.main_frame,
            width=350
        )

        self.histogram_frame.pack(
            side="right",
            fill="y"
        )

        self.histogram_frame.pack_propagate(False)

        # =====================================================
        # IMAGE CANVAS
        # =====================================================

        self.canvas = tk.Canvas(
            self.image_frame,
            bg="gray20",
            highlightthickness=0
        )

        self.canvas.pack(
            fill="both",
            expand=True
        )

        # =====================================================
        # HISTOGRAM CANVAS
        # =====================================================

        self.histogram_canvas = tk.Canvas(
            self.histogram_frame,
            width=350,
            height=450,
            bg="white",
            highlightthickness=0
        )

        self.histogram_canvas.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        # =====================================================
        # MOUSE / TRACKPAD
        # =====================================================

        # Normal mouse wheel
        self.canvas.bind(
            "<MouseWheel>",
            self.mouse_zoom
        )

        # Ctrl + mouse wheel
        #
        # On Windows, a precision trackpad pinch is
        # commonly exposed as Ctrl + MouseWheel.
        #
        self.canvas.bind(
            "<Control-MouseWheel>",
            self.mouse_zoom
        )

        # =====================================================
        # PAN
        # =====================================================

        self.canvas.bind(
            "<ButtonPress-1>",
            self.start_pan
        )

        self.canvas.bind(
            "<B1-Motion>",
            self.pan
        )

        # =====================================================
        # DOUBLE CLICK
        # =====================================================

        # EDITED:
        # Double-click resets zoom and pan.

        self.canvas.bind(
            "<Double-Button-1>",
            self.reset_view
        )

        # =====================================================
        # DISPLAY
        # =====================================================

        self.display_image()
        self.display_histogram()

    # =========================================================
    # DISPLAY IMAGE
    # =========================================================

    def display_image(self):

        width, height = self.image.size

        new_width = max(
            1,
            int(width * self.zoom)
        )

        new_height = max(
            1,
            int(height * self.zoom)
        )

        # Nearest neighbour is useful for PGM/image processing
        # because individual pixels remain visible when zoomed.

        resized = self.image.resize(
            (new_width, new_height),
            Image.Resampling.NEAREST
        )

        self.photo = ImageTk.PhotoImage(
            resized
        )

        self.canvas.delete("all")

        self.canvas.create_image(
            self.pan_x,
            self.pan_y,
            image=self.photo,
            anchor="nw"
        )

    # =========================================================
    # ZOOM
    # =========================================================

    def mouse_zoom(self, event):

        if self.image is None:
            return

        # EDITED:
        # Remember the old zoom before changing it.

        old_zoom = self.zoom

        # =====================================================
        # Determine zoom direction
        # =====================================================

        if event.delta > 0:

            self.zoom *= 1.2

        else:

            self.zoom /= 1.2

        # =====================================================
        # Limit zoom
        # =====================================================

        self.zoom = max(
            0.1,
            min(self.zoom, 20.0)
        )

        # =====================================================
        # Zoom around mouse position
        # =====================================================

        # EDITED:
        #
        # Without this, the image grows from the top-left
        # corner.
        #
        # With this, the pixel underneath the mouse remains
        # underneath the mouse while zooming.

        mouse_x = event.x
        mouse_y = event.y

        self.pan_x = (
            mouse_x
            - (mouse_x - self.pan_x)
            * (self.zoom / old_zoom)
        )

        self.pan_y = (
            mouse_y
            - (mouse_y - self.pan_y)
            * (self.zoom / old_zoom)
        )

        self.display_image()

    # =========================================================
    # START PAN
    # =========================================================

    def start_pan(self, event):

        self.drag_start_x = event.x
        self.drag_start_y = event.y

    # =========================================================
    # PAN
    # =========================================================

    def pan(self, event):

        dx = (
            event.x
            - self.drag_start_x
        )

        dy = (
            event.y
            - self.drag_start_y
        )

        self.pan_x += dx
        self.pan_y += dy

        self.drag_start_x = event.x
        self.drag_start_y = event.y

        self.display_image()

    # =========================================================
    # RESET VIEW
    # =========================================================

    def reset_view(self, event=None):

        # EDITED:
        # Double-click returns everything to the original state.

        self.zoom = 1.0

        self.pan_x = 0
        self.pan_y = 0

        self.display_image()

    # =========================================================
    # HISTOGRAM
    # =========================================================

    def display_histogram(self):

        self.histogram_canvas.delete("all")

        # Pillow → NumPy

        image_array = np.asarray(
            self.image
        )

        # =====================================================
        # Calculate histogram
        # =====================================================

        histogram = np.bincount(
            image_array.ravel(),
            minlength=256
        )

        max_count = histogram.max()

        # =====================================================
        # Histogram dimensions
        # =====================================================

        canvas_width = 330
        canvas_height = 430

        left = 35
        top = 40
        right = 15
        bottom = 40

        graph_width = (
            canvas_width
            - left
            - right
        )

        graph_height = (
            canvas_height
            - top
            - bottom
        )

        # =====================================================
        # TITLE
        # =====================================================

        self.histogram_canvas.create_text(
            canvas_width / 2,
            15,
            text="Histogram",
            font=("Arial", 12, "bold")
        )

        # =====================================================
        # AXES
        # =====================================================

        self.histogram_canvas.create_line(
            left,
            top,
            left,
            top + graph_height
        )

        self.histogram_canvas.create_line(
            left,
            top + graph_height,
            left + graph_width,
            top + graph_height
        )

        # =====================================================
        # HISTOGRAM BARS
        # =====================================================

        bar_width = graph_width / 256

        for i in range(256):

            if histogram[i] == 0:
                continue

            bar_height = (
                histogram[i]
                / max_count
                * graph_height
            )

            x1 = (
                left
                + i * bar_width
            )

            x2 = (
                left
                + (i + 1) * bar_width
            )

            y1 = (
                top
                + graph_height
                - bar_height
            )

            y2 = (
                top
                + graph_height
            )

            self.histogram_canvas.create_rectangle(
                x1,
                y1,
                x2,
                y2,
                fill="black",
                outline=""
            )

        # =====================================================
        # X AXIS VALUES
        # =====================================================

        self.histogram_canvas.create_text(
            left,
            top + graph_height + 15,
            text="0"
        )

        self.histogram_canvas.create_text(
            left + graph_width / 2,
            top + graph_height + 15,
            text="128"
        )

        self.histogram_canvas.create_text(
            left + graph_width,
            top + graph_height + 15,
            text="255"
        )

        # =====================================================
        # X AXIS LABEL
        # =====================================================

        self.histogram_canvas.create_text(
            left + graph_width / 2,
            canvas_height - 5,
            text="Pixel Intensity"
        )

        # =====================================================
        # Y AXIS LABEL
        # =====================================================

        self.histogram_canvas.create_text(
            10,
            top + graph_height / 2,
            text="Frequency",
            angle=90
        )


# =============================================================
# getImg
# =============================================================

def getImg(filepath: str):

    root = tk.Tk()

    PGMViewer(
        root,
        filepath
    )

    root.mainloop()

    return filepath
