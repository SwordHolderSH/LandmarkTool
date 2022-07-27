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


class MyUI:
    def __init__(self, opt):
        super().__init__()
        self.window = opt

    def set_my_ui(self):
        self.window.setObjectName("LandmarkTool")
        self.window.resize(1500, 1000)
        self.window.centralwidget = QtWidgets.QWidget(self.window)
        self.window.centralwidget.setObjectName("centralwidget")
        self.window.setCentralWidget(self.window.centralwidget)
        # ==========================================================
        self.window.scene = GraphicScene(self.window)  # 创建场景
        self.window.scene.setSceneRect(0, 0, 1000, 800)
        # ========================================================
        self.window.view = GraphicView(self.window.scene, self.window)  # 创建视图窗口
        self.window.view.setGeometry(QtCore.QRect(400, 100, 1000, 800))  # x , y， 宽， 高
        self.window.view.setScene(self.window.scene)
        # ============================================================
        self.window.menubar = QtWidgets.QMenuBar(self.window)
        self.window.menubar.setGeometry(QtCore.QRect(0, 0, 1121, 23))
        self.window.menubar.setObjectName("menubar")
        self.window.menu = QtWidgets.QMenu(self.window.menubar)
        self.window.menu.setObjectName("menu")
        self.window.setMenuBar(self.window.menubar)
        self.window.statusbar = QtWidgets.QStatusBar(self.window)
        self.window.statusbar.setObjectName("statusbar")
        self.window.setStatusBar(self.window.statusbar)
        self.window.action_open_image = QtWidgets.QAction(self.window)
        self.window.action_open_image.setObjectName("action_open_image")
        self.window.menu.addAction(self.window.action_open_image)
        self.window.menubar.addAction(self.window.menu.menuAction())
        # ===================================================================================
        self.window.pushButton_set_key_points = QtWidgets.QPushButton(self.window.centralwidget)
        self.window.pushButton_set_key_points.setGeometry(QtCore.QRect(30, 200, 131, 41))
        self.window.pushButton_set_key_points.setObjectName("pushButton_set_key_points")

        self.window.pushButton_show_pos = QtWidgets.QPushButton(self.window.centralwidget)
        self.window.pushButton_show_pos.setGeometry(QtCore.QRect(30, 300, 131, 41))
        self.window.pushButton_show_pos.setObjectName("pushButton_lock_image")
        # ==========================================================

        # self.window.setCentralWidget(self.window.view)  # 设置中央控件
        self.window.statusbar = self.window.statusBar()  # 添加状态栏
        self.window.labviewcorrd = QLabel('view坐标:')
        self.window.labviewcorrd.setMinimumWidth(150)
        self.window.statusbar.addWidget(self.window.labviewcorrd)
        self.window.labscenecorrd = QLabel('scene坐标：')
        self.window.labscenecorrd.setMinimumWidth(150)
        self.window.statusbar.addWidget(self.window.labscenecorrd)
        self.window.labitemcorrd = QLabel('item坐标：')
        self.window.labitemcorrd.setMinimumWidth(150)
        self.window.statusbar.addWidget(self.window.labitemcorrd)

        self.window.setMouseTracking(True)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self.window)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.window.setWindowTitle(_translate("MainWindow", "MainWindow"))
        # self.window.pushButton_set_key_points.setText(_translate("MainWindow", "设置关键点"))
        self.window.menu.setTitle(_translate("MainWindow", "Menu"))
        self.window.action_open_image.setText(_translate("MainWindow", "Open image"))
        self.window.pushButton_set_key_points.setText(_translate("MainWindow", "Set landmark"))
        self.window.pushButton_show_pos.setText(_translate("MainWindow", "Save landmark"))
