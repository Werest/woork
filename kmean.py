import cv2
from skimage import color
from skimage import io
from skimage import measure
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
import numpy as np
import os


def kmeans(image, level, num):
    fig, (ax, ax1) = plt.subplots(nrows=1, ncols=2, figsize=(8, 3))
    ax.axis('on')

    ax.imshow(image)
    ax1.imshow(image)

    counts = measure.find_contours(image, level)
    for n, contour in enumerate(counts):
        ax.plot(contour[:, 1], contour[:, 0], linewidth=2)

    yc = []
    xc = []
    for n, contour in enumerate(counts):
        for c in contour:
            yc.append(int(c[1]))
            xc.append(int(c[0]))
            # bt.append(image[int(c[0]), int(c[1])])

    z = [list(hhh) for hhh in zip(xc, yc)]
    k = KMeans(n_clusters=len(counts), random_state=0, n_init=100).fit(z)
    ax.plot(k.cluster_centers_[:, 1], k.cluster_centers_[:, 0], marker='+', markersize='5')

    plt.savefig('k/{}'.format(num))


path_img = 'konstantin/2019.10.02 ФИ-59/2019.10.02_actReg/2019.10.02_3/B3 97_ac.png'

image = color.rgb2gray(io.imread(path_img))
image = cv2.blur(image, (3, 3))
kmeans(image, level=0.2, num=556)

# files = os.listdir('Attachments_lalv@yandex')
# for num, ftf in enumerate(files):
#     opa = 'Attachments_lalv@yandex/' + ftf
#     image = color.rgb2gray(io.imread(opa))
#     image = cv2.blur(image, (3, 3))
#     kmeans(image, level=0.92, num=num)
