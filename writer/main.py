import model

document = model.DocumentModelNode()

document.footer_node.append_child(model.TextChunkModelNode(text="Page "))
document.footer_node.append_child(model.FieldChunkModelNode(field="page_number"))

paragraph_1 = document.append_child(model.ParagraphModelNode())
paragraph_1.append_child(model.TextChunkModelNode(text="Hello, "))
paragraph_1.append_child(model.TextChunkModelNode(text="world"))
paragraph_1.append_child(model.TextChunkModelNode(text="!"))

paragraph_2 = document.append_child(model.ParagraphModelNode())
paragraph_2.append_child(model.TextChunkModelNode(text="This is another paragraph."))

print(document, end="")
