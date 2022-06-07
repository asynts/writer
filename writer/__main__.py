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
