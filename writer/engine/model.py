class ModelNode:
    def __init__(self, *, name: str):
        self.__name = name
        self._children: list[ModelNode] = []

    def add_child(self, child_node: "ModelNode"):
        self._children.append(child_node)

    def children(self):
        return self._children

class DocumentModelNode(ModelNode):
    def __init__(self):
        super().__init__(name="DocumentModelNode")

class ParagraphModelNode(ModelNode):
    def __init__(self, *, text: str):
        super().__init__(name="ParagraphModelNode")

        self._text = text

    def get_text(self) -> str:
        return self._text
