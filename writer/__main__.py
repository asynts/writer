import sys
import math

from PyQt6 import QtWidgets, QtGui, QtCore

import writer.engine.layout as layout

def create_layout_tree():
    layout_tree = layout.PageLayoutNode()

    # FIXME: Get actual paragraphs working.
    paragraph_1 = layout.BlockLayoutNode(
        fixed_height=1 * layout.normal_font_metrics.height()
    )
    layout_tree.get_content_node().place_block_node(paragraph_1)

    return layout_tree

def draw_layout_node(painter: QtGui.QPainter, layout_node: layout.LayoutNode):
    rect = QtCore.QRectF(
        layout_node.get_absolute_x(),
        layout_node.get_absolute_y(),
        layout_node.get_width(),
        layout_node.get_height(),
    )

    if layout_node.get_background_color() is not None:
        painter.fillRect(rect, layout_node.get_background_color())

    if layout_node.get_border_color() is not None:
        border = layout_node.get_border_spacing()

        painter.fillRect(QtCore.QRectF(
            rect.x(),
            rect.y(),
            rect.width(),
            border.top,
        ), layout_node.get_border_color())

        painter.fillRect(QtCore.QRectF(
            rect.x(),
            rect.y() + rect.height() - border.bottom,
            rect.width(),
            border.bottom,
        ), layout_node.get_border_color())

        painter.fillRect(QtCore.QRectF(
            rect.x(),
            rect.y(),
            border.left,
            rect.height(),
        ), layout_node.get_border_color())

        painter.fillRect(QtCore.QRectF(
            rect.x() + rect.width() - border.right,
            rect.y(),
            border.right,
            rect.height(),
        ), layout_node.get_border_color())

    for child_node in layout_node.get_children():
        draw_layout_node(painter=painter, layout_node=child_node)

class WriterWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self._layout_node = create_layout_tree()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)

        draw_layout_node(painter, self._layout_node)

    def sizeHint(self):
        return QtCore.QSize(math.ceil(self._layout_node.get_width()), math.ceil(self._layout_node.get_height()))

class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self._writerWidget = WriterWidget()

        self._scrollArea = QtWidgets.QScrollArea()
        self._scrollArea.setWidget(self._writerWidget)
        self.setCentralWidget(self._scrollArea)

        self.setWindowTitle("Writer")
        self.show()
 
def main():
    app = QtWidgets.QApplication(sys.argv)
    window = Window()

    app.exec()
    
if __name__ == "__main__":
    main()
