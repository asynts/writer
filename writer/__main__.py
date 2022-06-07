import sys
import math

from PyQt6 import QtWidgets, QtGui, QtCore

import writer.engine.layout as layout
import writer.engine.model as model
import writer.engine.converter

def create_model_tree():
    model_tree = model.DocumentModelNode()

    model_tree.add_child(model.ParagraphModelNode(text="This is a very, very long paragraph which does not fit on a single line. It will have to be wrapped into the next line, possibly multiple times."))
    model_tree.add_child(model.ParagraphModelNode(text="Hello, world"))
    model_tree.add_child(model.ParagraphModelNode(text="This is another paragraph."))
    model_tree.add_child(model.ParagraphModelNode(text="By adding more and more long paragraphs, we eventually overflow the page and need to create a new one."))
    model_tree.add_child(model.ParagraphModelNode(text="It seems that it takes quite a bit of text to achieve this, and I am running out of ideas what I could write about."))
    model_tree.add_child(model.ParagraphModelNode(text="One more paragraph should overflow the page, if it is long enough. This paragraph should be the one that overflows the page. It is very long. I had to add this additional sentence, because it still wasn't long enough."))

    return model_tree

def create_layout_tree(model_tree: model.DocumentModelNode):
    return writer.engine.converter.generate_layout_tree(model_tree)

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

    if isinstance(layout_node, layout.InlineTextChunkLayoutNode):
        # Remember to subtract the border here.
        rect = rect.adjusted(
            layout_node.get_border_spacing().left,
            layout_node.get_border_spacing().top,
            layout_node.get_border_spacing().left + layout_node.get_border_spacing().right,
            layout_node.get_border_spacing().top + layout_node.get_border_spacing().bottom,
        )

        painter.setFont(layout.normal_font)
        painter.drawText(rect, layout_node.get_text());

    for child_node in layout_node.get_children():
        draw_layout_node(painter=painter, layout_node=child_node)

class WriterWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.MinimumExpanding)

        self._model_tree = create_model_tree()
        self._layout_tree = create_layout_tree(self._model_tree)

        print(self._layout_tree.to_string(), end="")

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)

        draw_layout_node(painter, self._layout_tree)

    def sizeHint(self):
        return QtCore.QSize(math.ceil(self._layout_tree.get_width()), math.ceil(self._layout_tree.get_height()))

class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self._writerWidget = WriterWidget()

        horizontalCenterLayout = QtWidgets.QHBoxLayout()
        horizontalCenterLayout.addStretch()
        horizontalCenterLayout.addWidget(self._writerWidget)
        horizontalCenterLayout.addStretch()

        scrollAreaContent = QtWidgets.QWidget()
        scrollAreaContent.setLayout(horizontalCenterLayout)
        scrollAreaContent.setStyleSheet("background-color: lightgrey;")

        self._scrollArea = QtWidgets.QScrollArea()
        self._scrollArea.setWidget(scrollAreaContent)
        self._scrollArea.setWidgetResizable(True)

        self.setCentralWidget(self._scrollArea)

        self.setWindowTitle("Writer")
        self.show()
 
def main():
    app = QtWidgets.QApplication(sys.argv)
    window = Window()

    app.exec()
    
if __name__ == "__main__":
    main()
