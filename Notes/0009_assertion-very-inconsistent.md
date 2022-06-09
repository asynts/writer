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
