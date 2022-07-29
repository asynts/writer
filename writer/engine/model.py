import dataclasses

from PyQt6 import QtGui

import writer.engine.layout as layout
import writer.engine.tree as tree

@dataclasses.dataclass(frozen=True, kw_only=True, slots=True)
class ModelStyle:
    is_bold: bool = None
    is_italic: bool = None
    font_size: int = None

# This class keeps track of the model styles that we encountered.
# Each style can override some properties, the most recent one is returned by the helpers.
class ModelStyleCascade:
    def __init__(self, model_style_list: list[ModelStyle]):
        self.__model_style_list = model_style_list

        # Cache.
        self.__font: QtGui.QFont = None

        # Cache.
        self.__font_metrics: QtGui.QFontMetricsF = None

    def _recursive_lookup(self, name: str):
        for model_style in reversed(self.__model_style_list):
            if getattr(model_style, name) is not None:
                return getattr(model_style, name)
        raise AssertionError

    def push_style(self, model_style: ModelStyle):
        self.__model_style_list.append(model_style)

        self.__font = None
        self.__font_metrics = None

    def pop_style(self, model_style: ModelStyle):
        poped_model_style = self.__model_style_list.pop()
        assert model_style == poped_model_style

        self.__font = None
        self.__font_metrics = None

    def copy_with(self, model_style: ModelStyle) -> "ModelStyleCascade":
        return ModelStyleCascade(self.__model_style_list + [model_style])

    @property
    def is_bold(self) -> bool:
        return self._recursive_lookup("is_bold")

    @property
    def is_italic(self) -> bool:
        return self._recursive_lookup("is_italic")

    @property
    def font_size(self) -> int:
        return self._recursive_lookup("font_size")

    @property
    def font(self):
        if self.__font is not None:
            return self.__font

        weight = QtGui.QFont.Weight.Normal
        if self.is_bold:
            weight = QtGui.QFont.Weight.Bold

        self.__font = QtGui.QFont("monospace", int(self.font_size), weight, self.is_italic)
        return self.__font

    @property
    def font_metrics(self):
        if self.__font_metrics is not None:
            return self.__font_metrics

        self.__font_metrics = QtGui.QFontMetricsF(self.font)
        return self.__font_metrics

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
        assert self.is_mutable
        self.__style = value

class DocumentModelNode(ModelNode):
    __slots__ = (
        "__cursor_node_path",
    )

    def __init__(
        self,
        *,
        style: ModelStyle,
        **kwargs
    ):
        super().__init__(style=style, **kwargs)

        # Property.
        self.__cursor_node_path: tree.NodePath = None

    # Override.
    def dump(self, *, name: str = "DocumentModelNode", indent: int = 0):
        return super().dump(name=name, indent=indent)

    @property
    def cursor_node_path(self):
        return self.__cursor_node_path

    @cursor_node_path.setter
    def cursor_node_path(self, value: tree.NodePath):
        assert self.is_mutable
        self.__cursor_node_path = value

class TextChunkModelNode(ModelNode):
    __slots__ = (
        "__text",
        "__cursor_offset",
    )

    def __init__(self, *, text: str, cursor_offset: int = None, **kwargs):
        super().__init__(**kwargs)

        # Property.
        self.__text = text

        # Property.
        self.__cursor_offset: int = cursor_offset

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
