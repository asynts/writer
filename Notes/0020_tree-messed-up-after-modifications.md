After updating the immutable tree logic, we now hit an assertion when generating the layout tree.

### Notes

-   It appears that the tree is in some sort of invalid state, when the layout callback runs.
    I was not yet able to print out the state.

-   ```none
    Traceback (most recent call last):
      File "/home/me/dev/writer/writer/__main__.py", line 71, in mousePressEvent
        events.mouse_click_event(
      File "/home/me/dev/writer/writer/engine/events.py", line 70, in mouse_click_event
        visit_layout_node(layout_tree, relative_x=absolute_x, relative_y=absolute_y)
      File "/home/me/dev/writer/writer/engine/events.py", line 52, in visit_layout_node
        b_event_consumed = visit_layout_node(
      File "/home/me/dev/writer/writer/engine/events.py", line 52, in visit_layout_node
        b_event_consumed = visit_layout_node(
      File "/home/me/dev/writer/writer/engine/events.py", line 52, in visit_layout_node
        b_event_consumed = visit_layout_node(
      [Previous line repeated 2 more times]
      File "/home/me/dev/writer/writer/engine/events.py", line 34, in visit_layout_node
        b_event_consumed = layout_node.on_mouse_click(
      File "/home/me/dev/writer/writer/engine/layout.py", line 743, in on_mouse_click
        history.global_history_manager.replace_node(key_path=key_path, new_node=new_node)
      File "/home/me/dev/writer/writer/engine/history.py", line 35, in replace_node
        self.update_model_tree(new_model_tree=new_model_tree)
      File "/home/me/dev/writer/writer/engine/history.py", line 42, in update_model_tree
        self.on_history_change()
      File "/home/me/dev/writer/writer/engine/history.py", line 21, in on_history_change
        callback()
      File "/home/me/dev/writer/writer/__main__.py", line 49, in on_history_change
        self.build_layout_tree()
      File "/home/me/dev/writer/writer/__main__.py", line 38, in build_layout_tree
        self._layout_tree = create_layout_tree(history.global_history_manager.get_model_tree())
      File "/home/me/dev/writer/writer/__main__.py", line 18, in create_layout_tree
        return writer.engine.converter.generate_layout_for_model(model_tree)
      File "/home/me/dev/writer/writer/engine/converter.py", line 379, in generate_layout_for_model
        placer = Placer(document_model_node=document_model_node)
      File "/home/me/dev/writer/writer/engine/converter.py", line 162, in __init__
        self.place_document(document_model_node)
      File "/home/me/dev/writer/writer/engine/converter.py", line 375, in place_document
        assert isinstance(paragraph_model_node, model.ParagraphModelNode)
    AssertionError
    ```

### Theories

-   The callback is triggered too early, since we are making multiple modifications.
