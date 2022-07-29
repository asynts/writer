from PyQt6 import QtGui

import writer.engine.layout as layout
import writer.engine.tree as tree

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

class ModelNode(tree.Node):
    __slots__ = (
        "__style",
    )

    def __init__(self, *, style: ModelStyle, **kwargs):
        super().__init__(**kwargs)

        # Property.
        self.__style = style

    # Override.
    def dump(self, *, name: str = "ModelNode", indent: int = 0):
        return super().dump(name=name, indent=indent)

    @property
    def style(self):
        return self.__style

    @style.setter
    def style(self, value: ModelStyle):
        assert self._is_mutable
        self.__style = value

class DocumentModelNode(ModelNode):
    __slots__ = (
        "_cursor_node_path",
    )

    def __init__(
        self,
        *,
        style: ModelStyle,
        **kwargs
    ):
        super().__init__(style=style, **kwargs)

        # Cache.
        self._cursor_node_path: tree.NodePath = None

    # Override.
    def dump(self, *, name: str = "DocumentModelNode", indent: int = 0):
        return super().dump(name=name, indent=indent)

class TextChunkModelNode(ModelNode):
    __slots__ = (
        "__text",
        "__font",
        "__font_metrics",
        "__cursor_offset",
    )

    def __init__(self, *, text: str, cursor_offset: int = None, **kwargs):
        super().__init__(**kwargs)

        # Property.
        self.__text = text

        # Property.
        self.__cursor_offset: int = cursor_offset

        # Cache.
        self.__font: QtGui.QFont = None

        # Cache.
        self.__font_metrics: QtGui.QFontMetricsF = None

    # Override.
    def dump_properties(self):
        return f"text={repr(self.text)} cursor_offset={repr(self.cursor_offset)}"

    # Override.
    def dump(self, *, name: str = "TextChunkModelNode", indent: int = 0):
        return super().dump(name=name, indent=indent)

    @property
    def cursor_offset(self):
        return self.__cursor_offset

    @cursor_offset.setter
    def cursor_offset(self, value: int):
        assert self.is_mutable
        self.__cursor_offset = value

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, value: str):
        assert self.is_mutable
        self.__text = value

    @property
    def font(self):
        assert not self.is_mutable

        if self.__font is not None:
            return self.__font

        weight = QtGui.QFont.Weight.Normal
        if self.style.is_bold:
            weight = QtGui.QFont.Weight.Bold

        self.__font = QtGui.QFont("monospace", int(self.style.font_size), weight, self.style.is_italic)
        return self.__font

    @property
    def font_metrics(self):
        assert not self.is_mutable

        if self.__font_metrics is not None:
            return self.__font_metrics

        self.__font_metrics = QtGui.QFontMetricsF(self.font)
        return self.__font_metrics

class ParagraphModelNode(ModelNode):
    __slots__ = (
        "__layout_nodes",
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Cache.
        self.__layout_nodes: list["layout.VerticalLayoutNode"] = None

    # Override.
    def make_mutable_copy(self):
        copy_ = super().make_mutable_copy()
        copy_.__layout_nodes = None
        return copy_

    # Override.
    def dump(self, *, name: str = "ParagraphModelNode", indent: int = 0):
        return super().dump(name=name, indent=indent)

    @property
    def layout_nodes(self):
        return self.__layout_nodes

    @layout_nodes.setter
    def layout_nodes(self, value: list["layout.VerticalLayoutNode"]):
        assert not self.is_mutable
        self.__layout_nodes = value
