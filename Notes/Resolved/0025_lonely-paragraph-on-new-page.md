When a paragraph overflows we place the first overflowing line on the next page and then split the paragraph.

### Notes

-   My understanding is that the paragraph doesn't have to be split in that situation.

-   I was able to to properly reproduce the issue using the `create_paragraph_subtree` helper function.
    It does indeed place the first line in a separate paragraph for some reason.

-   I found this code, it could be the culprit:

    ```python
    # This function assumes that the space avaliable in the parent node doesn't change while this node is in the 'PHASE_1_CREATED' phase.
    def get_max_remaining_width(self) -> float:
        pass
    ```

-   I was able to find out in the debugger, that:

    ```none
    self.pending_paragraph_layout_node.get_max_remaining_height() == 18.124999999999915
    self.pending_paragraph_layout_node.get_min_height() + self.pending_paragraph_layout_node.get_style().outer_spacing.y == 75.390625
    self.pending_page_layout_node.get_max_remaining_height() == 93.51562499999991
    current_line_height == 21.796875
    ```

    This was taken in the exact moment where it decides that the current line no longer fits.

    Thus I can conclude that the pending paragraph does fit on the page but that combined with the new
    line it doesn't fit.

    The other issue that I suspected might exist as well, but it didn't occur here I should test that later.
    Actually, I don't believe that this is an issue since we would otherwise reparent an empty paragraph.
    This case should never happen.

-   I felt like my logic was a bit messed up.
    My code did assume that the pending paragraph fits on the current page but it was a bit inconsitent about this.

    I have updated the code to enforce that invariant but I seem to hit the edge case where the newly created paragraph doesn't fit.

### Tasks

-   Find the location where we decide to place a paragraph on a new page.

### Theories

-   I suspect, that we are still caching the height of the previous parent node.

### Results

-   It could happen that we create a new paragraph in `new_pending_paragraph` and it already overflows the page because of the padding.
    I have not yet addressed this issue.

-   I did a major rewrite of `converter.py` and this solved the issue as a side product.
