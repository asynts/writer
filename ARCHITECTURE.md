### Model Tree

Primary Files:

-   [writer/engine/model.py](writer/engine/model.py)

-   [writer/engine/tree.py](writer/engine/tree.py)

The model tree represents the document in memory at a very high level of abstraction.

-   The model tree is not concerned with paging and there is no concept of pages in the model.

-   The model tree is immutable, to change it, a copy must be created an all parents must recursively be updated.

    -   This is very important since we are able to create a snapshot of the document without much effort.
        That is mandatory to implement undo and redo logic properly.

    -   In order to be able to reference nodes in the tree, each node is assigned a unique key upon creation.
        If a node is changed, it can keep the same key thus allowing references to stay intact.
        This is crutial, because we constantly need to update the parent hierarchy when a new child is created.

-   Since the model nodes are immutable, we can not reference the parent model node.

    -   Therefore, we always need to keep track of the parent hierarchy when iterating through the tree.

-   It is possible to cache some mutable information in the model tree, when switching between models, we have to be
    extremely careful to keep these values consistent.

    -   The layout nodes are cached in the model nodes.
        That is useful for incremental rebuilds.

To manage the complexity, model nodes go through several phases that determine which operations are valid.

-   First, a model node is mutable, this is used to create the model node.

-   Then, a model node can become immutable which is it's final state.

-   To modify a model node, a mutable copy can be created.
    This will clear any cached values from this node.

-   It is not possible for model nodes to have mutable child nodes.

-   Text chunks must not be empty unless the cursor is placed in them.
    When the cursor is moved, this invariant needs to be enforced.

### Layout Tree

Primary Files:

-   [writer/engine/layout.py](writer/engine/layout.py)

The layout tree describes how the model tree is rendered.

-   There can be multiple layout nodes for a single model node.

    -   For example, every line in every paragraph is a separate layout node.

    -   For example, every word in every line is a separate layout node.

-   We need to know where things are rendered to process mouse events.

-   Layout nodes sometimes reference model nodes.
    The important part is, that the parent hierarchy must match the model node.

    -   If a layout node references a model node, then the parent model node must be referenced by the next parent layout node.

To manage the complexity, layout nodes go through several phases that determine which operations are valid.

-   First, the layout node is crated, a temporary parent layout node is referenced in the constructor.

    -   No space is reserved and no position is assigned.

    -   The parent node is informed, but this is only used for assertions.

        Nodes can only have a single pending layout node, to discard a layout node, the parent must be changed or it needs to be
        disassociated.

        -   This is important, because layout nodes will cache the remaining space in the parent node which would change if other
            layout nodes were added.

-   Second, the parent is permanently assigned and can no longer be changed.

    -   The parent now considers the node a child node.

    -   Space is reserved and a position relative to the parent is assigned.

    -   Layout nodes in this phase may be reused.

    -   Layout nodes can not be permanently assigned if they have a pending child node.

-   Third, if all nodes in the tree are in the second phase, then we start caching absolute information in the nodes.

    -   This is done lazily and some nodes will never enter this phase.

    -   Layout nodes in this phase may be reused.

-   In the future it will become necessary to introduce another phase.
    Instead of placing nodes directly, we need to reserve space and then do the placement later.
    This will be mandatory for flexible containers.

-   It is possible to reuse layout nodes.

    -   They are transferred into the first phase and the absolute information is cleared.

    -   We also need to clear the information of all child nodes recursively and thus move them into the second phase.

### Conversion Logic

Primary Files:

-   [writer/engine/converter.py](writer/engine/converter.py)

Transforming the model tree into the layout tree is not trivial.

-   We need to create a new page if a paragraph doesn't fit.

    -   If the first line of the paragraph fits, we split the paragraph and only move
        the overflow to the next page.

-   We need to create a new line, when a text chunk is too long to fit in the current line.

-   When wraping text, we need to be extremely careful where we can wrap.
    If the formatting changes in the middle of the word, we still need to wrap the entire word.

-   Sometimes, we reuse layout nodes, if a model node was unchanged.

    -   We try to reuse paragraphs, if they only have a single layout node assigned to them and if they fit on the page.
        That is the common case and drastically reduces the render time.

    -   The conversion logic must be very deterministic, because we sometimes reuse layout nodes.
        We do not want flickering effects.

### Event Handling

Primary Files:

-   [writer/engine/events.py](writer/engine/events.py)

Processing events is not trivial due to the rather complex layout and model tree structures.

-   We need to be careful what we modify in event handers, because the event handers themselves are iterating through the trees.

    -   We must not modify the layout tree in any way.
        Often, we are iterating through layout nodes and since they are mutable we must not change them.

    -   The model tree may be modified, by creating a new tree, however, cached values must not be invalidated.
        Note, that new values may be cached implicitly.

-   We must enforce the invariant that text chunks must not be empty unless they contain the cursor.

-   Events return true if the event has been handled.
    This can be used to delegate events from other events.
