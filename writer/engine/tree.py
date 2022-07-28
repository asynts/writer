import copy

# Each node is assigned a unique id on creation.
# When we want to change a node we create a copy but keep the same key.
# Therefore, a list of keys can be used to identify a node in the tree while allowing modifications.
_next_node_key = 1
def create_node_key():
    global _next_node_key
    key = _next_node_key
    _next_node_key += 1
    return key

class NodeNotFound(Exception):
    pass

# At first nodes are mutable.
# However, they must become immutable before they can can become children of other nodes.
# Once immutable, they can not become mutable again.
class Node:
    __slots__ = (
        "__children",
        "__is_mutable",
        "__key",
    )

    def __init__(self, *, children: list["Node"]):
        # Property.
        self.__children = children

        # Property.
        self.__key = create_node_key()

        self.__is_mutable = True

    def make_immutable(self):
        assert self.is_mutable
        self.__is_mutable = False

    # Virtual.
    def make_mutable_copy(self):
        copy_ = copy.copy(self)
        copy_.__is_mutable = True
        return copy_

    # Finds a node in the subtree spanned by this node.
    def lookup_node_recursively(self, *, key_path: list[int]) -> "Node":
        assert len(key_path) >= 0
        assert key_path[0] == self.key

        if len(key_path) == 1:
            return self

        for child_node in self.children:
            if child_node.key == key_path[1]:
                return child_node.lookup_node_recursively(key_path=key_path[1:])

        raise NodeNotFound

    # Replace a node in the subtree spanned by this node.
    # Returns a copy of the current node with updated parents.
    # If they key path references this node, returns the new node.
    def replace_node_recursively(self, *, key_path: list[int], new_node: "Node") -> "Node":
        assert len(key_path) >= 0
        assert key_path[0] == self.key

        if len(key_path) == 1:
            return new_node

        for child_index, child_node in enumerate(self.children):
            if child_node.key == key_path[1]:
                mutable_copy = self.make_mutable_copy()

                mutable_copy.children = [
                    *self.children[:child_index],
                    child_node.replace_node_recursively(key_path=key_path[1:], new_node=new_node),
                    *self.children[child_index+1:],
                ]

                mutable_copy.make_immutable()
                return mutable_copy

        raise NodeNotFound

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
        result += f"{name}@{self.key}("
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

    @property
    def key(self):
        return self.__key

    @children.setter
    def children(self, value: list["Node"]):
        assert self.is_mutable
        self.__children = value

# Splits a list when it encounters a sentinel, returns a partition of the input list.
def partition_with_sentinel(list_: list, *, sentinel: any):
    for index in range(len(list_)):
        if list_[index] == sentinel:
            return list_[:index], list_[index:index+1], list_[index+1:]

    return list_, [], []
