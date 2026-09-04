import tkinter as tk
from tkinter import filedialog
import os

def getImg():
    root = tk.Tk()
    root.withdraw()
    
    filepath = filedialog.askopenfilename(
        title       =   "Select a PGM File",
        filetypes   =   [
            ("PGM Files","*.pgm")
        ]
    )
    
    root.destroy()
    
    return filepath

# class  PGMViewer:
#     def __init__(self,root:tk.Tk,imgPath:os.PathLike[str]):
        
#         #──Attributes─────────────────────────
#         self.path   =   imgPath
#         self.root   =   root
#         self. 