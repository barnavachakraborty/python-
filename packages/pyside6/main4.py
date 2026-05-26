from rocwidget import RocWidget
import sys
from PySide6.QtWidgets import QApplication,QWidget

app = QApplication(sys.argv)

window = RocWidget()
window.show()

app.exec()