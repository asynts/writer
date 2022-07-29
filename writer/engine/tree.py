import copy
import typing

from writer.engine import model

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

# FIXME: There is tons of redundancy in this function.
#        Many of these functions could be implemented by a single complex function.
class NodePath:
    __slots__ = (
        "_key_list",
    )

    def __init__(self, key_list: list[int]):
        assert isinstance(key_list, list)
        assert len(key_list) >= 1
        self._key_list = key_list

    def lookup(self, *, root_node: Node) -> Node:
        def visit_node(node: Node, *, remaining_key_list: list[int]):
            assert len(remaining_key_list) >= 1
            assert remaining_key_list[0] == node.key

            if len(remaining_key_list) == 1:
                return node

            for child_node in node.children:
                if child_node.key == remaining_key_list[1]:
                    return visit_node(child_node, remaining_key_list=remaining_key_list[1:])

            raise NodeNotFound

        return visit_node(root_node, remaining_key_list=self._key_list)

    def replace(self, new_node: Node, *, root_node: Node) -> Node:
        def visit_node(node: Node, *, remaining_key_list: list[int]):
            assert len(remaining_key_list) >= 1
            assert remaining_key_list[0] == node.key

            if len(remaining_key_list) == 1:
                return new_node
            else:
                for child_index, child_node in enumerate(node.children):
                    if child_node.key == remaining_key_list[1]:
                        patched_node = node.make_mutable_copy()
                        patched_node.children = [
                            *patched_node.children[:child_index],
                            visit_node(child_node, remaining_key_list=remaining_key_list[1:]),
                            *patched_node.children[child_index+1:],
                        ]
                        patched_node.make_immutable()
                        return patched_node

                raise NodeNotFound

        return visit_node(root_node, remaining_key_list=self._key_list)

    def parent_path(self, *, root_node: Node) -> "NodePath":
        assert len(self._key_list) >= 2
        return NodePath(self._key_list[:-1])

    def child_path(self, child_node: Node, *, root_node: Node) -> "NodePath":
        return NodePath(self._key_list + [child_node.key])

    def previous_sibling_path(self, *, root_node: Node) -> "NodePath":
        def visit_node(node: Node, *, remaining_key_list: list[int]):
            assert len(remaining_key_list) >= 1
            assert remaining_key_list[0] == node.key

            # If we are the parent of the target node.
            if len(remaining_key_list) == 2:
                previous_node = None
                for child_node in node.children:
                    if child_node.key == remaining_key_list[1]:
                        if previous_node is None:
                            return None
                        else:
                            return NodePath(self._key_list[:-1] + [previous_node.key])

                    previous_node = child_node

                raise NodeNotFound

            for child_node in node.children:
                if child_node.key == remaining_key_list[1]:
                    return visit_node(child_node, remaining_key_list=remaining_key_list[1:])

            raise NodeNotFound

        return visit_node(root_node, remaining_key_list=self._key_list)

# Splits a list when it encounters a sentinel, returns a partition of the input list.
def partition_with_sentinel(list_: list, *, sentinel: any):
    for index in range(len(list_)):
        if list_[index] == sentinel:
            return list_[:index], list_[index:index+1], list_[index+1:]

    return list_, [], []
