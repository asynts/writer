import writer.engine.model as model
import writer.engine.layout as layout
import writer.engine.style as style
import writer.engine.util as util
import writer.engine.text_placement as text_placement

class LayoutGenerator:
    def __init__(self, document_model_node: model.DocumentModelNode):
        self.document_layout_node = layout.VerticalLayoutNode(
            parent_node=None,
            model_node=document_model_node,
            style=style.LayoutStyle(),
        )

        # Invariant: There is always a pending page until 'self.finalize' is called.
        self.pending_page_layout_node: layout.VerticalLayoutNode = None
        self.new_pending_page()

        self.pending_paragraph_layout_node: layout.VerticalLayoutNode = None

    def _try_place_pending_page(self):
        if self.pending_page_layout_node is not None:
            self.document_layout_node.place_child_node(self.pending_page_layout_node)
            self.pending_page_layout_node = None

    def _try_place_pending_paragraph(self):
        if self.pending_paragraph_layout_node is not None:
            # Create new pending page if paragraph does not fit.
            if util.approximately_greater(self.pending_paragraph_layout_node.get_min_height(), self.pending_page_layout_node.get_max_remaining_height()):
                self.new_pending_page()

            self.pending_page_layout_node.place_child_node(self.pending_paragraph_layout_node)
            self.pending_paragraph_layout_node = None

    def new_pending_page(self):
        self._try_place_pending_page()

        self.pending_page_layout_node = layout.VerticalLayoutNode(
            parent_node=self.document_layout_node,
            model_node=None,
            style=style.LayoutStyle(
                fixed_width=layout.cm_to_pixel(21.0),
                fixed_height=layout.cm_to_pixel(29.7),

                background_color=layout.COLOR_WHITE,
                border_color=layout.COLOR_BLACK,

                border_spacing=layout.Spacing(left=1.0, right=1.0, top=1.0, bottom=1.0),
                margin_spacing=layout.Spacing(top=10.0, bottom=10.0),
                padding_spacing=layout.Spacing(left=20.0, right=20.0, top=layout.cm_to_pixel(1.9), bottom=layout.cm_to_pixel(3.67)),
            ),
        )

    def new_pending_paragraph(self, *, paragraph_model_node: model.ParagraphModelNode):
        assert self.pending_paragraph_layout_node is None

        self.pending_paragraph_layout_node = layout.VerticalLayoutNode(
            parent_node=self.pending_page_layout_node,
            model_node=paragraph_model_node,
            style=layout.LayoutStyle(
                margin_spacing=layout.Spacing(bottom=10.0),
            ),
        )

    def place_paragraph(self, paragraph_model_node: model.ParagraphModelNode):
        remaining_instructions = text_placement.compute_placement_instructions_for_paragraph(paragraph_model_node)

        self.new_pending_paragraph(paragraph_model_node=paragraph_model_node)

        pending_cursor_instruction: text_placement.CursorPlacementInstruction = None

        while len(remaining_instructions) >= 1:
            # Place one line at a time.

            max_line_width = self.pending_paragraph_layout_node.get_max_inner_width()

            current_line_instructions: list[text_placement.PlacementInstruction] = []
            current_line_width = 0.0

            while len(remaining_instructions) >= 1:
                instruction = remaining_instructions.pop(0)

                if isinstance(instruction, text_placement.WordPlacementInstruction):
                    if util.approximately_less(current_line_width + instruction.width, max_line_width):
                        # Place cursor if necessary.
                        if pending_cursor_instruction is not None:
                            current_line_instructions.append(pending_cursor_instruction)
                            pending_cursor_instruction = None

                        # Word does fit in the current line, continue.
                        current_line_instructions.append(instruction)
                        current_line_width += instruction.width
                        continue
                    else:
                        # Word does not fit in current line, break.
                        remaining_instructions.insert(0, instruction)
                        break
                elif isinstance(instruction, text_placement.WhitespacePlacementInstruction):
                    if util.approximately_less(current_line_width + instruction.width, max_line_width):
                        # Place cursor if necessary.
                        if pending_cursor_instruction is not None:
                            current_line_instructions.append(pending_cursor_instruction)
                            pending_cursor_instruction = None

                        # Whitespace does fit in the current line, continue.
                        current_line_instructions.append(instruction)
                        current_line_width += instruction.width
                    else:
                        if pending_cursor_instruction is None:
                            # Whitespace does not fit in current line, break.
                            # But we do not queue it again, since a new line is essentially whitespace.
                            break
                        else:
                            # Whitespace does not fit in current line, break.
                            # But we do queue again, because the cursor will otherwise be rendered incorrectly.
                            remaining_instructions.insert(0, instruction)
                            break
                elif isinstance(instruction, text_placement.CursorPlacementInstruction):
                    assert pending_cursor_instruction is None

                    # Cursor can always be placed, but delay placement.
                    pending_cursor_instruction = instruction
                    continue
                else:
                    raise AssertionError

            if pending_cursor_instruction is not None:
                # It can happen, that the cursor is placed at the very end.
                if len(remaining_instructions) == 0:
                    current_line_instructions.append(pending_cursor_instruction)
                    pending_cursor_instruction = None

            current_line_height = sum(instruction.height for instruction in current_line_instructions)

            # Not enough space in this paragraph, create a new one.
            if util.approximately_greater(current_line_height, self.pending_paragraph_layout_node.get_max_remaining_height()):
                self.new_pending_paragraph(paragraph_model_node=paragraph_model_node)

                # We assume that the new paragraph layout node has the same width, which should be reasonable.
                assert self.pending_paragraph_layout_node.get_max_inner_width() == max_line_width

            line_layout_node = layout.HorizontalLayoutNode(
                parent_node=self.pending_paragraph_layout_node,
                model_node=None,
                style=layout.LayoutStyle(),
            )

            # FIXME: Now, we need to create all the 'TextChunkLayoutNode' nodes.

            self.pending_paragraph_layout_node.place_child_node(line_layout_node)

            # We are now done with that line, however, we might carry a 'pending_cursor_instruction' into the next line.
            continue

        self._try_place_pending_paragraph()

    def finalize(self) -> layout.LayoutNode:
        self._try_place_pending_paragraph()
        self._try_place_pending_page()

        self.document_layout_node.on_placed_in_node(relative_x=0, relative_y=0)

        return self.document_layout_node

def generate_layout_for_model(document_model_node: model.DocumentModelNode) -> layout.LayoutNode:
    layout_generator = LayoutGenerator(document_model_node)

    for paragraph_model_node in document_model_node.children:
        assert isinstance(paragraph_model_node, model.ParagraphModelNode)
        layout_generator.place_paragraph(paragraph_model_node)

    return layout_generator.finalize()
