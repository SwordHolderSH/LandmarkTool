import sys
from PyQt5.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsRectItem, QMainWindow, QLabel, \
    QGraphicsItem, QGraphicsEllipseItem

from PyQt5.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsRectItem, QMainWindow, QLabel, \
    QGraphicsItem, QGraphicsEllipseItem, QGraphicsPixmapItem, QGraphicsLineItem
from PyQt5.QtCore import Qt, pyqtSignal, QPoint, QRectF, QRect, QPointF
# from UI.Qmygraphicview import QMyGraphicsView
# from UI.QItem import My_GraphicItem
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import QtWidgets
from PIL import Image
import numpy as np
import cv2
from PyQt5.QtGui import QImage, QPixmap
import utils


class MyAction:
    def __init__(self, opt):
        super().__init__()
        self.window = opt

    def show_pos(self):
        # point = self.window.main_image.pos()
        r = 10  # 关键点直径
        main_image = self.window.main_image
        pos_img = main_image.pos()
        pos_img_scene = self.window.view.mapFromScene(pos_img)
        pos_img_scene = [pos_img_scene.x(), pos_img_scene.y()]
        # main_image_pos = main_image.boundingRect()
        name = ['face', 'left_eyebrow', 'right_eyebrow', 'nose_bridge', 'nose', 'left_eye', 'right_eye', 'mouth']
        # rb = face_landmarks[]
        # re = face_landmarks['right_eye']
        # nose = face_landmarks['nose']
        # nb = face_landmarks['nose_bridge']
        # nt = face_landmarks['nose_tip']]
        key_pos_list_total = []
        for a_facial_feature in self.window.view.key_point_list_total:
            a_facial_feature_pos = []
            for point in a_facial_feature:
                # pos = point.boundingRect().center()
                # pos = point.X()
                pos = point.pos()
                pos_scene = self.window.view.mapFromScene(pos)
                pos_scene = pos_scene
                # pos = point.boundingRect().center()
                # pos = self.window.view.mapFromScene(pos)
                # pos = point.boundingRect().center()
                # pos_np = [pos_scene.x(), pos_scene.y()]
                pos_np = [pos_scene.x() - pos_img_scene[0] + r / 2, pos_scene.y() - pos_img_scene[1] + r / 2]
                a_facial_feature_pos.append(pos_np)
            key_pos_list_total.append(a_facial_feature_pos)
        print(key_pos_list_total)
        self.landmark68 = []
        for lm in key_pos_list_total:
            self.landmark68 = self.landmark68 + lm
        print("Total {} landmarks! ==========================".format(len(self.landmark68)))
        d = zip(name, key_pos_list_total)
        self.key_pos_dict_total = dict(d)
        self.landmark68 = np.array(self.landmark68).astype('float32')
        # np.save("./load_data/key_pos_dict_total.npy", self.key_pos_dict_total)
        save_npy_path = "./load_data/landmark68.npy"
        np.save(save_npy_path, self.landmark68)
        print('saved to {}'.format(save_npy_path))
        utils.test_lm(npy_path=save_npy_path, image_path=self.img_path)

    def list_add(self, plist, add):
        plist_new = []
        for p in plist:
            new_p = []
            for n in p:
                tup = [i + add for i in n]
                new_p.append(tup)
            plist_new.append(new_p)
        return plist_new

    def set_key_points(self):
        face_list = [[-50, 100], [-50, 160], [-50, 220], [-50, 280], [-40, 340], [-20, 400], [10, 460], [100, 520],
                     [200, 550],
                     [300, 520], [390, 460], [420, 400], [440, 340], [450, 280], [450, 220], [450, 160], [450, 100]]

        l_eyebrow_list = [[10, 105], [30, 100], [50, 100], [70, 100], [90, 100]]
        r_eyebrow_list = [[310, 105], [330, 100], [350, 100], [370, 100], [390, 100]]

        l_eye_list = [[0, 200], [30, 180], [50, 180], [80, 200], [50, 220], [30, 220]]
        # r_eye_list = [[310, 200], [330, 200], [350, 200], [370, 200], [390, 200]]
        r_eye_list = [[300, 200], [330, 180], [350, 180], [380, 200], [350, 220], [330, 220]]

        nose_list = [[200, 250], [200, 270], [200, 290], [200, 310]]
        nose2_list = [[180, 320], [190, 320], [200, 330], [210, 320], [220, 320]]

        # mouse_list = [[100, 425], [200, 400], [300, 425], [200, 450]]
        mouse_list_outter = [[100, 425], [130, 400], [160, 400], [200, 400], [240, 400], [270, 400], [300, 425],
                             [270, 450], [240, 450], [200, 450], [160, 450], [130, 450]]
        mouse_list_innner = [[120, 425], [160, 410], [200, 410], [240, 410], [280, 425],
                             [240, 435], [200, 435], [160, 435]]
        mouse_list = mouse_list_outter + mouse_list_innner

        color_list = [Qt.green, Qt.yellow, Qt.yellow, Qt.blue, Qt.blue, Qt.yellow, Qt.blue, Qt.yellow]
        start2end_list = [False, False, False, True, True, False, False, True]
        point_list = [face_list, l_eyebrow_list, r_eyebrow_list, nose_list, nose2_list, l_eye_list, r_eye_list,
                      mouse_list]

        # point_list = [i + 250 for i in point_list]
        point_list = self.list_add(point_list, add=150)

        # point_list_new = point_list_new + 250
        # for i in point_list:
        #     i = i + 250
        #     point_list_new.append(i)
        self.window.view.create_key_point_by_point_list(point_list=point_list, color_list=color_list,
                                                        start2end_list=start2end_list)

    def open_image(self):
        img_path, file_type = QtWidgets.QFileDialog.getOpenFileName(self.window, '打开文件', './',
                                                                    ("Images (*.png *.xpm *.jpg)"))
        # self.textEdit_1.setText(img_path)
        self.img_path = img_path
        img = Image.open(img_path)
        # img = img.convert('RGB')  # 转换图像通道
        img = np.array(img)
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

        img = cv2.resize(img, (new_width, new_height))
        frame = QImage(img.data, new_width, new_height, new_width * 3, QImage.Format_RGB888)
        pix = QPixmap.fromImage(frame)
        self.window.main_image = QGraphicsPixmapItem(pix)
        # self.pixmapItem = self.scene.addPixmap(pix)
        self.window.main_image.setPos(200, 100)
        self.window.main_image.setZValue(0)
        # self.main_image.setFlags(
        #     QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsFocusable | QGraphicsItem.ItemIsMovable)
        self.window.scene.addItem(self.window.main_image)
        # self.scene.clearSelection()
        # self.scene.addItem(self.main_image)
        # self.Qitem.add_item(self.main_image)
