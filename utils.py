import sys
from PyQt5.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsRectItem, QMainWindow, QLabel, \
    QGraphicsItem, QGraphicsEllipseItem

from PyQt5.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsRectItem, QMainWindow, QLabel, \
    QGraphicsItem, QGraphicsEllipseItem, QGraphicsPixmapItem, QGraphicsLineItem
from PyQt5.QtCore import Qt, pyqtSignal, QPoint, QRectF, QRect
# from UI.Qmygraphicview import QMyGraphicsView
# from UI.QItem import My_GraphicItem
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import QtWidgets
from PIL import Image
import numpy as np
import cv2
from PyQt5.QtGui import QImage, QPixmap
import pyqtgraph
from PyQt5.QtGui import QPainter, QPen, QColor
from Myscene import GraphicScene
from Myview import GraphicView

def cv_draw_landmark(img, pts, color=(0, 0, 255), size=2, save_path='./result.jpg'):
    for i in range(pts.shape[0]):
        cv2.circle(img, (int(round(pts[i, 0])), int(round(pts[i, 1]))), size, color, -1)
        cv2.putText(img, str(i), (int(round(pts[i, 0]) - 3), int(round(pts[i, 1]) - 3)), cv2.FONT_HERSHEY_COMPLEX, 0.4,
                    (255, 0, 0), 1)
    I = Image.fromarray(img)
    I = I.resize((2048, 2048))
    I.save(save_path)
    return I

def test_lm(npy_path, image_path):
    data = np.load(npy_path, allow_pickle=True)
    I = Image.open(image_path).convert('RGB')
    img = np.array(I)
    height = img.shape[0]
    width = img.shape[1]
    ratio = float(height / width)
    target_size = 600
    if height > width:
        new_height = target_size
        new_width = int(target_size / ratio)
    else:
        new_height = int(target_size / ratio)
        new_width = target_size
    face_np = cv2.resize(img, (new_width, new_height))
    i = cv_draw_landmark(img=face_np, pts=data)
    i.show()
