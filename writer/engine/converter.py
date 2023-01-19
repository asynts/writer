import writer.engine.model as model
import writer.engine.layout as layout
import writer.engine.style as style
import writer.engine.util as util
import writer.engine.text_placement as text_placement
import writer.engine.history as history

def new_page_layout_node(
    *
    dependencies: "layout.LayoutDependencies",
    document_layout_node: "layout.VerticalLayoutNode",
) -> "layout.VerticalLayoutNode":
    return layout.VerticalLayoutNode(
        dependencies=dependencies,
        parent_node=document_layout_node,
        model_node=None,
        style=style.LayoutStyle(
            fixed_width=dependencies.display_information.cm_to_pixel(21.0),
            fixed_height=dependencies.display_information.cm_to_pixel(29.7),

            background_color=layout.COLOR_WHITE,
            border_color=layout.COLOR_BLACK,

            border_spacing=layout.Spacing(left=1.0, right=1.0, top=1.0, bottom=1.0),
            margin_spacing=layout.Spacing(top=10.0, bottom=10.0),
            padding_spacing=layout.Spacing(
                left=20.0,
                right=20.0,
                top=dependencies.display_information.cm_to_pixel(1.9),
                bottom=dependencies.display_information.cm_to_pixel(3.67)
            ),
        ),
    )

# Paragraphs belong to a page but can be re-parented.
def new_paragraph_layout_node(
    *,
    paragraph_model_node: "model.ParagraphModelNode",
    page_layout_node: "layout.VerticalLayoutNode",
    dependencies: "layout.LayoutDependencies",
):
    return layout.VerticalLayoutNode(
        dependencies=dependencies,
        parent_node=page_layout_node,
        model_node=paragraph_model_node,
        style=layout.LayoutStyle(
            margin_spacing=layout.Spacing(bottom=10.0),
        ),
    )

# Assumes that the provided instructions fit into the line.
def new_line_layout_node(
    *,
    line_instruction_group: list["text_placement.PlacementInstruction"],

    # FIXME: This should be included in the 'excerpt' (add it to 'WhitespacePlacementInstruction').
    paragraph_model_node: "model.ParagraphModelNode",
):
    # FIXME
    pass

class LayoutGenerator:
    def __init__(
        self,
        *,
        document_model_node: "model.DocumentModelNode",
        history_manager: "history.HistoryManager",
        display_information: "layout.DisplayInformation",
    ):
        self.document_model_node = document_model_node

        # FIXME: This should be constructed by the caller.
        self.dependencies = layout.LayoutDependencies(
            history_manager=history_manager,
            display_information=display_information,
        )

        self.document_layout_node = layout.VerticalLayoutNode(
            dependencies=self.dependencies,
            parent_node=None,
            model_node=document_model_node,
            style=style.LayoutStyle(),
        )

        self.page_layout_node = new_page_layout_node(
            document_layout_node=self.document_layout_node,
            dependencies=self.dependencies,
        )

    # Creates new pages when needed.
    def place_paragraph(
        self,
        paragraph_model_node: "model.ParagraphModelNode",
    ):
        paragraph_layout_node = new_paragraph_layout_node(
            paragraph_model_node=paragraph_model_node,
            page_layout_node=self.page_layout_node,
            dependencies=self.dependencies,
        )
        line_width = paragraph_layout_node.get_max_inner_width()

        instructions = text_placement.compute_placement_instructions_for_paragraph(paragraph_model_node)

        line_instruction_groups = text_placement.group_instructions_by_line(
            instructions=instructions,
            line_width=line_width,
        )

        for line_instruction_group in line_instruction_groups:
            line_height = max(instruction.height for instruction in line_instruction_group)

            b_overflows_paragraph = util.approximately_greater(
                paragraph_layout_node.get_min_outer_height() + line_height,
                self.page_layout_node.get_max_remaining_height(),
            )
            if b_overflows_paragraph:
                b_paragraph_empty = util.approximately_equal(paragraph_layout_node.get_min_inner_height(), 0.00)
                if b_paragraph_empty:
                    # Create new page and reparent paragraph to it.

                    paragraph_layout_node.clear_parent()

                    self.document_layout_node.place_child_node(self.page_layout_node)
                    self.page_layout_node = new_page_layout_node(
                        dependencies=self.dependencies,
                        document_layout_node=self.document_layout_node,
                    )

                    paragraph_layout_node.set_parent(self.page_layout_node)
                else:
                    # Place paragraph and create new paragraph on next page.

                    self.page_layout_node.place_child_node(paragraph_layout_node)
                    self.page_layout_node = new_page_layout_node()
                    paragraph_layout_node = new_paragraph_layout_node(
                        paragraph_model_node=paragraph_model_node,
                        page_layout_node=self.page_layout_node,
                        dependencies=self.dependencies,
                    )

            line_layout_node = new_line_layout_node(
                line_instruction_group=line_instruction_group,
                paragraph_model_node=paragraph_model_node,
            )
            paragraph_layout_node.place_child_node(line_layout_node)

        self.page_layout_node.place_child_node(paragraph_layout_node)

    def generate(self) -> "layout.VerticalLayoutNode":
        for paragraph_model_node in self.document_model_node.children:
            assert isinstance(paragraph_model_node, model.ParagraphModelNode)
            self.place_paragraph(paragraph_model_node=paragraph_model_node)

        self.document_layout_node.on_placed_in_node(relative_x=0, relative_y=0)
        return self.document_layout_node
