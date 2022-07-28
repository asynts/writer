import dataclasses

next_node_key = 1

@dataclasses.dataclass(frozen=True, kw_only=True)
class Node:
    key: int
    value: int
    children: list["Node"]

    @staticmethod
    def make(*, value: int, children: list["Node"]) -> "Node":
        global next_node_key

        key = next_node_key
        next_node_key = next_node_key + 1

        return Node(
            key=key,
            value=value,
            children=children,
        )

    def modified_copy(self, *, value: int = None, children: list[int] = None) -> "Node":
        new_key = self.key
        new_value = self.value
        new_children = self.children

        if value is not None:
            new_value = value
        if children is not None:
            new_children = children

        return Node(
            key=new_key,
            value=new_value,
            children=new_children,
        )

    def lookup_node_recursively(self, *, key_path: list[int]):
        if len(key_path) == 0:
            return self

        for child_node in self.children:
            if child_node.key == key_path[0]:
                return child_node.lookup_node_recursively(key_path=key_path[1:])

        # Node not found.
        raise AssertionError

    def replace_node_recursively(self, *, key_path: list[int], new_node: "Node") -> "Node":
        if len(key_path) == 0:
            return new_node

        for child_index, child_node in enumerate(self.children):
            if child_node.key == key_path[0]:
                new_children = [
                    *self.children[:child_index],
                    child_node.replace_node_recursively(key_path=key_path[1:], new_node=new_node),
                    *self.children[child_index + 1:],
                ]

                return self.modified_copy(children=new_children)

        # Node not found.
        raise AssertionError

    # The keyword arguments can be used to place markers.
    # The name of the argument is the marker, the value is the key path.
    def dump(self, *, indent=int, parent_key_path=list[int], **kwargs) -> str:
        key_path = parent_key_path + [self.key]

        indent_string = " " * indent * 4

        position_string = ""
        for position_name, position_key_path in kwargs.items():
            if position_key_path == key_path:
                position_string += " <" + position_name + ">"

        result = f"{indent_string}Node(key={self.key}, value={self.value}){position_string}\n"
        for child in self.children:
            result += child.dump(indent=indent+1, parent_key_path=key_path, **kwargs)

        return result

def dump_node(node: Node, **kwargs):
    print(node.dump(indent=0, parent_key_path=[], **kwargs), end="")

class Document:
    def __init__(self, root_node: Node):
        self.root_node = root_node

    def lookup_node(self, key_path: list[int]) -> Node:
        assert self.root_node.key == key_path[0]
        return self.root_node.lookup_node_recursively(key_path=key_path[1:])

    def replace_node(self, key_path: list[int], new_node: Node):
        assert self.root_node.key == key_path[0]
        self.root_node = self.root_node.replace_node_recursively(key_path=key_path[1:], new_node=new_node)

node_1 = Node.make(
    value=14,
    children=[]
)
node_2 = Node.make(
    value=7,
    children=[],
)
node_3 = Node.make(
    value=3,
    children=[
        node_2,
    ]
)
node_4 = Node.make(
    value=20,
    children=[
        node_1,
        node_3,
    ]
)

position_1 = [
    node_4.key,
    node_1.key,
]

document = Document(root_node=node_4)

dump_node(document.root_node, position_1=position_1)

target_node = document.lookup_node(position_1)
assert target_node.value == 14
target_node_modified = target_node.modified_copy(value=100)
document.replace_node(position_1, target_node_modified)

target_node = document.lookup_node(position_1)
assert target_node.value == 100

dump_node(document.root_node, position_1=position_1)
