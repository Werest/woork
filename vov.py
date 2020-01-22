from PIL import Image
from skimage import color, io, measure, feature, img_as_ubyte, img_as_float64
import matplotlib.pyplot as plt
import numpy as np

path_img = 'konstantin/2019.10.02 ФИ-59/2019.10.02_actReg/2019.10.02_5/A5 96_ac.png'
path_img_v = 'konstantin/2019.10.02 ФИ-59/2019.10.02_actReg/2019.10.02_5/A5 96_an.png'

image = img_as_ubyte(color.rgb2gray(io.imread(path_img)))
image_v = img_as_ubyte(color.rgb2gray(io.imread(path_img_v)))

print(image.shape)
print(image_v.shape)


opppo = image_v-image


io.imsave('2.png', opppo)


img = io.imread("2.png")
print(img.dtype)
countours = measure.find_contours(img, level=0.1)


fig, ax = plt.subplots()
ax.imshow(img, cmap=plt.cm.gray)

for n, contour in enumerate(countours):
    ax.plot(contour[:, 1], contour[:, 0], linewidth=2)

ax.axis('image')
ax.set_xticks([])
ax.set_yticks([])
plt.show()

