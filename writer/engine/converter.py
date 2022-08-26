import writer.engine.model as model
import writer.engine.layout as layout
import writer.engine.style as style
import writer.engine.util as util
import writer.engine.text_placement as text_placement

class LayoutGenerator:
    def __init__(self, document_model_node: model.DocumentModelNode):
        self.document_layout_node: layout.BlockLayoutNode = None
        self.pending_page_layout_node: layout.BlockLayoutNode = None

        self.document_layout_node = layout.VerticalLayoutNode(
            parent_node=None,
            model_node=document_model_node,
            style=style.LayoutStyle(),
        )

        self.new_page()

    def try_place_pending_page(self):
        if self.pending_page_layout_node is not None:
            self.document_layout_node.place_child_node(self.pending_page_layout_node)
            self.pending_page_layout_node = None

    def new_page(self):
        self.try_place_pending_page()

        self.pending_page_layout_node = layout.VerticalLayoutNode(
            parent_node=self.document_layout_node,
            model_node=None,
            style=style.LayoutStyle(),

            fixed_width=layout.cm_to_pixel(21.0),
            fixed_height=layout.cm_to_pixel(29.7),

            background_color=layout.COLOR_WHITE,
            border_color=layout.COLOR_BLACK,

            border_spacing=layout.Spacing(left=1.0, right=1.0, top=1.0, bottom=1.0),
            margin_spacing=layout.Spacing(top=10.0, bottom=10.0),
            padding_spacing=layout.Spacing(left=20.0, right=20.0, top=layout.cm_to_pixel(1.9), bottom=layout.cm_to_pixel(3.67)),
        )

    def place_paragraph(self):
        # FIXME: Place paragraph.
        pass

    def finalize(self) -> layout.LayoutNode:
        self.try_place_pending_page()

        return self.document_layout_node

def generate_layout_for_model(document_model_node: model.DocumentModelNode) -> layout.LayoutNode:
    layout_generator = LayoutGenerator(document_model_node)

    for paragraph_model_node in document_model_node.children:
        assert isinstance(paragraph_model_node, model.ParagraphModelNode)
        layout_generator.place_paragraph(paragraph_model_node)

    return layout_generator.finalize()
