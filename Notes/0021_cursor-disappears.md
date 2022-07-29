Sometimes when I remove something with `Key_Backspace`, the cursor is no longer rendered.

### Notes

-   I am still able to continue modifying the tree, after this happened.

-   This appears to happen when I use backspace accross text chunk boundaries and then remove something up to a space character.
    This is what the tree looked like when the cursor was no longer visible:

    ```none
    DocumentModelNode@1()
      ParagraphModelNode@2()
        TextChunkModelNode@3(text='Title', cursor_offset=None)
      ParagraphModelNode@4()
        TextChunkModelNode@5(text='This is a paragrapith multiple sentences in ', cursor_offset=44)
        TextChunkModelNode@6(text='is is bold', cursor_offset=None)
    ```

    The cursor was placed past the end, after the space.

-   This can also happen if I place the cursor at the end manually and then use backspace.
    Crossing a boundary is not necessary.

-   This issue is caused because we compute the word groups and thereby discard the whitespace.
    None of the ranges will ever include the cursor.

-   I tried to resolve the issue by adding the `raw_text` to the excerpts when computing the word groups.
    That way, I can decide more acurately, if the cursor should be placed or not.

    In my opinion, this strategy could work, but the code can't deal with it right now.
    In `Placer.place_word_group_in_current_line` we end up placing a space too much, I don't yet know why this happens.
