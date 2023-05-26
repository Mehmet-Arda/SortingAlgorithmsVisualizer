from PyQt5.QtWidgets import *

from matplotlib.backends.backend_qt5agg import FigureCanvas

from matplotlib.figure import Figure

import matplotlib.pyplot as plt
from matplotlib import style


class MplWidget(QWidget):

    def __init__(self, parent=None):

        QWidget.__init__(self, parent)

        self.figure = Figure()

        self.canvas = FigureCanvas(self.figure)
        
        style.use("seaborn")
       

        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.canvas)

        self.canvas.axes = self.canvas.figure.add_subplot(1, 1, 1)
        self.setLayout(vertical_layout)
