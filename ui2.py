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

    d_x, d_y = True, True
    flag = 0
    eps = 0.01
    while d_x or d_y:
        sum_ex = 0.0
        xxx = Xc
        yyy = Yc
        if flag == 0:
            for i in range(0, len(X)):
                sum_ex = sum_ex + Ex(X[i], Xc, Y[i], Yc, label=0)
                Xc = Xc - step * sum_ex
            if d_y:
                flag = 1
            else:
                flag = 0
            if math.fabs(Xc-xxx) < eps:
                d_x = False
        elif flag == 1:
            for i in range(0, len(X)):
                sum_ex = sum_ex + Ex(X[i], Xc, Y[i], Yc, label=1)
                Yc = Yc - step * sum_ex
            if d_x:
                flag = 0
            else:
                flag = 1
            if math.fabs(Yc-yyy) < eps:
                d_y = False
        print('X', Yc-xxx, 'Y', Yc-yyy)
    return Xc, Yc


path_img = 'konstantin/2019.10.24 ФИ-68/2019.10.24_actReg/A3 97_ac.png'

image = color.rgb2gray(io.imread(path_img))
image = cv2.blur(image, (3, 3))
x0 = 10
y0 = 10

search_countrs(image, 0.8)
