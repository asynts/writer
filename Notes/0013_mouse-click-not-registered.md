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

### Ideas

-   Should I handle the event in the leaf first before allowing parent nodes to process the event?

### Theories

-   The space after doesn't really belong to a model node, therefore, we never go through the logic and can't fail.

-   I suspect that we don't consider scrolling.

-   Maybe the position I am getting has a different coordinate system?
