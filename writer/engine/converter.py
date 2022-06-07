from . import model, layout

# Returns the words that did not fit into this parent node.
def generate_layout_nodes_for_words_helper(*, parent_node: layout.BlockLayoutNode, words: list[str]):
    print(f">>> generate_layout_nodes_for_words_helper: parent_node")
    print(parent_node.to_string(), end="")
    print("<<<")

    # We do add the node here, but we might never place it, that is fine.
    new_layout_node = layout.BlockLayoutNode(parent_node=parent_node)

    def place_node_into_parent():
        print(">>> computing remaining_space")
        print(parent_node.get_parent_node().to_string(), end="")
        print("<<<")

        remaining_space = parent_node.get_max_remaining_height()
        assert remaining_space >= 0.0

        occupied_space = new_layout_node.get_min_height() + new_layout_node.get_margin_spacing().y

        if occupied_space > remaining_space:
            # Not enough space to fit this node, overflow to next page.

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
        new_child_node = layout.InlineTextChunkLayoutNode(text=word, parent_node=new_layout_node)
        new_layout_node.place_inline_node(new_child_node)

        # Advance.
        offset_x += new_child_node.get_width()

    if place_node_into_parent():
        return []
    else:
        return words[:]

# Returns the words that did not fit into this parent node.
def generate_layout_nodes_for_words(*, parent_node: layout.BlockLayoutNode, words: list[str]):
    print(f">>> generate_layout_nodes_for_words: parent_node")
    print(parent_node.to_string(), end="")
    print("<<<")

    new_layout_node = layout.BlockLayoutNode(parent_node=parent_node)

    # Break down the problem and treat each line recursively.
    # Returns the words that did not fit into this parent node.
    words = generate_layout_nodes_for_words_helper(parent_node=new_layout_node, words=words)

    parent_node.place_block_node(new_layout_node)

    return words

def generate_layout_tree(model_tree: model.DocumentModelNode) -> layout.LayoutNode:
    layout_tree = layout.BlockLayoutNode(parent_node=None)

    current_page_node = layout.PageLayoutNode(parent_node=layout_tree)

    for paragraph in model_tree.children():
        assert isinstance(paragraph, model.ParagraphModelNode)
        words = paragraph.get_text().split()

        # Returns the words that did not fit into this layout node and thus need to be placed on a new page.
        words = generate_layout_nodes_for_words(parent_node=current_page_node.get_content_node(), words=words)

        while len(words) >= 1:
            # We had some overflow and need to create a new page to fit it.

            layout_tree.place_block_node(current_page_node)
            current_page_node = layout.PageLayoutNode(parent_node=layout_tree)

            words = generate_layout_nodes_for_words(parent_node=current_page_node.get_content_node(), words=words)

    layout_tree.place_block_node(current_page_node)

    # The top level node isn't really placed but we still need to change the phase.
    layout_tree.on_placed_in_node(relative_x=0, relative_y=0)

    return layout_tree
