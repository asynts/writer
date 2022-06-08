# This is where the "cascade" happens.
# We take the style from the parent and then override some of the values.
# This happens recursively.
#
# Note, that this is not the style that will be used for rendering later.
# The layout style can be derived from this class, however, that process is context dependent.
class ModelStyle:
    def __init__(
        self,
        *,
        parent_model_style: "ModelStyle",
        is_bold: bool = None,
        is_italic: bool = None,
        font_size: float = None
    ):
        self._parent_model_style = parent_model_style
        self._is_bold = is_bold
        self._is_italic = is_italic
        self._font_size = font_size

    def _get_property(self, name: str):
        if getattr(self, name) is None:
            assert self._parent_model_style is not None
            return self._parent_model_style._get_property(name)
        else:
            return getattr(self, name)

    @property
    def is_bold(self) -> bool:
        return self._get_property("_is_bold")

    @property
    def is_italic(self) -> bool:
        return self._get_property("_is_italic")

    @property
    def font_size(self) -> bool:
        return self._get_property("_font_size")

class ModelNode:
    def __init__(self, *, name: str, style: ModelStyle):
        self.__name = name
        self.__children: list[ModelNode] = []
        self.__style = style

    def add_child(self, child_node: "ModelNode"):
        self.__children.append(child_node)
        return child_node

    def get_style(self) -> ModelStyle:
        return self.__style

    def get_children(self):
        return self.__children

class DocumentModelNode(ModelNode):
    def __init__(self):
        super().__init__(
            name="DocumentModelNode",

            # Global default style.
            style=ModelStyle(
                parent_model_style=None,
                is_bold=False,
                is_italic=False,
                font_size=None,
            ),
        )

class TextChunkModelNode(ModelNode):
    def __init__(self, *, text: str, style: ModelStyle):
        super().__init__(name="TextChunkModelNode", style=style)

        self.__text = text

    def get_text(self):
        return self.__text

class ParagraphModelNode(ModelNode):
    def __init__(self, *, style: ModelStyle):
        super().__init__(name="ParagraphModelNode", style=style)
