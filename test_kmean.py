from unittest import TestCase

import cv2
from skimage import color
from skimage import io


class Test(TestCase):
    def test_sql_(self):
        file = 'konstantin/2019.11.18 ФИ-73/2019.11.18_actReg/2019.11.18_12/A12 103_ac.png'
        image = color.rgb2gray(io.imread(file))
        image = cv2.blur(image, (3, 3))
        from kmean import kmeans
        kmeans(image, level_=(image.max() - 0.1), number=909010)
