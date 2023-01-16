import typing

from PyQt6 import QtGui, QtCore
from writer.engine import history

import writer.engine.model as model
import writer.engine.layout as layout
import writer.engine.tree as tree

def backspace_event(*, model_tree: model.DocumentModelNode, layout_tree: layout.LayoutNode, history_manager: history.HistoryManager):
    # FIXME: We are a bit inconsistent here.
    #        If we reference a node it should always belong to the current tree, otherwise, we should look it up again.

    new_model_tree = model_tree

    cursor_path = model_tree.cursor_node_path
    cursor_node = cursor_path.lookup(root_node=model_tree)

    # If are in the middle of a text chunk, delete character before cursor.
    if cursor_node.cursor_offset >= 1:
        new_node = cursor_node.make_mutable_copy()
        new_node.text = new_node.text[:new_node.cursor_offset-1] + new_node.text[new_node.cursor_offset:]
        new_node.cursor_offset -= 1
        new_node.make_immutable()
        new_model_tree = cursor_path.replace(new_node, root_node=new_model_tree)

        history_manager.update_model_tree(new_model_tree=new_model_tree)
        return True

    # We are at the start of a text chunk, is there a preceding text chunk?
    previous_path = cursor_path.previous_sibling_path(root_node=new_model_tree)
    if previous_path is not None:
        previous_node = previous_path.lookup(root_node=new_model_tree)

        # Remove last character of previous text chunk.
        new_node = previous_node.make_mutable_copy()
        new_node.text = new_node.text[:-1]
        new_node.cursor_offset = len(new_node.text)
        new_node.make_immutable()
        new_model_tree = previous_path.replace(new_node, root_node=new_model_tree)

        # Remove cursor from current node.
        new_node = cursor_node.make_mutable_copy()
        new_node.cursor_offset = None
        new_node.make_immutable()
        new_model_tree = cursor_path.replace(new_node, root_node=new_model_tree)

        # Update the reference to the new cursor node.
        new_node = new_model_tree.make_mutable_copy()
        new_node.cursor_node_path = previous_path
        new_node.make_immutable()
        new_model_tree = new_node

        history_manager.update_model_tree(new_model_tree=new_model_tree)
        return True
    else:
        parent_path = cursor_path.parent_path(root_node=new_model_tree)
        parent_node = parent_path.lookup(root_node=new_model_tree)

        # We are at the start of a paragraph, is there a preceding paragraph?
        prev_paragraph_path = parent_path.previous_sibling_path(root_node=new_model_tree)
        if prev_paragraph_path is not None:
            prev_paragraph_node = prev_paragraph_path.lookup(root_node=new_model_tree)

            last_chunk_node = prev_paragraph_node.children[-1]
            last_chunk_path = prev_paragraph_path.child_path(last_chunk_node, root_node=new_model_tree)

            # Remove last character of last text chunk of previous paragarph.
            new_node = last_chunk_node.make_mutable_copy()
            new_node.text = new_node.text[:-1]
            new_node.make_immutable()
            new_model_tree = last_chunk_path.replace(new_node, root_node=new_model_tree)

            # Update the reference to the cursor.
            new_node = new_model_tree.make_mutable_copy()
            new_node.cursor_node_path = prev_paragraph_path.child_path(cursor_node, root_node=new_model_tree)
            new_node.make_immutable()
            new_model_tree = new_node

            # Merge the following paragraph into the previous paragraph.
            new_node = prev_paragraph_node.make_mutable_copy()
            new_node.children += parent_node.children
            new_node.make_immutable()
            new_model_tree = prev_paragraph_path.replace(new_node, root_node=new_model_tree)

            # Delete the following paragraph.
            parent_parent_path = parent_path.parent_path(root_node=new_model_tree)
            parent_parent_node = parent_parent_path.lookup(root_node=new_model_tree)
            new_node = parent_parent_node.make_mutable_copy()
            new_node.children.remove(parent_node)
            new_node.make_immutable()
            new_model_tree = parent_parent_path.replace(new_node, root_node=new_model_tree)

            history_manager.update_model_tree(new_model_tree=new_model_tree)
            return True

    return False

def key_press_event(
    *,
    event: QtGui.QKeyEvent,
    model_tree: model.DocumentModelNode,
    layout_tree: layout.LayoutNode,
    history_manager: history.HistoryManager
):
    # Ignore key press events when no cursor is placed.
    if model_tree.cursor_node_path is None:
        return False

    if event.key() == QtCore.Qt.Key.Key_Backspace:
        return backspace_event(model_tree=model_tree, layout_tree=layout_tree, history_manager=history_manager)

    # Ignore key press events for unprintable characters.
    if not event.text().isprintable():
        return False

    new_model_tree = model_tree

    new_node = model_tree.cursor_node_path.lookup(root_node=model_tree).make_mutable_copy()
    new_node.text = new_node.text[:new_node.cursor_offset] + event.text() + new_node.text[new_node.cursor_offset:]
    new_node.cursor_offset += 1
    new_node.make_immutable()
    new_model_tree = model_tree.cursor_node_path.replace(new_node, root_node=new_model_tree)

    history_manager.update_model_tree(new_model_tree=new_model_tree)

    return True

# Calls 'LayoutNode.on_mouse_click' on any node that contains this position which has a model node assigned to it.
# It keeps track of the parent model nodes, since this information is required to describe a position in the model tree.
#
# Layout nodes that modify the model tree must return 'True' to indicate that they consume the event.
# We will not call any other hook after that.
#
# Invariant: When we mutate the model tree in the layout node hooks, the layout tree remains valid and keeps referencing the same model nodes.
#            This is important for the algorithm to finish properly.
def mouse_click_event(
    *,
    absolute_x: float,
    absolute_y: float,
    model_tree: model.DocumentModelNode,
    layout_tree: layout.LayoutNode,
    history_manager: history.HistoryManager
):
    # FIXME: Maybe I could rewrite this as a coroutine?
    #        Just spit out the next sensible layout node with the model tree position.

    key_list: list[int] = []

    def visit_layout_node(layout_node: layout.LayoutNode, *, relative_x: float, relative_y: float):
        nonlocal key_list

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
                path=tree.NodePath(key_list + [layout_node.get_model_node().key]),
            )
        else:
            b_event_consumed = False

        if b_event_consumed:
            return True

        for layout_child_node in layout_node.get_children():
            if layout_node.get_model_node():
                b_added_parent_node = True
                key_list.append(layout_node.get_model_node().key)
            else:
                b_added_parent_node = False

            b_event_consumed = visit_layout_node(
                layout_child_node,
                relative_x=relative_x - layout_child_node.get_relative_x(),
                relative_y=relative_y - layout_child_node.get_relative_y(),
            )

            if b_added_parent_node:
                key_list.pop()

            if b_event_consumed:
                return True

        return False

    return visit_layout_node(layout_tree, relative_x=absolute_x, relative_y=absolute_y)

# Layout nodes can reference model nodes.
# This "event" verifies that the layout tree is consistent with the model tree.
# If a model node has a parent, the same parent can be discovered in the layout tree.
def validate_parent_hierachy_event(*, model_tree: "model.DocumentModelNode", layout_tree: "layout.LayoutNode", history_manager: history.HistoryManager):
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

    return True

# There must only be one
def validate_cursor_unique_event(*, model_tree: "model.DocumentModelNode", layout_tree: "layout.LayoutNode", history_manager: history.HistoryManager):
    b_cursor_seen = False
    key_list: list[int] = []
    def visit_model_node(*, model_node: model.ModelNode):
        nonlocal b_cursor_seen
        nonlocal key_list

        key_list.append(model_node.key)

        if isinstance(model_node, model.TextChunkModelNode):
            if model_node.cursor_offset is not None:
                assert not b_cursor_seen
                assert model_tree.cursor_node_path is not None
                assert key_list == model_tree.cursor_node_path._key_list

                b_cursor_seen = True

        for child_node in model_node.children:
            visit_model_node(model_node=child_node)

        key_list.pop()

    visit_model_node(model_node=model_tree)

    return True
