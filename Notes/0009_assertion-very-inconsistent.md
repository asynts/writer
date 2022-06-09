commitid df5dc8470345178d10a4d7f438aea809262590ac

I made one small modification to the model tree and started hitting an assertion.

### Notes

-   In `__main__.py`, if I change:

    ```none
    paragraph.add_child(model.TextChunkModelNode(
        text=f".",
        style=normal_normal_text_chunk_style,
    ))
    ```

    to be

    ```none
    paragraph.add_child(model.TextChunkModelNode(
        text=f". ",
        style=normal_normal_text_chunk_style,
    ))
    ```

    I start hitting the assertion.

-   It seems that this happens to be the second paragraph on the page, where the first paragraph is so large, that the second one
    doesn't fit anymore.

    ```none
    previous_sibling=(relative_x=20, relative_y=20, height=850.078125)
    fixed_height=910.00000001083
    lhs=9.921875010830036 rhs=10.0 (0 + 10.0)
    ```

    The previous paragraph has `margin_bottom=10.0` so it reserves until `20 + 850.078125 + 10.0 = 880.078125`.

    The page has a `padding_bottom=20.0` so `880.078125 + 20 = 900.078125` space is reserved.
    This leaves exactly `9.921875010830036` which is not enough to fit another paragraph.

### Ideas

-   If a paragraph is empty, I don't have to place it.
    However, if I fix it like this, I should add a big comment there as warning.

### Theories

-   I suspect, that I do not cover the case where the margin of a paragraph causes it to not fit on the page.
    This seems to be it.

-   I suspect, that I do not properly consider the spacing when trying to place a paragraph.
