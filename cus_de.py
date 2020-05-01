from PyQt5 import QtWidgets
from PyQt5 import uic
import sys
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import math

from skimage import measure, color, io
from sklearn.cluster import KMeans
from yellowbrick.cluster import KElbowVisualizer

import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                    , level=logging.INFO)
log = logging.getLogger(__name__)

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('modus.ui', self)
        self.setWindowTitle('Автоматическая детекция гломерул обонятельной луковицы')
        self.button = self.findChild(QtWidgets.QPushButton, 'pushButton')
        self.button_exp = self.findChild(QtWidgets.QPushButton, 'pushButton_2')

        # Порог
        self.input_2 = self.findChild(QtWidgets.QDoubleSpinBox, 'doubleSpinBox_2')
        # Размер
        self.input_x = self.findChild(QtWidgets.QDoubleSpinBox, 'doubleSpinBox')
        # label
        self.label_max = self.findChild(QtWidgets.QLabel, 'label_3')
        self.label_min = self.findChild(QtWidgets.QLabel, 'label_4')

        self.directory = "2020-2/A4 98 um 20200325/"
        self.output_dir = 'a11'
        self.video_name = '1.avi'
        self.fileid = 'video.zip'

        # self.addToolBar(QtCore.Qt.TopToolBarArea, NavigationToolbar(self.plot, self))

        self.fig = Figure(figsize=(8, 3), dpi=100)
        self.axes = self.fig.add_subplot(131)
        self.axes1 = self.fig.add_subplot(132)
        self.axes2 = self.fig.add_subplot(133)

        self.plot = FigureCanvas(self.fig)
        self.lay = QtWidgets.QVBoxLayout(self.graph)

        self.lay.setContentsMargins(0, 0, 0, 0)
        self.lay.addWidget(self.plot)

        self.button_exp.clicked.connect(self.export_csv)
        self.button.clicked.connect(self.update_chart)
        self.update_chart()

    def update_chart(self):
        rz_x = float(self.input_x.text().replace(',', '.'))

        img, contours, y_t, x_t, parametr_p, mkm_width, caff, centroids = self.f_dir(d=self.directory,
                                                                                     p=float(
                                                                                         self.input_2.text().replace(
                                                                                             ',',
                                                                                             '.')),
                                                                                     od=self.output_dir,
                                                                                     vn=self.video_name,
                                                                                     fd=self.fileid,
                                                                                     rz_x=rz_x)
        self.axes.cla()
        self.axes1.cla()
        self.axes2.cla()

        self.axes.set_title('Центроиды')
        self.axes1.set_title('Оригинал')
        self.axes2.set_title('Контуры - {}'.format(parametr_p))

        self.axes.imshow(img)
        self.axes1.imshow(img)
        self.axes.scatter(y_t, x_t, s=5, c='red')
        # длина вектора по координатам
        # AB = sqrt (bx - ax)^2 + (by-ay)^2
        # DD_vector = []
        # for n, contour in enumerate(contours):
        #     A_Xmin = min(contour[:, 0])
        #     A_Ymax = max(contour[:, 1])
        #
        #     B_Xmax = max(contour[:, 0])
        #     B_Ymin = min(contour[:, 1])
        #     D_vector = pow((B_Xmax - A_Xmin), 2) + pow((B_Ymin - A_Ymax), 2)
        #     D_vector = math.sqrt(D_vector) * caff
        #     DD_vector.append(D_vector)
        #     if D_vector >= rz_x:
        #         self.axes2.plot(contour[:, 0], contour[:, 1], linewidth=2)

        self.plot.draw_idle()
        # max_DD_v, min_DD_v = max(DD_vector), min(DD_vector)
        # self.label_max.setText('Максимальная гломерула - {} мкм'.format(str(max_DD_v)))
        # self.label_min.setText('Минимальная гломерула - {} мкм'.format(str(min_DD_v)))

    def export_csv(self):
        rz_x = float(self.input_x.text().replace(',', '.'))
        rz_y = float(self.input_y.text().replace(',', '.'))

        img, contours, y_t, x_t, parametr_p, rz_x, rz_y, centroids = self.f_dir(d=self.directory,
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

    def km(self, img, number, g, dr, opa, parametr_p, rz_x):
        # plt.cla()
        # plt.clf()

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
            model = KMeans()
            vis = KElbowVisualizer(model, k=(1, 15))
            vis.fit(np.array(z))

            contours = measure.find_contours(img, 0.5)

            k = KMeans(n_clusters=vis.elbow_value_).fit(z)

            # [[z[i] for i in range(len(k.labels_))]]
            # arrayp = [for j in range(len() if j == k.labels_ [z[i] for i in range(len(k.labels_))]]
            arrayp = [[0]]* len(k.cluster_centers_)
            for d, c in enumerate(arrayp):
                kkk = []
                for i, m in enumerate(k.labels_):
                    if m == d:
                        kkk.append(z[i])
                arrayp[d] = np.array(kkk)

            hhhhh = len(k.cluster_centers_)
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
                    hhhhh = hhhhh - 1

            print(DD_vector)
            if len(z) > 0:
                k = KMeans(n_clusters=hhhhh).fit(z)

                x_t = list(k.cluster_centers_[:, 0])
                y_t = list(k.cluster_centers_[:, 1])
            else:
                self.label_max.setText('Заданный размер слишком высок')


            log.info('Параметр порога - {}'.format(parametr_p))

            return img, contours, y_t, x_t, parametr_p, mkm_width, caff, k.cluster_centers_
        else:
            log.info("Не можем определить центроиды")

    def rz(self, mkm, img, rz_x):
        iw, ih = img.shape[0], img.shape[1]
        # поиск сколько приходится на 1 пиксель мкм
        caff = mkm / iw
        mkm_width = round(caff * rz_x)
        return mkm_width, caff

    def f_dir(self, d, p, od, vn, fd, rz_x):
        # log.info('Сканирование директории для исследования - %s', d)
        # remove_ds_store = [name for name in os.listdir(d) if not name.startswith(('.', 'ORG'))]
        # sort_list = sorted(remove_ds_store)
        # log.info('Найдено %s образца', len(sort_list))

        log.info('Поиск центроидов начат')

        # ЧБ
        path = 'konstantin/2019.10.02 ФИ-59/2019.10.02_actReg/2019.10.02_2/B2 97_ac.png'
        image = color.rgb2gray(io.imread(path))
        # calculate
        fast = image.max() - p
        # load
        raze = image <= fast
        image = np.where(raze, 0, image)
        gosh = np.where(image >= fast)

        fig = self.km(image, number=91001, g=gosh, dr=od, opa=d, parametr_p=p, rz_x=rz_x)
        log.info('Поиск центроидов окончен')
        return fig


app = QtWidgets.QApplication(sys.argv)
window = Ui()
window.show()
app.exec_()
