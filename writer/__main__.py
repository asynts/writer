import sys
import math

from PyQt6 import QtWidgets, QtGui, QtCore

import writer.engine.layout as layout
import writer.engine.model as model
import writer.engine.converter

def create_model_tree():
    model_tree = model.DocumentModelNode()

    heading_paragraph_style = model.ModelStyle(
        parent_model_style=model_tree.get_style(),
        is_bold=True,
        font_size=20.0,
    )
    normal_paragraph_style = model.ModelStyle(
        parent_model_style=model_tree.get_style(),
        font_size=12.0,
    )

    normal_heading_text_chunk_style = model.ModelStyle(
        parent_model_style=heading_paragraph_style,
    )
    normal_normal_text_chunk_style = model.ModelStyle(
        parent_model_style=normal_paragraph_style,
    )
    bold_normal_text_chunk_style = model.ModelStyle(
        parent_model_style=normal_paragraph_style,
        is_bold=True,
    )

    paragraph_1 = model_tree.add_child(model.ParagraphModelNode(style=heading_paragraph_style))
    paragraph_1.add_child(model.TextChunkModelNode(text="This is a", style=normal_heading_text_chunk_style))
    paragraph_1.add_child(model.TextChunkModelNode(text=" heading.", style=normal_heading_text_chunk_style))

    paragraph_2 = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph_2.add_child(model.TextChunkModelNode(text="This is a normal paragraph, but ", style=normal_normal_text_chunk_style))
    paragraph_2.add_child(model.TextChunkModelNode(text="this", style=bold_normal_text_chunk_style))
    paragraph_2.add_child(model.TextChunkModelNode(text=" has some highlight applied to it.", style=normal_normal_text_chunk_style))

    return model_tree

def create_layout_tree(model_tree: model.DocumentModelNode):
    return writer.engine.converter.generate_layout_for_model(model_tree)

class WriterWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.MinimumExpanding)

        self._model_tree = create_model_tree()
        self._layout_tree = create_layout_tree(self._model_tree)

        print(self._layout_tree.to_string(), end="")

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        self._layout_tree.paint(painter=painter)

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
