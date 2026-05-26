import sys
from PySide6.QtWidgets import QApplication,QMainWindow
from button1 import ButtonHolder
from slider1 import Slider

App = QApplication(sys.argv)

#BUTTON


btn1 = ButtonHolder("btn1")
btn1.show()
btn2 = ButtonHolder("btn2",True)
btn2.show()


#SLIDER


slider1 = Slider()
slider1.show()
App.exec()


