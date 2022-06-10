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

-   At some point I will have to figure out how to implement the undo/redo functionality.
    This means that it's not possible to just cut of the layout tree, instead we probably need to modify the model tree and then make all the model nodes
    immutable, then, we should be able to store the old model nodes and revert somehow.

    That will be fun to implement, especially, because we might run into memory issues here.

-   We always need to compute the entire layout, because of the scroll bars.
    Or at the very least we need to know the exact height of the result, but this is essentially the same thing like computing the entire layout since
    we do need the whole word group thing.

-   The whole idea with cutting of the end of the layout tree doesn't work.
    This might improve performance in some areas, but the worst case performance likely becomes worse.

    If we edit at the beginning of the file, we do not save any of the work, but all of the extra calculations will make this even slower.

-   I should move the codebase to at least some amount of dependency injection in the engine to be able to add unit tests to some aspects.
