from . import model, layout

def generate_layout_nodes_for_words_helper(*, parent_node: layout.BlockLayoutNode, words: list[str]):
    # We do add the node here, but we might never place it, that is fine.
    new_layout_node = layout.BlockLayoutNode()
    new_layout_node.on_added_to_node(parent_node=parent_node)

    def place_node_into_parent():
        remaining_space = parent_node.get_max_inner_height() - parent_node.get_min_inner_height()
        assert remaining_space >= 0.0

        occupied_space = new_layout_node.get_height() + new_layout_node.get_margin_spacing().top + new_layout_node.get_margin_spacing().bottom

        print(f"placing: {remaining_space=} {occupied_space=}")

        if occupied_space > remaining_space:
            # Not enough space to fit this node, overflow to next page.

            # FIXME: Actually create a new page.
            print("page overflow")
            return False
        else:
            # We can safely place this node without causing overflow.

            parent_node.place_block_node(new_layout_node)
            return True

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

            if place_node_into_parent():
                return generate_layout_nodes_for_words_helper(parent_node=parent_node, words=words[index:])
            else:
                return words[:]

        # Create a new text layout node for this word.
        new_child_node = layout.InlineTextChunkLayoutNode(text=word)
        new_child_node.on_added_to_node(new_layout_node)
        new_layout_node.place_inline_node(new_child_node)

        # Advance.
        offset_x += new_child_node.get_width()

    if place_node_into_parent():
        return []
    else:
        return words[:]

def generate_layout_nodes_for_words(*, parent_node: layout.BlockLayoutNode, words: list[str]):
    new_layout_node = layout.BlockLayoutNode()
    new_layout_node.on_added_to_node(parent_node=parent_node)

    # Break down the problem and treat each line recursively.
    generate_layout_nodes_for_words_helper(parent_node=new_layout_node, words=words)

    parent_node.place_block_node(new_layout_node)

def generate_layout_tree(model_tree: model.DocumentModelNode) -> layout.LayoutNode:
    layout_tree = layout.BlockLayoutNode()

    current_page_node = layout.PageLayoutNode()
    current_page_node.on_added_to_node(layout_tree)

    for paragraph in model_tree.children():
        assert isinstance(paragraph, model.ParagraphModelNode)

        # FIXME: This is suboptimal, because we need to be able to pass information about the model node.
        words = paragraph.get_text().split()
        generate_layout_nodes_for_words(parent_node=current_page_node.get_content_node(), words=words)

    layout_tree.place_block_node(current_page_node)

    # Let's add another page for testing.
    current_page_node = layout.PageLayoutNode()
    current_page_node.on_added_to_node(layout_tree)
    layout_tree.place_block_node(current_page_node)

    return layout_tree