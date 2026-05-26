from tkinter import *
from PIL import Image, ImageTk
from registration import registration
from view import open_excel
def home(loc):

    frame1 = LabelFrame(loc,bg = 'white',bd = 0)

    original_img = ImageTk.PhotoImage(Image.open("E:/python/Registration_College/STCET.png").resize((600,500),Image.LANCZOS))
    logo = Label(frame1,image = original_img,bg = 'white')
    logo.pack()
    logo.image = original_img

    Collegename = Label(
        frame1,
        text = "St.Thomas College of Engineering and Technology",
        font = ('Bookman Old Style',30,'bold'),
        bg = 'white',
        fg='#271d56'
    )
    Collegename.pack(expand = True)
    Details = Label(
        frame1,
        text='4,Diamond harbourRoad,Kolkata:700023 | Tel : 2448-1081/1082',
        font = ('Bookman Old Style',15,'bold'),
        bg = 'white',
        fg='black'
        )
    Details.pack(expand= True)
    buttons = LabelFrame(
        frame1,
        bg = 'white',
        relief = FLAT
    )
    Continue = Button(
        buttons,
        text='Continue',
        bg="black",
        fg='white',
        font=('Bookman Old Style',15),
        padx =20,
        relief = FLAT,
        command= lambda: registration(loc,frame1,home)
        )
    Continue.grid(row=0,column=0,padx= 5)
    View = Button(
        buttons,
        text='View',
        bg="black",
        fg='white',
        font=('Bookman Old Style',15),
        padx =40,
        relief = FLAT,
        command = open_excel
        )
    View.grid(row=0,column=1,padx=5)
    buttons.pack(pady=10)
    
    frame1.pack(expand = True)
