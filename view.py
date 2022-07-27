from PyQt5.QtWidgets import QGraphicsView
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter

from item import GraphicItem
from edge import Edge
from key_point_item import EllipseItem


class GraphicView(QGraphicsView):

    def __init__(self, graphic_scene, parent=None):
        super().__init__(parent)

        self.gr_scene = graphic_scene
        self.parent = parent

        #self.edge_enable = False
        self.edge_enable = True
        self.drag_edge = None
        #self.create_key_point()

        self.init_ui()

    def init_ui(self):
        self.setScene(self.gr_scene)
        self.setRenderHints(QPainter.Antialiasing |
                            QPainter.HighQualityAntialiasing |
                            QPainter.TextAntialiasing |
                            QPainter.SmoothPixmapTransform |
                            QPainter.LosslessImageRendering)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setTransformationAnchor(self.AnchorUnderMouse)
        self.setDragMode(self.RubberBandDrag)

    def create_key_point(self):
        self.key_point_list = []
        for x, y in zip([100, 1, 200, 500], [100, 1, 200, 400]):
            item = EllipseItem()
            item.setPos(x, y)
            self.gr_scene.add_node(item)
            self.key_point_list.append(item)


        for i in range(len(self.key_point_list) - 1):
            item_s = self.key_point_list[i]
            item_e = self.key_point_list[i + 1]
            print("start {}, end {}".format(item_s.pos(), item_e.pos()))
            self.edge_drag_start(item_s)
            self.edge_drag_end(item_e)

    # def keyPressEvent(self, event):
    #     if event.key() == Qt.Key_N:
    #         item = GraphicItem()
    #         item.setPos(0, 0)
    #         self.gr_scene.add_node(item)
    #     if event.key() == Qt.Key_E:
    #         self.edge_enable = ~self.edge_enable

    def mousePressEvent(self, event):
        item = self.get_item_at_click(event)
        if event.button() == Qt.RightButton:
            if isinstance(item, GraphicItem):
                self.gr_scene.remove_node(item)
        elif self.edge_enable:
            if isinstance(item, GraphicItem):
                self.edge_drag_start(item)
        else:
            super().mousePressEvent(event)

    def get_item_at_click(self, event):
        """ Return the object that clicked on. """
        pos = event.pos()
        item = self.itemAt(pos)
        return item

    def get_items_at_rubber(self):
        """ Get group select items. """
        area = self.rubberBandRect()
        return self.items(area)

    def mouseMoveEvent(self, event):
        pos = event.pos()
        if self.edge_enable and self.drag_edge is not None:
            sc_pos = self.mapToScene(pos)
            self.drag_edge.gr_edge.set_dst(sc_pos.x(), sc_pos.y())
            self.drag_edge.gr_edge.update()
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.edge_enable:
            self.edge_enable = False
            item = self.get_item_at_click(event)
            if isinstance(item, GraphicItem) and item is not self.drag_start_item:
                self.edge_drag_end(item)
            else:
                self.drag_edge.remove()
                self.drag_edge = None
        else:
            super().mouseReleaseEvent(event)

    def edge_drag_start(self, item):
        self.drag_start_item = item
        self.drag_edge = Edge(self.gr_scene, self.drag_start_item, None)

    def edge_drag_end(self, item):
        new_edge = Edge(self.gr_scene, self.drag_start_item, item)
        self.drag_edge.remove()
        self.drag_edge = None
        new_edge.store()
