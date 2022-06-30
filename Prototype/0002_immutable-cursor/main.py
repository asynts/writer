class Node:
    def __init__(self, *, children: list["Node"], value: int):
        self.children = children
        self.value = value

    def dump(self, *, indent: int = 0):
        result = ""

        result += indent * " "
        result += f"Node(value={self.value})\n"

        for child in self.children:
            result += child.dump(indent=indent + 2)

        return result

tree_1 = Node(
    value=10,
    children=[
        Node(
            value=5,
            children=[
                Node(
                    value=1,
                    children=[],
                ),
                Node(
                    value=6,
                    children=[],
                ),
            ],
        ),
        Node(
            value=12,
            children=[],
        ),
    ],
)

print(tree_1.dump(), end="")
