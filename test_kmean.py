import csv
from unittest import TestCase

import cv2
from skimage import color
from skimage import io
from pandas import DataFrame


class Test(TestCase):
    def test_sql_(self):
        file = '2020-2/A4 98_ac.png'
        image = color.rgb2gray(io.imread(file))
        image = cv2.blur(image, (3, 3))
        pd = DataFrame(image)
        pd.to_csv('1.csv', index=False)
        from kmean import km
        km(image, level_=(image.max() - 0.5), number=1021110212121)
