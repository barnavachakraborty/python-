from tkinter import *
from home import home
root = Tk()
root.state("zoomed")

root.configure(bg='white')
root.title("College System")
home(root)

root.mainloop()