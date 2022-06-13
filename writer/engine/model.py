import enum

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

class ModelPhase(enum.Enum):
    # When a model node is first created, it is mutable.
    #
    # Some properties are derived from other properties and are cached inside the object.
    # They must not be accessed before the object becomes immutable.
    PHASE_1_MUTABLE = 1

    # One a model node has been fully initialized, it becomes immutable.
    # Nodes must be in this phase before they can become children of other nodes.
    #
    # Note that there are some special properties that can still change in immutable nodes.
    # However, this is restricted to caching the result of something derived from other immutable properties.
    PHASE_2_IMMUTABLE = 2

class ModelNode:
    __slots__ = (
        "__style",
        "__children",
        "_phase",
    )

    def __init__(self, *, style: ModelStyle, children: list["ModelNode"]):
        # Property.
        self.__children = children

        # Property.
        self.__style = style

        self._phase = ModelPhase.PHASE_1_MUTABLE

    def finalize(self):
        assert self._phase == ModelPhase.PHASE_1_MUTABLE
        self._phase = ModelPhase.PHASE_2_IMMUTABLE

    def append_child(self, child_node: "ModelNode"):
        assert self._phase == ModelPhase.PHASE_1_MUTABLE
        self.__children.append(child_node)
        return child_node

    # Virtual.
    def dump_properties(self):
        return ""

    # Virtual.
    def dump(self, *, name: str = "ModelNode", indent: int = 0):
        result = ""
        result += " " * indent
        result += f"{name}("
        result += self.dump_properties()
        result += ")\n"

        for child_node in self.children:
            result += child_node.dump(indent=indent+1)

        return result

    @property
    def children(self):
        return self.__children

    @children.setter
    def children(self, value: list["ModelNode"]):
        assert self._phase == ModelPhase.PHASE_1_MUTABLE
        self.__children = value

    @property
    def style(self):
        return self.__style

    @style.setter
    def style(self, value: ModelStyle):
        assert self._phase == ModelPhase.PHASE_1_MUTABLE
        self.__style = value

class DocumentModelNode(ModelNode):
    __slots__ = tuple()

    # Virtual.
    def dump(self, *, name: str = "DocumentModelNode", indent: int = 0):
        return super().dump(name=name, indent=indent)

class TextChunkModelNode(ModelNode):
    __slots__ = (
        "__text",
        "__font",
        "__font_metrics",
    )

    def __init__(self, *, text: str, **kwargs):
        super().__init__(**kwargs)

        # Property.
        self.__text = text

        # Cache.
        self.__font: QtGui.QFont = None

        # Cache.
        self.__font_metrics: QtGui.QFontMetricsF = None

    # Virtual.
    def dump_properties(self):
        return f"text={repr(self.text)}"

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, value: str):
        assert self._phase == ModelPhase.PHASE_1_MUTABLE
        self.__text = value

    @property
    def font(self):
        assert self._phase == ModelPhase.PHASE_2_IMMUTABLE

        if self.__font is not None:
            return self.__font

        weight = QtGui.QFont.Weight.Normal
        if self.style.is_bold:
            weight = QtGui.QFont.Weight.Bold

        self.__font = QtGui.QFont("monospace", int(self.style.font_size), weight, self.style.is_italic)
        return self.__font

    @property
    def font_metrics(self):
        assert self._phase == ModelPhase.PHASE_2_IMMUTABLE

        if self.__font_metrics is not None:
            return self.__font_metrics

        self.__font_metrics = QtGui.QFontMetricsF(self.get_font())
        return self.__font_metrics

class ParagraphModelNode(ModelNode):
    __slots__ = (
        "__layout_nodes",
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Cache.
        self.__layout_nodes: list["layout.VerticalLayoutNode"] = None

    # Virtual.
    def dump(self, *, name: str = "ParagraphModelNode", indent: int = 0):
        return super().dump(name=name, indent=indent)

    def clear_layout_nodes(self):
        assert self._phase == ModelPhase.PHASE_2_IMMUTABLE

        self.__layout_nodes = None

    def assign_layout_nodes(self, layout_nodes: list["layout.VerticalLayoutNode"]):
        assert self._phase == ModelPhase.PHASE_2_IMMUTABLE

        assert self.__layout_nodes is None
        self.__layout_nodes = layout_nodes
