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

-   I don't understand the difference between `get_qrect` and `get_inner_qrect`.

-   It seems that `QRect.adjusted` treats the points separately.
    However, my logic treated the first pair of arguments for the start point and the other pair for the size:

    ```python
    self.get_qrect().adjusted(
        self.get_style().inner_spacing.left,
        self.get_style().inner_spacing.top,
        -self.get_style().inner_spacing.x,
        -self.get_style().inner_spacing.y,
    )
    ```

    ```python
    self.get_qrect().adjusted(
        self.get_style().inner_spacing.left,
        self.get_style().inner_spacing.top,
        -self.get_style().inner_spacing.right,
        -self.get_style().inner_spacing.bottom,
    )
    ```

### Tasks

### Theories

-   I suspect, that only drawing the inner boxes of `BlockLayoutNode` doesn't tell the whole story.

-   I suspect, that `get_inner_qrect` doesn't work as intended.

### Results

-   This was just a rendering issue, but I fixed an issue in `get_inner_qrect` which might have hurt me later.
