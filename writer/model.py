from ast import Mod
from common import Node 

class ModelNode(Node):
    def append_child(self, child: "ModelNode"):
        assert isinstance(child, ModelNode)
        return super().append_child(child)

class DocumentModelNode(ModelNode):
    def __init__(self):
        super().__init__("Document")

        self.header_node = None
        self.footer_node = None
        self.content_nodes = []

    def add_content_node(self, node: ModelNode):
        self.append_child(node)
        self.content_nodes.append(node)
        return node

    def set_header_node(self, node: ModelNode):
        assert self.header_node is None
        self.append_child(node)
        self.header_node = node
        return node

    def set_footer_node(self, node: ModelNode):
        assert self.footer_node is None
        self.append_child(node)
        self.footer_node = node
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

class ParagraphModelNode(ModelNode):
    def __init__(self):
        super().__init__("Paragraph")

class TextChunkModelNode(ModelNode):
    def __init__(self, *, text: str):
        super().__init__("TextChunk")

        self.text = text

    def to_string_header(self):
        return f"{self.name}(text={repr(self.text)})";

class FieldChunkModelNode(ModelNode):
    def __init__(self, *, field: str):
        super().__init__("FieldChunk")

        self.field = field

    def to_string_header(self):
        return f"{self.name}(field={repr(self.field)})";
