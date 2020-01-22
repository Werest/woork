from skimage import color, io
import matplotlib.pyplot as plt
import numpy as np

path_img = 'konstantin/2019.10.02 ФИ-59/2019.10.02_actReg/2019.10.02_5/B5 97_an.png'

image = io.imread(path_img)
img_to_gray = color.rgb2gray(image)

print(img_to_gray.shape)

# img_to_gray[:,:,1] = 0

fig, ax = plt.subplots()
ax.imshow(img_to_gray, cmap=plt.cm.gray)

ax.axis('image')
ax.set_xticks([])
ax.set_yticks([])
plt.savefig("color_gray_o")
plt.show()

