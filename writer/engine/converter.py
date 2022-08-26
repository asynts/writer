import writer.engine.model as model
import writer.engine.layout as layout
import writer.engine.style as style
import writer.engine.util as util
import writer.engine.text_placement as text_placement

# We can't use PyQt from the PyTest environment.
b_simplify_font_metrics = False

class Placer:
    def __init__(self, *, document_model_node: "model.DocumentModelNode"):
        self._layout_tree = layout.VerticalLayoutNode(
            parent_node=None,
            model_node=document_model_node,
            style=style.LayoutStyle(),
        )

        self._style_cascade = model.ModelStyleCascade([
            document_model_node.style,
        ])

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
            self._style_cascade.push_style(excerpt.text_chunk_model_node.style)

            if excerpt.text_chunk_model_node.cursor_offset is not None:
                b_cursor_is_out_of_bounds_left = (excerpt.text_chunk_model_node.cursor_offset <= excerpt.offset_into_model_node)
                b_cursor_is_out_of_bounds_right = (excerpt.text_chunk_model_node.cursor_offset > excerpt.offset_into_model_node + len(excerpt.raw_text))

                b_place_cursor = (not b_cursor_is_out_of_bounds_left) and (not b_cursor_is_out_of_bounds_right)
            else:
                b_place_cursor = False

            if b_place_cursor:
                # FIXME: We sometimes place a space too much here.

                self._current_line.place_child_node(layout.TextChunkLayoutNode(
                    text=excerpt.text_chunk_model_node.text[excerpt.offset_into_model_node:excerpt.text_chunk_model_node.cursor_offset],
                    parent_node=self._current_line,

                    model_node=excerpt.text_chunk_model_node,
                    model_node_offset=excerpt.offset_into_model_node,

                    style_cascade=excerpt.style_cascade,
                ))

                self._current_line.place_child_node(layout.CursorLayoutNode(
                    parent_node=self._current_line,
                    model_node=excerpt.text_chunk_model_node,
                    model_node_offset=excerpt.offset_into_model_node + excerpt.text_chunk_model_node.cursor_offset,

                    style_cascade=excerpt.style_cascade,
                ))

                self._current_line.place_child_node(layout.TextChunkLayoutNode(
                    text=excerpt.text_chunk_model_node.text[excerpt.text_chunk_model_node.cursor_offset:excerpt.offset_into_model_node + len(excerpt.text)],
                    parent_node=self._current_line,

                    model_node=excerpt.text_chunk_model_node,
                    model_node_offset=excerpt.offset_into_model_node + excerpt.text_chunk_model_node.cursor_offset,

                    style_cascade=excerpt.style_cascade,
                ))
            else:
                self._current_line.place_child_node(layout.TextChunkLayoutNode(
                    text=excerpt.text,
                    parent_node=self._current_line,

                    model_node=excerpt.text_chunk_model_node,
                    model_node_offset=excerpt.offset_into_model_node,

                    style_cascade=excerpt.style_cascade,
                ))

            self._style_cascade.pop_style(excerpt.text_chunk_model_node.style)

        # We are taking the formatting from the last excerpt from the loop.
        assert excerpt is not None

        # FIXME: Do the spacing separately.
        self._current_line.place_child_node(layout.TextChunkLayoutNode(
            text=" ",
            parent_node=self._current_line,

            model_node=excerpt.text_chunk_model_node,
            model_node_offset=excerpt.offset_into_model_node + len(excerpt.text),

                    style_cascade=excerpt.style_cascade,
        ))

    def place_paragraph(self, paragraph_model_node: model.ParagraphModelNode):
        self._style_cascade.push_style(paragraph_model_node.style)

        placement_instructions = text_placement.compute_placement_instructions_for_paragraph(
            paragraph_node=paragraph_model_node,
            paragraph_style_cascade=self._style_cascade,
        )

        # FIXME: We need to terminate at some point.
        while True:
            self.create_new_paragraph()

            maximum_line_width = self._current_paragraph.get_width()

            current_line_placement_instructions = []
            current_line_width = 0.0
            pending_whitespace_instruction = None
            pending_cursor_instruction = None
            for placement_instruction in placement_instructions:
                if isinstance(placement_instruction, text_placement.WordPlacementInstruction):
                    if pending_whitespace_instruction is not None:
                        spacing_width = pending_whitespace_instruction.width
                    else:
                        spacing_width = 0.0

                    if util.approximately_less(current_line_width + spacing_width + placement_instruction.width, maximum_line_width):
                        if pending_whitespace_instruction:
                            current_line_placement_instructions.append(pending_whitespace_instruction)
                            pending_whitespace_instruction = None

                        current_line_placement_instructions.append(placement_instruction)
                    else:
                        # FIXME: Create new line.
                        pass
                elif isinstance(placement_instruction, text_placement.WhitespacePlacementInstruction):
                    assert pending_whitespace_instruction is None
                    pending_whitespace_instruction = placement_instruction
                elif isinstance(placement_instruction, text_placement.CursorPlacementInstruction):
                    # FIXME: Deal with pending cursor instruction
                    pass


        self._style_cascade.pop_style(paragraph_model_node.style)

    def place_paragraph(self, paragraph_model_node: model.ParagraphModelNode):
        assert isinstance(paragraph_model_node, model.ParagraphModelNode)

        # Check if this node has exactly one cached layout node.
        # If there are multiple, then we can't easily reuse them.
        if paragraph_model_node.layout_nodes is not None and len(paragraph_model_node.layout_nodes) == 1:
            layout_node = paragraph_model_node.layout_nodes[0]
            content_node = self._current_page.get_content_node()

            # Check if this cached layout node can be reused in this context.
            b_width_exactly_equal = util.approximately_equal(layout_node.get_width(), content_node.get_max_inner_width())
            b_fits_on_page = util.approximately_less(layout_node.get_height(), content_node.get_max_remaining_height())
            if b_width_exactly_equal and b_fits_on_page:
                # Place the existing layout node in this new environment.
                layout_node.on_reused_with_new_parent(parent_node=content_node)
                content_node.place_child_node(layout_node)
                return
        paragraph_model_node.layout_nodes = None

        self._current_model_paragraph_node = paragraph_model_node

        assert self._current_paragraph_layout_nodes is None
        self._current_paragraph_layout_nodes = []

        self._style_cascade.push_style(paragraph_model_node.style)

        self.create_new_paragraph()
        self.create_new_line()

        placement_instructions = text_placement.compute_placement_instructions_for_paragraph(paragraph_model_node)

        for placement_instruction in placement_instructions:


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

        self._style_cascade.pop_style(paragraph_model_node.style)

    def place_document(self, document_model_node: model.DocumentModelNode):
        assert isinstance(document_model_node, model.DocumentModelNode)

        self.create_new_page()

        for paragraph_model_node in document_model_node.children:
            assert isinstance(paragraph_model_node, model.ParagraphModelNode)
            self.place_paragraph(paragraph_model_node)

def generate_layout_for_model(document_model_node: model.DocumentModelNode) -> layout.BlockLayoutNode:
    placer = Placer(document_model_node=document_model_node)
    return placer.finalize()
