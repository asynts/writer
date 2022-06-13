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

        for child_node in self.child_nodes:
            result += child_node.dump(indent=indent+1)

        return result

class VerticalLayoutNode(ParentLayoutNode):
    # Virtual.
    def dump(self, indent: int = 0, name: str = "VerticalLayoutNode"):
        return super().dump(name=name, indent=indent)

class HorizontalLayoutNode(ParentLayoutNode):
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
        for child_node in current_node.child_nodes:
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
    # Collect all the old properties in a dictionary.
    properties = position.node.properties

    # Update some of the properties based on keyword arguments.
    for property_, value in { **kwargs }.items():
        assert property_ in properties
        properties[property_] = value

    # Create the new node.
    new_node = position.node.__class__(**properties)

    if len(position.parent_nodes) >= 1:
        # If we have parent nodes, recursively update the child nodes of parents.

        parent_node = position.parent_nodes[-1]
        assert isinstance(parent_node, ParentLayoutNode)

        siblings_before, sentinel, siblings_after = partition_with_sentinel(parent_node.child_nodes, position.node)
        print(f"siblings_before={[id(sibling) for sibling in siblings_before]} sentinel={id(sentinel)} siblings_after={[id(sibling) for sibling in siblings_after]} node={id(position.node)}")

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
