import cv2
import numpy as np
import random as rng

rng.seed(12345)


def thresh_callback(val):
    threshold = val
    # Detect edges using Canny
    canny_output = cv2.Canny(im_gray, threshold, threshold * 2)
    # Find contours
    _, contours, hierarchy = cv2.findContours(canny_output, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # Draw contours
    drawing = np.zeros((canny_output.shape[0], canny_output.shape[1], 3), dtype=np.uint8)
    for i in range(len(contours)):
        color = (rng.randint(0, 256), rng.randint(0, 256), rng.randint(0, 256))
        cv2.drawContours(drawing, contours, i, color, 2, cv2.LINE_8, hierarchy, 0)
    # Show in a window
    cv2.imshow('Contours', drawing)


path_img = 'konstantin/2019.10.22 ФИ-66/2019.10.22_actReg/A2 117_ac.png'

image = cv2.imread(path_img)
if image is None:
    print('Could not open or find the image: {}'.format(path_img))
    exit(0)

im_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
im_gray = cv2.blur(im_gray, (3, 3))

cv2.imshow('GRAY', im_gray)

threshold=100
canny_output = cv2.Canny(im_gray, threshold, threshold * 2)


cv2.waitKey()
