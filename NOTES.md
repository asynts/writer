### Notes

I didn't know where else to put it after removing it from the code.

-   When porting this to C++, the following roadmap could be used:

    -   Setup the layout tree.

    -   Render trivial block layout node.

    -   Prioritize getting background color working.

    -   Setup the model tree.

    -   Prepare everything for paging.

    -   Start rendering some text.

-   The idea is that, if we want to change the model, we delete all the layout nodes that correspond to that model node and all the following layout nodes.
    Then, we can just recompute these.
    Even simpler would be, if we just discard the whole layout tree.

-   There is another aspect that I didn't really think about.
    When we are cascading the style, this will differ between the model and layout nodes.
    The model nodes have essentially a linked list of styles that are applied to each node.
    On the other hand, the layout nodes have all the precomputed styles for each node.

    There is really no way around that because we need to translate the style from the model to the layout tree since something like splitting paragraphs
    means that the individual layout nodes have different style (only the last one has a margin bottom for example).
