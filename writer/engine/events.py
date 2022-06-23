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

    debug_rects = []

    print(f"mouse_click_event({absolute_x=}, {absolute_y=})")

    print(">>> model_tree")
    print(model_tree.dump(), end="")
    print("<<<")

    print(">>> layout_tree")
    print(layout_tree.to_string(), end="")
    print("<<<")

    def visit_layout_node(layout_node: layout.LayoutNode, *, relative_x: float, relative_y: float):
        nonlocal model_parent_nodes
        nonlocal debug_rects

        assert layout_node.get_phase() == layout.Phase.PHASE_3_FINAL

        print(f"visit_layout_node({relative_x=}, {relative_y=}, {id(layout_node)=})")

        # For simplicity, this function may be called with positions that do not make any sense.
        if relative_x < 0.0 or relative_y < 0.0:
            print("visit_layout_node: out of bounds, returning false")
            return False
        if relative_x > layout_node.get_absolute_width() or relative_y > layout_node.get_absolute_height():
            print("visit_layout_node: out of bounds, returning false")
            return False

        debug_rects.append(layout_node.get_qrect())

        # Only call the hook for layout nodes that define a model node.
        # Otherwise, we can't really associate this with the model tree.
        if layout_node.get_model_node():
            print(f"visit_layout_node: calling hook for {id(layout_node)=}")

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
            print(f"visit_layout_node: event consumed by current layout node {id(layout_node)=}")
            return True

        for layout_child_node in layout_node.get_children():
            if layout_node.get_model_node():
                b_added_parent_node = True
                model_parent_nodes.append(layout_node.get_model_node())
            else:
                b_added_parent_node = False

            print(f"visit_layout_node: recursive call by {id(layout_node)=}")
            b_event_consumed = visit_layout_node(
                layout_child_node,
                relative_x=relative_x - layout_node.get_relative_x(),
                relative_y=relative_y - layout_node.get_relative_y(),
            )

            if b_added_parent_node:
                model_parent_nodes.pop()

            if b_event_consumed:
                print(f"visit_layout_node: event consumed by child layout node {id(layout_node)=} {id(layout_child_node)=}")
                return True

        return False

    visit_layout_node(layout_tree, relative_x=absolute_x, relative_y=absolute_y)

    return debug_rects
