### Notes

-   If I place the cursor at the start of a paragraph and then use backspace:

    ```none
    Traceback (most recent call last):
    File "/home/me/dev/writer/writer/__main__.py", line 105, in keyPressEvent
        if events.key_press_event(
    File "/home/me/dev/writer/writer/engine/events.py", line 138, in key_press_event
        return backspace_event(model_tree=model_tree, layout_tree=layout_tree, history_manager=history_manager)
    File "/home/me/dev/writer/writer/engine/events.py", line 99, in backspace_event
        new_node.children.remove(parent_node)
    ValueError: list.remove(x): x not in list
    ```

### Theories

-   This could be related to `NodePath.fork_and_remove`.
