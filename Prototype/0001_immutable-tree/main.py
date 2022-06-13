import copy
import enum
import typing

Color = typing.Tuple[int, int, int]

# Invariant: All the getters return immutable objects, they must not be modified.

class Phase(enum.Enum):
    PHASE_1_MUTABLE = 1
    PHASE_2_IMMUTABLE = 2

class LayoutNode:
    __slots__ = (
        "_phase",
        "_background_color",
    )

    def __init__(self, *, background_color: Color):
        self._background_color = background_color
        self._phase = Phase.PHASE_1_MUTABLE

    def finalize(self):
        assert self._phase == Phase.PHASE_1_MUTABLE
        self._phase = Phase.PHASE_2_IMMUTABLE

    @property
    def background_color(self):
        return self._background_color
    @background_color.setter
    def background_color(self, value: Color):
        assert self._phase == Phase.PHASE_1_MUTABLE
        self._background_color = value

    # Virtual.
    @property
    def properties(self):
        return {
            "background_color": self._background_color,
        }

    def dump_header(self, *, name: str, indent: int):
        result = ""

        result += " " * indent
        result += f"{name}@{id(self)}("

        prefix = ""
        for property_, value in self.properties.items():
            if property_ == "child_nodes":
                continue

            result += prefix
            prefix = ", "

            result += f"{property_}={repr(value)}"

        result += ")\n"

        return result

    # Virtual.
    def dump(self, indent: int = 0, name: str = "LayoutNode"):
        return self.dump_header(name=name, indent=indent)

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
    @child_nodes.setter
    def child_nodes(self, value: list[LayoutNode]):
        assert self._phase == Phase.PHASE_1_MUTABLE
        self._child_nodes = value

    # Override.
    @property
    def properties(self):
        properties = super().properties
        properties.update({
            "child_nodes": self._child_nodes,
        })
        return properties

    # Override.
    def dump(self, indent: int = 0, name: str = "ParentLayoutNode"):
        result = super().dump(indent=indent, name=name)

        for child_node in self._child_nodes:
            result += child_node.dump(indent=indent+1)

        return result

class VerticalLayoutNode(ParentLayoutNode):
    __slots__ = tuple()

    # Virtual.
    def dump(self, indent: int = 0, name: str = "VerticalLayoutNode"):
        return super().dump(name=name, indent=indent)

class HorizontalLayoutNode(ParentLayoutNode):
    __slots__ = tuple()

    # Virtual.
    def dump(self, indent: int = 0, name: str = "HorizontalLayoutNode"):
        return super().dump(name=name, indent=indent)

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
    @text.setter
    def text(self, value: str):
        assert self._phase == Phase.PHASE_1_MUTABLE
        self._text = value

    @property
    def properties(self):
        properties = super().properties
        properties.update({
            "text": self._text,
        })
        return properties

    # Virtual.
    def dump(self, indent: int = 0, name: str = "TextLayoutNode"):
        return super().dump(name=name, indent=indent)

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
        for child_node in current_node._child_nodes:
            yield from iterate_nodes_of_type_in_pre_order_helper(current_node=child_node, class_=class_, parent_nodes=new_parent_nodes)

    if isinstance(current_node, class_):
        yield Position(node=current_node, parent_nodes=parent_nodes)

def iterate_nodes_of_type_in_pre_order(*, root_node: LayoutNode, class_: type):
    parent_nodes = []
    return iterate_nodes_of_type_in_pre_order_helper(current_node=root_node, class_=class_, parent_nodes=parent_nodes)

def partition_with_sentinel(list_: list, sentinel: any):
    for index in range(len(list_)):
        if list_[index] == sentinel:
            return list_[:index], list_[index], list_[index+1:]

    return list_, [], []

def mutate(position: Position, /, **kwargs):
    # Create a copy of the original node.
    new_node = copy.copy(position.node)

    # Update some of the properties based on keyword arguments.
    # In the C++ version we would have to implement this for each class manually.
    for property_, value in { **kwargs }.items():
        setattr(new_node, property_, value)

    new_node.finalize()

    if len(position.parent_nodes) >= 1:
        # If we have parent nodes, recursively update the child nodes of parents.

        parent_node = position.parent_nodes[-1]
        assert isinstance(parent_node, ParentLayoutNode)

        siblings_before, sentinel, siblings_after = partition_with_sentinel(parent_node._child_nodes, position.node)

        new_parent_position = mutate(
            Position(
                node=position.parent_nodes[-1],
                parent_nodes=position.parent_nodes[:-1]
            ),
            child_nodes=[
                *siblings_before,
                new_node,
                *siblings_after,
            ],
        )

        return Position(
            node=new_node,
            parent_nodes=[
                *new_parent_position.parent_nodes,
                new_parent_position.node,
            ],
        )
    else:
        # We are the root node.

        return Position(
            node=new_node,
            parent_nodes=[],
        )

text_node_iterator = iterate_nodes_of_type_in_pre_order(root_node=root_layout_node, class_=TextLayoutNode)
next(text_node_iterator)
old_position = next(text_node_iterator)

print(">>> before")
print(old_position.parent_nodes[0].dump(), end="")
print("<<<")

new_position = mutate(old_position, text="Paul")

print(">>> after")
print(new_position.parent_nodes[0].dump(), end="")
print("<<<")
