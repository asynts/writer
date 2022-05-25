class ModelNode:
    def __init__(self, name: str):
        self.name = name
        self.children = []

    def append_child(self, child: "ModelNode"):
        assert isinstance(child, ModelNode)
        self.children.append(child)
        return child
    
    def to_string_header(self):
        return f"{self.name}()"

    def to_string(self, *, indent=0, prefix=""):
        result = ""

        result += " " * (indent * 2)
        result += prefix + self.to_string_header() + "\n"

        for child in self.children:
            result += child.to_string(indent=indent + 1, prefix="<child> ")
        
        return result

    def __str__(self):
        return self.to_string()

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
