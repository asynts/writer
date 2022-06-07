commitid e44e50a714b9a23c35cc2f30cb9040d8a8a12bb6

Somehow, we are calling a method that assumes that the node can be changed when it is already placed.

### Notes

-   ```none
    Traceback (most recent call last):
    File "/usr/lib/python3.10/runpy.py", line 196, in _run_module_as_main
        return _run_code(code, main_globals, None,
    File "/usr/lib/python3.10/runpy.py", line 86, in _run_code
        exec(code, run_globals)
    File "/home/me/dev/writer/writer/__main__.py", line 132, in <module>
        main()
    File "/home/me/dev/writer/writer/__main__.py", line 127, in main
        window = Window()
    File "/home/me/dev/writer/writer/__main__.py", line 105, in __init__
        self._writerWidget = WriterWidget()
    File "/home/me/dev/writer/writer/__main__.py", line 89, in __init__
        self._layout_tree = create_layout_tree(self._model_tree)
    File "/home/me/dev/writer/writer/__main__.py", line 23, in create_layout_tree
        return writer.engine.converter.generate_layout_tree(model_tree)
    File "/home/me/dev/writer/writer/engine/converter.py", line 81, in generate_layout_tree
        words = generate_layout_nodes_for_words(parent_node=current_page_node.get_content_node(), words=words)
    File "/home/me/dev/writer/writer/engine/converter.py", line 65, in generate_layout_nodes_for_words
        words = generate_layout_nodes_for_words_helper(parent_node=new_layout_node, words=words)
    File "/home/me/dev/writer/writer/engine/converter.py", line 42, in generate_layout_nodes_for_words_helper
        if place_node_into_parent():
    File "/home/me/dev/writer/writer/engine/converter.py", line 9, in place_node_into_parent
        remaining_space = parent_node.get_max_remaining_height()
    File "/home/me/dev/writer/writer/engine/layout.py", line 267, in get_max_remaining_height
        return self.get_parent_node().get_max_remaining_height() - self.get_min_inner_height() - self.get_all_spacing().y
    File "/home/me/dev/writer/writer/engine/layout.py", line 263, in get_max_remaining_height
        assert self.get_phase() == Phase.PHASE_1_CREATED
    AssertionError
    ```

-   With my current understanding, `get_max_remaining_height` should never be called after a node has been placed.

-   The content node is already placed in the page before all of this starts.
    That is actually a bug that I found by adding these phase checks.
    Well done.

### Ideas

-   The content node can not be placed, or there needs to be some edge case for things with fixed height.

### Actions

-   We now defer the placement of special nodes in the page node.
