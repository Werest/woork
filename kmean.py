import cv2
from skimage import color
from skimage import io
from skimage import measure
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np
import os


def kmeans(image, level, num):
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(8, 3))
    ax.axis('on')

    ax.imshow(image)

    ind = np.where(image >= 0.9)
    z = [list(hhh) for hhh in zip(ind[0], ind[1])]
    # print(z)

    counts = measure.find_contours(image, level)
    for n, contour in enumerate(counts):
        ax.plot(contour[:, 1], contour[:, 0], linewidth=2)

    # k = KMeans(n_clusters=len(counts), random_state=0, n_init=100).fit(z)
    # print(k.cluster_centers_)
    # ax.plot(k.cluster_centers_[:, 1], k.cluster_centers_[:, 0], marker='x', markersize='5')

    plt.savefig('k/{}'.format(num))

path_img = 'konstantin/2019.10.02 ФИ-59/2019.10.02_actReg/2019.10.02_13/B13 97_ac.png'

files = os.listdir('Attachments_lalv@yandex')
for num, ftf in enumerate(files):
    opa = 'Attachments_lalv@yandex/' + ftf
    image = color.rgb2gray(io.imread(opa))
    image = cv2.blur(image, (3, 3))
    kmeans(image, level=0.7, num=num)


