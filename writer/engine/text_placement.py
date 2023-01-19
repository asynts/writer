# Generating the layout nodes for a paragraph is non-trivial.
# The formatting can change in the middle of a word and adjacent text chunks might need to be wrapped together.
# Sometimes, the cursor needs to be rendered with the following word to ensure that it's in the right location.
#
# Our strategy is to generate a series of word groups that should be rendered together along with special
# instructions for cursor and whitespace placement.

# FIXME: Provide some examples where weird things need to happen.

from PyQt6 import QtCore

import dataclasses
import string

import writer.engine.model as model

@dataclasses.dataclass(kw_only=True, slots=True)
class SizeMixin:
    __size: QtCore.QSizeF = None

    def get_size(self):
        raise NotImplementedError

    @property
    def width(self):
        if self.__size is None:
            self.__size = self.get_size()
        return self.__size.width()

    @property
    def height(self):
        if self.__size is None:
            self.__size = self.get_size()
        return self.__size.height()

# Invariant: Immutable after creation.
@dataclasses.dataclass(kw_only=True, slots=True)
class TextExcerpt(SizeMixin):
    model_node: "model.TextChunkModelNode"
    model_offset: int
    text: str
    style_cascade: "model.ModelStyleCascade"

    def get_size(self):
        return self.style_cascade.font_metrics.size(0, self.text)

# Invariant: Immutable after creation.
@dataclasses.dataclass(kw_only=True, slots=True)
class PlacementInstruction:
    pass

# Invariant: Immutable after creation.
@dataclasses.dataclass(kw_only=True, slots=True)
class WordPlacementInstruction(PlacementInstruction):
    excerpts: list[TextExcerpt]
    __width: float = None
    __height: float = None

    @property
    def width(self):
        if self.__width is None:
            self.__width = sum(excerpt.width for excerpt in self.excerpts)
        return self.__width

    @property
    def height(self):
        if self.__height is None:
            self.__height = max(excerpt.height for excerpt in self.excerpts)
        return self.__height

# Indicates that spacing should be added before the next word is placed.
#
# Invariant: Immutable after creation.
@dataclasses.dataclass(kw_only=True, slots=True)
class WhitespacePlacementInstruction(PlacementInstruction, SizeMixin):
    model_node: "model.TextChunkModelNode"
    model_offset: "model.TextChunkModelNode"
    style_cascade: "model.ModelStyleCascade"

    def get_size(self):
        # FIXME: Currently, we merge spaces here.
        #        I think we should stop doing that.
        return self.style_cascade.font_metrics.size(0, " ")

# Indicates that the cursor should be rendered when the next word is placed.
# This happens if the cursor is placed at the end of a node after whitespace.
# In that case it doesn't belong to the previous word and sticks to the next one.
#
# Invariant: Immutable after creation.
@dataclasses.dataclass(kw_only=True, slots=True)
class CursorPlacementInstruction(PlacementInstruction, SizeMixin):
    model_node: "model.TextChunkModelNode"
    model_offset: int

    def get_size(self):
        # The cursor does not reserve any space.
        return QtCore.QSizeF(0, 0)

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
            print(placement_instruction)
        elif isinstance(placement_instruction, CursorPlacementInstruction):
            print(placement_instruction)
        else:
            raise NotImplementedError

def compute_placement_instructions_for_paragraph(paragraph_node: "model.ParagraphModelNode") -> list[PlacementInstruction]:
    placement_instructions: list[PlacementInstruction] = []

    pending_excerpts: list[TextExcerpt] = []
    pending_whitespace_instruction: WhitespacePlacementInstruction = None
    pending_cursor_instruction: CursorPlacementInstruction = None

    def finish_pending_word():
        nonlocal placement_instructions
        nonlocal pending_excerpts
        nonlocal pending_whitespace_instruction
        nonlocal pending_cursor_instruction

        if pending_whitespace_instruction is not None:
            b_previous_was_whitespace_instruction = len(placement_instructions) >= 1 and isinstance(placement_instructions[-1], WhitespacePlacementInstruction)
            if not b_previous_was_whitespace_instruction:
                placement_instructions.append(pending_whitespace_instruction)
                pending_whitespace_instruction = None

        if pending_cursor_instruction is not None:
            placement_instructions.append(pending_cursor_instruction)
            pending_cursor_instruction = None

        if len(pending_excerpts) >= 1:
            placement_instructions.append(WordPlacementInstruction(
                excerpts=pending_excerpts,
            ))
            pending_excerpts=[]

    def add_pending_whitespace(whitespace_instruction: WhitespacePlacementInstruction):
        nonlocal pending_whitespace_instruction

        # By convention, if there are multiple spaces, we render the first one.
        if pending_whitespace_instruction is None:
            pending_whitespace_instruction = whitespace_instruction

    def add_pending_cursor(cursor_instruction: CursorPlacementInstruction):
        nonlocal pending_cursor_instruction
        nonlocal pending_whitespace_instruction

        assert pending_whitespace_instruction is not None
        assert pending_cursor_instruction is None

        pending_cursor_instruction = cursor_instruction

    for text_chunk_node in paragraph_node.children:
        assert isinstance(text_chunk_node, model.TextChunkModelNode)

        text_chunk_style_cascade = model.ModelStyleCascade(
            model_style_list=[
                paragraph_node.style,
                text_chunk_node.style,
            ],
            is_mutable=False,
        )

        remaining_text = text_chunk_node.text
        model_node_offset = 0

        while len(remaining_text) >= 1:
            if starts_with_whitespace(remaining_text):
                finish_pending_word()

                model_node_offset_before = model_node_offset

                # Consume whitespace.
                text_before, text_separator, text_after = partition_at_whitespace(remaining_text)
                assert len(text_before) == 0
                model_node_offset += len(text_before) + len(text_separator)
                remaining_text = text_after

                # If the cursor is within the separator, we must deal with it later and mark it as pending.
                # A similar check exists elsewhere but the '>' and '<' are different.
                if text_chunk_node.cursor_offset is not None:
                    b_cursor_offset_after_consumed_text = text_chunk_node.cursor_offset > model_node_offset_before + len(text_before)
                    b_cursor_offset_before_consumed_separator = text_chunk_node.cursor_offset < model_node_offset
                    if b_cursor_offset_after_consumed_text and b_cursor_offset_before_consumed_separator:
                        add_pending_cursor(CursorPlacementInstruction(
                            model_node=text_chunk_node,
                            model_offset=text_chunk_node.cursor_offset,
                        ))

                add_pending_whitespace(WhitespacePlacementInstruction(
                    model_node=text_chunk_node,
                    model_offset=model_node_offset_before,
                    style_cascade=text_chunk_style_cascade,
                ))

            if len(remaining_text) >= 1:
                model_node_offset_before = model_node_offset

                # Consume excerpt.
                text_before, text_separator, text_after = partition_at_whitespace(remaining_text)
                assert len(text_before) >= 1
                model_node_offset += len(text_before) + len(text_separator)
                remaining_text = text_after

                # Add to pending word group.
                # If the cursor is within this text excerpt, we do not care.
                pending_excerpts.append(TextExcerpt(
                    model_node=text_chunk_node,
                    model_offset=model_node_offset_before,
                    text=text_before,
                    style_cascade=text_chunk_style_cascade,
                ))

                # Finish the word group if whitespace consumed.
                if len(text_separator) >= 1:
                    finish_pending_word()

                    add_pending_whitespace(WhitespacePlacementInstruction(
                        model_node=text_chunk_node,
                        model_offset=model_node_offset_before + len(text_before),
                        style_cascade=text_chunk_style_cascade,
                    ))

                    # If the cursor is within the separator, we must deal with it later and mark it as pending.
                    # A similar check exists elsewhere but the '>' and '<=' are different.
                    if text_chunk_node.cursor_offset is not None:
                        b_cursor_offset_after_consumed_text = text_chunk_node.cursor_offset > model_node_offset_before + len(text_before)
                        b_cursor_offset_before_consumed_separator = text_chunk_node.cursor_offset <= model_node_offset
                        if b_cursor_offset_after_consumed_text and b_cursor_offset_before_consumed_separator:
                            add_pending_cursor(CursorPlacementInstruction(
                                model_node=text_chunk_node,
                                model_offset=text_chunk_node.cursor_offset,
                            ))

                            b_cursor_strictly_within_separator = text_chunk_node.cursor_offset < model_node_offset
                            if b_cursor_strictly_within_separator:
                                finish_pending_word()

                                add_pending_whitespace(WhitespacePlacementInstruction(
                                    model_node=text_chunk_node,
                                    model_offset=text_chunk_node.cursor_offset,
                                    style_cascade=text_chunk_style_cascade,
                                ))

    finish_pending_word()

    return placement_instructions

def group_instructions_by_line(*, instructions: list[PlacementInstruction], line_width: float):
    # FIXME
    pass
