### Notes

-   Cursor disappears when an entire paragraph is removed:

     1. Place cursor at end of paragraph.
        (Only a single text chunk in paragraph, this may not be relevant.)

     2. Erase with backspace until one character is remaining.

     3. The next backspace will remove the first character but it also hides the cursor.
        (This is correct, but the cursor should remain visible.)

     4. The next backspace will remove the paragraph but the cursor remains hidden.
        (This is correct, but the cursor should be visible at the end of the previous paragraph.)

     5. The next backspace will place the cursor at the end of the previous paragraph.

-   I was able to reproduce the issue with a paragraph that was not empty:

     1. Place the cursor in the middle of the paragraph.
        (Only a single text chunk in paragraph, and fits on one line, this may be relevant.)

     2. Backspace until one character remaining.

     4. The next backspace will remove the first character but also hides the cursor.
        (This is not very consistent.)

-   The issue only happens if I place the cursor before a space character.
    In the middle of a paragraph.

-   I tried resolving that issue by unconditionally running this code:

    ```python
    if len(cursor_node.text) == 0:
        # Empty nodes must not exist unless they contain the cursor.
        new_model_tree = cursor_path.fork_and_remove(root_node=new_model_tree)
    else:
        # Remove cursor from non-empty node.
        new_node = cursor_node.make_mutable_copy()
        new_node.cursor_offset = None
        new_node.make_immutable()
        new_model_tree = cursor_path.fork_and_replace(new_node, root_node=new_model_tree)
    ```

    That should remove the cursor from the tree.
    My understanding was that all other code paths then update `cursor_node_path` on the document node.
    However, when I run the code we crash:

    ```none
    Traceback (most recent call last):
    File "/home/me/dev/writer/writer/__main__.py", line 105, in keyPressEvent
        if events.key_press_event(
    File "/home/me/dev/writer/writer/engine/events.py", line 140, in key_press_event
        return backspace_event(model_tree=model_tree, layout_tree=layout_tree, history_manager=history_manager)
    File "/home/me/dev/writer/writer/engine/events.py", line 23, in backspace_event
        if cursor_node.cursor_offset >= 1:
    TypeError: '>=' not supported between instances of 'NoneType' and 'int'

    ```

-   For now, I decided to address the rendering issue first.
    I stashed the changes:

    ```none
    stash@{0}: WIP on develop: 6c1058f Meta: Update changelog and readme
    ```

-   The rendering issue was caused by `text_placement` which would not place the cursor at the start of a paragraph,
    if it starts with whitespace.

-   The problem seems to occur here:

    ```python
    b_cursor_offset_after_consumed_text = text_chunk_node.cursor_offset > model_node_offset_before + len(text_before)
    b_cursor_offset_before_consumed_separator = text_chunk_node.cursor_offset < model_node_offset
    if b_cursor_offset_after_consumed_text and b_cursor_offset_before_consumed_separator:
        add_pending_cursor(CursorPlacementInstruction(
            model_node=text_chunk_node,
            model_offset=text_chunk_node.cursor_offset,
        ))
    ```

    This is broken because we ignore the cursor if it's at the very beginning of the separator (the whitespace.)
    This may be required since the cursor would otherwise be associated with the previous word.

    I think this is an artifact of the justified print thing that I tried to do.

### Theories
