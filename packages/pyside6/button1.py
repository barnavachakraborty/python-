from PySide6.QtWidgets import QMainWindow,QPushButton
from typing import Literal

class ButtonHolder(QMainWindow):
    def __init__(self,name,checkable=False):
        super().__init__()
        self.setWindowTitle("ButtonHolder app")
        self.btn = QPushButton("Press Me")
        self.btn.setCheckable(checkable)
        sbtn = self.btn
        self.__name = name
        self.setCentralWidget(sbtn)
        self.btn.clicked.connect(lambda data:
            print(f"{self.name} is clicked with data being {data}")
        )
    
            
    @property
    def name(self):
        return self.__name
        
        