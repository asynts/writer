from common import Node

import pygame
import enum

normal_font: pygame.font.Font = None

font_width: int = None
font_height: int = None

@enum.Enum
class OverflowStrategy:
    TRUNCATE = 0

class LayoutNode:
    def __init__(self, *, name: str):
        # Name of the node.
        # This is usually the name of the class.
        self._name = name

        # Reference to parent node.
        # Assigned when inserting into parent node.
        self._parent_node: LayoutNode = None

        # Position in parent node.
        # Assigned when inserting into parent node.
        self._relative_x: int = None
        self._relative_y: int = None

        # How much space is needed to fit all children.
        # Updated as nodes are inserted.
        self._width_of_children = 0
        self._height_of_children = 0

        # FIXME: Documentation
        self._overflow_strategy = OverflowStrategy.TRUNCATE

    def on_placed_in_node(self, parent_node: "LayoutNode", *, relative_x: int, relative_y: int):
        assert self._parent_node is None
        self._parent_node = parent_node

        assert self._relative_x is None
        self._relative_x = relative_x

        assert self._relative_y is None
        self._relative_y = relative_y

    def get_relative_x(self) -> float:
        assert self._relative_x is not None
        return self._relative_x

    def get_relative_y(self) -> float:
        assert self._relative_y is not None
        return self._relative_y

    def get_absolute_x(self) -> float:
        assert self._parent_node is not None
        assert self._relative_x is not None
        return self._parent_node.get_absolute_x() + self._relative_x

    def get_absolute_y(self) -> float:
        assert self._parent_node is not None
        assert self._relative_y is not None
        return self._parent_node.get_absolute_y() + self._relative_y

    def get_min_width(self) -> float:
        return self._width_of_children

    def get_min_height(self) -> float:
        return self._height_of_children

    def get_width(self) -> float:
        return self.get_min_width()

    def get_height(self) -> float:
        return self.get_min_height()

class BlockLayoutNode(LayoutNode):
    def get_max_width(self) -> float:
        assert isinstance(self._parent_node, BlockLayoutNode)
        return self._parent_node.get_max_width()

    def get_max_height(self) -> float:
        assert isinstance(self._parent_node, BlockLayoutNode)
        return self._parent_node.get_max_height()

    def get_width(self) -> float:
        return self.get_max_width()

    # FIXME: place_node

# FIXME: Make it possible to define constraints on block nodes and then remove these specialized nodes.
#        Maybe, there can be a page layout node that just generates the children itself (that have constraints)
#        and then makes them accessible via getter methods?

# FIXME: Generalize this to ConstraintLayoutNode or something like that.
class PageBlockLayoutNode(BlockLayoutNode):
    def __init__(self):
        super().__init__(name="PageBlockLayoutNode")

    def get_min_width(self) -> float:
        return 15 * font_width
    
    def get_min_height(self) -> float:
        return 5 * font_height

    def get_max_width(self) -> float:
        return self.get_min_width()

    def get_max_height(self) -> float:
        return self.get_min_height()

    # FIXME: footer, header.

# This is used to model header and footer nodes.
# FIXME: It would be better to just have a normal block that is constrained by the page block node.
class DecorationBlockLayoutNode(BlockLayoutNode):
    def __init__(self):
        super().__init__(name="DecorationBlockLayoutNode")
    
    def get_min_height(self) -> float:
        return 1 * font_height

    def get_max_height(self) -> float:
        return self.get_min_height()

# FIXME: Integrate the remaining stuff.

class LayoutNode(Node):
    def __init__(self, name: str):
        super().__init__(name)

        self.relative_x = 0
        self.relative_y = 0

        self.fixed_width = None
        self.fixed_height = None

    def append_child(self, child: "LayoutNode") -> "LayoutNode":
        assert isinstance(child, LayoutNode)
        return super().append_child(child)

    def max_width(self):
        return None
    
    def max_height(self):
        return None

    def absolute_x(self):
        if self.parent is None:
            return self.relative_x
        else:
            return self.relative_x + self.parent.absolute_x()

    def absolute_y(self):
        if self.parent is None:
            return self.relative_y
        else:
            return self.relative_y + self.parent.absolute_y()

    def max_width(self):
        if self.fixed_width is None:
            if self.parent is None:
                return None
            else:
                return self.parent.max_width()
        else:
            return self.fixed_width

    def max_height(self):
        if self.fixed_height is None:
            if self.parent is None:
                return None
            else:
                return self.parent.max_height()
        else:
            return self.fixed_height

class PageLayoutNode(LayoutNode):
    def __init__(self):
        super().__init__("Page")

        self.header_node = None
        self.footer_node = None
        self.content_nodes = []
        self.main_region = None

        self.fixed_width = 15 * font_width
        self.fixed_height = 3 * font_height

    def set_header_node(self, node: LayoutNode):
        assert self.header_node is None
        assert isinstance(node, HeaderLayoutNode)
        self.append_child(node)
        self.header_node = node
        return node

    def set_footer_node(self, node: LayoutNode):
        assert self.footer_node is None
        assert isinstance(node, FooterLayoutNode)
        self.append_child(node)
        self.footer_node = node
        return node

    def add_content_node(self, node: LayoutNode):
        self.append_child(node)
        self.content_nodes.append(node)
        return node

    def to_string(self, *, indent=0, prefix=""):
        result = ""

        result += " " * indent
        result += prefix + self.to_string_header() + "\n"

        if self.header_node is not None:
            result += self.header_node.to_string(indent=indent + 1, prefix="<header> ")

        for child in self.content_nodes:
            result += child.to_string(indent=indent + 1, prefix="<content> ")

        if self.footer_node is not None:
            result += self.footer_node.to_string(indent=indent + 1, prefix="<footer> ")

        return result

class BlockLayoutNode(LayoutNode):
    def __init__(self, name="Block"):
        super().__init__(name)

class FooterLayoutNode(BlockLayoutNode):
    def __init__(self):
        super().__init__("Footer")

        self.fixed_height = 1 * font_height

class HeaderLayoutNode(BlockLayoutNode):
    def __init__(self):
        super().__init__("Footer")

        self.fixed_height = 1 * font_height

class TextLayoutNode(LayoutNode):
    def __init__(self, *, text: str):
        super().__init__("Text")

        self.text = text

    def to_string_header(self):
        return f"{self.name}(text={repr(self.text)}, x={self.relative_x}, y={self.relative_y})"
