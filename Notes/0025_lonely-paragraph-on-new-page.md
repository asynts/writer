When a paragraph overflows we place the first overflowing line on the next page and then split the paragraph.

### Notes

-   My understanding is that the paragraph doesn't have to be split in that situation.

-   I was able to to properly reproduce the issue using the `create_paragraph_subtree` helper function.
    It does indeed place the first line in a separate paragraph for some reason.

### Tasks

### Theories

-   I suspect, that we decide to split the paragraph without testing if the line fits on the new page.

-   I suspect, that we are still caching the height of the previous parent node.
