import csv
from unittest import TestCase

import cv2
from skimage import color
from skimage import io
from pandas import DataFrame


class Test(TestCase):
    def test_sql_(self):
        file = 'konstantin/2019.10.30 ФИ-70/2019.10.30_15/B15 105_ac.png'
        image = color.rgb2gray(io.imread(file))
        image = cv2.blur(image, (3, 3))
        pd = DataFrame(image)
        pd.to_csv('1.csv', index=False)
        from kmean import kmeans
        kmeans(image, level_=(image.max() - 0.5), number=909010)
