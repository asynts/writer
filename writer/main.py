import model

document = model.DocumentModelNode()

document.footer.append_child(model.TextChunkModelNode(text="Page "))
document.footer.append_child(model.FieldChunkModelNode(field="page_number"))

paragraph_1 = document.append_child(model.ParagraphModelNode())
paragraph_1.append_child(model.TextChunkModelNode(text="Hello, "))
paragraph_1.append_child(model.TextChunkModelNode(text="world"))
paragraph_1.append_child(model.TextChunkModelNode(text="!"))

paragraph_2 = document.append_child(model.ParagraphModelNode())
paragraph_2.append_child(model.TextChunkModelNode(text="This is another paragraph."))

print(document, end="")

layout_page_1 = layout.PageLayoutNode()

# We do not use 'append_child' here, since we need to know more structually to be able to compute the layout.
# The header, footer and content nodes are all added as children, but can be accessed separately too.
#
# When we are deciding where the next node should go, we always have a 'layout_region_node' that will keep track of the node we are currently filling.
# If that node overflows, we can ask the current page for a new layout region.
# By doing this, we can easily create new pages or even work with multi-column layouts.

layout_header_1 = layout_page_1.set_header_node(layout.BlockLayoutNode())

layout_footer_1 = layout_page_1.set_footer_node(layout.BlockLayoutNode())
layout_footer_1.append_child(layout.TextLayoutNode(text="Page "))
layout_footer_1.append_child(layout.TextLayoutNode(text="1"))

layout_block_1 = layout_page_1.add_content_node(layout.BlockLayoutNode())
layout_block_1.append_child(layout.TextLayoutNode(text="Hello, "))
layout_block_1.append_child(layout.TextLayoutNode(text="world"))
layout_block_1.append_child(layout.TextLayoutNode(text="!"))

layout_block_2 = layout_page_1.add_content_node(layout.BlockLayoutNode())
layout_block_2.append_child(layout.TextLayoutNode(text="This is another"))
layout_block_2.append_child(layout.TextLayoutNode(text="paragraph."))
