import typing

Color = typing.Tuple[int, int, int]

# Invariant: All the getters return immutable objects, they must not be modified.

class LayoutNode:
    __slots__ = (
        "_background_color",
    )

    def __init__(self, *, background_color: Color):
        self._background_color = background_color

    @property
    def background_color(self):
        return self._background_color

class ParentLayoutNode(LayoutNode):
    __slots__ = (
        "_child_nodes",
    )

    def __init__(self, *, child_nodes: list[LayoutNode], **kwargs):
        super().__init__(**kwargs)
        self._child_nodes = child_nodes

    @property
    def child_nodes(self):
        return self._child_nodes

class VerticalLayoutNode(ParentLayoutNode):
    pass

class HorizontalLayoutNode(ParentLayoutNode):
    pass

class TextLayoutNode(LayoutNode):
    __slots__ = (
        "_text",
    )

    def __init__(self, *, text: str, **kwargs):
        super().__init__(**kwargs)
        self._text = text

    @property
    def text(self):
        return self._text

root_layout_node = VerticalLayoutNode(
    background_color=(200, 200, 200),
    child_nodes=[
        VerticalLayoutNode(
            background_color=(255, 255, 255),
            child_nodes=[
                VerticalLayoutNode(
                    background_color=None,
                    child_nodes=[
                        HorizontalLayoutNode(
                            background_color=None,
                            child_nodes=[
                                TextLayoutNode(
                                    background_color=None,
                                    text="Hello, ",
                                ),
                                TextLayoutNode(
                                    background_color=None,
                                    text="world",
                                ),
                                TextLayoutNode(
                                    background_color=None,
                                    text="!",
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        ),
    ],
)

# Nodes can not reference their parent nodes because they are immutable.
# When iterating we therefore need to keep track of the parent nodes.
class Position:
    def __init__(self, *, node: LayoutNode, parent_nodes: list[LayoutNode]):
        self.node = node
        self.parent_nodes = parent_nodes

def iterate_nodes_of_type_in_pre_order_helper(*, current_node: LayoutNode, class_: type, parent_nodes: list[LayoutNode]):
    if isinstance(current_node, ParentLayoutNode):
        # We may have to optimize it by maintaining a stack, I don't think the optimizer will be able to do that for me.
        new_parent_nodes = parent_nodes + [ current_node ]
        for child_node in current_node.child_nodes:
            yield from iterate_nodes_of_type_in_pre_order_helper(current_node=child_node, class_=class_, parent_nodes=new_parent_nodes)

    if isinstance(current_node, class_):
        yield Position(node=current_node, parent_nodes=parent_nodes)

def iterate_nodes_of_type_in_pre_order(*, root_node: LayoutNode, class_: type):
    parent_nodes = []
    return iterate_nodes_of_type_in_pre_order_helper(current_node=root_node, class_=class_, parent_nodes=parent_nodes)

for position in iterate_nodes_of_type_in_pre_order(root_node=root_layout_node, class_=TextLayoutNode):
    print(f"node: {position.node.text=} {len(position.parent_nodes)=}")
