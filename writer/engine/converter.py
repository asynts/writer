from . import model, layout

def generate_layout_tree(model_tree: model.DocumentModelNode) -> layout.LayoutNode:
    layout_tree = layout.PageLayoutNode()

    for paragraph in model_tree.children():
        assert isinstance(paragraph, model.ParagraphModelNode)

        # FIXME: Actually get some text rendering here.
        new_layout_node = layout.BlockLayoutNode(
            fixed_height=20,
        )

        new_layout_node.place_inline_node(layout.InlineTextChunkLayoutNode(text=paragraph._text))

        layout_tree.get_content_node().place_block_node(new_layout_node)

    return layout_tree
