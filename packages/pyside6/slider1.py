from PySide6.QtWidgets import QSlider
from PySide6.QtCore import Qt

class Slider(QSlider):
    def __init__(self):
        super().__init__(Qt.Orientation.Horizontal)
        self.setMinimum(1)
        self.setMaximum(100)
        self.setValue(25)
        self.valueChanged.connect(lambda value:
            print(f"slider moved to {value}")    
        )
