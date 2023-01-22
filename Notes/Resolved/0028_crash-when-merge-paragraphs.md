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

-   This is the relevant code:

    ```python
    new_node.children.remove(parent_node)
    ```

-   I tried using this code instead:

    ```python
    new_node.children = list(filter(lambda item: item.key == parent_node.key, new_node.children))
    ```

    However, I now crash because the cursor is apparently duplicated.

-   If I then remove the call to `events.validate_cursor_unique_event`, it removes the wrong paragraph.
    The paragraph into which we are moving everything is removed instead.

-   I just realized that `filter` keeps the elements that return true and deletes the rest.
    Therefore, this code does the right thing:

    ```python
    new_node.children = list(filter(lambda item: item.key != parent_node.key, new_node.children))
    ```

### Tasks

-   Remove using the `key` instead.

### Theories

-   This could be related to `NodePath.fork_and_remove`.

-   I suspect, that since the identity changed when we updated the other paragraph, the comparison based on identity doesn't work.

-   I suspect, that we don't update the path to the cursor node if the cursor is in that paragraph.
