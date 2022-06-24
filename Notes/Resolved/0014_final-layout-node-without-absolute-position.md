commitid 801f43c61ad7a2e4934047635944974c0a45dee6

### Notes

-   Now, we crash again when trying to draw the whole thing:

    ```none
    Rebuild        43818030ns (   0.04382s)
    Traceback (most recent call last):
      File "/home/me/dev/writer/writer/__main__.py", line 50, in paintEvent
        self._layout_tree.paint(painter=painter, visible_rect=QtCore.QRectF(event.rect()))
      File "/home/me/dev/writer/writer/engine/layout.py", line 413, in paint
        child.paint(painter=painter, visible_rect=visible_rect)
      File "/home/me/dev/writer/writer/engine/layout.py", line 413, in paint
        child.paint(painter=painter, visible_rect=visible_rect)
      File "/home/me/dev/writer/writer/engine/layout.py", line 413, in paint
        child.paint(painter=painter, visible_rect=visible_rect)
      [Previous line repeated 1 more time]
      File "/home/me/dev/writer/writer/engine/layout.py", line 405, in paint
        if not self.get_qrect().intersects(visible_rect):
      File "/home/me/dev/writer/writer/engine/layout.py", line 334, in get_qrect
        return QtCore.QRectF(
    TypeError: arguments did not match any overloaded call:
      QRectF(): too many arguments
      QRectF(QPointF, QSizeF): argument 1 has unexpected type 'NoneType'
      QRectF(QPointF, QPointF): argument 1 has unexpected type 'NoneType'
      QRectF(float, float, float, float): argument 1 has unexpected type 'NoneType'
      QRectF(QRect): argument 1 has unexpected type 'NoneType'
      QRectF(QRectF): argument 1 has unexpected type 'NoneType'
    ./bin/run: line 4:  6430 Aborted                 (core dumped) python3 -m writer
    ```

    It seems that we are in the final phase, but we do not have an absolute position assigned.

### Ideas

-   I should reproduce this issue with a smaller example document.

-   Print out the layout tree and the node responsible for the crash.

### Conclusions

-   The problem was that I cleared the `_absolute_*` values without ever updating the `__phase` value.
