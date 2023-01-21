import pytest

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

@pytest.fixture
def default_tree():
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

    return node_a
