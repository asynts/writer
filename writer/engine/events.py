import writer.engine.model as model
import writer.engine.layout as layout
import writer.engine.tree as tree

# FIXME: Maybe I could rewrite this as a coroutine?
#        Just spit out the next sensible layout node with the model tree position.

# Calls 'LayoutNode.on_mouse_click' on any node that contains this position which has a model node assigned to it.
# It keeps track of the parent model nodes, since this information is required to describe a position in the model tree.
#
# Layout nodes that modify the model tree must return 'True' to indicate that they consume the event.
# We will not call any other hook after that.
#
# Invariant: When we mutate the model tree in the layout node hooks, the layout tree remains valid and keeps referencing the same model nodes.
#            This is important for the algorithm to finish properly.
def mouse_click_event(*, absolute_x: float, absolute_y: float, model_tree: model.DocumentModelNode, layout_tree: layout.LayoutNode):
    model_parent_nodes: list[model.ModelNode] = []

    def visit_layout_node(layout_node: layout.LayoutNode, *, relative_x: float, relative_y: float):
        nonlocal model_parent_nodes

        assert layout_node.get_phase() == layout.Phase.PHASE_3_FINAL

        # For simplicity, this function may be called with positions that do not make any sense.
        if relative_x < 0.0 or relative_y < 0.0:
            return False
        if relative_x > layout_node.get_absolute_width() or relative_y > layout_node.get_absolute_height():
            return False

        # Only call the hook for layout nodes that define a model node.
        # Otherwise, we can't really associate this with the model tree.
        if layout_node.get_model_node():
            print(f"visited {id(layout_node)=} ({id(layout_node.get_model_node())=})")

            b_event_consumed = layout_node.on_mouse_click(
                relative_x=relative_x,
                relative_y=relative_y,
                model_position=tree.Position(
                    node=layout_node.get_model_node(),
                    parent_nodes=model_parent_nodes,
                ),
            )
        else:
            b_event_consumed = False

        if b_event_consumed:
            print("event_consumed!")
            return True

        for layout_child_node in layout_node.get_children():
            if layout_node.get_model_node():
                b_added_parent_node = True
                model_parent_nodes.append(layout_node.get_model_node())
            else:
                b_added_parent_node = False

            b_event_consumed = visit_layout_node(
                layout_child_node,
                relative_x=relative_x - layout_node.get_relative_x(),
                relative_y=relative_y - layout_node.get_relative_y()
            )

            if b_added_parent_node:
                model_parent_nodes.pop()

            if b_event_consumed:
                return True

        return False

    visit_layout_node(layout_tree, relative_x=absolute_x, relative_y=absolute_y)
