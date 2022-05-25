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
