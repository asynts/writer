import enum
import functools
from re import M

from PyQt6 import QtGui, QtCore
from PyQt6.QtGui import QColor

import writer.engine.model as model
import writer.engine.tree as tree
import writer.engine.history as history

from .style import Spacing, LayoutStyle

COLOR_WHITE = QColor(255, 255, 255)
COLOR_BLACK = QColor(0, 0, 0)
COLOR_RED = QColor(255, 0, 0)
COLOR_GREEN = QColor(0, 255, 0)
COLOR_BLUE = QColor(0, 0, 255)
COLOR_PINK = QColor(255, 53, 184)
COLOR_YELLOW = QColor(255, 255, 0)

b_draw_debug_text_outline = False

# This is initialized on startup by Qt.
dots_per_cm = None

def cm_to_pixel(value: float):
    assert dots_per_cm is not None

    # This is a bit arbitrary, since this depends on the display resolution.
    return dots_per_cm * value

# There are several phases a layout node can be in.
@functools.total_ordering
class Phase(enum.Enum):
    # The node has been created and a temporary parent has been assigned.
    # Parent nodes are not allowed to be changed while such a node exists.
    #
    # Only exception is, if the node is discarded without ever being added to the parent.
    # This is very important because we are caching the parent node's remaining space and using it without checking for changes.
    PHASE_1_CREATED = 1

    # The node has been permanently placed in a parent node and may not be moved.
    PHASE_2_PLACED = 2

    # When all nodes have been placed, we do the final layout calculation where we determine the absolute positions and sizes.
    PHASE_3_FINAL = 3

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, Phase):
            return False
        return self.value.__eq__(__o.value)

    def __ge__(self, __o: object) -> bool:
        if not isinstance(__o, Phase):
            return False
        return self.value.__ge__(__o.value)

class LayoutNode:
    __slots__ = (
        "__phase",
        "__parent_node",
        "__model_node",
        "__associated_child_node",
        "__name",
        "_relative_x",
        "_relative_y",
        "_width_of_children",
        "_height_of_children",
        "__style",
        "__absolute_x",
        "__absolute_y",
        "_absolute_width",
        "_absolute_height",
    )

    def __init__(
        self,
        *,
        name: str,
        parent_node: "LayoutNode",
        model_node: "model.ModelNode",
        style: LayoutStyle):

        # The parent node needs to be extremely careful now.
        # We assume that the avaliable space does not change while we are associated.
        if parent_node is not None:
            parent_node.on_child_associated(self)

        # The phase in which the layout node is in.
        # Some operations can only be performed in some phases.
        self.__phase = Phase.PHASE_1_CREATED

        # References parent node.
        self.__parent_node = parent_node

        # Can reference the corresponding model node, or 'None'.
        self.__model_node = model_node

        # There can only be one child associated with this node.
        # To enforce this, we keep track of the associated child.
        self.__associated_child_node = None

        # Name of the node for debugging.
        self.__name = name

        # Position relative to parent node.
        # Includes the inner spacing of the parent node.
        self._relative_x: int = None
        self._relative_y: int = None

        # How much space is needed to fit all children.
        self._width_of_children = 0
        self._height_of_children = 0

        # Style applied to this node.
        self.__style = style

        # The absolute position and size of the node.
        self.__absolute_x = None
        self.__absolute_y = None
        self._absolute_width = None
        self._absolute_height = None

    def get_phase(self):
        return self.__phase

    def get_style(self):
        return self.__style

    def get_model_node(self):
        return self.__model_node

    def to_string(self, *, indent=0):
        result = f"{indent*' '}{self.__name}(relative_x={self._relative_x}, relative_y={self._relative_y}, id={id(self)} phase={self.__phase})\n"

        for child in self.get_children():
            result += child.to_string(indent=indent+1)

        return result

    # It is possible to assign a new parent node.
    # This is useful if we find a node to be too large and want to put it elsewhere.
    def set_parent(self, parent_node: "LayoutNode"):
        assert self.get_phase() == Phase.PHASE_1_CREATED
        self.__parent_node = parent_node

        # The parent node needs to be extremely careful now.
        self.__parent_node.on_child_associated(self)

    def on_reused_with_new_parent(self, *, parent_node: "LayoutNode"):
        assert self.get_phase() >= Phase.PHASE_2_PLACED
        self.__absolute_x = None
        self.__absolute_x = None

        # Undo the final layout calculations.
        def visit_layout_node(layout_node: LayoutNode):
            layout_node.__phase = Phase.PHASE_2_PLACED
            layout_node.__absolute_x = None
            layout_node.__absolute_y = None
            layout_node._absolute_width = None
            layout_node._absolute_height = None

            for child_node in layout_node.get_children():
                visit_layout_node(child_node)
        visit_layout_node(self)

        # Undo the placement of this node, children remain placed.
        self.__phase = Phase.PHASE_1_CREATED

        # Update the reference to the parent node.
        self.set_parent(parent_node)

    # Virtual.
    def on_child_associated(self, child_node: "LayoutNode"):
        assert self.__associated_child_node is None
        self.__associated_child_node = child_node

    # Virtual.
    def on_child_dissociated(self, child_node: "LayoutNode"):
        assert self.__associated_child_node is not None
        assert self.__associated_child_node is child_node
        self.__associated_child_node = None

    # Child nodes must not be changed after they are placed in their parent node.
    # Virtual.
    def on_placed_in_node(self, *, relative_x: int, relative_y: int):
        assert self.__phase == Phase.PHASE_1_CREATED
        assert self.__associated_child_node is None

        self._relative_x = relative_x
        self._relative_y = relative_y

        self.__phase = Phase.PHASE_2_PLACED

        # The parent no longer needs to worry about us.
        if self.__parent_node is not None:
            self.__parent_node.on_child_dissociated(self)

    # Absolutely nothing can change after the final layout calculation has been performed.
    # This is done lazily.
    def on_final_layout_calculation(self):
        assert self.__phase == Phase.PHASE_2_PLACED

        if self.__parent_node is None:
            assert self.__style.outer_spacing.top == 0.0

            self.__absolute_x = 0.0
            self.__absolute_y = 0.0
        else:
            assert self.__parent_node.__absolute_x is not None
            assert self.__parent_node.__absolute_y is not None

            self.__absolute_x = self.__parent_node.__absolute_x + self._relative_x
            self.__absolute_y = self.__parent_node.__absolute_y + self._relative_y

        self._absolute_width = self.get_width()
        self._absolute_height = self.get_height()

        self.__phase = Phase.PHASE_3_FINAL

    # Virtual.
    def on_mouse_click(self, *, relative_x: float, relative_y: float, path: tree.NodePath):
        return False

    def get_parent_node(self) -> "LayoutNode":
        return self.__parent_node

    def get_relative_x(self) -> float:
        return self._relative_x

    def get_relative_y(self) -> float:
        return self._relative_y

    def get_absolute_x(self) -> float:
        if self.get_phase() == Phase.PHASE_2_PLACED:
            self.on_final_layout_calculation()
        assert self.get_phase() == Phase.PHASE_3_FINAL

        return self.__absolute_x

    def get_absolute_y(self) -> float:
        if self.get_phase() == Phase.PHASE_2_PLACED:
            self.on_final_layout_calculation()
        assert self.get_phase() == Phase.PHASE_3_FINAL

        return self.__absolute_y

    def get_absolute_width(self) -> float:
        if self.get_phase() == Phase.PHASE_2_PLACED:
            self.on_final_layout_calculation()
        assert self.get_phase() == Phase.PHASE_3_FINAL

        return self._absolute_width

    def get_absolute_height(self) -> float:
        if self.get_phase() == Phase.PHASE_2_PLACED:
            self.on_final_layout_calculation()
        assert self.get_phase() == Phase.PHASE_3_FINAL

        return self._absolute_height

    def get_fixed_width(self) -> float:
        return self.__style.fixed_width

    def get_fixed_height(self) -> float:
        return self.__style.fixed_height

    def get_min_width(self) -> float:
        assert self.get_phase() <= Phase.PHASE_2_PLACED

        if self.get_fixed_width() is not None:
            return self.get_fixed_width()
        else:
            return self._width_of_children + self.get_style().inner_spacing.x

    # Virtual.
    def get_width(self) -> float:
        if self._absolute_width is not None:
            assert self.get_phase() == Phase.PHASE_3_FINAL
            return self._absolute_width

        assert self.get_phase() == Phase.PHASE_2_PLACED
        return self.get_min_width()

    def get_min_height(self) -> float:
        assert self.get_phase() <= Phase.PHASE_2_PLACED

        if self.get_fixed_height() is not None:
            return self.get_fixed_height()
        else:
            return self._height_of_children + self.get_style().inner_spacing.y

    def get_height(self) -> float:
        if self._absolute_height is not None:
            assert self.get_phase() == Phase.PHASE_3_FINAL
            return self._absolute_height

        assert self.get_phase() == Phase.PHASE_2_PLACED
        return self.get_min_height()

    def get_min_inner_height(self):
        assert self.get_phase() <= Phase.PHASE_2_PLACED
        return self._height_of_children

    def get_min_inner_width(self):
        assert self.get_phase() <= Phase.PHASE_2_PLACED
        return self._width_of_children

    # Virtual.
    def get_children(self) -> list["LayoutNode"]:
        return []

    def get_qrect(self):
        if self.get_phase() == Phase.PHASE_2_PLACED:
            self.on_final_layout_calculation()
        assert self.get_phase() == Phase.PHASE_3_FINAL

        return QtCore.QRectF(
            self.__absolute_x,
            self.__absolute_y,
            self._absolute_width,
            self._absolute_height,
        )

    def get_inner_qrect(self):
        if self.get_phase() == Phase.PHASE_2_PLACED:
            self.on_final_layout_calculation()
        assert self.get_phase() == Phase.PHASE_3_FINAL

        return self.get_qrect().adjusted(
            self.get_style().inner_spacing.left,
            self.get_style().inner_spacing.top,
            -self.get_style().inner_spacing.x,
            -self.get_style().inner_spacing.y,
        )

    def paint_background(self, *, painter: QtGui.QPainter):
        assert self.get_phase() == Phase.PHASE_3_FINAL

        if self.get_style().background_color is not None:
            painter.fillRect(self.get_qrect(), self.get_style().background_color)

    def paint_border(self, *, painter: QtGui.QPainter):
        assert self.get_phase() == Phase.PHASE_3_FINAL

        rect = self.get_qrect()

        if self.get_style().border_color is not None:
            border = self.get_style().border_spacing

            painter.fillRect(QtCore.QRectF(
                rect.x(),
                rect.y(),
                rect.width(),
                border.top,
            ), self.get_style().border_color)

            painter.fillRect(QtCore.QRectF(
                rect.x(),
                rect.y() + rect.height() - border.bottom,
                rect.width(),
                border.bottom,
            ), self.get_style().border_color)

            painter.fillRect(QtCore.QRectF(
                rect.x(),
                rect.y(),
                border.left,
                rect.height(),
            ), self.get_style().border_color)

            painter.fillRect(QtCore.QRectF(
                rect.x() + rect.width() - border.right,
                rect.y(),
                border.right,
                rect.height(),
            ), self.get_style().border_color)

    # Virtual.
    def paint_decoration(self, *, painter: QtGui.QPainter):
        assert self.get_phase() == Phase.PHASE_3_FINAL

    def paint(self, *, painter: QtGui.QPainter, visible_rect: QtCore.QRectF):
        if self.get_phase() == Phase.PHASE_2_PLACED:
            self.on_final_layout_calculation()
        assert self.get_phase() == Phase.PHASE_3_FINAL

        # If this element is not visible, we do not draw it.
        # Somehow, a rect with zero width never intersects.
        if not self.get_qrect().intersects(visible_rect) and self.get_qrect().width() > 0.0:
            return

        self.paint_background(painter=painter)
        self.paint_border(painter=painter)
        self.paint_decoration(painter=painter)

        for child in self.get_children():
            child.paint(painter=painter, visible_rect=visible_rect)

class BlockLayoutNode(LayoutNode):
    __slots__ = "_children"

    def __init__(self, *, name="BlockLayoutNode", **kwargs):
        super().__init__(name=name, **kwargs)

        self._children: list[LayoutNode] = []

    # Override.
    def get_children(self):
        return self._children

    def get_max_inner_width(self) -> float:
        if self.get_fixed_width() is None:
            if isinstance(self.get_parent_node(), BlockLayoutNode):
                return self.get_parent_node().get_max_inner_width() - self.get_style().all_spacing.x
            else:
                return None
        else:
            return self.get_fixed_width() - self.get_style().inner_spacing.x

    def get_max_inner_height(self) -> float:
        if self.get_fixed_height() is None:
            if isinstance(self.get_parent_node(), BlockLayoutNode):
                return self.get_parent_node().get_max_inner_height() - self.get_style().all_spacing.y
            else:
                return None
        else:
            return self.get_fixed_height() - self.get_style().inner_spacing.y

    def get_max_width(self):
        if self.get_fixed_width() is None:
            if isinstance(self.get_parent_node(), BlockLayoutNode):
                # FIXME: Margin?
                return self.get_parent_node().get_max_inner_width()
            else:
                return None
        else:
            return self.get_fixed_width()

    def get_max_height(self):
        if self.get_fixed_height() is None:
            if isinstance(self.get_parent_node(), BlockLayoutNode):
                # FIXME: Margin?
                return self.get_parent_node().get_max_inner_height()
            else:
                return None
        else:
            return self.get_fixed_height()

    def place_child_node(self, child_node: LayoutNode):
        raise AssertionError

class HorizontalLayoutNode(BlockLayoutNode):
    __slots__ = (
        "__max_remaining_width",
    )

    def __init__(self, *, name="HorizontalLayoutNode", **kwargs):
        super().__init__(name=name, **kwargs)

        self.__max_remaining_width = None

    def _get_max_remaining_width(self) -> float:
        assert self.get_phase() == Phase.PHASE_1_CREATED

        if self.get_fixed_width() is None:
            if isinstance(self.get_parent_node(), HorizontalLayoutNode):
                return self.get_parent_node().get_max_remaining_width() - self.get_min_inner_width() - self.get_style().all_spacing.x
            elif isinstance(self.get_parent_node(), VerticalLayoutNode):
                return self.get_parent_node().get_max_inner_width() - self.get_min_inner_width() - self.get_style().all_spacing.x
            else:
                return None
        else:
            return self.get_fixed_width() - self.get_min_inner_width() - self.get_style().inner_spacing.x

    # This function assumes that the space avaliable in the parent node doesn't change while this node is in the 'PHASE_1_CREATED' phase.
    def get_max_remaining_width(self) -> float:
        assert self.get_phase() == Phase.PHASE_1_CREATED

        if self.__max_remaining_width is not None:
            return self.__max_remaining_width

        self.__max_remaining_width = self._get_max_remaining_width()
        return self.__max_remaining_width

    def place_child_node(self, child_node: LayoutNode):
        assert self.get_phase() == Phase.PHASE_1_CREATED

        child_node.on_placed_in_node(
            relative_x=self.get_style().inner_spacing.left + child_node.get_style().outer_spacing.left + self._width_of_children,
            relative_y=self.get_style().inner_spacing.top + child_node.get_style().outer_spacing.top,
        )
        occupied_by_child = child_node.get_width() + child_node.get_style().outer_spacing.x

        self._width_of_children += occupied_by_child
        self.__max_remaining_width -= occupied_by_child
        assert self.__max_remaining_width >= 0.0

        self._height_of_children = max(
            self._height_of_children,
            child_node.get_height() + child_node.get_style().outer_spacing.y,
        )

        self._children.append(child_node)

class VerticalLayoutNode(BlockLayoutNode):
    __slots__ = tuple()

    def __init__(self, *, name="VerticalLayoutNode", **kwargs):
        super().__init__(name=name, **kwargs)

    def get_max_remaining_height(self) -> float:
        assert self.get_phase() == Phase.PHASE_1_CREATED

        if self.get_fixed_height() is None:
            if isinstance(self.get_parent_node(), VerticalLayoutNode):
                return self.get_parent_node().get_max_remaining_height() - self.get_min_inner_height() - self.get_style().all_spacing.y
            if isinstance(self.get_parent_node(), HorizontalLayoutNode):
                return self.get_parent_node().get_max_inner_height() - self.get_min_inner_height() - self.get_style().all_spacing.y
            else:
                return None
        else:
            return self.get_fixed_height() - self.get_min_inner_height() - self.get_style().inner_spacing.y

    # Override.
    def get_width(self) -> float:
        if self._absolute_width is not None:
            assert self.get_phase() == Phase.PHASE_3_FINAL
            return self._absolute_width

        assert self.get_phase() == Phase.PHASE_2_PLACED

        if self.get_fixed_width():
            return self.get_fixed_width()
        elif self.get_max_width() is not None:
            return self.get_max_width()
        else:
            return self.get_min_width()

    def place_child_node(self, child_node: LayoutNode):
        assert self.get_phase() == Phase.PHASE_1_CREATED

        child_node.on_placed_in_node(
            relative_x=self.get_style().inner_spacing.left + child_node.get_style().outer_spacing.left,
            relative_y=self.get_style().inner_spacing.top + child_node.get_style().outer_spacing.top + self._height_of_children,
        )
        self._height_of_children += child_node.get_height() + child_node.get_style().outer_spacing.y

        self._width_of_children = max(
            self._width_of_children,
            child_node.get_width() + child_node.get_style().outer_spacing.x,
        )

        self._children.append(child_node)

class PageLayoutNode(VerticalLayoutNode):
    __slots__ = (
        "__header_node",
        "__content_node",
        "__footer_node",
    )

    def __init__(self, *, parent_node: "LayoutNode"):
        super().__init__(
            name="PageLayoutNode",
            parent_node=parent_node,
            model_node=None,

            style=LayoutStyle(
                fixed_width=cm_to_pixel(21.0),
                fixed_height=cm_to_pixel(29.7),

                background_color=COLOR_WHITE,
                border_color=COLOR_BLACK,

                border_spacing=Spacing(left=1, right=1, top=1, bottom=1),
                margin_spacing=Spacing(top=10, bottom=10),
            ),
        )

        total_height = self.get_max_inner_height()
        header_height = cm_to_pixel(1.9)
        footer_height = cm_to_pixel(3.67)
        content_height = total_height - header_height - footer_height

        self.__header_node = VerticalLayoutNode(
            parent_node=self,

            # FIXME: Add HeaderModelNode.
            model_node=None,

            style=LayoutStyle(
                fixed_height=header_height,

                background_color=COLOR_GREEN,
            ),
        )

        self.__content_node = VerticalLayoutNode(
            parent_node=self,
            model_node=None,

            style=LayoutStyle(
                fixed_height=content_height,
                background_color=COLOR_BLUE,
                padding_spacing=Spacing(left=20, right=20, top=20, bottom=20),
            ),
        )

        self.__footer_node = VerticalLayoutNode(
            parent_node=self,

            # FIXME: Add HeaderModelNode.
            model_node=None,

            style=LayoutStyle(
                fixed_height=footer_height,
                background_color=COLOR_RED,
            ),
        )

    # Override.
    def on_child_associated(self, child_node: "LayoutNode"):
        # We don't track associated children in the page node, because there can be multiple pending and this is fine.
        pass

    # Override.
    def on_child_dissociated(self, child_node: "LayoutNode"):
        # We don't track associated children in the page node, because there can be multiple pending and this is fine.
        pass

    # Override.
    def on_placed_in_node(self, *, relative_x: int, relative_y: int):
        # We are not allowed to make modifications after placing nodes.
        # But we want to be able to add nodes to the areas, therefore, we defer the placement.
        self.place_child_node(self.__header_node)
        self.place_child_node(self.__content_node)
        self.place_child_node(self.__footer_node)

        super().on_placed_in_node(relative_x=relative_x, relative_y=relative_y)

    def get_header_node(self):
        return self.__header_node

    def get_content_node(self):
        return self.__content_node

    def get_footer_node(self):
        return self.__footer_node

class CursorLayoutNode(LayoutNode):
    __slots__ = (
        "_model_node",
        "_model_node_offset",
    )

    def __init__(self, *, parent_node: LayoutNode, model_node: "model.TextChunkModelNode", model_node_offset: int):
        assert isinstance(model_node, model.TextChunkModelNode)
        assert model_node.cursor_offset is not None

        rendered_size = model_node.font_metrics.size(0, "")

        super().__init__(
            name="CursorLayoutNode",
            parent_node=parent_node,
            model_node=model_node,

            style=LayoutStyle(
                fixed_width=0,
                fixed_height=rendered_size.height(),
            ),
        )

        self._model_node_offset = model_node_offset

    # Override.
    def paint_decoration(self, *, painter: QtGui.QPainter):
        super().paint_decoration(painter=painter)

        painter.fillRect(
            QtCore.QRectF(
                self.get_absolute_x() - 1,
                self.get_absolute_y() - 2,
                2,
                self.get_absolute_height() + 4,
            ),
            COLOR_YELLOW,
        )

class TextChunkLayoutNode(LayoutNode):
    __slots__ = (
        "_model_node",
        "_model_node_offset",
        "_text"
    )

    def __init__(
        self,
        *,
        text: str,
        parent_node: LayoutNode,

        model_node: "model.TextChunkModelNode",
        model_node_offset: int,

        rendered_size: QtCore.QSizeF,
    ):
        assert isinstance(model_node, model.TextChunkModelNode)

        super().__init__(
            name="TextChunkLayoutNode",
            parent_node=parent_node,
            model_node=model_node,

            style=LayoutStyle(
                fixed_width=rendered_size.width(),
                fixed_height=rendered_size.height(),
            ),
        )

        self._model_node_offset = model_node_offset
        self._text = text

    def _offset_into_model_node(self, *, relative_x: float) -> int:
        font_metrics: QtGui.QFontMetricsF = self.get_model_node().font_metrics

        offset = self._model_node_offset

        x = 0.0
        for character in self._text:
            character_width = font_metrics.size(0, character).width()

            if relative_x >= x + character_width / 2:
                offset += 1
                x += character_width
            else:
                break

        return offset

    # Override.
    def on_mouse_click(self, *, relative_x: float, relative_y: float, path: tree.NodePath):
        new_model_tree = history.global_history_manager.get_model_tree()

        # Remove the cursor from the the previously selected node.
        previous_cursor_path = new_model_tree.cursor_node_path
        if previous_cursor_path is not None:
            new_node = previous_cursor_path.lookup(root_node=new_model_tree).make_mutable_copy()
            new_node.cursor_offset = None
            new_node.make_immutable()

            new_model_tree = previous_cursor_path.replace(new_node, root_node=new_model_tree)

        # Place the cursor in the current layout node.
        new_node = self.get_model_node().make_mutable_copy()
        new_node.cursor_offset = self._offset_into_model_node(relative_x=relative_x)
        new_node.make_immutable()
        new_model_tree = path.replace(new_node, root_node=new_model_tree)

        # Update the reference that the document node keeps on the node with the cursor in it.
        new_node = new_model_tree.make_mutable_copy()
        new_node.cursor_node_path = path
        new_node.make_immutable()
        new_model_tree = new_node

        history.global_history_manager.update_model_tree(new_model_tree=new_model_tree)

        return True

    def get_text(self):
        return self._text

    # Override.
    def paint_decoration(self, *, painter: QtGui.QPainter):
        super().paint_decoration(painter=painter)

        painter.setPen(COLOR_BLACK)
        painter.setFont(self.get_model_node().font)
        painter.drawText(self.get_inner_qrect(), self.get_text())

        if b_draw_debug_text_outline:
            painter.setPen(COLOR_RED)
            painter.drawRect(self.get_inner_qrect())
