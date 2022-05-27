import dataclasses
import typing
import pygame

# Initialized by 'writer.__main__.main'.
# FIXME: Find a better way to achieve this.
normal_font: pygame.font.Font = None
font_width: int = None
font_height: int = None

COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (0, 0, 255)

Color = typing.Tuple[int, int, int]

@dataclasses.dataclass(kw_only=True, frozen=True)
class Spacing:
    left: int = 0
    right: int = 0
    top: int = 0
    bottom: int = 0

# Properties must not be changed, unless this is explicitly allowed.
class LayoutNode:
    def __init__(
        self,
        *,
        name: str,
        fixed_width: int = None,
        fixed_height: int = None,
        background_color: Color = None,
        border_color: Color = None,
        border_spacing: Spacing = None,
        padding_spacing: Spacing = None,
        margin_spacing: Spacing = None):

        if border_spacing is None:
            border_spacing = Spacing()
        if padding_spacing is None:
            padding_spacing = Spacing()
        if margin_spacing is None:
            margin_spacing = Spacing()
 
        # Name of the node for debugging.
        # Constant.
        # Assigned during initialization.
        self.__name = name

        # References parent node.
        # Constant.
        # Assigned when inserted into parent node.
        self.__parent_node: LayoutNode = None

        # Position in parent node.
        # Variable.
        # Assigned when inserted into parent node.
        # FIXME: Assigned when rebuilding layout tree.
        self._relative_x: int = None
        self._relative_y: int = None

        # How much space is needed to fit all children.
        # Variable.
        # Assigned when children are added.
        self._width_of_children = 0
        self._height_of_children = 0

        # Some nodes define their exact width independent of other nodes.
        # Variable.
        # Assigned during initialization.
        # FIXME: Assigned when rebuilding layout tree.
        self.__fixed_width = fixed_width
        self.__fixed_height = fixed_height

        # The colors of this node.
        # Constant.
        # Assigned during initialization.
        self.__background_color = background_color
        self.__border_color = border_color
        
        # Spacing of this noce.
        # Constant.
        # Assigned during initialization.
        self.__border_spacing = border_spacing
        self.__margin_spacing = margin_spacing
        self.__padding_spacing = padding_spacing

    # Child nodes must not be changed after they are placed in their parent node.
    # FIXME: When the parent node updates it's layout, it can update the children, but that is the only exception.
    def on_placed_in_node(self, parent_node: "LayoutNode", *, relative_x: int, relative_y: int):
        assert self.__parent_node is None
        self.__parent_node = parent_node

        assert self._relative_x is None
        self._relative_x = relative_x

        assert self._relative_y is None
        self._relative_y = relative_y

    def get_background_color(self) -> Color:
        return self.__background_color

    def get_parent_node(self) -> "LayoutNode":
        return self.__parent_node

    def get_relative_x(self) -> float:
        assert self._relative_x is not None
        return self._relative_x

    def get_relative_y(self) -> float:
        assert self._relative_y is not None
        return self._relative_y

    def get_absolute_x(self) -> float:
        if self.__parent_node is None:
            assert self._relative_x is None
            return 0
        else:
            assert self._relative_x is not None
            return self.__parent_node.get_absolute_x() + self._relative_x

    def get_absolute_y(self) -> float:
        if self.__parent_node is None:
            assert self._relative_y is None
            return 0
        else:
            assert self._relative_y is not None
            return self.__parent_node.get_absolute_y() + self._relative_y

    def get_fixed_width(self) -> float:
        return self.__fixed_width

    def get_fixed_height(self) -> float:
        return self.__fixed_height

    # Virtual.
    def get_width(self) -> float:
        if self.__fixed_width is not None:
            return self.__fixed_height
        else:
            return self._width_of_children \
                + self.__padding_spacing.left + self.__padding_spacing.right \
                + self.__border_spacing.left + self.__border_spacing.right

    def get_height(self) -> float:
        if self.__fixed_height is not None:
            return self.__fixed_height
        else:
            return self._height_of_children \
                + self.__padding_spacing.top + self.__padding_spacing.bottom \
                + self.__border_spacing.top + self.__border_spacing.bottom

    def get_margin_spacing(self):
        return self.__margin_spacing

    def get_border_spacing(self):
        return self.__border_spacing

    def get_padding_spacing(self):
        return self.__padding_spacing

    def get_border_color(self):
        return self.__border_color

    # FIXME: get_inner_spacing
    # FIXME: get_outer_spacing

    # Virtual.
    def get_children(self):
        return []

class BlockLayoutNode(LayoutNode):
    def __init__(self, *, name="BlockLayoutNode", **kwargs):
        super().__init__(name=name, **kwargs)

        self._children: list[LayoutNode] = []

    def get_max_inner_width(self) -> float:
        if self.get_fixed_width() is None:
            assert isinstance(self.get_parent_node(), BlockLayoutNode)
            return self.get_parent_node().get_max_inner_width() \
                - self.get_padding_spacing().left - self.get_padding_spacing().right \
                - self.get_border_spacing().left - self.get_border_spacing().right \
                - self.get_margin_spacing().left - self.get_margin_spacing().right
        else:
            return self.get_fixed_width() \
                - self.get_padding_spacing().left - self.get_padding_spacing().right \
                - self.get_border_spacing().left - self.get_border_spacing().right

    def get_max_inner_height(self) -> float:
        if self.get_fixed_height() is None:
            assert isinstance(self.get_parent_node(), BlockLayoutNode)
            return self.get_parent_node().get_max_inner_height() \
                - self.get_padding_spacing().top - self.get_padding_spacing().bottom \
                - self.get_border_spacing().top - self.get_border_spacing().bottom \
                - self.get_margin_spacing().top - self.get_margin_spacing().bottom
        else:
            return self.get_fixed_height() \
                - self.get_padding_spacing().top - self.get_padding_spacing().bottom \
                - self.get_border_spacing().top - self.get_border_spacing().bottom

    def get_max_width(self):
        if self.get_fixed_width() is None:
            assert isinstance(self.get_parent_node(), BlockLayoutNode)
            return self.get_parent_node().get_max_inner_width()
        else:
            return self.get_fixed_width()

    def get_max_height(self):
        if self.get_fixed_width() is None:
            assert isinstance(self.get_parent_node(), BlockLayoutNode)
            return self.get_parent_node().get_max_inner_height()
        else:
            return self.get_fixed_height()

    # Override.
    def get_width(self) -> float:
        if self.get_fixed_width():
            return self.get_fixed_width()
        else:
            return self.get_max_width()

    def place_block_node(self, child_node: "BlockLayoutNode"):
        child_node.on_placed_in_node(
            self,
            relative_x=self.get_border_spacing().left + self.get_padding_spacing().left \
                + child_node.get_margin_spacing().left,
            relative_y=self.get_border_spacing().top + self.get_padding_spacing().top + self._height_of_children \
                + child_node.get_margin_spacing().top,
        )
        self._height_of_children += child_node.get_height()

        self._children.append(child_node)

    # FIXME: Implement this.
    def place_inline_node(self, child_node: "InlineLayoutNode"):
        pass

    # Override.
    def get_children(self):
        return self._children

# FIXME: Implement this.
class InlineLayoutNode(LayoutNode):
    pass

class PageLayoutNode(BlockLayoutNode):
    def __init__(self):
        super().__init__(
            name="PageLayoutNode",
            fixed_width=40 * font_width,
            fixed_height=20 * font_height,
            background_color=COLOR_WHITE,
            padding_spacing=Spacing(left=10, right=10, top=20, bottom=20),
            border_spacing=Spacing(left=1, right=1, top=1, bottom=1),
            border_color=COLOR_BLACK,
        )

        self.__header_node = BlockLayoutNode(
            fixed_height=1 * font_height,
            background_color=COLOR_GREEN,
        )
        self.place_block_node(self.__header_node)

        self.__content_node = BlockLayoutNode(
            fixed_height=self.get_max_inner_height() - 2 * font_height,
            background_color=COLOR_BLUE,
        )
        self.place_block_node(self.__content_node)

        self.__footer_node = BlockLayoutNode(
            fixed_height=1 * font_height,
            background_color=COLOR_RED,
        )
        self.place_block_node(self.__footer_node)

    def get_header_node(self):
        return self.__header_node

    def get_content_node(self):
        return self.__content_node

    def get_footer_node(self):
        return self.__footer_node
