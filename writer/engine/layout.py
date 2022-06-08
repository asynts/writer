import enum
import typing

from PyQt6 import QtGui, QtCore
from PyQt6.QtGui import QColor

from .style import Spacing, LayoutStyle

normal_font = QtGui.QFont("monospace", 12)
normal_font_metrics = QtGui.QFontMetricsF(normal_font)

COLOR_WHITE = QColor(255, 255, 255)
COLOR_BLACK = QColor(0, 0, 0)
COLOR_RED = QColor(255, 0, 0)
COLOR_GREEN = QColor(0, 255, 0)
COLOR_BLUE = QColor(0, 0, 255)

def cm_to_pixel(value: float):
    # This is a bit arbitrary, since this depends on the display resolution.
    return 37.795275591 * value / 2

# There are several phases a layout node can be in.
class Phase(enum.Enum):
    # The node has been created and a temporary parent has been assigned.
    PHASE_1_CREATED = 1

    # The node has been permanently placed in a parent node and may not be moved.
    PHASE_2_PLACED = 3

# Properties must not be changed, unless this is explicitly allowed.
class LayoutNode:
    def __init__(
        self,
        *,
        name: str,
        parent_node: "LayoutNode",
        style: LayoutStyle):

        # The phase in which the layout node is in.
        # Some operations can only be performed in some phases.
        # Variable (PHASE_1_CREATED).
        # Constant (PHASE_2_PLACED).
        # Assigned on initialization.
        # Assigned during placed in parent.
        self.__phase = Phase.PHASE_1_CREATED

        # References parent node.
        # Variable (PHASE_1_CREATED).
        # Constant (PHASE_2_PLACED).
        self.__parent_node = parent_node

        # Name of the node for debugging.
        # Constant.
        self.__name = name

        # Position relative to parent node.
        # Includes the padding and border of the parent node.
        # Variable (PHASE_1_CREATED).
        # Constant (PHASE_2_PLACED).
        # Assigned when placed in parent node.
        self._relative_x: int = None
        self._relative_y: int = None

        # How much space is needed to fit all children.
        # Variable (PHASE_1_CREATED).
        # Constant (PHASE_2_PLACED).
        # Assigned when children are added.
        self._width_of_children = 0
        self._height_of_children = 0

        # Style applied to this node.
        # Constant.
        self.__style = style

    def get_phase(self):
        return self.__phase

    def get_style(self):
        return self.__style

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

    # Child nodes must not be changed after they are placed in their parent node.
    # Virtual.
    def on_placed_in_node(self, *, relative_x: int, relative_y: int):
        assert self.__phase == Phase.PHASE_1_CREATED
        self.__phase = Phase.PHASE_2_PLACED

        self._relative_x = relative_x
        self._relative_y = relative_y

    def get_parent_node(self) -> "LayoutNode":
        return self.__parent_node

    def get_relative_x(self) -> float:
        assert self.get_phase() == Phase.PHASE_2_PLACED
        return self._relative_x

    def get_relative_y(self) -> float:
        assert self.get_phase() == Phase.PHASE_2_PLACED
        return self._relative_y

    def get_absolute_x(self) -> float:
        assert self.get_phase() == Phase.PHASE_2_PLACED

        if self.__parent_node is None:
            assert self.get_style().outer_spacing.left == 0
            return 0
        else:
            return self.__parent_node.get_absolute_x() + self._relative_x

    def get_absolute_y(self) -> float:
        assert self.get_phase() == Phase.PHASE_2_PLACED

        if self.__parent_node is None:
            assert self.get_style().outer_spacing.top == 0
            return 0
        else:
            return self.__parent_node.get_absolute_y() + self._relative_y

    def get_fixed_width(self) -> float:
        return self.__style.fixed_width

    def get_fixed_height(self) -> float:
        return self.__style.fixed_height

    def get_min_width(self) -> float:
        if self.get_fixed_width() is not None:
            return self.get_fixed_width()
        else:
            return self._width_of_children + self.get_style().inner_spacing.x

    # Virtual.
    def get_width(self) -> float:
        assert self.get_phase() == Phase.PHASE_2_PLACED
        return self.get_min_width()

    def get_min_height(self) -> float:
        if self.get_fixed_height() is not None:
            return self.get_fixed_height()
        else:
            return self._height_of_children + self.get_style().inner_spacing.y

    def get_height(self) -> float:
        assert self.get_phase() == Phase.PHASE_2_PLACED
        return self.get_min_height()

    def get_min_inner_height(self):
        return self._height_of_children

    def get_min_inner_width(self):
        return self._width_of_children

    # Virtual.
    def get_children(self) -> list["LayoutNode"]:
        return []

    def get_qrect(self):
        assert self.get_phase() == Phase.PHASE_2_PLACED

        return QtCore.QRectF(
            self.get_absolute_x(),
            self.get_absolute_y(),
            self.get_width(),
            self.get_height(),
        )

    def get_inner_qrect(self):
        assert self.get_phase() == Phase.PHASE_2_PLACED

        return self.get_qrect().adjusted(
            self.get_style().inner_spacing.left,
            self.get_style().inner_spacing.top,
            -self.get_style().inner_spacing.x,
            -self.get_style().inner_spacing.y,
        )

    def paint_background(self, *, painter: QtGui.QPainter):
        assert self.get_phase() == Phase.PHASE_2_PLACED

        if self.get_style().background_color is not None:
            painter.fillRect(self.get_qrect(), self.get_style().background_color)

    def paint_border(self, *, painter: QtGui.QPainter):
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
        pass

    def paint(self, *, painter: QtGui.QPainter):
        assert self.get_phase() == Phase.PHASE_2_PLACED

        self.paint_background(painter=painter)
        self.paint_border(painter=painter)
        self.paint_decoration(painter=painter)

        for child in self.get_children():
            child.paint(painter=painter)

class BlockLayoutNode(LayoutNode):
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
    def __init__(self, *, name="HorizontalLayoutNode", **kwargs):
        super().__init__(name=name, **kwargs)

    def get_max_remaining_width(self) -> float:
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

    # FIXME: Do we need to override 'get_height' here?

    def place_child_node(self, child_node: LayoutNode):
        assert self.get_phase() == Phase.PHASE_1_CREATED

        child_node.on_placed_in_node(
            relative_x=self.get_style().inner_spacing.left + child_node.get_style().outer_spacing.left + self._width_of_children,
            relative_y=self.get_style().inner_spacing.top + child_node.get_style().outer_spacing.top,
        )
        self._width_of_children += child_node.get_width() + child_node.get_style().outer_spacing.x

        self._height_of_children = max(
            self._height_of_children,
            child_node.get_height() + child_node.get_style().outer_spacing.y,
        )

        self._children.append(child_node)

class VerticalLayoutNode(BlockLayoutNode):
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
    def __init__(self, parent_node: "LayoutNode"):
        super().__init__(
            name="PageLayoutNode",
            parent_node=parent_node,

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

            style=LayoutStyle(
                fixed_height=header_height,

                background_color=COLOR_GREEN,
            ),
        )

        self.__content_node = VerticalLayoutNode(
            parent_node=self,

            style=LayoutStyle(
                fixed_height=content_height,
                background_color=COLOR_BLUE,
            ),
        )

        self.__footer_node = VerticalLayoutNode(
            parent_node=self,

            style=LayoutStyle(
                fixed_height=footer_height,
                background_color=COLOR_RED,
            ),
        )

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

class TextChunkLayoutNode(LayoutNode):
    def __init__(self, *, text: str, parent_node: LayoutNode, font_size: float, is_bold: bool, is_italic: bool):
        font, font_metrics = self._compute_font(font_size=font_size, is_bold=is_bold, is_italic=is_italic)

        rendered_size = font_metrics.size(0, text)

        super().__init__(
            name="InlineTextChunkLayoutNode",
            parent_node=parent_node,

            style=LayoutStyle(
                # The fixed size includes the border, therefore, the odd calculation.
                fixed_width=rendered_size.width() + 2,
                fixed_height=rendered_size.height() + 2,

                border_spacing=Spacing(left=1, right=1, top=1, bottom=1),

                border_color=COLOR_RED,
            ),
        )

        self._text = text
        self._font = font
        self._font_metrics = font_metrics

    def _compute_font(self, *, font_size: float, is_bold: bool, is_italic: bool) -> typing.Tuple[QtGui.QFont, QtGui.QFontMetricsF]:
        weight = QtGui.QFont.Weight.Normal
        if is_bold:
            weight = QtGui.QFont.Weight.Bold

        font = QtGui.QFont(
            "monospace",
            int(font_size),
            weight,
            is_italic,
        )

        font_metrics = QtGui.QFontMetricsF(font)

        return font, font_metrics

    def get_font(self):
        return self._font

    def get_font_metrics(self):
        return self._font_metrics

    def get_text(self):
        return self._text

    # Override.
    def paint_decoration(self, *, painter: QtGui.QPainter):
        super().paint_decoration(painter=painter)

        painter.setFont(self._font)
        painter.drawText(self.get_inner_qrect(), self.get_text())
