import cv2
from skimage import color
from skimage import io
from skimage import measure
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np


def kmeans(image, level):
    fig, (ax, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(8, 3),
                                  sharex=True, sharey=True)
    ax.axis('on')
    ax2.axis('on')

    ax.imshow(image)

    ind = np.where(image >= 0.9)

    counts = measure.find_contours(image, level)
    for n, contour in enumerate(counts):
        ax.plot(contour[:, 1], contour[:, 0], linewidth=2)

    k = KMeans(n_clusters=1, random_state=0, n_init=10).fit(ind)
    # print(k.cluster_centers_)
    ax2.plot(k.cluster_centers_[:, 0], k.cluster_centers_[:, 1], marker='x', markersize='5')
    ax2.imshow(image)
    plt.savefig('k/50')

path_img = 'konstantin/2019.10.30 ФИ-70/2019.10.30_15/A15 94_ac.png'

image = color.rgb2gray(io.imread(path_img))
image = cv2.blur(image, (3, 3))
kmeans(image, level=0.8)
