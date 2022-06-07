class ModelNode:
    def __init__(self, *, name: str):
        self.__name = name
        self._children: list[ModelNode] = []

    def add_child(self, child_node: "ModelNode"):
        self._children.append(child_node)
        return child_node

    def get_children(self):
        return self._children

class DocumentModelNode(ModelNode):
    def __init__(self):
        super().__init__(name="DocumentModelNode")

class TextChunkModelNode(ModelNode):
    def __init__(self, *, text: str):
        super().__init__(name="TextChunkModelNode")

        self.__text = text
    
    def get_text(self):
        return self.__text

class ParagraphModelNode(ModelNode):
    def __init__(self):
        super().__init__(name="ParagraphModelNode")
