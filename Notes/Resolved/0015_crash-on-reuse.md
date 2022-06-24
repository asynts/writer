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

-   I created a smaller document and reproduced the issue there:

    ```none
    HistoryManager.modify
    >>> build_layout_tree: layout_tree
    VerticalLayoutNode(relative_x=0, relative_y=0, id=140053389005408 phase=Phase.PHASE_3_FINAL)
     PageLayoutNode(relative_x=0, relative_y=10, id=140053380155520 phase=Phase.PHASE_3_FINAL)
      VerticalLayoutNode(relative_x=1, relative_y=1, id=140053389005568 phase=Phase.PHASE_3_FINAL)
      VerticalLayoutNode(relative_x=1, relative_y=72.81102362204723, id=140053389005728 phase=Phase.PHASE_3_FINAL)
       VerticalLayoutNode(relative_x=20, relative_y=20, id=140053389006048 phase=Phase.PHASE_3_FINAL)
        HorizontalLayoutNode(relative_x=0, relative_y=0, id=140053389006208 phase=Phase.PHASE_3_FINAL)
         InlineTextChunkLayoutNode(relative_x=0, relative_y=0, id=140053380161504 phase=Phase.PHASE_3_FINAL)
         InlineTextChunkLayoutNode(relative_x=71.953125, relative_y=0, id=140053380162560 phase=Phase.PHASE_3_FINAL)
       VerticalLayoutNode(relative_x=20, relative_y=62.6875, id=140053389006368 phase=Phase.PHASE_3_FINAL)
        HorizontalLayoutNode(relative_x=0, relative_y=0, id=140053389006528 phase=Phase.PHASE_3_FINAL)
         InlineTextChunkLayoutNode(relative_x=0, relative_y=0, id=140053380169072 phase=Phase.PHASE_3_FINAL)
         InlineTextChunkLayoutNode(relative_x=38.375, relative_y=0, id=140053380171552 phase=Phase.PHASE_3_FINAL)
         InlineTextChunkLayoutNode(relative_x=47.96875, relative_y=0, id=140053380169792 phase=Phase.PHASE_3_FINAL)
         InlineTextChunkLayoutNode(relative_x=67.15625, relative_y=0, id=140053380171024 phase=Phase.PHASE_3_FINAL)
         InlineTextChunkLayoutNode(relative_x=76.75, relative_y=0, id=140053380171200 phase=Phase.PHASE_3_FINAL)
         InlineTextChunkLayoutNode(relative_x=86.34375, relative_y=0, id=140053380171376 phase=Phase.PHASE_3_FINAL)
         InlineTextChunkLayoutNode(relative_x=95.9375, relative_y=0, id=140053380302448 phase=Phase.PHASE_3_FINAL)
         InlineTextChunkLayoutNode(relative_x=191.875, relative_y=0, id=140053380302624 phase=Phase.PHASE_3_FINAL)
         InlineTextChunkLayoutNode(relative_x=201.46875, relative_y=0, id=140053380302800 phase=Phase.PHASE_3_FINAL)
         InlineTextChunkLayoutNode(relative_x=239.84375, relative_y=0, id=140053380302976 phase=Phase.PHASE_3_FINAL)
         InlineTextChunkLayoutNode(relative_x=249.4375, relative_y=0, id=140053380303152 phase=Phase.PHASE_3_FINAL)
         InlineTextChunkLayoutNode(relative_x=326.1875, relative_y=0, id=140053380303328 phase=Phase.PHASE_3_FINAL)
         InlineTextChunkLayoutNode(relative_x=335.78125, relative_y=0, id=140053380303504 phase=Phase.PHASE_3_FINAL)
         InlineTextChunkLayoutNode(relative_x=422.125, relative_y=0, id=140053380303680 phase=Phase.PHASE_3_FINAL)
         InlineTextChunkLayoutNode(relative_x=431.71875, relative_y=0, id=140053380303856 phase=Phase.PHASE_3_FINAL)
         InlineTextChunkLayoutNode(relative_x=450.90625, relative_y=0, id=140053380304032 phase=Phase.PHASE_3_FINAL)
         InlineTextChunkLayoutNode(relative_x=460.5, relative_y=0, id=140053380304208 phase=Phase.PHASE_3_FINAL)
         InlineTextChunkLayoutNode(relative_x=489.28125, relative_y=0, id=140053380304384 phase=Phase.PHASE_3_FINAL)
      VerticalLayoutNode(relative_x=1, relative_y=982.8110236220471, id=140053389005888 phase=Phase.PHASE_3_FINAL)
    <<<
    b_width_exactly_equal=True b_fits_on_page=True lhs=751.7007874015748 rhs=751.7007874015748
    LayoutNode.on_reused_with_new_parent: id(self)=140053389006048
    >>> get_height: self
    VerticalLayoutNode(relative_x=20, relative_y=20, id=140053389006048 phase=Phase.PHASE_2_PLACED)
     HorizontalLayoutNode(relative_x=0, relative_y=0, id=140053389006208 phase=Phase.PHASE_2_PLACED)
      InlineTextChunkLayoutNode(relative_x=0, relative_y=0, id=140053380161504 phase=Phase.PHASE_2_PLACED)
      InlineTextChunkLayoutNode(relative_x=71.953125, relative_y=0, id=140053380162560 phase=Phase.PHASE_2_PLACED)
    <<<
    Traceback (most recent call last):
      File "/home/me/dev/writer/writer/__main__.py", line 78, in mousePressEvent
        self.build_layout_tree()
      File "/home/me/dev/writer/writer/__main__.py", line 41, in build_layout_tree
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
      File "/home/me/dev/writer/writer/engine/layout.py", line 569, in place_child_node
        self._height_of_children += child_node.get_height() + child_node.get_style().outer_spacing.y
      File "/home/me/dev/writer/writer/engine/layout.py", line 318, in get_height
        assert self.get_phase() == Phase.PHASE_3_FINAL
    AssertionError
    ./bin/run: line 4:  9373 Aborted                 (core dumped) python3 -m writer
    ```

-   I was trying to figure out, if we crash on the first layout node we try to reuse, or if we crash when
    we try to reuse the first layout node.
    Therefore, I did the same thing again, but instead, I clicked on the first paragraph and looked where it crashed:

    ```none
    HistoryManager.modify
    >>> build_layout_tree: layout_tree
    VerticalLayoutNode(relative_x=0, relative_y=0, id=139937189761792 phase=Phase.PHASE_3_FINAL)
     PageLayoutNode(relative_x=0, relative_y=10, id=139937185302128 phase=Phase.PHASE_3_FINAL)
      VerticalLayoutNode(relative_x=1, relative_y=1, id=139937189761952 phase=Phase.PHASE_3_FINAL)
      VerticalLayoutNode(relative_x=1, relative_y=72.81102362204723, id=139937189762112 phase=Phase.PHASE_3_FINAL)
       VerticalLayoutNode(relative_x=20, relative_y=20, id=139937189762432 phase=Phase.PHASE_3_FINAL)
        HorizontalLayoutNode(relative_x=0, relative_y=0, id=139937189762592 phase=Phase.PHASE_3_FINAL)
         InlineTextChunkLayoutNode(relative_x=0, relative_y=0, id=139937185308112 phase=Phase.PHASE_3_FINAL)
         InlineTextChunkLayoutNode(relative_x=71.953125, relative_y=0, id=139937185309168 phase=Phase.PHASE_3_FINAL)
       VerticalLayoutNode(relative_x=20, relative_y=62.6875, id=139937189762752 phase=Phase.PHASE_3_FINAL)
        HorizontalLayoutNode(relative_x=0, relative_y=0, id=139937189762912 phase=Phase.PHASE_3_FINAL)
         InlineTextChunkLayoutNode(relative_x=0, relative_y=0, id=139937185315680 phase=Phase.PHASE_3_FINAL)
         InlineTextChunkLayoutNode(relative_x=38.375, relative_y=0, id=139937185316208 phase=Phase.PHASE_3_FINAL)
         InlineTextChunkLayoutNode(relative_x=47.96875, relative_y=0, id=139937185334544 phase=Phase.PHASE_3_FINAL)
         InlineTextChunkLayoutNode(relative_x=67.15625, relative_y=0, id=139937185334016 phase=Phase.PHASE_3_FINAL)
         InlineTextChunkLayoutNode(relative_x=76.75, relative_y=0, id=139937185334192 phase=Phase.PHASE_3_FINAL)
         InlineTextChunkLayoutNode(relative_x=86.34375, relative_y=0, id=139937185334368 phase=Phase.PHASE_3_FINAL)
         InlineTextChunkLayoutNode(relative_x=95.9375, relative_y=0, id=139937185465440 phase=Phase.PHASE_3_FINAL)
         InlineTextChunkLayoutNode(relative_x=191.875, relative_y=0, id=139937185465616 phase=Phase.PHASE_3_FINAL)
         InlineTextChunkLayoutNode(relative_x=201.46875, relative_y=0, id=139937185465792 phase=Phase.PHASE_3_FINAL)
         InlineTextChunkLayoutNode(relative_x=239.84375, relative_y=0, id=139937185465968 phase=Phase.PHASE_3_FINAL)
         InlineTextChunkLayoutNode(relative_x=249.4375, relative_y=0, id=139937185466144 phase=Phase.PHASE_3_FINAL)
         InlineTextChunkLayoutNode(relative_x=326.1875, relative_y=0, id=139937185466320 phase=Phase.PHASE_3_FINAL)
         InlineTextChunkLayoutNode(relative_x=335.78125, relative_y=0, id=139937185466496 phase=Phase.PHASE_3_FINAL)
         InlineTextChunkLayoutNode(relative_x=422.125, relative_y=0, id=139937185466672 phase=Phase.PHASE_3_FINAL)
         InlineTextChunkLayoutNode(relative_x=431.71875, relative_y=0, id=139937185466848 phase=Phase.PHASE_3_FINAL)
         InlineTextChunkLayoutNode(relative_x=450.90625, relative_y=0, id=139937185467024 phase=Phase.PHASE_3_FINAL)
         InlineTextChunkLayoutNode(relative_x=460.5, relative_y=0, id=139937185467200 phase=Phase.PHASE_3_FINAL)
         InlineTextChunkLayoutNode(relative_x=489.28125, relative_y=0, id=139937185467376 phase=Phase.PHASE_3_FINAL)
      VerticalLayoutNode(relative_x=1, relative_y=982.8110236220471, id=139937189762272 phase=Phase.PHASE_3_FINAL)
    <<<
    b_width_exactly_equal=True b_fits_on_page=True lhs=751.7007874015748 rhs=751.7007874015748
    LayoutNode.on_reused_with_new_parent: id(self)=139937189762752
    >>> get_height: self
    VerticalLayoutNode(relative_x=20, relative_y=30.0, id=139937189762752 phase=Phase.PHASE_2_PLACED)
     HorizontalLayoutNode(relative_x=0, relative_y=0, id=139937189762912 phase=Phase.PHASE_2_PLACED)
      InlineTextChunkLayoutNode(relative_x=0, relative_y=0, id=139937185315680 phase=Phase.PHASE_2_PLACED)
      InlineTextChunkLayoutNode(relative_x=38.375, relative_y=0, id=139937185316208 phase=Phase.PHASE_2_PLACED)
      InlineTextChunkLayoutNode(relative_x=47.96875, relative_y=0, id=139937185334544 phase=Phase.PHASE_2_PLACED)
      InlineTextChunkLayoutNode(relative_x=67.15625, relative_y=0, id=139937185334016 phase=Phase.PHASE_2_PLACED)
      InlineTextChunkLayoutNode(relative_x=76.75, relative_y=0, id=139937185334192 phase=Phase.PHASE_2_PLACED)
      InlineTextChunkLayoutNode(relative_x=86.34375, relative_y=0, id=139937185334368 phase=Phase.PHASE_2_PLACED)
      InlineTextChunkLayoutNode(relative_x=95.9375, relative_y=0, id=139937185465440 phase=Phase.PHASE_2_PLACED)
      InlineTextChunkLayoutNode(relative_x=191.875, relative_y=0, id=139937185465616 phase=Phase.PHASE_2_PLACED)
      InlineTextChunkLayoutNode(relative_x=201.46875, relative_y=0, id=139937185465792 phase=Phase.PHASE_2_PLACED)
      InlineTextChunkLayoutNode(relative_x=239.84375, relative_y=0, id=139937185465968 phase=Phase.PHASE_2_PLACED)
      InlineTextChunkLayoutNode(relative_x=249.4375, relative_y=0, id=139937185466144 phase=Phase.PHASE_2_PLACED)
      InlineTextChunkLayoutNode(relative_x=326.1875, relative_y=0, id=139937185466320 phase=Phase.PHASE_2_PLACED)
      InlineTextChunkLayoutNode(relative_x=335.78125, relative_y=0, id=139937185466496 phase=Phase.PHASE_2_PLACED)
      InlineTextChunkLayoutNode(relative_x=422.125, relative_y=0, id=139937185466672 phase=Phase.PHASE_2_PLACED)
      InlineTextChunkLayoutNode(relative_x=431.71875, relative_y=0, id=139937185466848 phase=Phase.PHASE_2_PLACED)
      InlineTextChunkLayoutNode(relative_x=450.90625, relative_y=0, id=139937185467024 phase=Phase.PHASE_2_PLACED)
      InlineTextChunkLayoutNode(relative_x=460.5, relative_y=0, id=139937185467200 phase=Phase.PHASE_2_PLACED)
      InlineTextChunkLayoutNode(relative_x=489.28125, relative_y=0, id=139937185467376 phase=Phase.PHASE_2_PLACED)
    <<<
    Traceback (most recent call last):
      File "/home/me/dev/writer/writer/__main__.py", line 78, in mousePressEvent
        self.build_layout_tree()
      File "/home/me/dev/writer/writer/__main__.py", line 41, in build_layout_tree
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
      File "/home/me/dev/writer/writer/engine/layout.py", line 569, in place_child_node
        self._height_of_children += child_node.get_height() + child_node.get_style().outer_spacing.y
      File "/home/me/dev/writer/writer/engine/layout.py", line 318, in get_height
        assert self.get_phase() == Phase.PHASE_3_FINAL
    AssertionError
    ./bin/run: line 4:  9527 Aborted                 (core dumped) python3 -m writer
    ```

    It clearly crashes, when it actually tries to reuse a paragraph.

### Ideas

-   Print out every time we access the `_absolute_height`.

### Theories

-   I suspect, that I mixed up `_absolute_height` and `__absolute_height` or something like that.

### Conclusions

-   The problem was that I forgot to reset `_absolute_*` for the parent node, I only did that for the child nodes.
