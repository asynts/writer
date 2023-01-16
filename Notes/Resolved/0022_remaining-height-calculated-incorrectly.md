After a while, we start putting every line into a new paragraph.

### Notes

-   Notice that we are not creating new pages, only new paragraphs.

-   When adding boxes around the blocks, the text appears to exceed the page.

-   We also crash if we need multiple pages:

    ```none
        Traceback (most recent call last):
    File "/usr/lib/python3.10/runpy.py", line 196, in _run_module_as_main
        return _run_code(code, main_globals, None,
    File "/usr/lib/python3.10/runpy.py", line 86, in _run_code
        exec(code, run_globals)
    File "/home/me/dev/writer/writer/__main__.py", line 163, in <module>
        main()
    File "/home/me/dev/writer/writer/__main__.py", line 158, in main
        window = Window()
    File "/home/me/dev/writer/writer/__main__.py", line 113, in __init__
        self._writerWidget = WriterWidget()
    File "/home/me/dev/writer/writer/__main__.py", line 36, in __init__
        self.build_layout_tree()
    File "/home/me/dev/writer/writer/__main__.py", line 40, in build_layout_tree
        self._layout_tree = converter.generate_layout_for_model(
    File "/home/me/dev/writer/writer/engine/converter.py", line 247, in generate_layout_for_model
        layout_generator.place_paragraph(paragraph_model_node)
    File "/home/me/dev/writer/writer/engine/converter.py", line 207, in place_paragraph
        self._try_place_pending_paragraph()
    File "/home/me/dev/writer/writer/engine/converter.py", line 45, in _try_place_pending_paragraph
        self.new_pending_page()
    File "/home/me/dev/writer/writer/engine/converter.py", line 99, in new_pending_page
        self._try_place_pending_page()
    File "/home/me/dev/writer/writer/engine/converter.py", line 38, in _try_place_pending_page
        self.document_layout_node.place_child_node(self.pending_page_layout_node)
    File "/home/me/dev/writer/writer/engine/layout.py", line 568, in place_child_node
        child_node.on_placed_in_node(
    File "/home/me/dev/writer/writer/engine/layout.py", line 201, in on_placed_in_node
        assert self.__associated_child_node is None
    AssertionError
    ```

    -   We also crash with the whole book, I suspect, for the same reason.

-   The inside of the page doesn't seem to be large enough.
    Maybe that's an unrelated issue.

### Ideas

### Theories

-   I suspect, that only drawing the inner boxes of `BlockLayoutNode` doesn't tell the whole story.

-   I suspect, that the remaining height is calculated incorrectly.
    Thus we start creating new paragraphs.

-   I suspect, that we are calculating the remaining height in two places:

    -   When deciding if a line will fit or not.
        This could be the culprit.

    -   When deciding if the paragraph will fit or not.
        This appears to be broken as well, but in a different way.

-   I suspect, that this was broken when I added the `DisplayInformation` service.

-   I suspect, that we are somewhere calculating the width and height incorrectly.

-   I suspect, that we are caching old values that should not be cached.

-   Maybe we get a negative value somewhere?

-   I suspect that margin or padding isn't considered.

### Result

-   I used `sum` instead of `max` when computing the maximum height of a given line.
    After resolving that issue, paragraphs are no longer split incorrectly.
    The issue with crashing when a new page is needed still persists.
