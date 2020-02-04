from skimage import io, measure, color, feature
import cv2
import matplotlib.pyplot as plt
import numpy as np
import math


# размеры картинки в микронах 1214,6x1214,6 мкм
def Ex(x, xc, y, yc, label):
    first = 0.0
    if label == 0:
        first = x - xc
    else:
        first = y - yc
    two = math.pow((x - xc), 2) + math.pow((y - yc), 2)
    r = first / math.sqrt(two)
    return r


def search_countrs(image, level):
    fig, (ax, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(8, 3),
                                       sharex=True, sharey=True)
    ax.axis('on')
    ax2.axis('on')

    ax.imshow(image)

    counts = measure.find_contours(image, level)

    Xc = np.random.randint(50, 100, len(counts))
    Yc = np.random.randint(50, 100, len(counts))

    X, Y = 50, 50
    for i in range(len(Xc)):
        X, Y = c1(Xc[i], Yc[i], counts[i][:, 0], counts[i][:, 1])
        ax2.plot(X, Y, marker='x', markersize='10')
        print('X0', X, '//', 'Y0', Y)

    ax2.imshow(image)

    plt.savefig('k/50')


# Xc, Yc - координаты центроида
def c1(Xc, Yc, ind_c_x=None, ind_c_y=None):
    # image[np.array(ind_c_x.astype(int)), np.array(ind_c_y.astype(int))]

    step = 0.01

    X = ind_c_x.astype(int)
    Y = ind_c_y.astype(int)

    X0 = Xc
    Y0 = Yc

    d = True
    flag = 0
    while d:
        sumEx = 0.0
        xxx = X0
        yyy = Y0
        if flag == 0:
            for i in range(0, len(X)):
                sumEx = sumEx + Ex(X[i], X0, Y[i], Y0, label=0)
            X0 = X0 + step * sumEx
            flag = 1
            if int(X0) == int(xxx):
                d = False
        else:
            for i in range(0, len(X)):
                sumEx = sumEx + Ex(X[i], X0, Y[i], Y0, label=1)
            Y0 = Y0 + step * sumEx
            flag = 0
            if int(Y0) == int(yyy):
                d = False
    return X0, Y0


path_img = 'konstantin/2019.10.02 ФИ-59/2019.10.02_actReg/2019.10.02_7/B7 97_ac.png'

image = color.rgb2gray(io.imread(path_img))
image = cv2.blur(image, (3, 3))
x0 = 10
y0 = 10

search_countrs(image, 0.8)
