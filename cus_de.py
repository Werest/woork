import random
from PyQt5 import QtWidgets, uic, QtCore
import sys
import numpy as np

from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

import kmean

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('modus.ui', self)
        self.setWindowTitle('Hello!')
        self.button = self.findChild(QtWidgets.QPushButton, 'pushButton')
        self.input = self.findChild(QtWidgets.QDoubleSpinBox, 'doubleSpinBox')
        self.input_2 = self.findChild(QtWidgets.QDoubleSpinBox, 'doubleSpinBox_2')
        self.label = self.findChild(QtWidgets.QLabel, 'label')

        # test data
        # data = np.array([0.7, 0.7, 0.7, 0.8, 0.9, 0.9, 1.5, 1.5, 1.5, 1.5])
        # fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(8, 3))
        # bins = np.arange(0.6, 1.62, 0.02)
        # n1, bins1, patches1 = ax1.hist(data, bins, alpha=0.6, density=False, cumulative=False)
        # n1, bins1, patches1 = ax2.hist(data, bins, alpha=0.6, density=False, cumulative=False)

        # config directory, files and etc.
        directory = "2020-2/A4 98 um 20200325/"
        output_dir = 'a11'

        video_name = '1.avi'
        fileid = 'video.zip'

        # log.info('Директория для исследования - %s', directory)
        # log.info('Директория для выходных изображений - %s', output_dir)
        fig = kmean.f_dir(d=directory, p=0.5, od=output_dir, vn=video_name, fd=fileid)
        # plot
        self.plotWidget = FigureCanvas(fig)
        lay = QtWidgets.QVBoxLayout(self.graph)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(self.plotWidget)
        # add toolbar
        self.addToolBar(QtCore.Qt.TopToolBarArea, NavigationToolbar(self.plotWidget, self))






app = QtWidgets.QApplication(sys.argv)
window = Ui()
window.show()
app.exec_()
