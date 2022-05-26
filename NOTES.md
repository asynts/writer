### Notes

I didn't know where else to put it after removing it from the code.

-   We don't use `append_child` in many cases, because we need to track the nodes in some special way.
    This is really a workaround and we should be able to iterate on all the children without this workaround.

-   When we are deciding where the next node should go, we always have a 'layout_region_node' that will keep track of the node we are currently filling.
    If that node overflows, we can ask the current page for a new layout region.
    By doing this, we can easily create new pages or even work with multi-column layouts.
