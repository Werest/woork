from skimage import io, measure, color, feature
import cv2
import matplotlib.pyplot as plt
import numpy as np
import math
from scipy.misc import derivative
import pandas as pd

# + math.pow((y - yc), 2) + math.pow((brightness - 1), 2)
# размеры картинки в микронах 1214,6x1214,6 мкм
def Jx(x):
    return math.sqrt(math.pow((x - x0), 2))
# подумать
def Jy(y):
    return math.sqrt(math.pow((y - y0), 2))

def Jbt(brightness):
    return math.sqrt(math.pow((brightness - 1), 2))

def beggin():
    global x0, y0, step
    x0 = 114
    y0 = 0
    step = 0.1
    pass


# def new_x_y(xxx, yyy):
#     xn = xxx - step * derivative(J, xxx)
#     yn = yyy - step * derivative(J, yyy)
#     return xn


# условная функция рассчёта евклидово расстояния
# cluster_of_points - скопление точек
def calc(image, index_cluster_of_points):
    beggin()
    print(x0)
    print("De", derivative(Jx, 200))
    index_cluster_of_points = np.array(index_cluster_of_points)
    array_J = np.zeros((image.shape[0], image.shape[1]))

    x = index_cluster_of_points[0][0]
    y = index_cluster_of_points[1][0]

    print(image[x, y])

    uri = []

    for i in index_cluster_of_points[0]:
        for j in index_cluster_of_points[1]:
            brigh = image[i, j]
            E = math.sqrt(math.pow((i - 140), 2) + math.pow((j - 130), 2) + math.pow((brigh - 1), 2))
            uri.append(E)

    print(np.argmin(uri))
    print(np.amin(uri))

    # for i in range(0, image.shape[0]):
    #     for j in range(0, image.shape[1]):
    #         sum_xc_yc = 0.0
    #         print(i, "//", j)
    #         for r in index_cluster_of_points[0]:
    #             for u in index_cluster_of_points[1]:
    #                 X_c = i
    #                 Y_c = j
    #
    #                 X_1 = r
    #                 Y_1 = u
    #
    #                 brightness_0 = image[X_1, Y_1]
    #
    #                 sum_xc_yc += math.pow((X_1 - X_c), 2) + math.pow((Y_1 - Y_c), 2) + math.pow((brightness_0 - 1), 2)
    #
    #
    #         array_J[i, j] = math.sqrt(sum_xc_yc)
    #
    # m_J = np.amin(array_J)
    # print(np.where(array_J == m_J))
    # print(m_J)

    pass


def c1(image, number):
    fig, (ax, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(8, 3),
                                  sharex=True, sharey=True)
    ax.axis('on')
    ax2.axis('on')

    ax.imshow(image)

    ind = np.where(image >= 0.9)
    # print(ind)
    # Y, X
    ax2.imshow(image)
    plt.savefig('k/{}'.format(number))
    calc(image, ind)


path_img = 'konstantin/2019.10.21 ФИ-65/2019.10.21_actReg/A7 76_ac.png'
path_img_v = 'konstantin/2019.10.02 ФИ-59/2019.10.02_actReg/2019.10.02_5/B5 97_an.png'

image = color.rgb2gray(io.imread(path_img))
image_v = color.rgb2gray(io.imread(path_img_v))
image = cv2.blur(image, (3, 3))

print(image.shape)
c1(image, 50)
