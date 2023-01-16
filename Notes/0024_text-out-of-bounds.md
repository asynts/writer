Sometimes, the rendered text is slightly overflowing the page.

### Notes

-   The inside of the page doesn't seem to be large enough.
    Maybe that's an unrelated issue.

-   I found this while debugging another issue:

    ```python
    # This function assumes that the space avaliable in the parent node doesn't change while this node is in the 'PHASE_1_CREATED' phase.
    def get_max_remaining_width(self) -> float:
        pass
    ```

### Tasks

### Theories

-   I suspect, that only drawing the inner boxes of `BlockLayoutNode` doesn't tell the whole story.
