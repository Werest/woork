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
    print(first, "//", two)
    r = first / two
    result = math.sqrt(r)
    return result

def c1(image, number):
    X0 = 0
    Y0 = 0
    step = 0.01
    fig, (ax, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(8, 3),
                                  sharex=True, sharey=True)
    ax.axis('on')
    ax2.axis('on')

    ax.imshow(image)

    ind = np.where(image >= 0.9)

    X = ind[0]
    Y = ind[1]

    sumEx = 0.0
    sumEy = 0.0

    eps = 0.001
    d = True
    flag = 0
    iii = 0
    while d:
        if flag == 0:
            for j in Y:
                for i in X:
                    sumEx = sumEx + Ex(X0, i, Y0, j, label=0)
            Y0 = X0 - step * sumEx
            flag = 1
            # if math.fabs(sumEx) < eps:
            #     d = False
            print('Y0', Y0)
        else:
            for j in X:
                for i in Y:
                    sumEy = sumEy + Ex(X0, i, Y0, j, label=1)
            X0 = Y0 - step * sumEy
            flag = 0
            # if math.fabs(sumEy) < eps:
            #     d = False
            print('X0', X0)

        ax2.plot(X0, Y0, marker='x', markersize='20')

    # Y, X
        ax2.imshow(image)
        plt.savefig('hh/{}'.format(iii))
        iii = iii + 1


path_img = 'konstantin/2019.10.21 ФИ-65/2019.10.21_actReg/A7 76_ac.png'
path_img_v = 'konstantin/2019.10.02 ФИ-59/2019.10.02_actReg/2019.10.02_5/B5 97_an.png'

image = color.rgb2gray(io.imread(path_img))
image_v = color.rgb2gray(io.imread(path_img_v))
image = cv2.blur(image, (3, 3))
x0 = 10
y0 = 10

print(image.shape)
c1(image, 50)
