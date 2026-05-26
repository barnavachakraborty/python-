from PySide6.QtWidgets import QPushButton,QWidget,QHBoxLayout

class RocWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("New Window")
        button1 = QPushButton("Click Me")
        button2 = QPushButton("Click Me")
        button_Layout = QHBoxLayout()
        button_Layout.addWidget(button1)
        button_Layout.addWidget(button2)
        self.setLayout(button_Layout)