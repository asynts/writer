commitid b867cdd53c2f2a170a8eb5c6c6e031198d5b1fa6

When I click, somehow, we don't detect the mouse click correctly.

### Notes

-   This appears to be inconsistent.
    -   Sometimes, `TextChunkLayoutNode.on_mouse_click` is called, in this case we crash:

        ```none
        Document: 'Immutable Tree Example'
        Rebuild         9886130ns (  0.009886s)
        Painting         523284ns ( 0.0005233s)
        >>> mousePressEvent before
        DocumentModelNode@139792806866688()
        ParagraphModelNode@139792806866816()
        TextChunkModelNode@139792806826352(text='Title')
        <<<
        visited id(layout_node)=139792811315008 (id(layout_node.get_model_node())=139792806866688)
        visited id(layout_node)=139792811315648 (id(layout_node.get_model_node())=139792806866816)
        visited id(layout_node)=139792806808384 (id(layout_node.get_model_node())=139792806826352)
        HistoryManager.modify
        Traceback (most recent call last):
        File "/home/me/dev/writer/writer/__main__.py", line 65, in mousePressEvent
            events.mouse_click_event(
        File "/home/me/dev/writer/writer/engine/events.py", line 71, in mouse_click_event
            visit_layout_node(layout_tree, relative_x=absolute_x, relative_y=absolute_y)
        File "/home/me/dev/writer/writer/engine/events.py", line 57, in visit_layout_node
            b_event_consumed = visit_layout_node(
        File "/home/me/dev/writer/writer/engine/events.py", line 57, in visit_layout_node
            b_event_consumed = visit_layout_node(
        File "/home/me/dev/writer/writer/engine/events.py", line 57, in visit_layout_node
            b_event_consumed = visit_layout_node(
        [Previous line repeated 2 more times]
        File "/home/me/dev/writer/writer/engine/events.py", line 35, in visit_layout_node
            b_event_consumed = layout_node.on_mouse_click(
        File "/home/me/dev/writer/writer/engine/layout.py", line 672, in on_mouse_click
            history.global_history_manager.modify(
        File "/home/me/dev/writer/writer/engine/history.py", line 17, in modify
            new_model_tree = tree.new_tree_with_modified_node(position, **kwargs)
        File "/home/me/dev/writer/writer/engine/tree.py", line 86, in new_tree_with_modified_node
            setattr(new_node, property_, value)
        File "/home/me/dev/writer/writer/engine/model.py", line 118, in text
            assert self.is_mutable
        AssertionError
        ./bin/run: line 4: 12269 Aborted                 (core dumped) python3 -m writer
        ```

    -   In other cases, we just never execute that code:

        ```none
        Document: 'Immutable Tree Example'
        Rebuild         9847978ns (  0.009848s)
        Painting         326669ns ( 0.0003267s)
        >>> mousePressEvent before
        DocumentModelNode@140650669960768()
        ParagraphModelNode@140650669960896()
        TextChunkModelNode@140650669920624(text='Title')
        <<<
        visited id(layout_node)=140650674409280 (id(layout_node.get_model_node())=140650669960768)
        visited id(layout_node)=140650674409920 (id(layout_node.get_model_node())=140650669960896)
        >>> mousePressEvent after
        DocumentModelNode@140650669960768()
        ParagraphModelNode@140650669960896()
        TextChunkModelNode@140650669920624(text='Title')
        <<<
        Rebuild          388198ns ( 0.0003882s)
        Painting         306150ns ( 0.0003061s)
        ```

    My understanding is, that the first one happens when I click on the "Title" text and the other happens if I click on
    the space after.

-   I added some debug rects that show which nodes are visited when I click somewhere.
    The result is really confusing.

    -   First, we encounter the root node, this is correct.

    -   Then we encounter the page node, that is correct too.

    -   Then we encounter the content node, this is correct too.

    -   Then we encounter the footer node which makes no sense.

-   I added a bunch of debug statements into the event handling logic:

    ```none
    # We visit the root node, the target is contained and we have a model node we can visit.
    relative_x=71.0 relative_y=120.0 layout_node.get_absolute_width()=793.7007874015748 layout_node.get_absolute_height()=1142.51968503937
    visited id(layout_node)=139698164796768 (id(layout_node.get_model_node())=139698159972864)

    # We look at the header node.
    recursive call: relative_x=71.0 layout_node.get_relative_x()=0 relative_y=120.0 layout_node.get_relative_y()=0
    relative_x=71.0 relative_y=120.0 layout_node.get_absolute_width()=793.7007874015748 layout_node.get_absolute_height()=1122.51968503937

    # This I do not understand.
    recursive call: relative_x=71.0 layout_node.get_relative_x()=0 relative_y=120.0 layout_node.get_relative_y()=10
    relative_x=71.0 relative_y=110.0 layout_node.get_absolute_width()=791.7007874015748 layout_node.get_absolute_height()=71.81102362204723
    node outside (2)
    recursive call: relative_x=71.0 layout_node.get_relative_x()=0 relative_y=120.0 layout_node.get_relative_y()=10
    relative_x=71.0 relative_y=110.0 layout_node.get_absolute_width()=791.7007874015748 layout_node.get_absolute_height()=909.9999999999999
    recursive call: relative_x=71.0 layout_node.get_relative_x()=1 relative_y=110.0 layout_node.get_relative_y()=72.81102362204723
    relative_x=70.0 relative_y=37.18897637795277 layout_node.get_absolute_width()=751.7007874015748 layout_node.get_absolute_height()=32.6875
    node outside (2)
    recursive call: relative_x=71.0 layout_node.get_relative_x()=0 relative_y=120.0 layout_node.get_relative_y()=10
    relative_x=71.0 relative_y=110.0 layout_node.get_absolute_width()=791.7007874015748 layout_node.get_absolute_height()=138.70866141732282
    ```

-   I did draw a rect where I clicked on the screen and it seems to appear in the correct location.

-   I started more systematically printing out the state of the event logic:

    ```none
    mouse_click_event(absolute_x=53.0, absolute_y=109.0)
    >>> model_tree
    DocumentModelNode@140392506340160()
     ParagraphModelNode@140392506199040()
      TextChunkModelNode@140392506315280(text='Title')
    <<<
    >>> layout_tree
    VerticalLayoutNode(relative_x=0, relative_y=0, id=140392511901024 phase=Phase.PHASE_3_FINAL)
     PageLayoutNode(relative_x=0, relative_y=10, id=140392506264560 phase=Phase.PHASE_3_FINAL)
      VerticalLayoutNode(relative_x=1, relative_y=1, id=140392511901184 phase=Phase.PHASE_3_FINAL)
      VerticalLayoutNode(relative_x=1, relative_y=72.81102362204723, id=140392511901344 phase=Phase.PHASE_3_FINAL)
       VerticalLayoutNode(relative_x=20, relative_y=20, id=140392511901664 phase=Phase.PHASE_3_FINAL)
        HorizontalLayoutNode(relative_x=0, relative_y=0, id=140392511901824 phase=Phase.PHASE_3_FINAL)
         InlineTextChunkLayoutNode(relative_x=0, relative_y=0, id=140392506264736 phase=Phase.PHASE_3_FINAL)
         InlineTextChunkLayoutNode(relative_x=71.953125, relative_y=0, id=140392506264912 phase=Phase.PHASE_3_FINAL)
      VerticalLayoutNode(relative_x=1, relative_y=982.8110236220471, id=140392511901504 phase=Phase.PHASE_3_FINAL)
    <<<
    visit_layout_node(relative_x=53.0, relative_y=109.0, id(layout_node)=140392511901024)
    visit_layout_node: calling hook for id(layout_node)=140392511901024
    visit_layout_node: recursive call by id(layout_node)=140392511901024
    visit_layout_node(relative_x=53.0, relative_y=109.0, id(layout_node)=140392506264560)
    visit_layout_node: recursive call by id(layout_node)=140392506264560
    visit_layout_node(relative_x=53.0, relative_y=99.0, id(layout_node)=140392511901184)
    visit_layout_node: out of bounds, returning false
    visit_layout_node: recursive call by id(layout_node)=140392506264560
    visit_layout_node(relative_x=53.0, relative_y=99.0, id(layout_node)=140392511901344)
    visit_layout_node: recursive call by id(layout_node)=140392511901344
    visit_layout_node(relative_x=52.0, relative_y=26.18897637795277, id(layout_node)=140392511901664)
    visit_layout_node: calling hook for id(layout_node)=140392511901664
    visit_layout_node: recursive call by id(layout_node)=140392511901664
    visit_layout_node(relative_x=32.0, relative_y=6.18897637795277, id(layout_node)=140392511901824)
    visit_layout_node: recursive call by id(layout_node)=140392511901824
    visit_layout_node(relative_x=32.0, relative_y=6.18897637795277, id(layout_node)=140392506264736)
    visit_layout_node: calling hook for id(layout_node)=140392506264736
    HistoryManager.modify
    Traceback (most recent call last):
      File "/home/me/dev/writer/writer/__main__.py", line 89, in mousePressEvent
        self._debug_rects = events.mouse_click_event(
      File "/home/me/dev/writer/writer/engine/events.py", line 92, in mouse_click_event
        visit_layout_node(layout_tree, relative_x=absolute_x, relative_y=absolute_y)
      File "/home/me/dev/writer/writer/engine/events.py", line 77, in visit_layout_node
        b_event_consumed = visit_layout_node(
      File "/home/me/dev/writer/writer/engine/events.py", line 77, in visit_layout_node
        b_event_consumed = visit_layout_node(
      File "/home/me/dev/writer/writer/engine/events.py", line 77, in visit_layout_node
        b_event_consumed = visit_layout_node(
      [Previous line repeated 2 more times]
      File "/home/me/dev/writer/writer/engine/events.py", line 54, in visit_layout_node
        b_event_consumed = layout_node.on_mouse_click(
      File "/home/me/dev/writer/writer/engine/layout.py", line 673, in on_mouse_click
        history.global_history_manager.modify(
      File "/home/me/dev/writer/writer/engine/history.py", line 17, in modify
        new_model_tree = tree.new_tree_with_modified_node(position, **kwargs)
      File "/home/me/dev/writer/writer/engine/tree.py", line 86, in new_tree_with_modified_node
        setattr(new_node, property_, value)
      File "/home/me/dev/writer/writer/engine/model.py", line 118, in text
        assert self.is_mutable
    AssertionError
    ./bin/run: line 4:  4008 Aborted                 (core dumped) python3 -m writer
    ```

    This all looks correct, just the modification logic is broken.

-   Same thing, but this time, I did trigger the case where the click isn't registered:

    ```none
    mouse_click_event(absolute_x=60.0, absolute_y=133.0)
    >>> model_tree
    DocumentModelNode@139916960347072()
     ParagraphModelNode@139916960347200()
      TextChunkModelNode@139916960322304(text='Title')
    <<<
    >>> layout_tree
    VerticalLayoutNode(relative_x=0, relative_y=0, id=139916964875616 phase=Phase.PHASE_3_FINAL)
     PageLayoutNode(relative_x=0, relative_y=10, id=139916960270992 phase=Phase.PHASE_3_FINAL)
      VerticalLayoutNode(relative_x=1, relative_y=1, id=139916964875776 phase=Phase.PHASE_3_FINAL)
      VerticalLayoutNode(relative_x=1, relative_y=72.81102362204723, id=139916964875936 phase=Phase.PHASE_3_FINAL)
       VerticalLayoutNode(relative_x=20, relative_y=20, id=139916964876256 phase=Phase.PHASE_3_FINAL)
        HorizontalLayoutNode(relative_x=0, relative_y=0, id=139916964876416 phase=Phase.PHASE_3_FINAL)
         InlineTextChunkLayoutNode(relative_x=0, relative_y=0, id=139916960271520 phase=Phase.PHASE_3_FINAL)
         InlineTextChunkLayoutNode(relative_x=71.953125, relative_y=0, id=139916960271696 phase=Phase.PHASE_3_FINAL)
      VerticalLayoutNode(relative_x=1, relative_y=982.8110236220471, id=139916964876096 phase=Phase.PHASE_3_FINAL)
    <<<
    visit_layout_node(relative_x=60.0, relative_y=133.0, id(layout_node)=139916964875616)
    visit_layout_node: calling hook for id(layout_node)=139916964875616
    visit_layout_node: recursive call by id(layout_node)=139916964875616
    visit_layout_node(relative_x=60.0, relative_y=133.0, id(layout_node)=139916960270992)
    visit_layout_node: recursive call by id(layout_node)=139916960270992
    visit_layout_node(relative_x=60.0, relative_y=123.0, id(layout_node)=139916964875776)
    visit_layout_node: out of bounds, returning false
    visit_layout_node: recursive call by id(layout_node)=139916960270992
    visit_layout_node(relative_x=60.0, relative_y=123.0, id(layout_node)=139916964875936)
    visit_layout_node: recursive call by id(layout_node)=139916964875936
    visit_layout_node(relative_x=59.0, relative_y=50.18897637795277, id(layout_node)=139916964876256)
    visit_layout_node: out of bounds, returning false
    visit_layout_node: recursive call by id(layout_node)=139916960270992
    visit_layout_node(relative_x=60.0, relative_y=123.0, id(layout_node)=139916964876096)
    ```

### Ideas

-   Should I handle the event in the leaf first before allowing parent nodes to process the event?

-   Is the border properly considered when defining the width of the header, content and footer nodes?

### Theories

-   The space after doesn't really belong to a model node, therefore, we never go through the logic and can't fail.

-   I suspect that we don't consider scrolling.

-   Maybe the position I am getting has a different coordinate system?

-   Maybe, I have x and y swapped somewhere?

### Conclusions

-   One problem was that I was making a copy and assumed that I could mutate the copy.
    However, I also copied the hidden `__is_mutable` property which remained false.

    I fixed this by adding a `make_mutable_copy` method that creates a copy and then changes this property.

-   The problem was, that I mixed up `layout_node` and `layout_child_node` when computing the position of the child node.

    That resolved the issue.
