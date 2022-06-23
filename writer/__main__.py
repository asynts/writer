import sys
import math
import time

from PyQt6 import QtWidgets, QtGui, QtCore

import writer.engine.layout as layout
import writer.engine.model as model
import writer.engine.tree as tree
import writer.engine.converter
import writer.engine.history as history
import writer.engine.events as events

from . import example


def create_layout_tree(model_tree: model.DocumentModelNode):
    return writer.engine.converter.generate_layout_for_model(model_tree)

class WriterWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.MinimumExpanding)

        writer.engine.history.global_history_manager = history.HistoryManager(
            model_tree=example.create_model_tree(),
        )

        self._debug_rects = []
        self._debug_rect_offset = 0

        self._timer = QtCore.QTimer(self)
        self._timer.setInterval(500)
        self._timer.timeout.connect(self.timerTimeout)
        self._timer.start()

        self.build_layout_tree()

    def build_layout_tree(self):
        before_ns = time.perf_counter_ns()
        self._layout_tree = create_layout_tree(history.global_history_manager.get_model_tree())
        after_ns = time.perf_counter_ns()

        events.validate_parent_hierachy_event(
            model_tree=history.global_history_manager.get_model_tree(),
            layout_tree=self._layout_tree,
        )

        print(f"Rebuild  {after_ns - before_ns:>14}ns ({(after_ns - before_ns) / (1000 * 1000 * 1000):>10.4}s)")

    def timerTimeout(self):
        self._debug_rect_offset += 1
        self.update()

    # Override.
    def paintEvent(self, event: QtGui.QPaintEvent):
        painter = QtGui.QPainter(self)
        painter.setClipRect(event.rect())

        before_ns = time.perf_counter_ns()
        self._layout_tree.paint(painter=painter, visible_rect=QtCore.QRectF(event.rect()))
        after_ns = time.perf_counter_ns()

        if len(self._debug_rects) >= 1:
            debug_rect_index = self._debug_rect_offset % len(self._debug_rects)
            painter.setPen(QtGui.QPen(layout.COLOR_PINK, 3))
            painter.drawRect(self._debug_rects[debug_rect_index])

        print(f"Painting {after_ns - before_ns:>14}ns ({(after_ns - before_ns) / (1000 * 1000 * 1000):>10.4}s)")

    # Override.
    def sizeHint(self):
        return QtCore.QSize(math.ceil(self._layout_tree.get_absolute_width()), math.ceil(self._layout_tree.get_absolute_height()))

    # Override.
    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        super().mousePressEvent(event)

        print(">>> mousePressEvent: model_tree (before)")
        print(
            history.global_history_manager.get_model_tree().dump(),
            end="",
        )
        print("<<<")

        print(">>> mousePressEvent: layout_tree (before)")
        print(
            self._layout_tree.to_string(),
            end="",
        )
        print("<<<")

        self._debug_rects = events.mouse_click_event(
            absolute_x=event.position().x(),
            absolute_y=event.position().y(),
            model_tree=history.global_history_manager.get_model_tree(),
            layout_tree=self._layout_tree
        )
        self._debug_rect_offset = 0

        self._debug_rects.append(
            QtCore.QRectF(event.position().x() - 4, event.position().y() - 4, 8, 8)
        )

        print(">>> mousePressEvent after")
        print(
            history.global_history_manager.get_model_tree().dump(),
            end="",
        )
        print("<<<")

        # Redraw the widget.
        self.build_layout_tree()
        self.update()

class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        layout.dots_per_cm = self.screen().logicalDotsPerInch() / 2.54

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
