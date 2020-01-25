from skimage import io, measure, color, feature
import cv2
import matplotlib.pyplot as plt
import numpy as np
import math
import pandas as pd


# размеры картинки в микронах 1214,6x1214,6 мкм


def J(x, xc, y, yc, brightness):
    sum = math.pow((x - xc), 2) + math.pow((y - yc), 2) + math.pow((brightness - 1), 2)
    J = math.sqrt(sum)
    return J


def c1(image, number):
    global x0, y0
    fig, (ax, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(8, 3),
                                  sharex=True, sharey=True)
    countours = measure.find_contours(image, level=0.7, fully_connected='high', positive_orientation='high')

    # for n, countours in enumerate(countours):
    #     ax.plot(countours[:, 1], countours[:, 0], linewidth=2)

    ax.axis('on')
    ax2.axis('off')

    ax.imshow(image)

    max_el = np.amax(image)
    ind = np.where(image >= 0.9)
    # Y, X
    for i in ind[0]:
        for j in ind[1]:
            image[i, j] = 0.1

    ax2.imshow(image)



    plt.savefig('k/{}'.format(number))
    # plt.show()


# for i in range(2, 8):
path_img = 'konstantin/2019.10.21 ФИ-65/2019.10.21_actReg/A7 76_ac.png'
path_img_v = 'konstantin/2019.10.02 ФИ-59/2019.10.02_actReg/2019.10.02_5/B5 97_an.png'

image = color.rgb2gray(io.imread(path_img))
image_v = color.rgb2gray(io.imread(path_img_v))
image = cv2.blur(image, (3, 3))
x0 = 10
y0 = 10

print(image.shape)
c1(image, 50)
