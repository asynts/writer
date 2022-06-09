### Model Tree

The model tree represents the document in memory at a very high level of abstraction.

It has the following structure:

-   *DocumentNode*

    -   *HeaderNode* (special, not a child)

    -   *FooterNode* (special, not a child)

    -   *ParagraphNode*

        Can overflow pages and might be split into multiple layout nodes.

        -   *ChunkNode*

            Adjacent chunks with the same style must be merged.

        -   *FieldNode*

            The most obvious one would be page numbers, but there could be others.

### Layout Tree

The layout tree describes how the model tree is rendered.

-   We need to know where we put things to process things like click events.

-   An important part is, that the layout tree needs to be invalidated when the model is changed.

-   The layout logic that converts the model nodes into layout nodes must be deterministic, otherwise, we get issues
    when we are invalidating too aggressively.

-   There can be multiple layout nodes for a single model node, for example the dot used by a list, or the headers and footers on each page.

-   In some cases, we need to fill in some information like page numbers that are abstracted in the model.

It has the following structure:

-   *PageNode*

-   *BlockLayoutNode*

-   *InlineLayoutNode*

    -   *WordChunkNode*

### Layout Phases

Not all of the layout operation can be performed in a single step.
We need to place child nodes before we can place the parent since we don't know the height of the parent before the children are placed.
Therefore, there are two phases:

-   In the first phase, a temporary parent is assigned that can be changed.
    The parent doesn't know about this at this point.
    No space is reserved and no position is assigned.

-   We might have to add another phase here.
    Instead of placing children directly, we could reserve space and figure out the placement later.
    That is needed for flexible containers where children can influence each other.

-   In the second phase, the parent is permanently assigned and can no longer be changed.
    The parent now knows about this child.
    Space is reserved and a position relative to the parent is assigned.

-   When all nodes have been placed, we compute all of the absolute positions and sizes and cache them in the nodes.
