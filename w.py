from skimage import io, measure, color, feature
import cv2
import matplotlib.pyplot as plt
import numpy as np
import math
from scipy.spatial import distance

# размеры картинки в микронах 1214,6x1214,6 мкм

def c1(image, number):
    countours = measure.find_contours(image, level=0.7, fully_connected='high', positive_orientation='high')
    countours1 = feature.canny(image, sigma=10)

    fig, (ax, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(8, 3),
                                  sharex=True, sharey=True)
    ax.imshow(image)
    ax2.imshow(countours1, cmap=plt.cm.gray)
    ax2.axis('off')

    for c in countours:
        Xmin = np.amin(c[:, 0])
        Xmax = np.amax(c[:, 0])

        Ymin = np.amin(c[:, 1])
        Ymax = np.amax(c[:, 1])

        Xx = [Xmin, Xmax]
        Yy = [Ymin, Ymax]
        dst_scipy = distance.euclidean(Xx, Yy)

        dst = (Xmax-Xmin)+(Ymax-Ymin)
        dst = dst**2
        dst = math.sqrt(dst)

        ax.plot(Ymin, Xmin, marker='o')
        ax.plot(Ymin, Xmin, marker='o')

        print("Евклид=", dst, "//", dst_scipy)


    for n, countours in enumerate(countours):
        ax.plot(countours[:, 1], countours[:, 0], linewidth=2)

    ax.axis('image')
    ax.set_xticks([])
    ax.set_yticks([])

    plt.savefig('k/{}'.format(number))
    # plt.show()

# for i in range(2, 8):
path_img = 'konstantin/2019.10.02 ФИ-59/2019.10.02_actReg/2019.10.02_3/B3 97_ac.png'
path_img_v = 'konstantin/2019.10.02 ФИ-59/2019.10.02_actReg/2019.10.02_5/B5 97_an.png'

image = color.rgb2gray(io.imread(path_img))
image_v = color.rgb2gray(io.imread(path_img_v))
image = cv2.blur(image, (3, 3))

c1(image, 50)
