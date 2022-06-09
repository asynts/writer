import sys
import math
import time

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
    paragraph_1.add_child(model.TextChunkModelNode(text="This  is a", style=normal_heading_text_chunk_style))
    paragraph_1.add_child(model.TextChunkModelNode(text=" heading.", style=normal_heading_text_chunk_style))

    paragraph_2 = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph_2.add_child(model.TextChunkModelNode(text="This is a normal paragraph, but ", style=normal_normal_text_chunk_style))
    paragraph_2.add_child(model.TextChunkModelNode(text="this", style=bold_normal_text_chunk_style))
    paragraph_2.add_child(model.TextChunkModelNode(text=" has some highlight applied to it.", style=normal_normal_text_chunk_style))

    for i in range(100):
        paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
        for j in range(100):
            paragraph.add_child(model.TextChunkModelNode(
                text=f"This is paragraph ",
                style=normal_normal_text_chunk_style,
            ))
            paragraph.add_child(model.TextChunkModelNode(
                text=f"{i}",
                style=bold_normal_text_chunk_style,
            ))
            paragraph.add_child(model.TextChunkModelNode(
                text=f" and text chunk",
                style=normal_normal_text_chunk_style,
            ))
            paragraph.add_child(model.TextChunkModelNode(
                text=f" {j}",
                style=bold_normal_text_chunk_style,
            ))
            # FIXME: If I add another space here, we hit an assertion.
            paragraph.add_child(model.TextChunkModelNode(
                text=f".",
                style=normal_normal_text_chunk_style,
            ))

    return model_tree

def create_layout_tree(model_tree: model.DocumentModelNode):
    return writer.engine.converter.generate_layout_for_model(model_tree)

class WriterWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.MinimumExpanding)

        self._model_tree = create_model_tree()
        self.build_layout_tree()

    def build_layout_tree(self):
        before_ns = time.perf_counter_ns()
        self._layout_tree = create_layout_tree(self._model_tree)
        after_ns = time.perf_counter_ns()

        print(f"Rebuild  {after_ns - before_ns:>14}ns ({(after_ns - before_ns) / (1000 * 1000 * 1000):>10.4}s)")

    # Override.
    def paintEvent(self, event: QtGui.QPaintEvent):
        painter = QtGui.QPainter(self)

        before_ns = time.perf_counter_ns()
        self._layout_tree.paint(painter=painter)
        after_ns = time.perf_counter_ns()

        print(f"Painting {after_ns - before_ns:>14}ns ({(after_ns - before_ns) / (1000 * 1000 * 1000):>10.4}s)")

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
        self.build_layout_tree()
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

    app.exec()

if __name__ == "__main__":
    main()
