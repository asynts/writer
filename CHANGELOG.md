## Version 0.2.0

This release was primarily focused on fixing bugs and rewriting some of the code.

### Added Features

-   Separate word placement algorithm into `text_placement` module.

-   Use dependency injection to avoid global variables.

-   Add unit tests to `tree` module.

-   Add keyboard shortcuts for undo and redo.

### Removed Features

-   We only support deletion using backspace and insertion using normal keys.
    I simply have not yet updated the code with the new logic.

-   We no longer reuse the layout nodes for normal paragraphs from the previous render.
    This should be simple to add back in.

## Version 0.1.0

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
