import model
import layout

class LayoutTreeGenerator:
    def __init__(self, document: model.DocumentModelNode):
        self.document = document
        self.pages = []

        self.next_page()
        self.next_region()

    # When we can't fit something into the current region, we request a new region.
    # This can either find another region on the same page (multi-column layout) or
    # it can create a new page to provide the region.
    def next_region(self):
        # FIXME: We should generalize this somehow, for header and footer.
        #        In that case we want to return none, but not sure, how to approach this.

        self.current_region = self.current_page.add_content_node(layout.BlockLayoutNode())

    def next_page(self):
        new_page = layout.PageLayoutNode()
        self.pages.append(new_page)
        self.current_page = new_page

        if self.document.header_node is not None:
            layout_header_node = self.current_page.set_header_node(layout.BlockLayoutNode())
            self.add_block_model_node(self.document.header_node, region=layout_header_node)

        if self.document.footer_node is not None:
            layout_footer_node = self.current_page.set_footer_node(layout.BlockLayoutNode())
            self.add_block_model_node(self.document.footer_node, region=layout_footer_node)

    def add_inline_model_node(self, node: model.ModelNode, *, container_node: layout.BlockLayoutNode):
        # FIXME: We have to be able to split paragraphs here.

        if isinstance(node, model.TextChunkModelNode):
            # FIXME: Implement text wrapping here.
            container_node.append_child(layout.TextLayoutNode(text=node.text))
        elif isinstance(node, model.FieldChunkModelNode):
            if node.field == "page_number":
                container_node.append_child(layout.TextLayoutNode(text=str(len(self.pages))))
            else:
                raise NotImplementedError
        else:
            raise NotImplementedError

    def add_block_model_node(self, node: model.ModelNode, *, region: layout.LayoutNode = None):
        if region is None:
            region = self.current_region

        if isinstance(node, model.ParagraphModelNode):
            paragraph_node = layout.BlockLayoutNode()
            region.append_child(paragraph_node)

            for child_node in node.children:
                self.add_inline_model_node(child_node, container_node=paragraph_node)
        else:
            raise NotImplementedError

def generate_layout_tree(document: model.DocumentModelNode):
    generator = LayoutTreeGenerator(document)

    for child_node in document.content_nodes:
        generator.add_block_model_node(child_node)

    return generator.pages
