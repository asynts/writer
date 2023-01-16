We crash when we add enough text that we need a second page.

### Notes

-   This is where the crash occurs:

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

-   I was able to reproduce the issue after fixing the issue with the incorrectly calculated remaining height:

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

-   The same issue occurs when I add a new paragraph that is completely moved to the next page.

### Tasks

-   Read through the architecture documentation.

-   Figure out how `on_placed_in_node` works with all the `__associated_child_node` stuff.

### Theories
