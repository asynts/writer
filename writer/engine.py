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

            assert isinstance(self.document.header_node, model.ParagraphModelNode)
            self.add_paragraph(self.document.header_node, region=layout_header_node)

        if self.document.footer_node is not None:
            layout_footer_node = self.current_page.set_footer_node(layout.BlockLayoutNode())

            assert isinstance(self.document.footer_node, model.ParagraphModelNode)
            self.add_paragraph(self.document.footer_node, region=layout_footer_node)

    def add_paragraph(self, model_node: model.ParagraphModelNode, region: layout.LayoutNode = None):
        if region is None:
            region = self.current_region

        current_block_node = layout.BlockLayoutNode()
        region.append_child(current_block_node)

        offset_x = 0
        offset_y = 0

        for inline_node in model_node.children:
            # Compute what text we want to add.
            if isinstance(inline_node, model.TextChunkModelNode):
                text = inline_node.text
            elif isinstance(inline_node, model.FieldChunkModelNode):
                if inline_node.field == "page_number":
                    text = str(len(self.pages))
                else:
                    raise NotImplementedError
            else:
                raise NotImplementedError

            # Break the text into words.
            for word in text.split():
                word_width = (len(word) + 1) * layout.FONT_CHARACTER_WIDTH

                # Try to add the word in the current line.
                if offset_x + word_width <= current_block_node.max_width():
                    # Add the word to the current line.

                    text_node = layout.TextLayoutNode(text=word)
                    text_node.relative_x = offset_x
                    text_node.relative_y = offset_y
                    current_block_node.append_child(text_node)

                    offset_x += word_width
                else:
                    # Put the word on the next line.

                    offset_x = 0
                    offset_y += layout.FONT_CHARACTER_HEIGHT

                    # FIXME: Split the paragraph here, if necessary.

                    text_node = layout.TextLayoutNode(text=word)
                    text_node.relative_x = offset_x
                    text_node.relative_y = offset_y
                    current_block_node.append_child(text_node)

                    offset_x += word_width

def generate_layout_tree(document: model.DocumentModelNode):
    generator = LayoutTreeGenerator(document)

    for child_node in document.content_nodes:
        assert isinstance(child_node, model.ParagraphModelNode)
        generator.add_paragraph(child_node)

    return generator.pages
