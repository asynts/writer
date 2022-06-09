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

### Ideas

-   It should be possible to drastically improve the rendering time with some basic culling.
    That should be fairly easy to implement too.
