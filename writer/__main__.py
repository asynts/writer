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
    italic_normal_text_chunk_style = model.ModelStyle(
        parent_model_style=normal_paragraph_style,
        is_italic=True,
    )

    paragraph_1 = model_tree.add_child(model.ParagraphModelNode(style=heading_paragraph_style))
    paragraph_1.add_child(model.TextChunkModelNode(text="About", style=normal_heading_text_chunk_style))

    paragraph_2 = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph_2.add_child(model.TextChunkModelNode(text="I am creating a word processor in Python. ", style=normal_normal_text_chunk_style))
    paragraph_2.add_child(model.TextChunkModelNode(text="You are likely already familiar with other word processors such as ", style=normal_normal_text_chunk_style))
    paragraph_2.add_child(model.TextChunkModelNode(text="Microsoft Word ", style=bold_normal_text_chunk_style))
    paragraph_2.add_child(model.TextChunkModelNode(text="or ", style=normal_normal_text_chunk_style))
    paragraph_2.add_child(model.TextChunkModelNode(text="Libre Office Writer", style=bold_normal_text_chunk_style))
    paragraph_2.add_child(model.TextChunkModelNode(text=".", style=normal_normal_text_chunk_style))

    paragraph_2 = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph_2.add_child(model.TextChunkModelNode(text="Originally, I started programming this in ", style=normal_normal_text_chunk_style))
    paragraph_2.add_child(model.TextChunkModelNode(text="C++ ", style=bold_normal_text_chunk_style))
    paragraph_2.add_child(model.TextChunkModelNode(text="and was planning to add it to the ", style=normal_normal_text_chunk_style))
    paragraph_2.add_child(model.TextChunkModelNode(text="SerenityOS ", style=bold_normal_text_chunk_style))
    paragraph_2.add_child(model.TextChunkModelNode(text="project. ", style=normal_normal_text_chunk_style))
    paragraph_2.add_child(model.TextChunkModelNode(text="This is still the plan, however, creating a writer application is much harder than I originally anticipated. ", style=normal_normal_text_chunk_style))
    paragraph_2.add_child(model.TextChunkModelNode(text="Now, I am creating this prototype before porting it to ", style=normal_normal_text_chunk_style))
    paragraph_2.add_child(model.TextChunkModelNode(text="C++", style=bold_normal_text_chunk_style))
    paragraph_2.add_child(model.TextChunkModelNode(text=".", style=normal_normal_text_chunk_style))

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

    # Override.
    def paintEvent(self, event: QtGui.QPaintEvent):
        painter = QtGui.QPainter(self)
        self._layout_tree.paint(painter=painter)

    # Override.
    def sizeHint(self):
        return QtCore.QSize(math.ceil(self._layout_tree.get_absolute_width()), math.ceil(self._layout_tree.get_absolute_height()))

    # Override.
    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        super().mousePressEvent(event)

        self._layout_tree.on_mouse_click(
            relative_x=event.position().x(),
            relative_y=event.position().y()
        )

        # Redraw the widget.
        self._layout_tree = create_layout_tree(self._model_tree)
        self.update()

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
    window.setFixedWidth(598)

    app.exec()

if __name__ == "__main__":
    main()
