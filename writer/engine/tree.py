import copy

# At first nodes are mutable.
# However, they must become immutable before they can can become children of other nodes.
# Once immutable, they can not become mutable again.
class Node:
    __slots__ = (
        "__children",
        "__is_mutable",
    )

    def __init__(self, *, children: list["Node"]):
        # Property.
        self.__children = children

        self.__is_mutable = True

    def make_immutable(self):
        assert self.is_mutable
        self.__is_mutable = False

    def append_child(self, child_node: "Node"):
        assert self.is_mutable
        self.__children.append(child_node)

    # Virtual.
    def dump_properties(self):
        return ""

    # Virtual.
    def dump(self, *, name: str = "Node", indent: int = 0):
        result = ""
        result += " " * indent
        result += f"{name}@{id(self)}("
        result += self.dump_properties()
        result += ")\n"

        for child_node in self.children:
            result += child_node.dump(indent=indent+1)

        return result

    @property
    def is_mutable(self):
        return self.__is_mutable

    @property
    def children(self):
        return self.__children

    @children.setter
    def children(self, value: list["Node"]):
        assert self.is_mutable
        self.__children = value

# Since nodes become immutable before being inserted in their parent node,
# we can not add a reference to the parent node inside the node.
#
# Instead, all code that interacts with the tree must remember the parent nodes itself.
class Position:
    __slots__ = (
        "node",
        "parent_nodes",
    )

    def __init__(self, *, node: Node, parent_nodes: list[Node]):
        self.node = node
        self.parent_nodes = parent_nodes

# Splits a list when it encounters a sentinel, returns a partition of the input list.
def partition_with_sentinel(list_: list, *, sentinel: any):
    for index in range(len(list_)):
        if list_[index] == sentinel:
            return list_[:index], list_[index:index+1], list_[index+1:]

    return list_, [], []

def modified_copy(position: Position, /, **kwargs):
    # Create a copy of the original node.
    new_node = copy.copy(position.node)

    # Update some of the properties based on keyword arguments.
    # In the C++ version we would have to implement this for each class manually.
    for property_, value in { **kwargs }.items():
        setattr(new_node, property_, value)

    new_node.make_immutable()

    if len(position.parent_nodes) >= 1:
        # If we have parent nodes, recursively update the child nodes of parents.

        parent_node = position.parent_nodes[-1]

        siblings_before, _, siblings_after = partition_with_sentinel(parent_node.children, sentinel=position.node)

        new_parent_position = modified_copy(
            Position(
                node=position.parent_nodes[-1],
                parent_nodes=position.parent_nodes[:-1]
            ),
            children=[
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
