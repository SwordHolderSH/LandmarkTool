import sys
from PyQt5.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsRectItem, QMainWindow, QLabel, \
    QGraphicsItem, QGraphicsEllipseItem, QGraphicsPixmapItem
from actions import MyAction
from ui import MyUI


class MyMainWindow(QMainWindow):
    def __init__(self):
        super(MyMainWindow, self).__init__()
        self.set_my_ui()
        self.set_action()
        self.actions = MyAction(opt=self)

    def set_action(self):
        self.action_open_image.triggered.connect(self.open_image)
        self.pushButton_set_key_points.clicked.connect(self.set_key_points)
        self.pushButton_show_pos.clicked.connect(self.show_pos)

    def set_key_points(self):
        self.actions.set_key_points()

    def set_my_ui(self):
        self.ui = MyUI(opt=self)
        self.ui.set_my_ui()

    def show_pos(self):
        self.actions.show_pos()

    def open_image(self):
        self.actions.open_image()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # myMainWindow = QMainWindow()
    ex = MyMainWindow()
    ex.showMaximized()
    ex.show()
    sys.exit(app.exec_())
