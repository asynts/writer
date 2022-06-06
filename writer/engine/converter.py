from . import model, layout

def generate_layout_nodes_for_words_helper(*, parent_node: layout.BlockLayoutNode, words: list[str]):
    new_layout_node = layout.BlockLayoutNode()

    offset_x = 0.0

    prefix = ""
    for index in range(len(words)):
        word = prefix + words[index]
        prefix = " "

        word_width = layout.normal_font_metrics.size(0, word).width()

        if parent_node.get_max_width() is None:
            # This block can fit text of any width, nothing to be concerned about.
            pass
        elif offset_x + word_width > parent_node.get_max_width():
            # The next word doesn't fit anymore.

            # FIXME: Find a better way to deal with words that don't fit.
            assert index != 0

            parent_node.place_block_node(new_layout_node)
            generate_layout_nodes_for_words_helper(parent_node=parent_node, words=words[index:])
            return

        # Create a new text layout node for this word.
        new_child_node = layout.InlineTextChunkLayoutNode(text=word)
        new_layout_node.place_inline_node(new_child_node)

        # Advance.
        offset_x += new_child_node.get_width()

    parent_node.place_block_node(new_layout_node)

def generate_layout_nodes_for_words(*, parent_node: layout.BlockLayoutNode, words: list[str]):
    new_layout_node = layout.BlockLayoutNode()

    # Break down the problem and treat each line recursively.
    generate_layout_nodes_for_words_helper(parent_node=new_layout_node, words=words)

    parent_node.place_block_node(new_layout_node)

def generate_layout_tree(model_tree: model.DocumentModelNode) -> layout.LayoutNode:
    layout_tree = layout.BlockLayoutNode()

    current_page_node = layout.PageLayoutNode()

    for paragraph in model_tree.children():
        assert isinstance(paragraph, model.ParagraphModelNode)

        # FIXME: This is suboptimal, because we need to be able to pass information about the model node.
        words = paragraph.get_text().split()
        generate_layout_nodes_for_words(parent_node=current_page_node.get_content_node(), words=words)

    layout_tree.place_block_node(current_page_node)

    # Let's add another page for testing.
    current_page_node = layout.PageLayoutNode()
    layout_tree.place_block_node(current_page_node)

    return layout_tree
