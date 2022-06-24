### Notes

I didn't know where else to put it after removing it from the code.

-   When porting this to C++, the following roadmap could be used:

    -   Setup the layout tree.

    -   Render trivial block layout node.

    -   Prioritize getting background color working.

    -   Setup the model tree.

    -   Prepare everything for paging.

    -   Start rendering some text.

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

-   I should disconnect layout nodes from their parents in some organized way.
    This is important to assert in the parent that no other pending children exist.

    In other words, parent layout nodes should track pending children to verify that at most one is pending.

-   I had some thoughts while I was taking a break from the project:

    -   The layout nodes can not be immutable, because they must contain references to the model tree.
        If they were immutable, they would have to be copied.

    -   We can reuse layout nodes relatively safely, because there is only one layout tree that is being rendered.
        This is because the code runs synchronously, if we change that it will cause issues.

        Maybe copying the tree is better?

    -   It may be smart to make some parts of the layout nodes immutable though, maybe we don't go back to the first
        initialization phase but only after that.

    -   I was thinking about caching some more information in the model nodes about the length of words, however, this doesn't work
        because of word groups.

-   We need to reference model nodes in almost all layout nodes to be able to build the parent hierachy.

    The difficulty here is that we need to ensure that this hierachy is complete.

-   If we modify the model tree from a hook in the layout tree, we must not modify any layout nodes because the calling code might rely on it still.

-   I was thinking about creating copies of the layout nodes before reusing them.
    This doesn't appear to be necessary.

    -   At first I thought, this could be used to compute the layout in another thread.
        That would not work, because we must only interact with the most recent layout tree.

    -   On that note, some other things could be done without waiting for the layout computation to be finished.
        For example when adding new text by typing normally, we can simply update the model directly and wait for the layout to finish.
