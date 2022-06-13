commitid 04056049e35394e9b666bf3cb8bb9fdd20b18c37

Fast clicking crashes the application.

### Notes

-   ```none
    Painting       29748106ns (   0.02975s)
    Rebuild       246124102ns (    0.2461s)
    Traceback (most recent call last):
    File "/home/me/dev/writer/writer/__main__.py", line 52, in mousePressEvent
        self._layout_tree.on_mouse_click(
    File "/home/me/dev/writer/writer/engine/layout.py", line 207, in on_mouse_click
        assert self.get_phase() == Phase.PHASE_3_FINAL
    AssertionError
    ./bin/run: line 4:  5263 Aborted                 (core dumped) python3 -m writer
    ```

### Theories

-   My understanding is, that we get the mouse event before we get the paint event.
    But during the paint event, we compute the absolute position and therefore, they are not
    avaliable for the mouse event.
