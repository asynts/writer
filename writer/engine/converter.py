import string
from . import model, layout, style

import dataclasses

# We can't use PyQt from the PyTest environment.
b_simplify_font_metrics = False

# Represents an excerpt from a text chunk in the model.
# Text chunks can belong to multiple word groups.
@dataclasses.dataclass(frozen=True, kw_only=True, slots=True)
class TextExcerpt:
    text_chunk_model_node: model.TextChunkModelNode
    text: str
    offset_into_model_node: int

# Represents one word that should be wrapped as one.
# Words can span over multiple text chunks in the model.
class WordGroup:
    __slots__ = (
        "excerpts",
        "width",
        "height",
    )

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

    def __repr__(self):
        result = "WordGroup("
        for excerpt in self.excerpts:
            result += f" {excerpt}"
        result += " )"
        return result

    def add_excerpt(self, excerpt: TextExcerpt):
        if b_simplify_font_metrics:
            self.width += len(excerpt.text + " ")
            self.height = 1
        else:
            # We reserve space for an additional space character such that the placement algorithm has enough space for that.
            # In block mode, we won't actually draw that space but we still need to reserve space for it.
            text = excerpt.text + " "

            size = excerpt.text_chunk_model_node.font_metrics.size(0, text)

            self.width += size.width()
            self.height = max(self.height, size.height())

        self.excerpts.append(excerpt)

    def is_empty(self) -> bool:
        return len(self.excerpts) == 0

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

    for text_chunk_model_node in paragraph_model_node.children:
        assert isinstance(text_chunk_model_node, model.TextChunkModelNode)

        offset_into_model_node = 0
        remaining_text = text_chunk_model_node.text

        while len(remaining_text) >= 1:
            # We split of the first word and update our offset calculation.
            offset_into_model_node_before = offset_into_model_node
            text, separator, remaining_text = partition_at_whitespace(remaining_text)
            offset_into_model_node += len(text) + len(separator)

            # If we encounter a separator without anything any text before it, open a new word group.
            if len(text) == 0:
                finish_word_group()
                continue

            # Add this text to the current word group.
            current_word_group.add_excerpt(TextExcerpt(
                text_chunk_model_node=text_chunk_model_node,
                offset_into_model_node=offset_into_model_node_before,
                text=text,
            ))

            # If a separator was encountered, open a new word group.
            # Notice that this is different from the other edge case, because the code runs after the text was added.
            if len(separator) >= 1:
                finish_word_group()

    finish_word_group()

    return word_groups

class Placer:
    def __init__(self, *, document_model_node: "model.DocumentModelNode"):
        self._layout_tree = layout.VerticalLayoutNode(
            parent_node=None,
            model_node=document_model_node,
            style=style.LayoutStyle(),
        )

        self._current_page: layout.PageLayoutNode = None
        self._current_paragraph: layout.VerticalLayoutNode = None
        self._current_line: layout.HorizontalLayoutNode = None

        # The paragraph needs to know which layout nodes are used to represent it.
        # We keep track of the layout nodes that we already created for the current paragraph, then we
        # assign it to the model node in the end.
        self._current_paragraph_layout_nodes: list[layout.VerticalLayoutNode] = None

        self._current_model_paragraph_node: layout.VerticalLayoutNode = None

        self.place_document(document_model_node)

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

        # This is not an optimization.
        # An empty paragraph can have spacing which already exceeds the remaining size.
        # That would result in a crash.
        if len(self._current_paragraph.get_children()) == 0:
            self._current_paragraph.get_parent_node().on_child_dissociated(self._current_paragraph)
            self._current_paragraph = None
            return

        content_node = self._current_page.get_content_node()
        assert content_node.get_max_remaining_height() >= self._current_paragraph.get_min_height() + self._current_paragraph.get_style().outer_spacing.y

        self._current_paragraph_layout_nodes.append(self._current_paragraph)
        content_node.place_child_node(self._current_paragraph)

        self._current_paragraph = None

    def create_new_paragraph(self):
        assert self._current_paragraph is None

        content_node = self._current_page.get_content_node()
        self._current_paragraph = layout.VerticalLayoutNode(
            parent_node=content_node,
            model_node=self._current_model_paragraph_node,

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
            current_line.get_parent_node().on_child_dissociated(current_line)
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
            model_node=None,

            style=style.LayoutStyle(),
        )

    def place_word_group_in_current_line(self, word_group: WordGroup):
        assert self._current_line.get_max_remaining_width() >= word_group.width

        excerpt = None
        for excerpt in word_group.excerpts:
            self._current_line.place_child_node(layout.TextChunkLayoutNode(
                text=excerpt.text,
                parent_node=self._current_line,

                model_node=excerpt.text_chunk_model_node,
                model_node_offset=excerpt.offset_into_model_node,
            ))

        # We are taking the formatting from the last excerpt from the loop.
        assert excerpt is not None

        # FIXME: Do the spacing separately.
        self._current_line.place_child_node(layout.TextChunkLayoutNode(
            text=" ",
            parent_node=self._current_line,

            model_node=excerpt.text_chunk_model_node,
            model_node_offset=excerpt.offset_into_model_node + len(excerpt.text),
        ))

    def place_paragraph(self, paragraph_model_node: model.ParagraphModelNode):
        assert isinstance(paragraph_model_node, model.ParagraphModelNode)

        # Check if this node has exactly one cached layout node.
        # If there are multiple, then we can't easily reuse them.
        if paragraph_model_node.layout_nodes is not None and len(paragraph_model_node.layout_nodes) == 1:
            layout_node = paragraph_model_node.layout_nodes[0]
            content_node = self._current_page.get_content_node()

            # FIXME: What about floating point inaccuracies?

            # Check if this cached layout node can be reused in this context.
            b_width_exactly_equal = (layout_node.get_absolute_width() == content_node.get_max_width())
            b_fits_on_page = (layout_node.get_absolute_height() <= content_node.get_max_remaining_height())
            if b_width_exactly_equal and b_fits_on_page:
                # Place the existing layout node in this new environment.
                layout_node.on_reused_with_new_parent(parent_node=content_node)
                content_node.place_child_node(layout_node)
                return
        paragraph_model_node.layout_nodes = None

        self._current_model_paragraph_node = paragraph_model_node

        assert self._current_paragraph_layout_nodes is None
        self._current_paragraph_layout_nodes = []

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

        paragraph_model_node.layout_nodes = self._current_paragraph_layout_nodes
        self._current_paragraph_layout_nodes = None

        self._current_model_paragraph_node = None

    def place_document(self, document_model_node: model.DocumentModelNode):
        assert isinstance(document_model_node, model.DocumentModelNode)

        self.create_new_page()

        for paragraph_model_node in document_model_node.children:
            assert isinstance(paragraph_model_node, model.ParagraphModelNode)
            self.place_paragraph(paragraph_model_node)

def generate_layout_for_model(document_model_node: model.DocumentModelNode) -> layout.BlockLayoutNode:
    placer = Placer(document_model_node=document_model_node)

    # FIXME: We should clear the saved layout nodes before we start here, or we should ignore them entirely.

    return placer.finalize()
