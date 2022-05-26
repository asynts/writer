from common import Node

# FIXME: Setup some rendering thing with actual fonts.
FONT_CHARACTER_WIDTH = 3
FONT_CHARACTER_HEIGHT = 5

class LayoutNode(Node):
    def __init__(self, name: str):
        super().__init__(name)

    def append_child(self, child: "LayoutNode"):
        assert isinstance(child, LayoutNode)
        return super().append_child(child)

    def max_width(self):
        return None
    
    def max_height(self):
        return None

class PageLayoutNode(LayoutNode):
    def __init__(self):
        super().__init__("Page")

        self.header_node = None
        self.footer_node = None
        self.content_nodes = []

    def max_width(self):
        return FONT_CHARACTER_HEIGHT * 10
    
    def max_height(self):
        return FONT_CHARACTER_HEIGHT * 2

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
        return FONT_CHARACTER_HEIGHT * 1

class HeaderLayoutNode(BlockLayoutNode):
    def __init__(self):
        super().__init__("Footer")

    def max_height(self):
        return FONT_CHARACTER_HEIGHT * 1

class TextLayoutNode(LayoutNode):
    def __init__(self, *, text: str):
        super().__init__("Text")
        self.text = text

        self.relative_x = None
        self.relative_y = None

    def to_string_header(self):
        return f"{self.name}(text={repr(self.text)}, x={self.relative_x}, y={self.relative_y})"
