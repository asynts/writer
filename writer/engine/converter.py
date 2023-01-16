import writer.engine.model as model
import writer.engine.layout as layout
import writer.engine.style as style
import writer.engine.util as util
import writer.engine.text_placement as text_placement
import writer.engine.history as history

class LayoutGenerator:
    def __init__(
        self,
        *,
        document_model_node: model.DocumentModelNode,
        history_manager: history.HistoryManager,
        display_information: layout.DisplayInformation
    ):
        self.display_information = display_information

        self.layout_dependencies = layout.LayoutDependencies(
            history_manager=history_manager,
            display_information=display_information,
        )

        self.document_layout_node = layout.VerticalLayoutNode(
            dependencies=self.layout_dependencies,
            parent_node=None,
            model_node=document_model_node,
            style=style.LayoutStyle(),
        )

        # Invariant: There is always a pending page until 'self.finalize' is called.
        #
        # Invariant: The pending paragraph always fits on the current page.
        #            FIXME: My code doesn't correctly enforce this yet.
        self.pending_page_layout_node: layout.VerticalLayoutNode = None
        self.new_pending_page()

        self.pending_paragraph_layout_node: layout.VerticalLayoutNode = None

    def _try_place_pending_page(self):
        if self.pending_page_layout_node is not None:
            self.document_layout_node.place_child_node(self.pending_page_layout_node)
            self.pending_page_layout_node = None

    def _try_place_pending_paragraph(self):
        if self.pending_paragraph_layout_node is not None:
            # The pending paragraph always fits on the current page.
            assert util.approximately_less(self.pending_paragraph_layout_node.get_min_outer_height(), self.pending_page_layout_node.get_max_remaining_height())

            self.pending_page_layout_node.place_child_node(self.pending_paragraph_layout_node)
            self.pending_paragraph_layout_node = None

    # This function assumes that all the line instructions fit in one line.
    # The caller needs to verify that.
    def _generate_line_layout_node(
        self,
        *,
        line_width: float,
        line_instructions: list["text_placement.PlacementInstruction"],
        paragraph_model_node: "model.ParagraphModelNode",
    ) -> "layout.LayoutNode":
        line_layout_node = layout.HorizontalLayoutNode(
            dependencies=self.layout_dependencies,
            parent_node=self.pending_paragraph_layout_node,
            model_node=None,
            style=layout.LayoutStyle(),
        )

        for instruction in line_instructions:
            if isinstance(instruction, text_placement.CursorPlacementInstruction):
                # FIXME: Place the cursor here.
                #        Or delay the placement.
                pass
            elif isinstance(instruction, text_placement.WhitespacePlacementInstruction):
                line_layout_node.place_child_node(layout.SpacingLayoutNode(
                    dependencies=self.layout_dependencies,
                    parent_node=line_layout_node,
                    model_node=instruction.model_node,
                    fixed_width=instruction.width,
                    style_cascade=model.ModelStyleCascade([
                        paragraph_model_node.style,
                        instruction.model_node.style,
                    ])
                ))
            elif isinstance(instruction, text_placement.WordPlacementInstruction):
                for excerpt in instruction.excerpts:
                    # FIXME: If the cursor is in the middle, we need to split the text node.
                    line_layout_node.place_child_node(layout.TextChunkLayoutNode(
                        dependencies=self.layout_dependencies,
                        text=excerpt.text,
                        parent_node=line_layout_node,
                        model_node=excerpt.model_node,
                        model_node_offset=excerpt.model_offset,
                        style_cascade=excerpt.style_cascade,
                    ))
            else:
                raise AssertionError

        return line_layout_node

    def new_pending_page(self):
        self._try_place_pending_page()

        self.pending_page_layout_node = layout.VerticalLayoutNode(
            dependencies=self.layout_dependencies,
            parent_node=self.document_layout_node,
            model_node=None,
            style=style.LayoutStyle(
                fixed_width=self.display_information.cm_to_pixel(21.0),
                fixed_height=self.display_information.cm_to_pixel(29.7),

                background_color=layout.COLOR_WHITE,
                border_color=layout.COLOR_BLACK,

                border_spacing=layout.Spacing(left=1.0, right=1.0, top=1.0, bottom=1.0),
                margin_spacing=layout.Spacing(top=10.0, bottom=10.0),
                padding_spacing=layout.Spacing(
                    left=20.0,
                    right=20.0,
                    top=self.display_information.cm_to_pixel(1.9),
                    bottom=self.display_information.cm_to_pixel(3.67)
                ),
            ),
        )

    def new_pending_paragraph(self, *, paragraph_model_node: model.ParagraphModelNode):
        self._try_place_pending_paragraph()

        self.pending_paragraph_layout_node = layout.VerticalLayoutNode(
            dependencies=self.layout_dependencies,
            parent_node=self.pending_page_layout_node,
            model_node=paragraph_model_node,
            style=layout.LayoutStyle(
                margin_spacing=layout.Spacing(bottom=10.0),
            ),
        )

        # FIXME: It could happen that the padding already overflows the page.
        #        Then we would have to re-parent the paragraph to the next page.

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

            current_line_height = max(instruction.height for instruction in current_line_instructions)

            # Ensure we have enough space for this paragraph.
            if util.approximately_greater(current_line_height, self.pending_paragraph_layout_node.get_max_remaining_height()):
                if util.approximately_equal(self.pending_paragraph_layout_node.get_min_inner_height(), 0.00):
                    # If the pending paragraph is empty, create new page and re-parent.
                    self.pending_paragraph_layout_node.clear_parent()
                    self.new_pending_page()
                    self.pending_paragraph_layout_node.set_parent(self.pending_page_layout_node)
                else:
                    # Otherwise, create new paragraph.
                    self.new_pending_paragraph(paragraph_model_node=paragraph_model_node)

                # We assume that the new paragraph layout node has the same width, which should be reasonable.
                assert self.pending_paragraph_layout_node.get_max_inner_width() == max_line_width

            line_layout_node = self._generate_line_layout_node(
                line_width=current_line_width,
                line_instructions=current_line_instructions,
                paragraph_model_node=paragraph_model_node,
            )
            self.pending_paragraph_layout_node.place_child_node(line_layout_node)

            # We are now done with that line, however, we might carry a 'pending_cursor_instruction' into the next line.
            continue

        self._try_place_pending_paragraph()

    def finalize(self) -> layout.LayoutNode:
        self._try_place_pending_paragraph()
        self._try_place_pending_page()

        self.document_layout_node.on_placed_in_node(relative_x=0, relative_y=0)

        return self.document_layout_node

def generate_layout_for_model(
    document_model_node: model.DocumentModelNode,
    *,
    history_manager: history.HistoryManager,
    display_information: layout.DisplayInformation,
) -> layout.LayoutNode:
    layout_generator = LayoutGenerator(
        document_model_node=document_model_node,
        history_manager=history_manager,
        display_information=display_information,
    )

    for paragraph_model_node in document_model_node.children:
        assert isinstance(paragraph_model_node, model.ParagraphModelNode)
        layout_generator.place_paragraph(paragraph_model_node)

    return layout_generator.finalize()
