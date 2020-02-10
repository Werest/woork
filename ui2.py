from skimage import io, measure, color, feature
import cv2
import matplotlib.pyplot as plt
import numpy as np
import math


# размеры картинки в микронах 1214,6x1214,6 мкм
def Ex(x, xc, y, yc, label):
    if label == 0:
        first = x - xc
    else:
        first = y - yc
    two = math.pow((x - xc), 2) + math.pow((y - yc), 2)
    r = first / math.sqrt(two)
    return r


def Ex_simple(x, xc, y, yc):
    two = math.pow((x - xc), 2) + math.pow((y - yc), 2)
    r = math.sqrt(two)
    return r


def search_co(image, level):
    fig, (ax, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(8, 3),
                                  sharex=True, sharey=True)
    ax.axis('on')
    ax2.axis('on')

    ax.imshow(image)

    counts = measure.find_contours(image, level)

    Xc = np.random.randint(50, 100, len(counts))
    Yc = np.random.randint(50, 100, len(counts))

    for i in range(len(Xc)):
        X, Y = c1(Xc[i], Yc[i], counts[i][:, 0], counts[i][:, 1])
        ax2.plot(X, Y, marker='x', markersize='5')
        print('X0', X, '//', 'Y0', Y)

    ax2.imshow(image)

    plt.savefig('k/50')


# Xc, Yc - координаты центроида
def c1(Xc, Yc, ind_c_x=None, ind_c_y=None):
    # image[np.array(ind_c_x.astype(int)), np.array(ind_c_y.astype(int))]
    global Xc_last, Yc_last
    step = 0.01

    X = ind_c_x.astype(int)
    Y = ind_c_y.astype(int)

    eps = 0.01
    mistake_x = []
    mistake_y = []
    while True:
        Xc_last = Xc
        Yc_last = Yc
        for i in range(len(X)):
            sumex = Ex(X[i], Xc, Y[i], Yc, label=0)
            Xc = Xc - step * sumex
            sumex = Ex(X[i], Xc, Y[i], Yc, label=1)
            Yc = Yc - step * sumex

        mistake_x.append(math.fabs(Xc - Xc_last))
        mistake_y.append(math.fabs(Yc - Yc_last))

        if len(mistake_x) > 1:
            print(mistake_x)
            print(mistake_x[1] - mistake_x[0])
            break

        # if math.fabs(Xc - Xc_last) < eps or math.fabs(Yc - Yc_last) < eps:
        #     print(math.fabs(Xc - Xc_last), "//", math.fabs(Yc - Yc_last))
        #     break
        # else:
        #     print(math.fabs(Xc - Xc_last), "//", math.fabs(Yc - Yc_last))
    return Xc, Yc


path_img = 'konstantin/2019.10.24 ФИ-68/2019.10.24_actReg/A3 97_ac.png'

image = color.rgb2gray(io.imread(path_img))
image = cv2.blur(image, (3, 3))

search_co(image, 0.8)
