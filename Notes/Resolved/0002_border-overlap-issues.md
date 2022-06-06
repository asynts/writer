commitid b00c971a11b20637d00514ee5413c49f21e6f9c6

### Notes

-   After adding some text, I noticed that some elements were overlapping.

### Theories

-   I suspect, that this is a sign error somewhere.

-   I suspect, that I forgot to emulate the behaviour of a `BlockLayoutNode` correctly.

-   I suspect, that I am not considering the border correctly in some calculation.

-   I suspect, that I am rounding some floating point number to an integer somewhere.

-   The position relative to the parent does include the border and padding, maybe that is the issue.

### Conclusions

-   When generating the layout tree, I defined a fixed height for each paragraph, independent of the contents of the paragraph.
