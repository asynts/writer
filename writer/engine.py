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

    # FIXME: I don't think we can just have a method to deal with an inline node without considering the paragraph node around.
    def add_inline_model_node(self, node: model.ModelNode, *, container_node: layout.BlockLayoutNode):
        # FIXME: We have to be able to split paragraphs here.

        if isinstance(node, model.TextChunkModelNode):
            # FIXME: We need to keep track of this on a paragraph level.
            offset_x = 0
            offset_y = 0

            current_text_node = layout.TextLayoutNode(text="")
            container_node.append_child(current_text_node)
            for word in node.text.split():
                # FIXME: We do not always need the '+1', only if this isn't the first word.
                if offset_x + (len(word) + 1) * layout.FONT_CHARACTER_WIDTH <= container_node.max_width():
                    # We are able to fit this word into this line.
                    if len(current_text_node.text) >= 1:
                        current_text_node.text += " "
                    current_text_node.text += word

                    offset_x += (len(word) + 1) * layout.FONT_CHARACTER_WIDTH
                else:
                    # We need to put this onto another line.
                    current_text_node = layout.TextLayoutNode(text=word)
                    container_node.append_child(current_text_node)

                    offset_y += layout.FONT_CHARACTER_HEIGHT
                    offset_x = 0
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
