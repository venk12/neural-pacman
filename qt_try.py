import sys
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget
from PyQt5.QtCore import QTimer
from pyqtgraph import PlotWidget, plot

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Real-Time Data Simulation")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.plot_widget = PlotWidget()
        self.layout.addWidget(self.plot_widget)

        self.btn_start_stop = QPushButton("Start")
        self.layout.addWidget(self.btn_start_stop)

        self.data_x = []
        self.data_y = []

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer_interval = 1000  # milliseconds
        self.is_running = False

        self.btn_start_stop.clicked.connect(self.toggle_simulation)

    def toggle_simulation(self):
        if not self.is_running:
            self.timer.start(self.timer_interval)
            self.btn_start_stop.setText("Stop")
            self.is_running = True
        else:
            self.timer.stop()
            self.btn_start_stop.setText("Start")
            self.is_running = False

    def update_plot(self):
        # Generate random data
        new_x = len(self.data_x)
        new_y = random.randint(0, 100)

        self.data_x.append(new_x)
        self.data_y.append(new_y)

        self.plot_widget.plot(self.data_x, self.data_y, clear=True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
