from skimage import color
from skimage import io
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import os
import pymysql
import numpy as np


def km(img, number, g):
    plt.cla()
    plt.clf()
    fig, (ax, ax1) = plt.subplots(nrows=1, ncols=2, figsize=(8, 3))
    ax.axis('on')

    ax.imshow(img)
    ax1.imshow(img)

    x = g[0]
    y = g[1]
    # Если имеется массив центроидов
    if len(x) > 0 and len(y) > 0:
        z = [list(hhh) for hhh in zip(x, y, img[x, y])]
        k = KMeans(n_clusters=3).fit(z)
        x_t = list(k.cluster_centers_[:, 0])
        y_t = list(k.cluster_centers_[:, 1])
        ax.scatter(y_t, x_t, s=5, c='red')
        print("Центроиды: \n", k.cluster_centers_)
        plt.savefig('k1/{}'.format(number))
        plt.close(fig)
    else:
        print("Не можем определить центроиды")


connection = pymysql.connect(host='localhost',
                             user='newuser',
                             password='PASSWORD',
                             db='dbo',
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)


def f_dir(d, p):
    remove_ds_store = [name for name in os.listdir(d) if not name.startswith('.')]
    sort_list = sorted(remove_ds_store)

    for num, path in enumerate(sort_list):
        # ЧБ
        path = d + path
        image = color.rgb2gray(io.imread(path))
        raize = image <= (image.max() - p)
        image = np.where(raize, 0, image)
        gosh = np.where(image >= (image.max() - p))
        km(image, number=num, g=gosh)
        plt.scatter(gosh[0], gosh[1], color='red')
        plt.show()
        if num == 20:
            break


directory = "2020-2/A4 98 um 20200325/"
f_dir(directory, 0.1)
