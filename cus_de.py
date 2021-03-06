from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5 import uic
import sys
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NT
from matplotlib.figure import Figure
import math
from skimage import measure, color, io
from sklearn.cluster import KMeans, MeanShift
from yellowbrick.cluster import KElbowVisualizer
import logging
import pandas as pd

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                    , level=logging.INFO)
log = logging.getLogger(__name__)

version = '1.0.6 beta'


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('modus.ui', self)
        self.setWindowTitle('Автоматическая детекция гломерул обонятельной луковицы')
        self.button = self.findChild(QtWidgets.QPushButton, 'pushButton')
        self.button_exp = self.findChild(QtWidgets.QPushButton, 'pushButton_2')
        self.button_file = self.findChild(QtWidgets.QPushButton, 'pushButton_3')

        self.file = QtWidgets.QFileDialog.getOpenFileName(self,
                                                          "Выберите файл",
                                                          None,
                                                          filter="(*.png *.jpg *.tiff)")[0]
        log.info(self.file)
        if not self.file:
            rep = QtWidgets.QMessageBox.question(self, 'Предупреждение', 'Вы не выбрали файл. Выбрать снова?',
                                                 QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                 QtWidgets.QMessageBox.Yes)
            if rep == QtWidgets.QMessageBox.Yes:
                self.open_file()
            else:
                return

        # Порог
        self.input_2 = self.findChild(QtWidgets.QDoubleSpinBox, 'doubleSpinBox_2')
        # Размер
        self.input_x = self.findChild(QtWidgets.QDoubleSpinBox, 'doubleSpinBox')
        # label
        self.label_max = self.findChild(QtWidgets.QLabel, 'label_3')
        self.label_min = self.findChild(QtWidgets.QLabel, 'label_4')
        # ver
        self.lab_ver = self.findChild(QtWidgets.QLabel, 'label_5')
        self.lab_ver.setText(version)

        self.fig = Figure(figsize=(10, 4), dpi=100)
        self.axes = self.fig.add_subplot(131)
        self.axes1 = self.fig.add_subplot(132)
        self.axes2 = self.fig.add_subplot(133)

        self.plot = FigureCanvas(self.fig)
        self.lay = QtWidgets.QVBoxLayout(self.graph)

        self.lay.setContentsMargins(0, 0, 0, 0)
        self.lay.addWidget(self.plot)

        self.button_exp.clicked.connect(self.export_csv)
        self.button.clicked.connect(self.update_chart)
        self.button_file.clicked.connect(self.open_file)

        self.addToolBar(QtCore.Qt.TopToolBarArea, NT(self.plot, self))

        self.update_chart()

    def open_file(self):
        self.file = QtWidgets.QFileDialog.getOpenFileName(self,
                                                          "Выберите файл",
                                                          filter="(*.png *.jpg *.tiff)")[0]
        if len(self.file) > 0:
            self.update_chart()
        else:
            return

    def update_chart(self):
        rz_x = float(self.input_x.text().replace(',', '.'))

        img, contours, y_t, x_t, parametr_p, mkm_width, caff, centroids = self.f_dir(
            p=float(
                self.input_2.text().replace(
                    ',',
                    '.')),

            rz_x=rz_x,
            file=self.file)
        self.axes.cla()
        self.axes1.cla()
        self.axes2.cla()

        self.axes.set_title('Центроиды')
        self.axes1.set_title('Оригинал')
        self.axes2.set_title('Контуры - {}'.format(parametr_p))

        self.axes.imshow(img)
        self.axes1.imshow(img)
        self.axes.scatter(y_t, x_t, s=5, c='red')
        self.axes2.scatter(y_t, x_t, s=5, c='red')

        self.axes.set_xlabel('px', fontsize=8)
        self.axes.set_ylabel('px', fontsize=8)
        self.axes1.set_xlabel('px', fontsize=8)
        self.axes1.set_ylabel('px', fontsize=8)
        self.axes2.set_xlabel('px', fontsize=8)
        self.axes2.set_ylabel('px', fontsize=8)

        # длина вектора по координатам
        # AB = sqrt (bx - ax)^2 + (by-ay)^2

        DD_vector = []
        for n, contour in enumerate(contours):
            A_Xmin = min(contour[:, 0])
            A_Ymax = max(contour[:, 1])

            B_Xmax = max(contour[:, 0])
            B_Ymin = min(contour[:, 1])
            D_vector = pow((B_Xmax - A_Xmin), 2) + pow((B_Ymin - A_Ymax), 2) - 1
            # D_vector = math.sqrt(D_vector) * caff
            DD_vector.append(D_vector)
            self.axes2.plot(contour[:, 1], contour[:, 0], linewidth=2, color='red')
        log.info("cont === %s", DD_vector)

        self.axes2.invert_yaxis()
        self.fig.tight_layout()
        self.plot.draw_idle()

    def export_csv(self):
        rz_x = float(self.input_x.text().replace(',', '.'))

        img, contours, y_t, x_t, parametr_p, rz_x, rz_y, centroids = self.f_dir(
            p=float(
                self.input_2.text().replace(',',
                                            '.')),
            rz_x=rz_x,
            file=self.file)

        df = []
        for c in contours:
            for k in c:
                df.append(k)

        pd.DataFrame(df, columns=['X', 'Y']).to_excel('contours.xlsx', index=False)
        pd.DataFrame(centroids, columns=['X', 'Y']).to_excel('centroids.xlsx')

    def km(self, img, number, g, parametr_p, rz_x):
        x = g[0]
        y = g[1]

        # Если имеется массив центроидов
        if len(x) > 0 and len(y) > 0:
            x_t = []
            y_t = []
            mkm_width, caff = self.rz(1214.6, img, rz_x)

            # zip (..., ..., img[x, y])
            z = [list(hhh) for hhh in zip(x, y)]

            # elbow method
            # model = KMeans()
            # vis = KElbowVisualizer(model, k=(1, 15))
            # vis.fit(np.array(z))
            #
            # k = KMeans(n_clusters=vis.elbow_value_).fit(z)
            af = MeanShift().fit(z)

            arrayp = [[0]] * len(af.cluster_centers_)
            for d, c in enumerate(arrayp):
                kkk = []
                for i, m in enumerate(af.labels_):
                    if m == d:
                        kkk.append(z[i])
                arrayp[d] = np.array(kkk)

            hhhhh = len(af.cluster_centers_)
            DD_vector = []
            for n, aaa in enumerate(arrayp):
                A_Xmin = min(aaa[:, 0])
                A_Ymax = max(aaa[:, 1])

                B_Xmax = max(aaa[:, 0])
                B_Ymin = min(aaa[:, 1])
                D_vector = pow((B_Xmax - A_Xmin), 2) + pow((B_Ymin - A_Ymax), 2)
                D_vector = math.sqrt(D_vector) * caff
                DD_vector.append(D_vector)
                if D_vector <= rz_x:
                    g = aaa[:].tolist()
                    z = [s for s in z if s not in g]
                    img[aaa[:, 0], aaa[:, 1]] = 0
                    # hhhhh = hhhhh - 1

            log.info("img === %s --- centroid === %s ---- cenhhhh ==== %s", DD_vector, len(af.cluster_centers_), hhhhh)
            # self.label_max.text()
            contours = measure.find_contours(img, number)
            # for n, contour in enumerate(contours):
            #     self.axes2.plot(contour[:, 1], contour[:, 0], linewidth=2)

            if len(z) > 0:
                x_t = list(af.cluster_centers_[:, 0])
                y_t = list(af.cluster_centers_[:, 1])
            else:
                self.label_max.setText('Заданный размер слишком высок')

            log.info('Параметр порога - {}'.format(parametr_p))
            return img, contours, y_t, x_t, parametr_p, mkm_width, caff, af.cluster_centers_
        else:
            log.info("Не можем определить центроиды")

    def rz(self, mkm, img, rz_x):
        iw, ih = img.shape[0], img.shape[1]
        # поиск сколько приходится на 1 пиксель мкм
        caff = mkm / iw
        mkm_width = round(caff * rz_x)
        return mkm_width, caff

    def f_dir(self, p, rz_x, file):
        log.info('Поиск центроидов начат')

        # ЧБ
        image = color.rgb2gray(io.imread(file))
        # pltt.clf()
        # pltt.imshow(image)
        # pltt.savefig('1.png')
        # pltt.clf()
        # np.savetxt('g.csv', image, delimiter=',', fmt='%.5f')
        # calculate
        # fast = image.max() - p
        # load
        raze = image <= p
        image = np.where(raze, 0, image)
        gosh = np.where(image >= p)

        fig = self.km(image, number=p, g=gosh, parametr_p=p, rz_x=rz_x)
        log.info('Поиск центроидов окончен')
        return fig


app = QtWidgets.QApplication(sys.argv)
window = Ui()
window.show()
app.exec_()
