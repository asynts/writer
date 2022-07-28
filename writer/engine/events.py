import typing

from PyQt6 import QtGui
from writer.engine import history

import writer.engine.model as model
import writer.engine.layout as layout
import writer.engine.tree as tree

# FIXME: Maybe I could rewrite this as a coroutine?
#        Just spit out the next sensible layout node with the model tree position.

def key_press_event(*, event: QtGui.QKeyEvent, model_tree: model.DocumentModelNode, layout_tree: layout.LayoutNode):
    # Ignore key press events when no cursor is placed.
    if model_tree._key_path_to_text_chunk_with_cursor is None:
        return False

    # FIXME: Deal with deleting characters.
    # FIXME: I had all of this implemented already, port that here.

    # Ignore key press events for unprintable characters.
    if not event.text().isprintable():
        return False

    # FIXME: Use the actual character from the keyboard here.
    new_node = model_tree.lookup_node_recursively(key_path=model_tree._key_path_to_text_chunk_with_cursor).make_mutable_copy()
    new_node.text = new_node.text[:new_node.cursor_offset] + event.text() + new_node.text[new_node.cursor_offset:]
    new_node.cursor_offset += 1
    new_node.make_immutable()

    history.global_history_manager.replace_node(key_path=model_tree._key_path_to_text_chunk_with_cursor, new_node=new_node)

    return True

# Calls 'LayoutNode.on_mouse_click' on any node that contains this position which has a model node assigned to it.
# It keeps track of the parent model nodes, since this information is required to describe a position in the model tree.
#
# Layout nodes that modify the model tree must return 'True' to indicate that they consume the event.
# We will not call any other hook after that.
#
# Invariant: When we mutate the model tree in the layout node hooks, the layout tree remains valid and keeps referencing the same model nodes.
#            This is important for the algorithm to finish properly.
def mouse_click_event(*, absolute_x: float, absolute_y: float, model_tree: model.DocumentModelNode, layout_tree: layout.LayoutNode):
    key_path: list[int] = []

    def visit_layout_node(layout_node: layout.LayoutNode, *, relative_x: float, relative_y: float):
        nonlocal key_path

        assert layout_node.get_phase() == layout.Phase.PHASE_3_FINAL

        # For simplicity, this function may be called with positions that do not make any sense.
        if relative_x < 0.0 or relative_y < 0.0:
            return False
        if relative_x > layout_node.get_absolute_width() or relative_y > layout_node.get_absolute_height():
            return False

        # Only call the hook for layout nodes that define a model node.
        # Otherwise, we can't really associate this with the model tree.
        if layout_node.get_model_node():
            b_event_consumed = layout_node.on_mouse_click(
                relative_x=relative_x,
                relative_y=relative_y,
                key_path=key_path + [layout_node.get_model_node().key]
            )
        else:
            b_event_consumed = False

        if b_event_consumed:
            return True

        for layout_child_node in layout_node.get_children():
            if layout_node.get_model_node():
                b_added_parent_node = True
                key_path.append(layout_node.get_model_node().key)
            else:
                b_added_parent_node = False

            b_event_consumed = visit_layout_node(
                layout_child_node,
                relative_x=relative_x - layout_child_node.get_relative_x(),
                relative_y=relative_y - layout_child_node.get_relative_y(),
            )

            if b_added_parent_node:
                key_path.pop()

            if b_event_consumed:
                return True

        return False

    return visit_layout_node(layout_tree, relative_x=absolute_x, relative_y=absolute_y)

# Layout nodes can reference model nodes.
# This "event" verifies that the layout tree is consistent with the model tree.
# If a model node has a parent, the same parent can be discovered in the layout tree.
def validate_parent_hierachy_event(*, model_tree: "model.DocumentModelNode", layout_tree: "layout.LayoutNode"):
    model_node_to_parents: typing.Dict[model.ModelNode, list[model.ModelNode]] = {}

    # First, we find the parents for each model node.
    current_model_parents = []
    def visit_model_node(model_node: model.ModelNode):
        nonlocal current_model_parents

        assert model_node not in model_node_to_parents
        model_node_to_parents[model_node] = current_model_parents[:]

        current_model_parents.append(model_node)
        for child_node in model_node.children:
            visit_model_node(child_node)
        assert current_model_parents.pop() == model_node

    visit_model_node(model_tree)

    # Then we go through the layout node and verify the parents.
    current_model_parents = []
    def visit_layout_node(layout_node: layout.LayoutNode):
        nonlocal current_model_parents

        if layout_node.get_model_node() is not None:
            assert model_node_to_parents[layout_node.get_model_node()] == current_model_parents

        if layout_node.get_model_node() is not None:
            current_model_parents.append(layout_node.get_model_node())
        for child_node in layout_node.get_children():
            visit_layout_node(child_node)
        if layout_node.get_model_node() is not None:
            assert current_model_parents.pop() == layout_node.get_model_node()

    visit_layout_node(layout_tree)

# There must only be one
def validate_cursor_unique_event(*, model_tree: "model.DocumentModelNode", layout_tree: "layout.LayoutNode"):
    pass
