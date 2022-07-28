import dataclasses

next_node_key = 1

@dataclasses.dataclass(frozen=True, kw_only=True)
class Node:
    key: int
    value: int
    children: list["Node"]

    @staticmethod
    def make(*, value: int, children: list["Node"]):
        global next_node_key

        key = next_node_key
        next_node_key = next_node_key + 1

        return Node(
            key=key,
            value=value,
            children=children,
        )

    # The keyword arguments can be used to place markers.
    # The name of the argument is the marker, the value is the key path.
    def dump(self, *, indent=int, parent_key_path=list[int], **kwargs):
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

tree = node_4
dump_node(tree, position_1=position_1)
