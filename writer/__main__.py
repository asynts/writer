import sys
import math
import time

from PyQt6 import QtWidgets, QtGui, QtCore

import writer.engine.layout as layout
import writer.engine.model as model
import writer.engine.tree as tree
import writer.engine.history as history
import writer.engine.events as events
import writer.engine.converter as converter

from . import example


class WriterWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.MinimumExpanding)
        self.setFocusPolicy(QtCore.Qt.FocusPolicy.ClickFocus)

        self._layout_tree = None

        self.history_manager = history.HistoryManager(
            model_tree=example.create_model_tree(),
        )

        self.history_manager.notify_on_history_change(self.on_history_change)

        self.build_layout_tree()

    def build_layout_tree(self):
        before_ns = time.perf_counter_ns()
        self._layout_tree = converter.generate_layout_for_model(
            self.history_manager.get_model_tree(),
            history_manager=self.history_manager,
        )
        after_ns = time.perf_counter_ns()

        events.validate_parent_hierachy_event(
            model_tree=self.history_manager.get_model_tree(),
            layout_tree=self._layout_tree,
            history_manager=self.history_manager,
        )

        events.validate_cursor_unique_event(
            model_tree=self.history_manager.get_model_tree(),
            layout_tree=self._layout_tree,
            history_manager=self.history_manager,
        )

        print(f"Rebuild  {after_ns - before_ns:>14}ns ({int((after_ns - before_ns) / (1000 * 1000)):>10}ms)")

    def on_history_change(self):
        self.build_layout_tree()
        self.update()

    # Override.
    def paintEvent(self, event: QtGui.QPaintEvent):
        painter = QtGui.QPainter(self)
        painter.setClipRect(event.rect())

        before_ns = time.perf_counter_ns()
        self._layout_tree.paint(painter=painter, visible_rect=QtCore.QRectF(event.rect()))
        after_ns = time.perf_counter_ns()

        print(f"Painting {after_ns - before_ns:>14}ns ({int((after_ns - before_ns) / (1000 * 1000)):>10}ms)")

    # Override.
    def sizeHint(self):
        return QtCore.QSize(math.ceil(self._layout_tree.get_absolute_width()), math.ceil(self._layout_tree.get_absolute_height()))

    # Override.
    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        super().mousePressEvent(event)

        if events.mouse_click_event(
            absolute_x=event.position().x(),
            absolute_y=event.position().y(),
            model_tree=self.history_manager.get_model_tree(),
            layout_tree=self._layout_tree,
            history_manager=self.history_manager,
        ):
            print("Focus set.")
            self.setFocus(QtCore.Qt.FocusReason.MouseFocusReason)
        else:
            print("Focus cleared.")
            self.clearFocus()

    # Override.
    def keyPressEvent(self, event: QtGui.QKeyEvent):
        super().keyPressEvent(event)

        if events.key_press_event(
            event=event,
            model_tree=self.history_manager.get_model_tree(),
            layout_tree=self._layout_tree,
            history_manager=self.history_manager,
        ):
            event.accept()

        print(">>>")
        print(self.history_manager.get_model_tree().dump(), end="")
        print("<<<")

class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # FIXME: This really shouldn't be a global variable.
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

        menubar = QtWidgets.QMenuBar()
        file_menu = menubar.addMenu("File")
        edit_menu = menubar.addMenu("Edit")
        self._edit_undo_action = edit_menu.addAction("Undo")
        self._edit_undo_action.triggered.connect(self.on_edit_undo_action)
        self._edit_undo_action.setShortcut(QtGui.QKeySequence("Ctrl+Z"))
        self._edit_redo_action = edit_menu.addAction("Redo")
        self._edit_redo_action.triggered.connect(self.on_edit_redo_action)
        self._edit_redo_action.setShortcut(QtGui.QKeySequence("Ctrl+Y"))
        self.setMenuBar(menubar)

        self._writerWidget.history_manager.notify_on_history_change(self.on_history_changed)
        self.on_history_changed()

        self.setCentralWidget(self._scrollArea)

        self.setWindowTitle("Writer")
        self.show()

    def on_history_changed(self):
        self._edit_undo_action.setEnabled(self._writerWidget.history_manager.is_undo_possible())
        self._edit_redo_action.setEnabled(self._writerWidget.history_manager.is_redo_possible())

    def on_edit_undo_action(self):
        self._writerWidget.history_manager.undo()

    def on_edit_redo_action(self):
        self._writerWidget.history_manager.redo()

def main():
    app = QtWidgets.QApplication(sys.argv)

    window = Window()

    app.exec()

if __name__ == "__main__":
    main()
