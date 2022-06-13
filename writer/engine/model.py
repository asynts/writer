from PyQt6 import QtGui

import writer.engine.layout as layout

# This is where the "cascade" happens.
# We take the style from the parent and then override some of the values.
# This happens recursively.
#
# Note, that this is not the style that will be used for rendering later.
# The layout style can be derived from this class, however, that process is context dependent.
class ModelStyle:
    __slots__ = (
        "_parent_model_style",
        "_is_bold",
        "_is_italic",
        "_font_size",
    )

    def __init__(
        self,
        *,
        parent_model_style: "ModelStyle",
        is_bold: bool = None,
        is_italic: bool = None,

        # FIXME: Qt wants this to be an integer, we later have to truncate it.
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
    __slots__ = (
        "__name",
        "__children",
        "__style",
        "__parent_node",
    )

    def __init__(self, *, name: str, style: ModelStyle, parent_node: "ModelNode" = None):
        self.__name = name
        self.__children: list[ModelNode] = []
        self.__style = style
        self.__parent_node = parent_node

    def get_parent(self):
        return self.__parent_node

    def add_child(self, child_node: "ModelNode"):
        self.__children.append(child_node)
        return child_node

    def get_style(self) -> ModelStyle:
        return self.__style

    def get_children(self):
        return self.__children

class DocumentModelNode(ModelNode):
    __slots__ = tuple()

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
    __slots__ = (
        "__text",
        "__font",
        "__font_metrics",
    )

    def __init__(self, *, text: str, style: ModelStyle, parent_node: ModelNode):
        super().__init__(name="TextChunkModelNode", style=style, parent_node=parent_node)

        self.__text = text
        self.__font = None
        self.__font_metrics = None

    def get_text(self):
        return self.__text

    def set_text(self, text: str):
        self.__text = text

    def get_font(self):
        if self.__font is not None:
            return self.__font

        style = self.get_style()

        weight = QtGui.QFont.Weight.Normal
        if style.is_bold:
            weight = QtGui.QFont.Weight.Bold

        self.__font = QtGui.QFont("monospace", int(style.font_size), weight, style.is_italic)
        return self.__font

    def get_font_metrics(self):
        if self.__font_metrics is not None:
            return self.__font_metrics

        self.__font_metrics = QtGui.QFontMetricsF(self.get_font())
        return self.__font_metrics

class ParagraphModelNode(ModelNode):
    __slots__ = (
        "__layout_nodes",
    )

    def __init__(self, *, style: ModelStyle, parent_node: ModelNode):
        super().__init__(name="ParagraphModelNode", style=style, parent_node=parent_node)

        # The layout nodes that are used to render this paragraph.
        # If this paragraph overflows a page or multiple pages, there can be multiple layout nodes.
        self.__layout_nodes: list["layout.VerticalLayoutNode"] = None

    def clear_layout_nodes(self):
        self.__layout_nodes = None

    def assign_layout_nodes(self, layout_nodes: list["layout.VerticalLayoutNode"]):
        assert self.__layout_nodes is None
        self.__layout_nodes = layout_nodes
