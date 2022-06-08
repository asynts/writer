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

    def is_empty(self) -> bool:
        return len(self.excerpts) >= 1

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
    # FIXME: Implement this.
    return []
