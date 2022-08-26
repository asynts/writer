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
            if util.approximately_greater(self.pending_paragraph_layout_node.get_height(), self.pending_page_layout_node.get_max_remaining_height()):
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

    def new_pending_paragraph(self, paragraph_model_node: model.ParagraphModelNode):
        assert self.pending_paragraph_layout_node is None

        self.pending_paragraph_layout_node = layout.VerticalLayoutNode(
            parent_node=self.pending_page_layout_node,
            model_node=paragraph_model_node,
            style=layout.LayoutStyle(
                margin_spacing=layout.Spacing(bottom=10.0),
            ),
        )

    def place_paragraph(self, paragraph_model_node: model.ParagraphModelNode):
        placement_instructions = text_placement.compute_placement_instructions_for_paragraph(paragraph_model_node)

        # FIXME: Magic.

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
