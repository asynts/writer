# import pygame

# import writer.engine.layout as layout

# COLOR_WHITE = (255, 255, 255)
# COLOR_BLACK = (0, 0, 0)
# COLOR_RED = (255, 0, 0)
# COLOR_GRAY = (200, 200, 200)

# def create_layout_tree():
#     layout_tree = layout.PageLayoutNode()

#     # FIXME: Get actual paragraphs working.
#     paragraph_1 = layout.BlockLayoutNode(
#         fixed_height=1 * layout.font_height
#     )
#     layout_tree.get_content_node().place_block_node(paragraph_1)

#     return layout_tree

# def draw_layout_node(screen: pygame.Surface, layout_node: layout.LayoutNode):
#     rect = (
#         layout_node.get_absolute_x(),
#         layout_node.get_absolute_y(),
#         layout_node.get_width(),
#         layout_node.get_height(),
#     )

#     if layout_node.get_background_color() is not None:
#         screen.fill(layout_node.get_background_color(), rect)

#     if layout_node.get_border_color() is not None:
#         pygame.draw.rect(screen, layout_node.get_border_color(), rect, width=1)

#     for child_node in layout_node.get_children():
#         draw_layout_node(screen=screen, layout_node=child_node)

# def main():
#     pygame.display.init()
#     pygame.font.init()

#     layout.normal_font = pygame.font.SysFont("monospace", 12)
#     layout.font_width, layout.font_height = layout.normal_font.size("x")

#     layout_tree = create_layout_tree()

#     screen = pygame.display.set_mode([ 500, 500 ])

#     while True:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.display.quit()
#                 return

#         screen.fill(COLOR_GRAY)

#         draw_layout_node(screen, layout_tree)

#         pygame.display.flip()

# if __name__ == "__main__":
#     main()

import sys

from PyQt6 import QtWidgets, QtGui, QtCore

class WriterWidget(QtWidgets.QWidget):
    def paintEvent(self, event):
        painter = QtGui.QPainter(self)

        painter.setPen(QtGui.QColor(255, 0, 0))
        painter.setBrush(QtGui.QColor(255, 0, 0))
        painter.drawRect(0, 0, 100, 100)

    def sizeHint(self):
        return QtCore.QSize(500, 500)

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
