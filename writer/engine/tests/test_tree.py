import pytest

from dataclasses import dataclass

import writer.engine.tree as tree


class NamedNode(tree.Node):
    __slots__ = (
        "__name",
    )

    def __init__(self, *args, name: str, **kwargs):
        super().__init__(*args, **kwargs)

        # Property.
        self.__name = name

    # Override.
    def dump_properties(self):
        return f"name={repr(self.name)}"

    @property
    def name(self):
        return self.__name

    def is_equivalent_to(self, other_node: "NamedNode"):
        if self.name != other_node.name:
            return False

        if len(self.children) != len(other_node.children):
            return False

        for child, other_child in zip(self.children, other_node.children):
            if not child.is_equivalent_to(other_child):
                return False

        return True

@dataclass
class TreeFixture:
    root_node: NamedNode
    lookup_node: dict[str, NamedNode]
    lookup_key: dict[str, int]

@pytest.fixture
def fixture_default_tree():
    # <node name="a">
    #     <node name="b">
    #         <node name="c" />
    #         <node name="d" />
    #     </node>
    #     <node name="e">
    #         <node name="f" />
    #     </node>
    # </node>

    node_f = NamedNode(
        name="f",
        children=[],
    )
    node_f.make_immutable()

    node_e = NamedNode(
        name="e",
        children=[
            node_f,
        ],
    )
    node_e.make_immutable()

    node_d = NamedNode(
        name="d",
        children=[],
    )
    node_d.make_immutable()

    node_c = NamedNode(
        name="c",
        children=[],
    )
    node_c.make_immutable()

    node_b = NamedNode(
        name="b",
        children=[
            node_c,
            node_d,
        ],
    )
    node_b.make_immutable()

    node_a = NamedNode(
        name="a",
        children=[
            node_b,
            node_e,
        ],
    )
    node_a.make_immutable()

    root_node = node_a
    lookup_node = {
        "a": node_a,
        "b": node_b,
        "c": node_c,
        "d": node_d,
        "e": node_e,
        "f": node_f,
    }
    lookup_key = {
        "a": node_a.key,
        "b": node_b.key,
        "c": node_c.key,
        "d": node_d.key,
        "e": node_e.key,
        "f": node_f.key,
    }

    return TreeFixture(
        root_node=root_node,
        lookup_node=lookup_node,
        lookup_key=lookup_key,
    )

@pytest.fixture
def fixture_node_y():
    node = NamedNode(
        name="y",
        children=[],
    )
    node.make_immutable()
    return node

@pytest.fixture
def fixture_node_x(fixture_node_y: tree.Node):
    node = NamedNode(
        name="x",
        children=[
            fixture_node_y,
        ],
    )
    node.make_immutable()
    return node

def test_immutable_raises_exception():
    node_1 = tree.Node(children=[])
    node_1.make_immutable()

    node_2 = tree.Node(children=[])
    node_2.append_child(node_1)
    node_2.make_immutable()

    node_3 = tree.Node(children=[])
    node_3.make_immutable()

    with pytest.raises(AssertionError):
        node_3.append_child(node_1)

def test_mutable_copy_does_not_influence_source():
    node_1 = tree.Node(children=[])
    node_1.make_immutable()

    node_2 = tree.Node(children=[])
    node_2.make_immutable()

    node_3 = node_1.make_mutable_copy()
    node_3.append_child(node_2)

    assert len(node_3.children) == 1
    assert len(node_1.children) == 0

def test_lookup_root_node(fixture_default_tree: TreeFixture):
    node_path = tree.NodePath([
        fixture_default_tree.lookup_key["a"],
    ])

    assert node_path.lookup(root_node=fixture_default_tree.root_node) is fixture_default_tree.lookup_node["a"]

def test_lookup_nested_node_1(fixture_default_tree: TreeFixture):
    node_path = tree.NodePath([
        fixture_default_tree.lookup_key["a"],
        fixture_default_tree.lookup_key["b"],
        fixture_default_tree.lookup_key["d"],
    ])

    assert node_path.lookup(root_node=fixture_default_tree.root_node) is fixture_default_tree.lookup_node["d"]

def test_lookup_nested_node_2(fixture_default_tree: TreeFixture):
    node_path = tree.NodePath([
        fixture_default_tree.lookup_key["a"],
        fixture_default_tree.lookup_key["e"],
    ])

    assert node_path.lookup(root_node=fixture_default_tree.root_node) is fixture_default_tree.lookup_node["e"]

def test_lookup_not_found(fixture_default_tree: TreeFixture):
    node_path = tree.NodePath([
        fixture_default_tree.lookup_key["a"],
        fixture_default_tree.lookup_key["d"],
    ])

    with pytest.raises(tree.NodeNotFound):
        node_path.lookup(root_node=fixture_default_tree.root_node)

def test_lookup_not_found_root(fixture_default_tree: TreeFixture):
    node_path = tree.NodePath([
        123,
        fixture_default_tree.lookup_key["b"],
        fixture_default_tree.lookup_key["c"],
    ])

    with pytest.raises(tree.NodeNotFound):
        node_path.lookup(root_node=fixture_default_tree.root_node)

def test_replace_root(fixture_default_tree: TreeFixture):
    node_path = tree.NodePath([
        fixture_default_tree.lookup_key["a"],
    ])

    new_node = NamedNode(
        name="x",
        children=[],
    )
    new_node.make_immutable()

    new_root_node = node_path.fork_and_replace(new_node, root_node=fixture_default_tree.root_node)

    assert new_root_node.is_equivalent_to(new_node)

@pytest.fixture
def fixture_nested_1_tree():
    # <node name="a">
    #     <node name="b">
    #         <node name="c" />
    #         <node name="d" />
    #     </node>
    #     <node name="x">
    #         <node name="y" />
    #     </node>
    # </node>

    node_y = NamedNode(
        name="y",
        children=[],
    )
    node_y.make_immutable()

    node_x = NamedNode(
        name="x",
        children=[
            node_y,
        ],
    )
    node_x.make_immutable()

    node_d = NamedNode(
        name="d",
        children=[],
    )
    node_d.make_immutable()

    node_c = NamedNode(
        name="c",
        children=[],
    )
    node_c.make_immutable()

    node_b = NamedNode(
        name="b",
        children=[
            node_c,
            node_d,
        ],
    )
    node_b.make_immutable()

    node_a = NamedNode(
        name="a",
        children=[
            node_b,
            node_x,
        ],
    )
    node_a.make_immutable()

    root_node = node_a
    lookup_node = {
        "a": node_a,
        "b": node_b,
        "c": node_c,
        "d": node_d,
        "x": node_x,
        "y": node_y,
    }
    lookup_key = {
        "a": node_a.key,
        "b": node_b.key,
        "c": node_c.key,
        "d": node_d.key,
        "x": node_x.key,
        "y": node_y.key,
    }

    return TreeFixture(
        root_node=root_node,
        lookup_node=lookup_node,
        lookup_key=lookup_key,
    )

def test_replace_nested_1(fixture_default_tree: TreeFixture, fixture_nested_1_tree: TreeFixture, fixture_node_x: tree.Node):
    node_path = tree.NodePath([
        fixture_default_tree.lookup_key["a"],
        fixture_default_tree.lookup_key["e"],
    ])

    new_root_node = node_path.fork_and_replace(fixture_node_x, root_node=fixture_default_tree.root_node)

    assert fixture_nested_1_tree.root_node.is_equivalent_to(new_root_node)

@pytest.fixture
def fixture_nested_2_tree():
    # <node name="a">
    #     <node name="y" />
    #     <node name="e">
    #         <node name="f" />
    #     </node>
    # </node>

    node_f = NamedNode(
        name="f",
        children=[],
    )
    node_f.make_immutable()

    node_e = NamedNode(
        name="e",
        children=[
            node_f,
        ],
    )
    node_e.make_immutable()

    node_y = NamedNode(
        name="y",
        children=[],
    )
    node_y.make_immutable()

    node_a = NamedNode(
        name="a",
        children=[
            node_y,
            node_e,
        ],
    )
    node_a.make_immutable()

    root_node = node_a
    lookup_node = {
        "a": node_a,
        "y": node_y,
        "e": node_e,
        "f": node_f,
    }
    lookup_key = {
        "a": node_a.key,
        "y": node_y.key,
        "e": node_e.key,
        "f": node_f.key,
    }

    return TreeFixture(
        root_node=root_node,
        lookup_node=lookup_node,
        lookup_key=lookup_key,
    )

def test_replace_nested_2(fixture_default_tree: TreeFixture, fixture_nested_2_tree: TreeFixture, fixture_node_y: tree.Node):
    node_path = tree.NodePath([
        fixture_default_tree.lookup_key["a"],
        fixture_default_tree.lookup_key["b"],
    ])

    new_root_node = node_path.fork_and_replace(fixture_node_y, root_node=fixture_default_tree.root_node)

    print(fixture_nested_2_tree.root_node.dump())
    print(new_root_node.dump())

    assert fixture_nested_2_tree.root_node.is_equivalent_to(new_root_node)

def test_replace_not_found(fixture_default_tree: TreeFixture, fixture_node_y: tree.Node):
    node_path = tree.NodePath([
        fixture_default_tree.lookup_key["a"],
        fixture_default_tree.lookup_key["b"],
        fixture_default_tree.lookup_key["b"],
    ])

    with pytest.raises(tree.NodeNotFound):
        node_path.fork_and_replace(fixture_node_y, root_node=fixture_default_tree.root_node)

def test_replace_not_found_root(fixture_default_tree: TreeFixture, fixture_node_y: tree.Node):
    node_path = tree.NodePath([
        123,
    ])

    with pytest.raises(tree.NodeNotFound):
        node_path.fork_and_replace(fixture_node_y, root_node=fixture_default_tree.root_node)

@pytest.fixture
def fixture_remove_leaf():
    # <node name="a">
    #     <node name="b">
    #         <node name="d" />
    #     </node>
    #     <node name="e">
    #         <node name="f" />
    #     </node>
    # </node>

    node_f = NamedNode(
        name="f",
        children=[],
    )
    node_f.make_immutable()

    node_e = NamedNode(
        name="e",
        children=[
            node_f,
        ],
    )
    node_e.make_immutable()

    node_d = NamedNode(
        name="d",
        children=[],
    )
    node_d.make_immutable()

    node_b = NamedNode(
        name="b",
        children=[
            node_d,
        ],
    )
    node_b.make_immutable()

    node_a = NamedNode(
        name="a",
        children=[
            node_b,
            node_e,
        ],
    )
    node_a.make_immutable()

    root_node = node_a
    lookup_node = {
        "a": node_a,
        "b": node_b,
        "d": node_d,
        "e": node_e,
        "f": node_f,
    }
    lookup_key = {
        "a": node_a.key,
        "b": node_b.key,
        "d": node_d.key,
        "e": node_e.key,
        "f": node_f.key,
    }

    return TreeFixture(
        root_node=root_node,
        lookup_node=lookup_node,
        lookup_key=lookup_key,
    )

def test_remove_leaf(fixture_default_tree: TreeFixture, fixture_remove_leaf: TreeFixture):
    node_path = tree.NodePath([
        fixture_default_tree.lookup_key["a"],
        fixture_default_tree.lookup_key["b"],
        fixture_default_tree.lookup_key["c"],
    ])

    new_root_node = node_path.fork_and_remove(root_node=fixture_default_tree.root_node)

    assert fixture_remove_leaf.root_node.is_equivalent_to(new_root_node)

@pytest.fixture
def fixture_remove_parent():
    # <node name="a">
    #     <node name="b">
    #         <node name="c" />
    #         <node name="d" />
    #     </node>
    # </node>

    node_d = NamedNode(
        name="d",
        children=[],
    )
    node_d.make_immutable()

    node_c = NamedNode(
        name="c",
        children=[],
    )
    node_c.make_immutable()

    node_b = NamedNode(
        name="b",
        children=[
            node_c,
            node_d,
        ],
    )
    node_b.make_immutable()

    node_a = NamedNode(
        name="a",
        children=[
            node_b,
        ],
    )
    node_a.make_immutable()

    root_node = node_a
    lookup_node = {
        "a": node_a,
        "b": node_b,
        "c": node_c,
        "d": node_d,
    }
    lookup_key = {
        "a": node_a.key,
        "b": node_b.key,
        "c": node_c.key,
        "d": node_d.key,
    }

    return TreeFixture(
        root_node=root_node,
        lookup_node=lookup_node,
        lookup_key=lookup_key,
    )

def test_remove_parent(fixture_default_tree: TreeFixture, fixture_remove_parent: TreeFixture):
    node_path = tree.NodePath([
        fixture_default_tree.lookup_key["a"],
        fixture_default_tree.lookup_key["e"],
    ])

    new_root_node = node_path.fork_and_remove(root_node=fixture_default_tree.root_node)

    assert fixture_remove_parent.root_node.is_equivalent_to(new_root_node)

def test_remove_root(fixture_default_tree: TreeFixture):
    node_path = tree.NodePath([
        fixture_default_tree.lookup_key["a"],
    ])

    with pytest.raises(AssertionError):
        node_path.fork_and_remove(root_node=fixture_default_tree.root_node)
