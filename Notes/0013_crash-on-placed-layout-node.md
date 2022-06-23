commitid a828b65d5467b0b0ff463217e98172862ca67e30

When clicking on a node in the bigger example document, we crash when generating the new layout.

### Notes

-   This seems to happen when a layout node is in `PHASE_2_PLACED` and we try to reuse it.

-   I started making some changes but some weird things happend, I stashed these changes.

### Theories

-   I suspect, that the layout node doesn't have an absolute position but my code assumes that.
