import cv2
from skimage import color
from skimage import io
from skimage import measure
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import os
import pymysql
import numpy as np


def kmeans(imagep, level_, number):
    plt.cla()
    plt.clf()
    fig, (ax, ax1) = plt.subplots(nrows=1, ncols=2, figsize=(8, 3))
    ax.axis('on')

    ax.imshow(imagep)
    ax1.imshow(imagep)

    # Поиск контуров по уровню (пределу)
    ci = measure.find_contours(imagep, level_)

    # X и Y центроида bt - яркость
    yc = []
    xc = []
    bt = []
    for n, contour in enumerate(ci):
        for c in contour:
            yc.append(int(c[1]))
            xc.append(int(c[0]))
            bt.append(imagep[int(c[0]), int(c[1])])

    # Если имеется массив центроидов
    if len(xc) > 0 and len(yc) > 0:
        z = [list(hhh) for hhh in zip(xc, yc, bt)]
        k = KMeans(n_clusters=len(ci), n_init=20).fit(z)
        x_t = list(k.cluster_centers_[:, 0])
        y_t = list(k.cluster_centers_[:, 1])
        ax.scatter(y_t, x_t, s=5, c='red')
        print("Центроиды: \n", k.cluster_centers_)
        plt.savefig('k/{}'.format(number))
        plt.close(fig)
    else:
        print("Не можем определить центроиды")


connection = pymysql.connect(host='localhost',
                             user='newuser',
                             password='PASSWORD',
                             db='dbo',
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)


def sql():
    try:
        with connection.cursor() as cursor:
            sql = "call dbo.get_File();"
            cursor.execute(sql)
            result = cursor.fetchall()
            for j, res in enumerate(result):
                file = 'konstantin' + result[j]['name_file']
                if os.path.exists(file):
                    sp = file.split('/')
                    for i, k in enumerate(sp[:-1]):
                        sp[i] = sp[i] + '_'
                    name_finally = ''.join(sp[1:])
                    image = color.rgb2gray(io.imread(file))
                    image = cv2.blur(image, (3, 3))
                    kmeans(image)
                    kmeans(image, level_=(image.min() + 0.1), number=name_finally)
    finally:
        connection.close()


# sql()
