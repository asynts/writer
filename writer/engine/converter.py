import string
import typing
from . import model, layout

import dataclasses

# This represents part of a 'TextChunkModelNode' this is necessary, because these nodes can contain
# spaces and thus contain multiple words.
@dataclasses.dataclass(frozen=True, kw_only=True)
class TextExcerpt:
    text_chunk_model_node: model.TextChunkModelNode
    text: str

# One rendered word could belong to multiple model nodes with different formatting.
# They are obviously rendered separately, however, for text wrapping we need to consider them together.
# This class represents one rendered word with everything that belongs to it.
#
# In the future, we could implement hypernation and this would be a good place to start.
# But for now, we just place entire words.
class WordGroup:
    def __init__(self):
        self.excerpts: list[TextExcerpt] = []
        self.width = 0.0
        self.height = 0.0

    def is_empty(self) -> bool:
        return len(self.excerpts) >= 1

# Replace all whitespace with spaces.
# Removes adjacent whitespace.
def normalize_whitespace(string_: str):
    result = []
    b_previous_character_was_whitespace = False
    for ch in string_:
        if ch in string.whitespace:
            if not b_previous_character_was_whitespace:
                result.append(" ")
                b_previous_character_was_whitespace = True
        else:
            result.append(ch)
            b_previous_character_was_whitespace = False

    return "".join(result)

# Wrapping text is more complicated than one might think at first.
# The formatting can change in the middle of a word and one chunk of text can contain multiple words.
# This function takes a paragraph and prepares word groups that should be wrapped together.
def compute_word_groups_in_paragraph(paragraph_model_node: model.ParagraphModelNode) -> list[WordGroup]:
    word_groups: list[WordGroup] = []

    # FIXME: Prepare test cases before moving on.

    # FIXME: What if the first text chunk starts with a space?
    current_word_group = WordGroup()

    for text_chunk_model_node in paragraph_model_node.get_children():
        assert isinstance(text_chunk_model_node, model.TextChunkModelNode)

        # The text in the chunk node is normalized such that it can be processed with 'str.partition'.
        remaining = text_chunk_model_node.get_text()
        remaining = normalize_whitespace(remaining)

        # If the word starts with a whitespace, then a new word group is started.
        # Otherwise, we keep adding to the previous group.
        if remaining.startswith(" "):
            word_groups.append(current_word_group)
            current_word_group = WordGroup()
            remaining = remaining.lstrip(" ")

        # FIXME: The spaces need to appear in the output as well.

        while len(remaining) >= 1:
            text, separator, remaining = remaining.partition(" ")

            if len(text) == 0:
                # This can only happen on the first iteration.
                # The remaining text started with the separator and thus a new word group is created.

                assert separator == " "

                if not current_word_group.is_empty():
                    word_groups.append(current_word_group)
                    current_word_group = WordGroup()

                continue

            # FIXME: Update width and height.

            # This text chunk is added to the current word group.
            current_word_group.excerpts.append(TextExcerpt(
                text_chunk_model_node=text_chunk_model_node,
                text=text,
            ))

            # If a separator was found, then a new word group is started.
            if len(separator) >= 1:
                assert separator == " "

                if not current_word_group.is_empty():
                    word_groups.append(current_word_group)
                    current_word_group = WordGroup()

    # Add the last word group if it ocontains something.
    if not current_word_group.is_empty():
        word_groups.append(current_word_group)

    return word_groups

def place_paragraph(paragraph_model_node: model.ParagraphModelNode):
    # First, we construct a list of all the word groups in the paragraph.


    # This is the rough algorithm that I have in mind.
    # The idea is to construct word groups which represent the things being wrapped.
    # Maybe, we could even do this in advance and then just do the placement in a separate step. <-- THIS SEEMS GOOD

    # At some point, we need to store enough information to be able to find the model node from the layout node.
    # On top of that, the model node needs to know the layout nodes that were generated for it.
    # Maybe, not all layout nodes need to know the exact position, they only need to know what needs to be discarded when things are changed.
    # When all of that works, I finally need to start working on the editing, that will be fun.

    # NEW IDEA:

    # Loop throuh all the text chunk in this paragraph.

        # Construct text excerpts.

        # Add text excerpt to current word group, creating new ones as needed.
    
    # Loop through the word groups.

        # Try to fit the current word group into the current line.

            # If it fits, move on and place the next word group.

            # Otherwise, place the old line and create a new one to place the group in.

                # If the old line doesn't fit, we create a new page and continue the placement there.
                # In order to be able to do this, we need to keep track of the word groups that are being placed in the current line.
                # The width of the new area could be different.

    # OLD IDEA:

    # Loop through all the text chunks in this paragraph.

        # Construct text excerpts until a word group is completed.

        # Try to fit the word group onto the current line.

            # If fit, move on and construct the next word group.

            # Otherwise, place the old line, and create a new line.

                # If the old line doesn't fit on this page, create a new page.
                # FIXME: In that case we would have to redo the layout, no?

### OLD IMPLEMENTATION

# Returns the words that did not fit into this parent node.
def generate_layout_nodes_for_words_helper(*, parent_node: layout.BlockLayoutNode, words: list[str]):
    # We do add the node here, but we might never place it, that is fine.
    new_layout_node = layout.BlockLayoutNode(parent_node=parent_node)

    def place_node_into_parent():
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
    new_layout_node = layout.BlockLayoutNode(parent_node=parent_node)

    # Break down the problem and treat each line recursively.
    # Returns the words that did not fit into this parent node.
    words = generate_layout_nodes_for_words_helper(parent_node=new_layout_node, words=words)

    parent_node.place_block_node(new_layout_node)

    return words

# FIXME: I don't think that this approach works where the caller repeats the call.
#        Instead the function should be able to figure out a solution by itself.
#        Transporting that much information over function arguments and return values isn't good practice.

# Generate the layout nodes for words belonging to this text chunk.
# If some text chunks don't fit on this line, it returns the remaining words.
# The caller should repeat the call until all text chunks have been placed.
def place_text_chunk(
    *,
    model_text_chunk_node: model.TextChunkModelNode,
    layout_line_node: layout.BlockLayoutNode,
    remaining_words: list[str]):

# Generate layout nodes for text chunks belonging to this paragraph.
# If some text chunks don't fit on this page, it returns the remaining text chunks.
# The caller should repeat the call until all text chunks have been placed.
def place_paragraph(
    *,
    model_paragraph_node: model.ParagraphModelNode,
    layout_paragraph_node: layout.BlockLayoutNode,
    # FIXME: This is not ehough, we might have to split them across pages.
    remaining_text_chunk_nodes: list[model.TextChunkModelNode]):

    def create_new_layout_line():
        node = layout.BlockLayoutNode(parent=layout_paragraph_node)

        # Place a dummy child node such that the height calcuation is correct later on.
        dummy_child_node = layout.InlineTextChunkLayoutNode(text="", parent_node=node)
        node.place_inline_node(dummy_child_node)

        return node

    layout_line_node = create_new_layout_line()

    def does_current_line_fit():
        return layout_line_node.get_min_height() + layout_line_node.get_outer_spacing().y <= layout_paragraph_node.get_max_remaining_height():

    if not does_current_line_fit():
        return remaining_text_chunk_nodes

    for index in range(len(remaining_text_chunk_nodes)):
        model_text_chunk_node = remaining_text_chunk_nodes[index]

        pending_words = model_text_chunk_node.get_text().split()
        remaining_words = pending_words

        # We try to place the text chunk, usually, this is enough.
        remaining_words = place_text_chunk(
            model_text_chunk_node=model_text_chunk_node,
            layout_line_node=layout_line_node,
            remaining_words=remaining_words,
        )

        # If we can't fit this line, we need to return all the words
        if not does_current_line_fit():
            # FIXME: This is bad, we should instead assume that the height of the line remains constant.
            return pending_words

        # We might have to create a new line
        while len(remaining_words) >= 1:
            if not does_current_line_fit():
                # The line we created doesn't actually fit, a new page needs to be created, the caller needs to do that.
                # We discard everything we already did for this text chunk, unless it belongs to a line that has already been placed.
                return pending_words

            # Place the old line node and create a new one.
            layout_paragraph_node.place_block_node(layout_line_node)
            layout_line_node = layout.BlockLayoutNode(parent_node=layout_paragraph_node)

            # Repeat the call with the new layout node.
            remaining_words = place_text_chunk(
                model_text_chunk_node=model_text_chunk_node,
                layout_line_node=layout_line_node,
                remaining_words=remaining_words,
            )

            # Since this line has been place, we only need to worry about the other words if something doesn't fit.
            pending_words = remaining_words

def generate_layout_tree(model_tree: model.DocumentModelNode) -> layout.LayoutNode:
    layout_tree = layout.BlockLayoutNode(parent_node=None)

    current_page_node = layout.PageLayoutNode(parent_node=layout_tree)

    for paragraph in model_tree.get_children():
        assert isinstance(paragraph, model.ParagraphModelNode)

        # FIXME: This is a hack, get actual text chunks working.
        words = sum(map(lambda chunk: chunk.get_text().split(), paragraph.get_children()), [])

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
