## About

This is a prototype of a writer application that I want to add to Serenity OS.

-   It should be similar to Libre Office Writer or Microsoft Word, but much simpler.

-   My goal here is to write my own layout engine, which is essentially a simplified version of CSS
    but without a text representation to define the rules.

## Demo

This is in an early state of development, however, I do have a prototype working.
The following code is used to describe what should be presented on the screen:

```python
model_tree = model.DocumentModelNode()

paragraph_1 = model_tree.add_child(model.ParagraphModelNode(style=heading_paragraph_style))
paragraph_1.add_child(model.TextChunkModelNode(text="This  is a", style=normal_heading_text_chunk_style))
paragraph_1.add_child(model.TextChunkModelNode(text=" heading.", style=normal_heading_text_chunk_style))

paragraph_2 = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
paragraph_2.add_child(model.TextChunkModelNode(text="This is a normal paragraph, but ", style=normal_normal_text_chunk_style))
paragraph_2.add_child(model.TextChunkModelNode(text="this", style=bold_normal_text_chunk_style))
paragraph_2.add_child(model.TextChunkModelNode(text=" has some highlight applied to it.", style=normal_normal_text_chunk_style))

paragraph_1 = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
paragraph_1.add_child(model.TextChunkModelNode(text="Here is another paragraph which is much longer than the ", style=normal_normal_text_chunk_style))
paragraph_1.add_child(model.TextChunkModelNode(text="previous ", style=bold_normal_text_chunk_style))
paragraph_1.add_child(model.TextChunkModelNode(text="one. On top of that, the formatting is all ", style=normal_normal_text_chunk_style))
paragraph_1.add_child(model.TextChunkModelNode(text="over the place", style=bold_normal_text_chunk_style))
paragraph_1.add_child(model.TextChunkModelNode(text=".", style=normal_normal_text_chunk_style))
```

All of this is then rendered on the screen and it is possible to click on words to delete them from the model (which then updates the layout as well):

https://user-images.githubusercontent.com/31994781/192720179-6e014be6-9ca7-4e91-aca0-d2edbc03a5fe.mp4
