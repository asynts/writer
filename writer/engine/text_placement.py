# Generating the layout nodes for a paragraph is non-trivial.
# The formatting can change in the middle of a word and adjacent text chunks might need to be wrapped together.
# Sometimes, the cursor needs to be rendered with the following word to ensure that it's in the right location.
#
# Our strategy is to generate a series of word groups that should be rendered together along with special
# instructions for cursor and whitespace placement.

# FIXME: Provide some examples where weird things need to happen.

import dataclasses
import string

import writer.engine.model as model

@dataclasses.dataclass(frozen=True, kw_only=True, slots=True)
class TextExcerpt:
    pass

@dataclasses.dataclass(frozen=True, kw_only=True, slots=True)
class PlacementInstruction:
    pass

@dataclasses.dataclass(frozen=True, kw_only=True, slots=True)
class WordGroup(PlacementInstruction):
    pass

@dataclasses.dataclass(frozen=True, kw_only=True, slots=True)
class WhitespaceMarker(PlacementInstruction):
    pass

@dataclasses.dataclass(frozen=True, kw_only=True, slots=True)
class CursorMarker(PlacementInstruction):
    pass

# This works similar to 'str.partition'.
# The string is split into three parts, the text before the separator, the separator and the text after.
# Instead of using a simple separator, we are using arbitrary whitespace.
def partition_at_whitespace(string_: str):
    for index in range(len(string_)):
        if string_[index] in string.whitespace:
            start_index = index
            end_index = index + 1

            while end_index < len(string_):
                if string_[end_index] in string.whitespace:
                    end_index += 1
                else:
                    break

            return string_[:start_index], string_[start_index:end_index], string_[end_index:]

    return string_, "", ""

def starts_with_whitespace(text: string) -> bool:
    if len(text) == 0:
        return False
    else:
        return text[0] in string.whitespace

def compute_placement_instructions_for_paragraph(paragraph_node: model.ParagraphModelNode) -> list[PlacementInstruction]:
    placement_instructions: list[PlacementInstruction] = []

    for text_chunk_node in paragraph_node.children:
        assert isinstance(text_chunk_node, model.TextChunkModelNode)

        remaining_text = text_chunk_node.text
        model_node_offset = 0

        while len(remaining_text) >= 1:
            if starts_with_whitespace(remaining_text):
                # FIXME

                # Consume whitespace.
                text_before, text_separator, text_after = partition_at_whitespace(remaining_text)
                assert len(text_before) == 0
                model_node_offset += len(text_separator)
                remaining_text = text_after

            if len(remaining_text) >= 0:
                # Consume excerpt.
                text_before, text_separator, text_after = partition_at_whitespace(remaining_text)
                model_node_offset += len(text_before) + len(text_separator)
                remaining_text = text_after

                # FIXME

    return placement_instructions
