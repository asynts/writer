import string
from . import model, layout, style

import dataclasses

# We can't use PyQt from the PyTest environment.
b_simplify_font_metrics = False

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

        self.width = 0.0
        self.height = 0.0

    @property
    def text(self):
        return "".join(excerpt.text for excerpt in self.excerpts)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, WordGroup):
            return False

        # We don't compare the width and height here, because it's difficult to test for.
        return self.excerpts == other.excerpts

    def add_excerpt(self, excerpt: TextExcerpt):
        if b_simplify_font_metrics:
            self.width += len(excerpt.text + " ")
            self.height = 1
        else:
            # We reserve space for an additional space character such that the placement algorithm has enough space for that.
            # In block mode, we won't actually draw that space but we still need to reserve space for it.
            size = layout.normal_font_metrics.size(0, excerpt.text + " ")

            self.width += size.width()
            self.height = max(self.height, size.height())

        self.excerpts.append(excerpt)

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
            current_word_group.add_excerpt(TextExcerpt(
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

class Placer:
    def __init__(self):
        self._layout_tree = layout.VerticalLayoutNode(
            parent_node=None,
            style=style.LayoutStyle(),
        )

        self._current_page: layout.PageLayoutNode = None
        self._current_paragraph: layout.VerticalLayoutNode = None
        self._current_line: layout.HorizontalLayoutNode = None

    @property
    def layout_tree(self) -> layout.BlockLayoutNode:
        assert self._layout_tree is not None
        return self._layout_tree

    def finalize(self):
        layout_tree = self.layout_tree

        self.place_current_page()

        layout_tree.on_placed_in_node(relative_x=0, relative_y=0)

        self._layout_tree = None
        return layout_tree

    def place_current_page(self):
        assert self._current_paragraph is None

        self.layout_tree.place_child_node(self._current_page)

        self._current_page = None

    def create_new_page(self):
        if self._current_page is not None:
            self.place_current_page()

        self._current_page = layout.PageLayoutNode(parent_node=self.layout_tree)

    def place_current_paragraph(self):
        assert self._current_line is None

        content_node = self._current_page.get_content_node()

        assert content_node.get_max_remaining_height() >= self._current_paragraph.get_min_height() + self._current_paragraph.get_style().outer_spacing.y
        content_node.place_child_node(self._current_paragraph)

        self._current_paragraph = None

    def create_new_paragraph(self):
        assert self._current_paragraph is None

        content_node = self._current_page.get_content_node()
        self._current_paragraph = layout.VerticalLayoutNode(
            parent_node=content_node,
            style=style.LayoutStyle(
                margin_spacing=style.Spacing(bottom=10.0)
            ),
        )

    def try_place_current_line(self):
        if self._current_paragraph.get_max_remaining_height() >= self._current_line.get_min_height() + self._current_line.get_style().outer_spacing.y:
            # There is enough space to place this line in the current paragraph.
            self._current_paragraph.place_child_node(self._current_line)
            self._current_line = None

            return True
        else:
            # There is not enough space to place this line in the current paragraph.
            return False

    def place_current_line(self):
        if self.try_place_current_line():
            pass
        else:
            # We need to create a new paragraph on the next page.

            # The paragraph logic assumes that no line is pending.
            current_line = self._current_line
            self._current_line = None

            self.place_current_paragraph()
            self.create_new_page()
            self.create_new_paragraph()

            # We need to reparent the current line to the current paragraph.
            self._current_line = current_line
            self._current_line.set_parent(self._current_paragraph)

            # Now, it must work.
            assert self.try_place_current_line()

    def create_new_line(self):
        assert self._current_line is None
        self._current_line = layout.HorizontalLayoutNode(
            parent_node=self._current_paragraph,
            style=style.LayoutStyle(),
        )

    def place_word_group_in_current_line(self, word_group: WordGroup):
        assert self._current_line.get_max_remaining_width() >= word_group.width

        model_style = None
        for excerpt in word_group.excerpts:
            model_style = excerpt.text_chunk_model_node.get_style()

            self._current_line.place_child_node(layout.TextChunkLayoutNode(
                text=excerpt.text,
                parent_node=self._current_line,
                font_size=model_style.font_size,
                is_bold=model_style.is_bold,
                is_italic=model_style.is_italic,
            ))

        # This is a bit naughty, we simply take the style from the last excerpt.
        assert model_style is not None

        # FIXME: Do the spacing separately.
        self._current_line.place_child_node(layout.TextChunkLayoutNode(
            text=" ",
            parent_node=self._current_line,
            font_size=model_style.font_size,
            is_bold=model_style.is_bold,
            is_italic=model_style.is_italic,
        ))

    def place_paragraph(self, paragraph_model_node: model.ParagraphModelNode):
        assert isinstance(paragraph_model_node, model.ParagraphModelNode)

        self.create_new_paragraph()
        self.create_new_line()

        word_groups = compute_word_groups_in_paragraph(paragraph_model_node)

        for word_group in word_groups:
            if self._current_line.get_max_remaining_width() >= word_group.width:
                # There is enough space to place this word group in the current line.
                self.place_word_group_in_current_line(word_group)
            else:
                # There is not enough space in the current line to fit this word group, create a new line.
                self.place_current_line()
                self.create_new_line()
                self.place_word_group_in_current_line(word_group)

        self.place_current_line()
        self.place_current_paragraph()

    def place_document(self, document_model_node: model.DocumentModelNode):
        assert isinstance(document_model_node, model.DocumentModelNode)

        self.create_new_page()

        for paragraph_model_node in document_model_node.get_children():
            assert isinstance(paragraph_model_node, model.ParagraphModelNode)
            self.place_paragraph(paragraph_model_node)

def generate_layout_for_model(document_model_node: model.DocumentModelNode) -> layout.BlockLayoutNode:
    placer = Placer()

    placer.place_document(document_model_node)

    return placer.finalize()
