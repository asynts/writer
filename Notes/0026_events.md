### Notes

-   If I press backspace at the beginning of the page, the cursor disappears.

-   I need to decide what invariants I enforce for the cursor.

-   Invariant: Text chunks can not be empty unless the cursor is placed in them.

    -   I think this creates issues with the cursor navigation.
        Say, that I am in an empty text chunk at the beginning of a word.
        If I then press right it would leave the cursor at the same location.

    -   Maybe I could optionally associate formatting with the cursor directly.
        This would be optional.

        -   If the "bold" button is pressed, it will fork the style of the current text into the cursor.

        -   If we move the cursor in any way, it will reset to the surrounding format.

        -   With that we can dictate that no empty text chunks may exist.

        -   This doesn't work, because there is no longer a cursor node in the model tree.

-   It could be better to rewrite the code to add a separate `CursorModelNode`.
    However, I feel like this will only add complexity in other places.

-   First I am going to look at the `backspace_event`.
    The backspace event can occur in the cartesian product of the following states:

    -   If the cursor is placed or not.
        We should ignore the event if no cursor is placed.

        -   There is a cursor placed.

        -   There is no cursor placed.
            (This should be checked first then all other states can be skipped.)

    -   Where the cursor is placed in the text chunk.
        We may have to move the cursor into the previous text chunk.

        -   At the start.

        -   In the middle.

        -   At the end.
            (This is equivalent to being placed in the middle.)

    -   Does the text chunk contain text?
        This is relevant because me might have to enforce the variant with empty text chunks.

        -   The text chunk contains text.

        -   The text chunk is empty.
            (This implies that we are at the start of the text chunk.)

    -   Is there a previous text chunk?
        We may have to move the cursor there.

        -   There is a previous text chunk.
            (This is irrelevant if the cursor isn't at the start of the text chunk.)

        -   There is no previous text chunk.
            (This is irrelevant if the cursor isn't at the start of the text chunk.)

    -   Is there a previous paragraph?
        We may have to merge the current paragraph into it.

        -   There is a previous paragraph.
            (This isn't relevant unless there is no previous text chunk.)

        -   There is not previous paragraph.
            (This isn't relevant unless there is no previous text chunk.)

-   I created another pseudo event that verifies that there are no empty text chunks unless the cursor is placed in them.

### Bugs

-   Bug: If I press backspace at the beginning of the page, the cursor disappears.

### Tasks
