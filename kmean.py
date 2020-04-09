import cv2
import os
import logging
import numpy as np
import matplotlib.pyplot as plt
from skimage import color
from skimage import io
from sklearn.cluster import KMeans, MeanShift
from sklearn.preprocessing import StandardScaler, MinMaxScaler, normalize
from zipfile import ZipFile, ZIP_DEFLATED
from yellowbrick.cluster import KElbowVisualizer

# config for logging
# https://docs.python.org/3/library/logging.html#logrecord-attributes
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                    , level=logging.INFO)
log = logging.getLogger(__name__)

array_x_t = []
array_y_t = []


def km(img, number, g, dr):
    plt.cla()
    plt.clf()

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

        fig, (ax, ax1) = plt.subplots(nrows=1, ncols=2, figsize=(8, 3))
        ax.axis('on')

        ax.imshow(img)
        ax1.imshow(img)

        k = KMeans(n_clusters=vis.elbow_value_).fit(z)
        x_t = list(k.cluster_centers_[:, 0])
        y_t = list(k.cluster_centers_[:, 1])
        ax.scatter(y_t, x_t, s=5, c='red')

        plt.savefig('{}/{}'.format(dr, number))
        plt.close(fig)

        array_x_t.append(x_t)
        array_y_t.append(y_t)
    else:
        log.info("Не можем определить центроиды")


def gen_video():
    img_folder = 'k1'
    video_name = '1.avi'
    fileid = 'video.zip'

    if not os.path.isfile(video_name):
        imgs = [img for img in os.listdir(img_folder)]
        frame = cv2.imread(os.path.join(img_folder, imgs[0]))
        height, width, layers = frame.shape
        video = cv2.VideoWriter(video_name, 0, 1, (width, height))

        for image in imgs:
            video.write(cv2.imread(os.path.join(img_folder, image)))
        cv2.destroyAllWindows()
        video.release()

    if not os.path.isfile(fileid):
        log.info('Создание zip файла - %s', fileid)
        with ZipFile(fileid, mode='w', compression=ZIP_DEFLATED) as misfile:
            misfile.write(video_name)


def f_dir(d, p, od):
    log.info('Сканирование директории для исследования - %s', d)
    remove_ds_store = [name for name in os.listdir(d) if not name.startswith(('.', 'ORG'))]
    sort_list = sorted(remove_ds_store)
    log.info('Найдено %s образца', len(sort_list))

    log.info('Поиск центроидов начат')
    for num, path in enumerate(sort_list):
        # ЧБ
        path = d + path
        image = color.rgb2gray(io.imread(path))

        # calculate
        fast = image.max() - p
        # load
        raze = image <= fast
        image = np.where(raze, 0, image)
        gosh = np.where(image >= fast)

        km(image, number=num, g=gosh, dr=od)
        # plt.scatter(gosh[0], gosh[1], color='red')
        # plt.show()
        # if num == 3:
        #     break
    log.info('Поиск центроидов окончен')


# config directory, files and etc.
directory = "2020-2/A4 98 um 20200325/"
output_dir = 'k1'

log.info('Директория для исследования - %s', directory)
log.info('Директория для выходных изображений - %s', output_dir)
f_dir(d=directory, p=0.2, od=output_dir)

log.info('Началась генерация видео')
gen_video()
log.info('Окончена генерация видео')
