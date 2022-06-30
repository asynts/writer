import weakref

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

class ImmutableTree:
    def __init__(self, *, root: Node):
        self.root = root
        self.weak_cursors = []

    def update(self, *, new_root: Node):
        # Update all the cursors.
        for cursor in self.cursors:
            # FIXME: Find a more efficent version to achieve this.
            #        We can't go through the entire tree for every node.

            sequence = []
            def visit_node(node: Node):
                sequence.append(node)

                if cursor.node is node:
                    cursor.on_sequence_updated(new_sequence=sequence)
                    b_found = True
                else:
                    b_found = False

                if not b_found:
                    for child_node in node.children:
                        b_found = visit_node(child_node)
                        if b_found:
                            break

                sequence.pop()

                return b_found

            if not visit_node(new_root):
                # This cursor no longer points at anything valid.
                cursor.on_sequence_updated(new_sequence=None)

        self.root = new_root

    @property
    def cursors(self) -> list["Cursor"]:
        for weak_cursor in self.weak_cursors:
            cursor = weak_cursor()

            if cursor is not None:
                yield cursor

    def dump(self):
        print(">>>")

        indent = 0
        def visit_node(node: Node):
            nonlocal indent

            print(indent * "  ", end="")

            cursor_note = ""
            for cursor in self.cursors:
                if cursor.node is node:
                    cursor_note += f" {id(cursor)}"

            print(f"Node(value={node.value}){cursor_note}")

            indent += 1
            for child_node in node.children:
                visit_node(child_node)
            indent -= 1

        visit_node(self.root)

        print("<<<")

    def on_register_cursor(self, cursor: "Cursor"):
        # We do not want to keep the cursor alive here.
        # If nobody has a reference to it anymore, we do not care about it.
        self.weak_cursors.append(weakref.ref(cursor))

# Cursors point at a position in an immutable tree.
# Since nodes don't know their parent nodes, we save a sequence of nodes that lead to this node.
# If the tree is changed, the sequence is updated or removed if the node is no longer in the tree.
class Cursor:
    def __init__(self, *, tree: ImmutableTree, sequence: list[Node]):
        self.tree = tree
        self.sequence = sequence

        self.tree.on_register_cursor(self)

    def node(self):
        return self.sequence[-1]

    # The new sequence can be none, if the node can not be found anymore.
    def on_sequence_updated(self, *, new_sequence: list[Node]):
        print(f"on_sequence_updated: {new_sequence}")

        if new_sequence is None:
            self.sequence = None
        else:
            self.sequence = new_sequence[:]

tree = ImmutableTree(
    root=Node(
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
    ),
)

cursor_1 = Cursor(
    tree=tree,
    sequence=[
        tree.root,
        tree.root.children[0],
        tree.root.children[0].children[1],
    ],
)

tree.dump()

tree.update(
    new_root=Node(
        value=11,
        children=tree.root.children,
    ),
)

tree.dump()
