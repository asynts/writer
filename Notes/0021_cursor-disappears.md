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

-   I suspect, this is because we split because of the cursor and create a node with no text in it which somehow still reserves space.

-   I printed out the text before the cursor and somehow it includes a space:

    ```none
    text_before_cursor='in ' text_after_cursor=''
    ```

-   I tried creating a workaround by simply detecting this and not printing the space if it is the last chunk.
    However, that is wrong and not only puts the cursor at the wrong position, but it also defeats the purpose of word groups.

    Instead, I could introduce some sort of invariant but I can't think exactly what would work.

-   This whole thing will not work if we use block formatting.
    I think the trick here is to separate the cursor rendering from the text chunk that mentions the cursor.

    We should keep track if the cursor should be rendered in front of the next chunk.
    And if it's the last chunk, we manually place it after.

    But this leaves the edge case where the cursor is within a text chunk.

-   Here are all the edge cases that I can think of:

    -   The cursor is at the start of the text excerpt ...

        -   ... it is left bound (space at start).

        -   ... it is right bound.

    -   The cursor is at the end of the text excerpt ...

        -   ... it is left bound.

        -   ... it is right bound (space at end).

    -   The cursor is within the text excerpt.

-   Instead of doing any of this, I could do more work ahead of time doring the word group calculation and simply create a sequence of
    instructions that are used during rendering, like "put cursor here", not sure if that would help though.
