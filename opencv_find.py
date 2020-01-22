import cv2 as cv
import numpy as np


img = cv.imread('konstantin/2019.10.02 ФИ-59/2019.10.02_actReg/2019.10.02_4/B4 97_ac.png')
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
gray = cv.GaussianBlur(gray, (3, 3), 0)
cv.imwrite("gray.jpg", gray)

edged = cv.Canny(gray, 10, 250)
cv.imwrite("edged.jpg", edged)

kernel = cv.getStructuringElement(cv.MORPH_RECT, (7, 7))
closed = cv.morphologyEx(edged, cv.MORPH_CLOSE, kernel)
cv.imwrite("closed.jpg", closed)

cnts = cv.findContours(closed.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)[1]
total = 0

# цикл по контурам
for c in cnts:
    # аппроксимируем (сглаживаем) контур
    peri = cv.arcLength(c, True)
    approx = cv.approxPolyDP(c, 0.02 * peri, True)

    # если у контура 4 вершины, предполагаем, что это книга
    if len(approx) == 4:
        cv.drawContours(img, [approx], -1, (0, 255, 0), 4)
        total += 1

print("Я нашёл {0} книг на этой картинке".format(total))
cv.imwrite("output.jpg", img)