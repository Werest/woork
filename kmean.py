import cv2
import os
import logging
import numpy as np
import matplotlib.pyplot as plt
import sqlite3
from skimage import color, measure, feature
from skimage import io
from sklearn.cluster import KMeans, MeanShift
from zipfile import ZipFile, ZIP_DEFLATED
from yellowbrick.cluster import KElbowVisualizer


# plt.style.use('dark_background')
# config for logging
# https://docs.python.org/3/library/logging.html#logrecord-attributes
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                    , level=logging.INFO)
log = logging.getLogger(__name__)

array_x_t = []
array_y_t = []

# conn = sqlite3.connect('i.db')
# cursor = conn.cursor()


def km(img, number, g, dr, opa):
    # plt.cla()
    # plt.clf()

    x = g[0]
    y = g[1]
    # Если имеется массив центроидов
    if len(x) > 0 and len(y) > 0:
        # zip (..., ..., img[x, y])
        z = [list(hhh) for hhh in zip(x, y)]

        # elbow method
        model = KMeans()
        vis = KElbowVisualizer(model, k=(1, 15))

        vis.fit(np.array(z))

        plt.cla()
        plt.clf()
        contours = measure.find_contours(img, 0.5)
        fig, (ax, ax1, ax2) = plt.subplots(nrows=1, ncols=3, figsize=(8, 3))
        ax.axis('on')

        ax.set_title('Центроиды')
        ax1.set_title('Оригинал')
        ax2.set_title('Контуры')

        ax.imshow(img)
        ax1.imshow(img)
        for n, contour in enumerate(contours):
            ax2.plot(contour[:, 0], contour[:, 1], linewidth=2)

        k = KMeans(n_clusters=vis.elbow_value_).fit(z)
        x_t = list(k.cluster_centers_[:, 0])
        y_t = list(k.cluster_centers_[:, 1])
        ax.scatter(y_t, x_t, s=5, c='red')

        # plt.savefig('{}/{}'.format(dr, number))
        # plt.close(fig)
        # log.info(number)

        array_x_t.append(x_t)
        array_y_t.append(y_t)
        return fig
    else:
        log.info("Не можем определить центроиды")


def gen_video(img_folder, vn, fd):
    if not os.path.isfile(video_name):
        imgs = [img for img in os.listdir(img_folder)]
        frame = cv2.imread(os.path.join(img_folder, imgs[0]))
        height, width, layers = frame.shape
        video = cv2.VideoWriter(vn, 0, 1, (width, height))

        for image in imgs:
            video.write(cv2.imread(os.path.join(img_folder, image)))
        cv2.destroyAllWindows()
        video.release()

    if not os.path.isfile(fd):
        log.info('Создание zip файла - %s', fd)
        with ZipFile(fd, mode='w', compression=ZIP_DEFLATED) as misfile:
            misfile.write(video_name)


def f_dir(d, p, od, vn, fd):
    log.info('Сканирование директории для исследования - %s', d)
    remove_ds_store = [name for name in os.listdir(d) if not name.startswith(('.', 'ORG'))]
    sort_list = sorted(remove_ds_store)
    log.info('Найдено %s образца', len(sort_list))

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

    fig = km(image, number=91001, g=gosh, dr=od, opa=d)
        # plt.scatter(gosh[0], gosh[1], color='red')
        # plt.show()
    log.info('Поиск центроидов окончен')
    return fig
    # log.info('Началась генерация видео')
    # gen_video(img_folder=d, vn=vn, fd=fd)
    # log.info('Окончена генерация видео')

# config directory, files and etc.
directory = "2020-2/A4 98 um 20200325/"
output_dir = 'a11'

video_name = '1.avi'
fileid = 'video.zip'

log.info('Директория для исследования - %s', directory)
log.info('Директория для выходных изображений - %s', output_dir)
f_dir(d=directory, p=0.5, od=output_dir, vn=video_name, fd=fileid)