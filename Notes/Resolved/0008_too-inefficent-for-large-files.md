commitid 98547b664a2bb955b4b57591b8e509ee11b2cacf

As I suspected, my current implementation is too inefficent to be used in any real context.

### Notes

-   I ran a benchmark and the result isn't good:

    ```none
    Document: 'Extremely Long'
    Rebuild      6667293512ns (     6.667s)
    Painting     3805168215ns (     3.805s)
    ```

    This was for an extremely large file with about 10000 lines of text.

-   In a slightly different benchmark, I clicked on a word to trigger a redraw:

    ```none
    Document: 'Extremely Long'
    Rebuild      6680747048ns (     6.681s)
    Painting     3740714299ns (     3.741s)
    Rebuild      6665600045ns (     6.666s)
    Painting     3755506283ns (     3.756s)
    ```

    Seems that there is no noticible difference.

-   After adding some basic culling, the rendering itself is fast enough to navigate the page without any noticable lag:

    ```none
    Document: 'Extremely Long'
    Rebuild      7371958048ns (     7.372s)
    Painting       11476634ns (   0.01148s)
    ```

    However, the time required to rebuild the layout tree is still a big problem.

-   After doing the transition to `PHASE_3_FINAL` lazily, I was able to drastically improve performance again:

    ```none
    Document: 'Extremely Long'
    Rebuild      6178246457ns (     6.178s)
    Painting       15264888ns (   0.01526s)
    ```

-   After using `__slots__` in all places where this was possible, I was able to drastically improve the performance again:

    ```none
    Document: 'Extremely Long'
    Rebuild      4968573793ns (     4.969s)
    Painting       14246275ns (   0.01425s)
    ```

-   I created a more suitable test case.
    This is an excerpt from "A Study in Scarlet" by "A. Conan Doyle".

    It is much shorter but long enough to provide a realistic maximum case to optimize for.
    Here are the results:

    ```none
    Document: 'A Study in Scarlet'
    Rebuild       391047729ns (     0.391s)
    Painting       12300102ns (    0.0123s)
    ```

-   When I used `py-spy` to create a flame graph, the following things were slow, but have already been addressed since then:

    -   Another thing that is generally slow is the absolute layout calculation in the end.

        This could be done lazily with caching to benifit from the culling as well.

    -   `TextChunkModelNode.get_font_metrics` when building the word groups.

        -   This could be cached in some font helper class.

        -   On top of that, we should store the reference in the `TextChunkLayoutNode` to avoid the lookup in the cache.

            This would not affect the initial layout time.

    -   Generally, the contructors of many classes show up in the profile, slots could really help here.

### Ideas

### Actions

-   I added culling during the painting phase.
    We only draw the things that are actually visible on the screen.

    That was extremely easy to implement and drastically improved the performance.

-   I improved on the culling by computing the absolute positions of nodes lazily.

    That was extremely easy to implement and drastically improved the performance again.
    This is likely the last simple optimization that is possible.

-   I added a font cache to avoid creating `QFont` and `QFontMetricsF` objects all the time, but this didn't do much.
    It was still an improvement so I am keeping it, but this was underwhelming.

    I did revert these changes even though they improved the performance a bit, in my opinion this is a micro-optimization
    which was not justified.

-   I used `__slots__` everywhere to drastically improve performance.
