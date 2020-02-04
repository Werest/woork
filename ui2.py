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

def c1(image, number):
    X0 = 50
    Y0 = 50
    step = 0.01
    counts = measure.find_contours(image, 0.8)
    print(counts)

    fig, (ax, ax2, ax3) = plt.subplots(nrows=1, ncols=3, figsize=(8, 3),
                                  sharex=True, sharey=True)

    ax.axis('on')
    ax2.axis('on')

    ax3.imshow(image)
    for n, contour in enumerate(counts):
        ax3.plot(contour[:, 1], contour[:, 0], linewidth=2)

    ax.imshow(image)
    ind = np.where(image >= 0.9)

    X = ind[0]
    Y = ind[1]

    # eps = 0.001
    d = True
    flag = 0
    iii = 0
    while d:
        sumEx = 0.0
        xxx = X0
        yyy = Y0
        if flag == 0:
            for i in range(0, len(X)):
                sumEx = sumEx + Ex(X[i], X0, Y[i], Y0, label=0)
            print(sumEx)
            X0 = X0 + step * sumEx
            flag = 1
            if int(X0) == int(xxx):
                d = False
            print('X0', X0, '//', xxx)
        else:
            for i in range(0, len(X)):
                sumEx = sumEx + Ex(X[i], X0, Y[i], Y0, label=1)
            Y0 = Y0 + step * sumEx
            print(sumEx)
            flag = 0
            if int(Y0) == int(yyy):
                d = False
            print('Y0', Y0, '//', yyy)
        iii = iii + 1

    ax2.imshow(image)
    ax2.plot(X0, Y0, marker='x', markersize='10')


    print('Итераций прошло:', iii)
    plt.plot(X0, Y0, marker='x', markersize='10')
    plt.savefig('k/50')


path_img = 'konstantin/2019.10.02 ФИ-59/2019.10.02_actReg/2019.10.02_3/B3 97_ac.png'
path_img_v = 'konstantin/2019.10.02 ФИ-59/2019.10.02_actReg/2019.10.02_5/B5 97_an.png'

image = color.rgb2gray(io.imread(path_img))
image_v = color.rgb2gray(io.imread(path_img_v))
image = cv2.blur(image, (3, 3))
x0 = 10
y0 = 10

print(image.shape)
c1(image, 50)
