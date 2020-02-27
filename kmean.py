import cv2
from skimage import color
from skimage import io
from skimage import measure
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
import numpy as np
import os


def kmeans(imagep, level_, num):
    fig, (ax, ax1) = plt.subplots(nrows=1, ncols=2, figsize=(8, 3))
    ax.axis('on')

    ax.imshow(imagep)
    ax1.imshow(imagep)

    ci = measure.find_contours(imagep, level_)

    yc = []
    xc = []
    bt = []
    for n, contour in enumerate(ci):
        for c in contour:
            yc.append(int(c[1]))
            xc.append(int(c[0]))
            bt.append(imagep[int(c[0]), int(c[1])])

    if len(xc) > 0 and len(yc) > 0:
        z = [list(hhh) for hhh in zip(xc, yc, bt)]
        k = KMeans(n_clusters=len(ci), n_init=20).fit(z)
        ax.plot(k.cluster_centers_[:, 1], k.cluster_centers_[:, 0], marker='+', markersize='5')
        print("Центроиды: \n", k.cluster_centers_)
        plt.savefig('k/{}'.format(num))
    else:
        print("Не можем определить центроды")


path_img = "konstantin/2019.12.20 ФИ-80/2019.12.20_actReg/2019.12.20_16/A16 111_ac.png"

image = color.rgb2gray(io.imread(path_img))
image = cv2.blur(image, (5, 5))
kmeans(image, level_=0.8, num=559)

# files = os.listdir('Attachments_lalv@yandex')
# for num, ftf in enumerate(files):
#     opa = 'Attachments_lalv@yandex/' + ftf
#     image = color.rgb2gray(io.imread(opa))
#     image = cv2.blur(image, (3, 3))
#     kmeans(image, level=0.92, num=num)
