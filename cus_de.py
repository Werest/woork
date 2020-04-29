import random
from PyQt5 import QtWidgets, uic, QtCore
import sys
import numpy as np
import time
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import pandas as pd

import kmean


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('modus.ui', self)
        self.setWindowTitle('Автоматическая детекция гломерул обонятельной луковицы')
        self.button = self.findChild(QtWidgets.QPushButton, 'pushButton')
        self.button_exp = self.findChild(QtWidgets.QPushButton, 'pushButton_2')

        # Порог
        self.input_2 = self.findChild(QtWidgets.QDoubleSpinBox, 'doubleSpinBox_2')
        # Размеры x,y
        self.input_x = self.findChild(QtWidgets.QDoubleSpinBox, 'doubleSpinBox')
        self.input_y = self.findChild(QtWidgets.QDoubleSpinBox, 'doubleSpinBox_3')

        self.directory = "2020-2/A4 98 um 20200325/"
        self.output_dir = 'a11'
        self.video_name = '1.avi'
        self.fileid = 'video.zip'

        # self.addToolBar(QtCore.Qt.TopToolBarArea, NavigationToolbar(self.plot, self))

        self.fig = Figure(figsize=(8, 3), dpi=100)
        self.axes = self.fig.add_subplot(131)
        self.axes1 = self.fig.add_subplot(132)
        self.axes2 = self.fig.add_subplot(133)

        img, contours, y_t, x_t, parametr_p, rz_x, rz_y, centroids = kmean.f_dir(d=self.directory,
                                                                                 p=0.5,
                                                                                 od=self.output_dir,
                                                                                 vn=self.video_name,
                                                                                 fd=self.fileid,
                                                                                 rz_x=float(
                                                                                     self.input_x.text().replace(',',
                                                                                                                 '.')),
                                                                                 rz_y=float(
                                                                                     self.input_y.text().replace(',',
                                                                                                                 '.')))

        self.axes.set_title('Центроиды')
        self.axes1.set_title('Оригинал')
        self.axes2.set_title('Контуры - {}'.format(parametr_p))

        self.axes.imshow(img)
        self.axes1.imshow(img)
        self.axes.scatter(y_t, x_t, s=5, c='red')
        for n, contour in enumerate(contours):
            self.axes2.plot(contour[:, 0], contour[:, 1], linewidth=2)

        self.plot = FigureCanvas(self.fig)
        self.lay = QtWidgets.QVBoxLayout(self.graph)

        self.lay.setContentsMargins(0, 0, 0, 0)
        self.lay.addWidget(self.plot)

        self.button_exp.clicked.connect(self.export_csv)
        self.button.clicked.connect(self.update_chart)

    def update_chart(self):
        rz_x = float(self.input_x.text().replace(',', '.'))
        rz_y = float(self.input_y.text().replace(',', '.'))

        img, contours, y_t, x_t, parametr_p, rz_x, rz_y, centroids = kmean.f_dir(d=self.directory,
                                                                                 p=float(
                                                                                     self.input_2.text().replace(',',
                                                                                                                 '.')),
                                                                                 od=self.output_dir,
                                                                                 vn=self.video_name,
                                                                                 fd=self.fileid,
                                                                                 rz_x=rz_x,
                                                                                 rz_y=rz_y)
        self.axes.cla()
        self.axes1.cla()
        self.axes2.cla()

        self.axes.set_title('Центроиды')
        self.axes1.set_title('Оригинал')
        self.axes2.set_title('Контуры - {}'.format(parametr_p))

        self.axes.imshow(img)
        self.axes1.imshow(img)
        self.axes.scatter(y_t, x_t, s=5, c='red')
        for n, contour in enumerate(contours):
            self.axes2.plot(contour[:, 0], contour[:, 1], linewidth=2)

        self.plot.draw_idle()
        pass

    def export_csv(self):
        rz_x = float(self.input_x.text().replace(',', '.'))
        rz_y = float(self.input_y.text().replace(',', '.'))

        img, contours, y_t, x_t, parametr_p, rz_x, rz_y, centroids = kmean.f_dir(d=self.directory,
                                                                                 p=float(
                                                                                     self.input_2.text().replace(',',
                                                                                                                 '.')),
                                                                                 od=self.output_dir,
                                                                                 vn=self.video_name,
                                                                                 fd=self.fileid,
                                                                                 rz_x=rz_x,
                                                                                 rz_y=rz_y)

        df = []
        for c in contours:
            for k in c:
                df.append(k)

        np.savetxt('contours.csv', df, delimiter=',')
        np.savetxt('centroids.csv', centroids, delimiter=',')


app = QtWidgets.QApplication(sys.argv)
window = Ui()
window.show()
app.exec_()
