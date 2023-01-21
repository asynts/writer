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

@dataclass
class TreeFixture:
    tree: NamedNode
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

    tree = node_a
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
        tree=tree,
        lookup_node=lookup_node,
        lookup_key=lookup_key,
    )

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

    assert node_path.lookup(root_node=fixture_default_tree.tree) is fixture_default_tree.lookup_node["a"]

def test_lookup_nested_node_1(fixture_default_tree: TreeFixture):
    node_path = tree.NodePath([
        fixture_default_tree.lookup_key["a"],
        fixture_default_tree.lookup_key["b"],
        fixture_default_tree.lookup_key["d"],
    ])

    assert node_path.lookup(root_node=fixture_default_tree.tree) is fixture_default_tree.lookup_node["d"]

def test_lookup_nested_node_2(fixture_default_tree: TreeFixture):
    node_path = tree.NodePath([
        fixture_default_tree.lookup_key["a"],
        fixture_default_tree.lookup_key["e"],
    ])

    assert node_path.lookup(root_node=fixture_default_tree.tree) is fixture_default_tree.lookup_node["e"]

def test_lookup_invalid_path(fixture_default_tree: TreeFixture):
    node_path = tree.NodePath([
        fixture_default_tree.lookup_key["a"],
        fixture_default_tree.lookup_key["d"],
    ])

    with pytest.raises(tree.NodeNotFound):
        node_path.lookup(root_node=fixture_default_tree.tree)
