import string
import typing
from . import model, layout

import dataclasses

# Represents an excerpt from a text chunk in the model.
# Text chunks can belong to multiple word groups.
@dataclasses.dataclass(frozen=True, kw_only=True)
class TextExcerpt:
    text_chunk_model_node: model.TextChunkModelNode
    text: str

# Represents one word that should be wrapped as one.
# Words can span over multiple text chunks in the model.
class WordGroup:
    def __init__(self, excerpts: list[TextExcerpt] = None):
        if excerpts is None:
            excerpts = []

        self.excerpts = excerpts

        # FIXME: Add width and height here.

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, WordGroup):
            return False
        return self.excerpts == other.excerpts

    def is_empty(self) -> bool:
        return len(self.excerpts) == 0

# Replace all whitespace with spaces.
# Removes adjacent whitespace.
# Keeps leading and trailing whitespace.
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

    current_word_group = WordGroup()

    def finish_word_group():
        nonlocal current_word_group

        if not current_word_group.is_empty():
            word_groups.append(current_word_group)

        current_word_group = WordGroup()

    for text_chunk_model_node in paragraph_model_node.get_children():
        assert isinstance(text_chunk_model_node, model.TextChunkModelNode)

        remaining_text = text_chunk_model_node.get_text()
        remaining_text = normalize_whitespace(remaining_text)

        while len(remaining_text) >= 1:
            text, separator, remaining_text = remaining_text.partition(" ")

            # If we encounter a separator without anything any text before it, open a new word group.
            if len(text) == 0:
                assert separator == " "
                finish_word_group()
                continue

            # Add this text to the current word group.
            current_word_group.excerpts.append(TextExcerpt(
                text_chunk_model_node=text_chunk_model_node,
                text=text,
            ))

            # If a separator was encountered, open a new word group.
            # Notice that this is different from the other edge case, because the code runs after the text was added.
            if len(separator) >= 1:
                assert separator == " "
                finish_word_group()

    finish_word_group()

    return word_groups
