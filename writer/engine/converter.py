from . import model, layout

def generate_layout_tree(model_tree: model.DocumentModelNode) -> layout.LayoutNode:
    layout_tree = layout.BlockLayoutNode()

    current_page_node = layout.PageLayoutNode()

    for paragraph in model_tree.children():
        assert isinstance(paragraph, model.ParagraphModelNode)

        new_layout_node = layout.BlockLayoutNode()
        new_layout_node.place_inline_node(layout.InlineTextChunkLayoutNode(text=paragraph._text))

        current_page_node.get_content_node().place_block_node(new_layout_node)

    layout_tree.place_block_node(current_page_node)

    # Let's add another page for testing.
    current_page_node = layout.PageLayoutNode()
    layout_tree.place_block_node(current_page_node)

    return layout_tree
