from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

class RawPlotWidget(QWidget):
    def __init__(self, raw):
        super().__init__()
        self.raw = raw
        self.init_ui()

    def init_ui(self):
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.fig)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def update_plot(self):
        self.ax.clear()
        self.raw.plot(duration=2, n_channels=20, show=False, axes=self.ax)
        self.canvas.draw()