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
    model_node: "model.TextChunkModelNode"
    model_offset: int
    text: str

@dataclasses.dataclass(frozen=True, kw_only=True, slots=True)
class PlacementInstruction:
    pass

@dataclasses.dataclass(frozen=True, kw_only=True, slots=True)
class WordPlacementInstruction(PlacementInstruction):
    excerpts: list[TextExcerpt]

@dataclasses.dataclass(frozen=True, kw_only=True, slots=True)
class WhitespacePlacementInstruction(PlacementInstruction):
    model_node: "model.TextChunkModelNode"
    model_offset: "model.TextChunkModelNode"

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

def print_placement_instructions(placement_instructions: list[PlacementInstruction]):
    for placement_instruction in placement_instructions:
        if isinstance(placement_instruction, WordPlacementInstruction):
            print("WordPlacementInstruction")

            for excerpt in placement_instruction.excerpts:
                print(f"  {excerpt}")
        elif isinstance(placement_instruction, WhitespacePlacementInstruction):
            print(f"WhitespacePlacementInstruction(model_node={placement_instruction.model_node}, model_offset={placement_instruction.model_offset}")
        else:
            raise NotImplementedError

def compute_placement_instructions_for_paragraph(paragraph_node: "model.ParagraphModelNode") -> list[PlacementInstruction]:
    placement_instructions: list[PlacementInstruction] = []

    pending_excerpts: list[TextExcerpt] = []
    pending_whitespace_instruction: WhitespacePlacementInstruction = None

    def finish_pending_word_group():
        nonlocal placement_instructions
        nonlocal pending_excerpts
        nonlocal pending_whitespace_instruction

        if len(pending_excerpts) >= 1:
            if pending_whitespace_instruction is not None:
                placement_instructions.append(pending_whitespace_instruction)
                pending_whitespace_instruction = None

            placement_instructions.append(WordPlacementInstruction(
                excerpts=pending_excerpts,
            ))
            pending_excerpts=[]

    for text_chunk_node in paragraph_node.children:
        assert isinstance(text_chunk_node, model.TextChunkModelNode)

        remaining_text = text_chunk_node.text
        model_node_offset = 0

        while len(remaining_text) >= 1:
            if starts_with_whitespace(remaining_text):
                finish_pending_word_group()

                model_node_offset_before = model_node_offset

                # Consume whitespace.
                text_before, text_separator, text_after = partition_at_whitespace(remaining_text)
                assert len(text_before) == 0
                model_node_offset += len(text_separator)
                remaining_text = text_after

                pending_whitespace_instruction = WhitespacePlacementInstruction(
                    model_node=text_chunk_node,
                    model_offset=model_node_offset_before,
                )

            if len(remaining_text) >= 1:
                model_node_offset_before = model_node_offset

                # Consume excerpt.
                text_before, text_separator, text_after = partition_at_whitespace(remaining_text)
                assert len(text_before) >= 1
                model_node_offset += len(text_before) + len(text_separator)
                remaining_text = text_after

                # Add to pending word group.
                pending_excerpts.append(TextExcerpt(
                    model_node=text_chunk_node,
                    model_offset=model_node_offset_before,
                    text=text_before,
                ))

                # Finish the word group if whitespace consumed.
                if len(text_separator) >= 1:
                    finish_pending_word_group()

                    pending_whitespace_instruction = WhitespacePlacementInstruction(
                        model_node=text_chunk_node,
                        model_offset=model_node_offset_before,
                    )

    finish_pending_word_group()

    return placement_instructions