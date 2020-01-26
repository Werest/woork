from skimage import io, measure, color, feature
import cv2
import matplotlib.pyplot as plt
import numpy as np
import math


# размеры картинки в микронах 1214,6x1214,6 мкм
def J(x, xc, y, yc, brightness):
    sum = math.pow((x - xc), 2) + math.pow((y - yc), 2) + math.pow((brightness - 1), 2)
    J = math.sqrt(sum)
    return J

# условная функция рассчёта евклидово расстояния
def calc(image):
    X_c = 10
    Y_c = 10

    X_1 = 140
    Y_1 = 114

    brightness_0 = image[X_1, Y_1]

    J_F = J(X_1, X_c, Y_1, Y_c, brightness_0)
    print(J_F)

    pass

def c1(image, number):
    global x0, y0
    fig, (ax, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(8, 3),
                                  sharex=True, sharey=True)
    ax.axis('on')
    ax2.axis('off')

    ax.imshow(image)

    ind = np.where(image >= 0.9)
    # print(ind)
    # Y, X
    ax2.imshow(image)
    plt.savefig('k/{}'.format(number))
    calc(image)

path_img = 'konstantin/2019.10.21 ФИ-65/2019.10.21_actReg/A7 76_ac.png'
path_img_v = 'konstantin/2019.10.02 ФИ-59/2019.10.02_actReg/2019.10.02_5/B5 97_an.png'

image = color.rgb2gray(io.imread(path_img))
image_v = color.rgb2gray(io.imread(path_img_v))
image = cv2.blur(image, (3, 3))
x0 = 10
y0 = 10

print(image.shape)
c1(image, 50)
