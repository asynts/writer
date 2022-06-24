commitid a828b65d5467b0b0ff463217e98172862ca67e30

When clicking on a node in the bigger example document, we crash when generating the new layout.

### Notes

-   This seems to happen when a layout node is in `PHASE_2_PLACED` and we try to reuse it.

-   I started making some changes but some weird things happend, I stashed these changes.

-   It seems, that there is another issue:

    ```none
    Document: 'A Study in Scarlet'
    Rebuild       122734894ns (    0.1227s)
    Painting       10578786ns (   0.01058s)
    HistoryManager.modify
    b_width_exactly_equal=True b_fits_on_page=True lhs=751.7007874015748 rhs=751.7007874015748
    LayoutNode.on_reused_with_new_parent: id(self)=139835610322304
    b_width_exactly_equal=True b_fits_on_page=True lhs=751.7007874015748 rhs=751.7007874015748
    LayoutNode.on_reused_with_new_parent: id(self)=139835610324384
    b_width_exactly_equal=True b_fits_on_page=True lhs=751.7007874015748 rhs=751.7007874015748
    LayoutNode.on_reused_with_new_parent: id(self)=139835610325824
    b_width_exactly_equal=True b_fits_on_page=True lhs=751.7007874015748 rhs=751.7007874015748
    Traceback (most recent call last):
      File "/home/me/dev/writer/writer/__main__.py", line 71, in mousePressEvent
        self.build_layout_tree()
      File "/home/me/dev/writer/writer/__main__.py", line 34, in build_layout_tree
        self._layout_tree = create_layout_tree(history.global_history_manager.get_model_tree())
      File "/home/me/dev/writer/writer/__main__.py", line 18, in create_layout_tree
        return writer.engine.converter.generate_layout_for_model(model_tree)
      File "/home/me/dev/writer/writer/engine/converter.py", line 352, in generate_layout_for_model
        placer = Placer(document_model_node=document_model_node)
      File "/home/me/dev/writer/writer/engine/converter.py", line 163, in __init__
        self.place_document(document_model_node)
      File "/home/me/dev/writer/writer/engine/converter.py", line 349, in place_document
        self.place_paragraph(paragraph_model_node)
      File "/home/me/dev/writer/writer/engine/converter.py", line 309, in place_paragraph
        layout_node.on_reused_with_new_parent(parent_node=content_node)
      File "/home/me/dev/writer/writer/engine/layout.py", line 170, in on_reused_with_new_parent
        assert self.get_phase() == Phase.PHASE_3_FINAL
    AssertionError
    ./bin/run: line 4:  4907 Aborted                 (core dumped) python3 -m writer
    ```

    It seems to correctly reuse some paragraphs, but then something goes wrong.

### Ideas

### Theories

### Actions

-   I incorrectly used `content_node.get_max_width` instead of `content_node.get_max_inner_width`.

-   Instead of comparing floating point numbers directly, I added `util.approximately_equal`.

-   My `on_reused_with_new_parent` logic assumed, that the absolute position was computed already.
    However, this is done lazily and isn't actually required.
