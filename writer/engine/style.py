import dataclasses

from PyQt6.QtGui import QColor as Color

@dataclasses.dataclass(kw_only=True, frozen=True, slots=True)
class Spacing:
    left: int = 0
    right: int = 0
    top: int = 0
    bottom: int = 0

    def __add__(self, other: "Spacing"):
        return Spacing(
            left=self.left + other.left,
            right=self.right + other.right,
            top=self.top + other.top,
            bottom=self.bottom + other.bottom,
        )

    @property
    def x(self):
        return self.left + self.right

    @property
    def y(self):
        return self.top + self.bottom

class LayoutStyle:
    __slots__ = (
        "__fixed_width",
        "__fixed_height",
        "__margin_spacing",
        "__border_spacing",
        "__padding_spacing",
        "__background_color",
        "__border_color",
    )

    def __init__(
        self,
        *,

        # Some nodes define their exact dimensions independent of other nodes.
        fixed_width: float = None,
        fixed_height: float = None,

        # Spacing of this node, the margin does not contribute to the size of the node, the others do.
        margin_spacing: Spacing = None,
        border_spacing: Spacing = None,
        padding_spacing: Spacing = None,

        # The colors of this node.
        background_color: Color = None,
        border_color: Color = None):

        self.__fixed_width = fixed_width
        self.__fixed_height = fixed_height

        if margin_spacing is None:
            margin_spacing = Spacing()
        if border_spacing is None:
            border_spacing = Spacing()
        if padding_spacing is None:
            padding_spacing = Spacing()

        self.__margin_spacing = margin_spacing
        self.__border_spacing = border_spacing
        self.__padding_spacing = padding_spacing

        self.__background_color = background_color
        self.__border_color = border_color

    @property
    def fixed_width(self):
        return self.__fixed_width

    @property
    def fixed_height(self):
        return self.__fixed_height

    @property
    def margin_spacing(self):
        return self.__margin_spacing

    @property
    def border_spacing(self):
        return self.__border_spacing

    @property
    def padding_spacing(self):
        return self.__padding_spacing

    @property
    def background_color(self):
        return self.__background_color

    @property
    def border_color(self):
        return self.__border_color

    @property
    def inner_spacing(self):
        return self.__border_spacing + self.__padding_spacing

    @property
    def outer_spacing(self):
        return self.__margin_spacing

    @property
    def all_spacing(self):
        return self.__margin_spacing + self.__border_spacing + self.__padding_spacing
