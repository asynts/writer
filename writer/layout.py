import typing
import pygame
import enum

normal_font: pygame.font.Font = None

font_width: int = None
font_height: int = None

COLOR_WHITE = (255, 255, 255)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (0, 0, 255)

# FIXME: Use '__' for members in some cases to hide them.

# The idea is that, if we want to change the model, we delete all the layout nodes that correspond to that model node and all the following layout nodes.
# Then, we can just recompute these.
# Even simpler would be, if we just discard the whole layout tree.

# FIXME: Keep track of which values are constant on initialization and what needs to be updated.

class OverflowStrategy(enum.Enum):
    # Do not render any child elements that overflow.
    DISCARD = 0

Color = typing.Tuple[int, int, int]

class LayoutNode:
    def __init__(self, *, name: str, fixed_width: int = None, fixed_height: int = None, background_color: Color):
        # Name of the node.
        # This is usually the name of the class.
        self._name = name

        # Reference to parent node.
        # Assigned when inserting into parent node.
        self._parent_node: LayoutNode = None

        # Position in parent node.
        # Assigned when inserting into parent node.
        self._relative_x: int = None
        self._relative_y: int = None

        # How much space is needed to fit all children.
        # Updated as nodes are inserted.
        self._width_of_children = 0
        self._height_of_children = 0

        # The exact width and height of this node.
        # May be overwritten in inheriting classes.
        self._fixed_width = fixed_width
        self._fixed_height = fixed_height

        # Defines what happens if child elements do not fit.
        self._overflow_strategy = OverflowStrategy.DISCARD

        # The background color of this layout node.
        self._background_color = background_color

    def get_background_color(self) -> Color:
        return self._background_color

    def on_placed_in_node(self, parent_node: "LayoutNode", *, relative_x: int, relative_y: int):
        assert self._parent_node is None
        self._parent_node = parent_node

        assert self._relative_x is None
        self._relative_x = relative_x

        assert self._relative_y is None
        self._relative_y = relative_y

    def get_relative_x(self) -> float:
        assert self._relative_x is not None
        return self._relative_x

    def get_relative_y(self) -> float:
        assert self._relative_y is not None
        return self._relative_y

    def get_absolute_x(self) -> float:
        if self._parent_node is None:
            assert self._relative_x is None
            return 0
        else:
            assert self._relative_x is not None
            return self._parent_node.get_absolute_x() + self._relative_x

    def get_absolute_y(self) -> float:
        if self._parent_node is None:
            assert self._relative_y is None
            return 0
        else:
            assert self._relative_y is not None
            return self._parent_node.get_absolute_y() + self._relative_y

    # FIXME: Rename 'get_min_*' methods.

    def get_min_width(self) -> float:
        return self._width_of_children

    def get_min_height(self) -> float:
        return self._height_of_children

    def get_fixed_width(self) -> float:
        return self._fixed_width

    def get_fixed_height(self) -> float:
        return self._fixed_height

    def get_width(self) -> float:
        if self.get_fixed_width() is not None:
            return self.get_fixed_width()
        else:
            return self.get_min_width()

    def get_height(self) -> float:
        if self.get_fixed_height() is not None:
            return self.get_fixed_height()
        else:
            return self.get_min_height()

    def get_children(self):
        return []

class BlockLayoutNode(LayoutNode):
    def __init__(self, *, name="BlockLayoutNode", fixed_width: int = None, fixed_height: int = None, background_color: Color = None):
        super().__init__(
            name=name,
            fixed_width=fixed_width,
            fixed_height=fixed_height,
            background_color=background_color
        )

        self._children: list[LayoutNode] = []

    def get_max_width(self) -> float:
        if self.get_fixed_width() is None:
            assert isinstance(self._parent_node, BlockLayoutNode)
            return self._parent_node.get_max_width()
        else:
            return self.get_fixed_width()

    def get_max_height(self) -> float:
        if self.get_fixed_height() is None:
            assert isinstance(self._parent_node, BlockLayoutNode)
            return self._parent_node.get_max_height()
        else:
            return self.get_fixed_height()

    def get_width(self) -> float:
        if self.get_fixed_width():
            return self.get_fixed_width()
        else:
            return self.get_max_width()

    # This method assumes that the node that is being inserted will not change.
    def place_block_node(self, child_node: "BlockLayoutNode"):
        child_node._parent_node = self
        child_node._relative_x = 0
        child_node._relative_y = self._height_of_children
        self._height_of_children += child_node.get_height()

        self._children.append(child_node)

    # FIXME: Implement this.
    def place_inline_node(self, child_node: "InlineLayoutNode"):
        pass

    def get_children(self):
        return self._children

# FIXME: Implement this.
class InlineLayoutNode(LayoutNode):
    pass

class PageLayoutNode(BlockLayoutNode):
    def __init__(self):
        super().__init__(
            name="PageLayoutNode",
            fixed_width=15 * font_width,
            fixed_height=5 * font_height,
            background_color=COLOR_WHITE
        )

        self._header_node = BlockLayoutNode(
            fixed_height=1 * font_height,
            background_color=COLOR_GREEN,
        )
        self.place_block_node(self._header_node)

        self._content_node = BlockLayoutNode(
            fixed_height=3 * font_height,
            background_color=COLOR_BLUE,
        )
        self.place_block_node(self._content_node)

        self._footer_node = BlockLayoutNode(
            fixed_height=1 * font_height,
            background_color=COLOR_RED,
        )
        self.place_block_node(self._footer_node)

    def get_header_node(self):
        return self._header_node

    def get_content_node(self):
        return self._content_node

    def get_footer_node(self):
        return self._footer_node
