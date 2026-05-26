import sys
from PySide6.QtWidgets import QMainWindow, QApplication, QPushButton

class Buttonholder(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Welcome")
        button = QPushButton("Press Me")
        self.setCentralWidget(button)
app = QApplication(sys.argv)
window = Buttonholder()
window.show()

app.exec()