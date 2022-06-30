commitid 7e98c6febb7ce1e253a52a392a21356c1a451f73

The cursor isn't painted for some reason.

### Notes

-   I printed out the layout tree and it seems correct:

    ```none
    VerticalLayoutNode(relative_x=0, relative_y=0, id=139745222890080 phase=Phase.PHASE_2_PLACED)
     PageLayoutNode(relative_x=0, relative_y=10, id=139745218318352 phase=Phase.PHASE_2_PLACED)
      VerticalLayoutNode(relative_x=1, relative_y=1, id=139745222890240 phase=Phase.PHASE_2_PLACED)
      VerticalLayoutNode(relative_x=1, relative_y=72.81102362204723, id=139745222890400 phase=Phase.PHASE_2_PLACED)
       VerticalLayoutNode(relative_x=20, relative_y=20, id=139745222890720 phase=Phase.PHASE_2_PLACED)
        HorizontalLayoutNode(relative_x=0, relative_y=0, id=139745222890880 phase=Phase.PHASE_2_PLACED)
         InlineTextChunkLayoutNode(relative_x=0, relative_y=0, id=139745218324688 phase=Phase.PHASE_2_PLACED)
         InlineTextChunkLayoutNode(relative_x=71.953125, relative_y=0, id=139745218325040 phase=Phase.PHASE_2_PLACED)
       VerticalLayoutNode(relative_x=20, relative_y=62.6875, id=139745222891040 phase=Phase.PHASE_2_PLACED)
        HorizontalLayoutNode(relative_x=0, relative_y=0, id=139745222891200 phase=Phase.PHASE_2_PLACED)
         InlineTextChunkLayoutNode(relative_x=0, relative_y=0, id=139745218328912 phase=Phase.PHASE_2_PLACED)
         CursorLayoutNode(relative_x=38.375, relative_y=0, id=139745222891360 phase=Phase.PHASE_2_PLACED)
         InlineTextChunkLayoutNode(relative_x=38.375, relative_y=0, id=139745218367856 phase=Phase.PHASE_2_PLACED)
         InlineTextChunkLayoutNode(relative_x=38.375, relative_y=0, id=139745218365568 phase=Phase.PHASE_2_PLACED)
         InlineTextChunkLayoutNode(relative_x=47.96875, relative_y=0, id=139745218366096 phase=Phase.PHASE_2_PLACED)
         InlineTextChunkLayoutNode(relative_x=67.15625, relative_y=0, id=139745218367328 phase=Phase.PHASE_2_PLACED)
         InlineTextChunkLayoutNode(relative_x=76.75, relative_y=0, id=139745218367504 phase=Phase.PHASE_2_PLACED)
         InlineTextChunkLayoutNode(relative_x=86.34375, relative_y=0, id=139745218367680 phase=Phase.PHASE_2_PLACED)
         InlineTextChunkLayoutNode(relative_x=95.9375, relative_y=0, id=139745218482368 phase=Phase.PHASE_2_PLACED)
         InlineTextChunkLayoutNode(relative_x=191.875, relative_y=0, id=139745218482544 phase=Phase.PHASE_2_PLACED)
         InlineTextChunkLayoutNode(relative_x=201.46875, relative_y=0, id=139745218482720 phase=Phase.PHASE_2_PLACED)
         InlineTextChunkLayoutNode(relative_x=239.84375, relative_y=0, id=139745218482896 phase=Phase.PHASE_2_PLACED)
         InlineTextChunkLayoutNode(relative_x=249.4375, relative_y=0, id=139745218483072 phase=Phase.PHASE_2_PLACED)
         InlineTextChunkLayoutNode(relative_x=326.1875, relative_y=0, id=139745218483248 phase=Phase.PHASE_2_PLACED)
         InlineTextChunkLayoutNode(relative_x=335.78125, relative_y=0, id=139745218483424 phase=Phase.PHASE_2_PLACED)
         InlineTextChunkLayoutNode(relative_x=422.125, relative_y=0, id=139745218483600 phase=Phase.PHASE_2_PLACED)
         InlineTextChunkLayoutNode(relative_x=431.71875, relative_y=0, id=139745218483776 phase=Phase.PHASE_2_PLACED)
         InlineTextChunkLayoutNode(relative_x=450.90625, relative_y=0, id=139745218483952 phase=Phase.PHASE_2_PLACED)
         InlineTextChunkLayoutNode(relative_x=460.5, relative_y=0, id=139745218484128 phase=Phase.PHASE_2_PLACED)
         InlineTextChunkLayoutNode(relative_x=489.28125, relative_y=0, id=139745218484304 phase=Phase.PHASE_2_PLACED)
      VerticalLayoutNode(relative_x=1, relative_y=982.8110236220471, id=139745222890560 phase=Phase.PHASE_2_PLACED)
    ```

-   Somehow, the `CursorLayoutNode.paint_decorations` method is never called, I do not understand why.

### Conclusions

-   The problem was that `QRectF.intersects` doesn't consider the case where the width of one of the rects is zero.
    In my opinion, this is a bug, but whatever.
