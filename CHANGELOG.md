### Next Version

-   We need to be able to keep references to other nodes in the model tree that do not break when the children are changed.
    The key here is to add a unique identifier to each node that is not changed when we copy it for changes.

-   We need to be able to make multiple changes to the model tree, this can be done by keeping references in some places.
    Not sure exactly how this will turn out.

### Version 0.1.0

-   We are able to take a model tree that represents a document and convert it
    into a layout tree that can be rendered.

-   We are able to associate the mouse position with a layout node and can
    update a corresponding model node accordingly.

-   The application is sufficently optimized for use.

    -   The initial layout takes quite a bit of time, but this only needs to
        happen when a large file is opened.

    -   If the model is changed, we can reuse a substantial amount of work and
        rebuild the layout tree in real time.

-   The model tree is immutable, therefore, we are able to undo and redo
    changes very efficently.
