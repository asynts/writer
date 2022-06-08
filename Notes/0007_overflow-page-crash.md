commitid b19548113e0b3bc8b43a8aaf2e6a3932e75b3c09

When we overflow the page, this causes another crash.

### Notes

-   ```none
    Traceback (most recent call last):
    File "/usr/lib/python3.10/runpy.py", line 196, in _run_module_as_main
        return _run_code(code, main_globals, None,
    File "/usr/lib/python3.10/runpy.py", line 86, in _run_code
        exec(code, run_globals)
    File "/home/me/dev/writer/writer/__main__.py", line 99, in <module>
        main()
    File "/home/me/dev/writer/writer/__main__.py", line 94, in main
        window = Window()
    File "/home/me/dev/writer/writer/__main__.py", line 72, in __init__
        self._writerWidget = WriterWidget()
    File "/home/me/dev/writer/writer/__main__.py", line 57, in __init__
        self._layout_tree = create_layout_tree(self._model_tree)
    File "/home/me/dev/writer/writer/__main__.py", line 48, in create_layout_tree
        return writer.engine.converter.generate_layout_for_model(model_tree)
    File "/home/me/dev/writer/writer/engine/converter.py", line 247, in generate_layout_for_model
        placer.place_document(document_model_node)
    File "/home/me/dev/writer/writer/engine/converter.py", line 242, in place_document
        self.place_paragraph(paragraph_model_node)
    File "/home/me/dev/writer/writer/engine/converter.py", line 228, in place_paragraph
        self.place_current_line()
    File "/home/me/dev/writer/writer/engine/converter.py", line 188, in place_current_line
        self.place_current_paragraph()
    File "/home/me/dev/writer/writer/engine/converter.py", line 157, in place_current_paragraph
        assert self._current_line is None
    AssertionError
    ```
