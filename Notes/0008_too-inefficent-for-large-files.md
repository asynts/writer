commitid 98547b664a2bb955b4b57591b8e509ee11b2cacf

As I suspected, my current implementation is too inefficent to be used in any real context.

### Notes

-   I ran a benchmark and the result isn't good:

    ```none
    Rebuild      6667293512ns (     6.667s)
    Painting     3805168215ns (     3.805s)
    ```

    This was for an extremely large file with about 10000 lines of text.

-   In a slightly different benchmark, I clicked on a word to trigger a redraw:

    ```none
    Rebuild      6680747048ns (     6.681s)
    Painting     3740714299ns (     3.741s)
    Rebuild      6665600045ns (     6.666s)
    Painting     3755506283ns (     3.756s)
    ```

    Seems that there is no noticible difference.

-   After adding some basic culling, the rendering itself is fast enough to navigate the page without any noticable lag:

    ```none
    Rebuild      7371958048ns (     7.372s)
    Painting       11476634ns (   0.01148s)
    ```

    However, the time required to rebuild the layout tree is still a big problem.

-   I used `py-spy` to create a flame graph of the application.

    The following functions had some noticable inpact on performance, where I did not expect that:

    -   `TextChunkModelNode.get_font_metrics` when building the word groups.

        -   This could be cached in some font helper class.

    -   `get_max_remaining_width` when trying to place words in the current line.

        -   This could be cached in the layout node.

    -   `TextChunkLayoutNode.__init__`

        -   This might be because it uses `TextChunkModelNode.get_font_metrics`.

        -   I could make use of slots here.

### Ideas

### Actions

-   I added culling during the painting phase.
    We only draw the things that are actually visible on the screen.

    That was extremely easy to implement and drastically improved the performance.
