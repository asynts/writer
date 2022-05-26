from common import Node

import pygame

normal_font: pygame.font.Font = None

font_width: int = None
font_height: int = None

class LayoutNode(Node):
    def __init__(self, name: str):
        super().__init__(name)

        self.relative_x = 0
        self.relative_y = 0

    def append_child(self, child: "LayoutNode"):
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

class PageLayoutNode(LayoutNode):
    def __init__(self):
        super().__init__("Page")

        self.header_node = None
        self.footer_node = None
        self.content_nodes = []

    def max_width(self):
        width, height = normal_font.size("x")
        return 10 * font_width
    
    def max_height(self):
        return 3 * font_height

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
    
    def max_width(self):
        if self.parent is None:
            return None
        else:
            return self.parent.max_width()

    def max_height(self):
        if self.parent is None:
            return None
        else:
            return self.parent.max_height()

class FooterLayoutNode(BlockLayoutNode):
    def __init__(self):
        super().__init__("Footer")

    def max_height(self):
        return 1 * font_height

class HeaderLayoutNode(BlockLayoutNode):
    def __init__(self):
        super().__init__("Footer")

    def max_height(self):
        return 1 * font_height

class TextLayoutNode(LayoutNode):
    def __init__(self, *, text: str):
        super().__init__("Text")
        self.text = text

    def to_string_header(self):
        return f"{self.name}(text={repr(self.text)}, x={self.relative_x}, y={self.relative_y})"
