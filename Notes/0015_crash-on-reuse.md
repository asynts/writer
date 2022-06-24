commitid 801f43c61ad7a2e4934047635944974c0a45dee6

### Notes

-   We appear to crash when trying to reuse the first paragraph:

    ```none
    HistoryManager.modify
    b_width_exactly_equal=True b_fits_on_page=True lhs=751.7007874015748 rhs=751.7007874015748
    LayoutNode.on_reused_with_new_parent: id(self)=140444896220544
    Traceback (most recent call last):
      File "/home/me/dev/writer/writer/__main__.py", line 75, in mousePressEvent
        self.build_layout_tree()
      File "/home/me/dev/writer/writer/__main__.py", line 34, in build_layout_tree
        self._layout_tree = create_layout_tree(history.global_history_manager.get_model_tree())
      File "/home/me/dev/writer/writer/__main__.py", line 18, in create_layout_tree
        return writer.engine.converter.generate_layout_for_model(model_tree)
      File "/home/me/dev/writer/writer/engine/converter.py", line 350, in generate_layout_for_model
        placer = Placer(document_model_node=document_model_node)
      File "/home/me/dev/writer/writer/engine/converter.py", line 163, in __init__
        self.place_document(document_model_node)
      File "/home/me/dev/writer/writer/engine/converter.py", line 347, in place_document
        self.place_paragraph(paragraph_model_node)
      File "/home/me/dev/writer/writer/engine/converter.py", line 308, in place_paragraph
        content_node.place_child_node(layout_node)
      File "/home/me/dev/writer/writer/engine/layout.py", line 564, in place_child_node
        self._height_of_children += child_node.get_height() + child_node.get_style().outer_spacing.y
      File "/home/me/dev/writer/writer/engine/layout.py", line 313, in get_height
        assert self.get_phase() == Phase.PHASE_3_FINAL
    AssertionError
    ./bin/run: line 4:  7927 Aborted                 (core dumped) python3 -m writer
    ```

### Ideas

### Theories

-   I suspect, that when I fixed `0014` I did so improperly.

### Conclusions
