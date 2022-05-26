from common import Node

class LayoutNode(Node):
    def append_child(self, child: "LayoutNode"):
        assert isinstance(child, LayoutNode)
        return super().append_child(child)

class PageLayoutNode(LayoutNode):
    def __init__(self):
        super().__init__("Page")

        self.header_node = None
        self.footer_node = None
        self.content_nodes = []

    def set_header_node(self, node: LayoutNode):
        assert self.header_node is None
        self.append_child(node)
        self.header_node = node
        return node

    def set_footer_node(self, node: LayoutNode):
        assert self.footer_node is None
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
    def __init__(self):
        super().__init__("Block")

class TextLayoutNode(LayoutNode):
    def __init__(self, *, text: str):
        super().__init__("Text")
        self.text = text

    def to_string_header(self):
        return f"{self.name}(text={repr(self.text)})"
