from PyQt5.QtWidgets import QGraphicsItem, QGraphicsPixmapItem, QGraphicsEllipseItem
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, pyqtSignal, QPoint, QRectF, QRect


class EllipseItem(QGraphicsEllipseItem):

    def __init__(self, parent=None, r=60):
        super().__init__(parent)

        self.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsFocusable | QGraphicsItem.ItemIsMovable)

        self.r = r  # 直径
        self.width = self.r
        self.height = self.r
        self.x = 0
        self.y = 0
        # self.x = -1 * self.r / 2
        # self.y = -1 * self.r / 2
        self.setBrush(Qt.red)
        # self.setPos(self.x, self.y)
        # self.setRect(-1 * self.r / 2, -1 * self.r / 2, self.r, self.r)
        # self.setRect(-1 * self.r / 2, -1 * self.r / 2, self.r, self.r)
        self.setRect(self.x, self.y, self.r, self.r)
        self.setZValue(10)

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        # update selected node and its edge
        if self.isSelected():
            for gr_edge in self.scene().edges:
                gr_edge.edge_wrap.update_positions()
