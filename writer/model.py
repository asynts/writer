from common import Node 

class ModelNode(Node):
    def append_child(self, child: "ModelNode"):
        assert isinstance(child, ModelNode)
        return super().append_child(child)
    
class DocumentModelNode(ModelNode):
    def __init__(self):
        super().__init__("Document")

        self.header_node = ParagraphModelNode()
        self.footer_node = ParagraphModelNode()

    def to_string(self, *, indent=0, prefix=""):
        result = super().to_string(indent=indent, prefix=prefix)
        result += self.header_node.to_string(indent=indent + 1, prefix="<header> ")
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
