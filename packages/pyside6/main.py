from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton

import sys

app = QApplication(sys.argv)

window = QMainWindow()
window.setWindowTitle("Our First MainWindow App")

button = QPushButton()
button.setText("Press Me!!")

window.setCentralWidget(button)
window.show()

window.show()

app.exec()