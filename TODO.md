### Current

### Done

### Next Up

-   Implement the cursor properly.

    -   Create some clear documentation about how the cursor is tracked and how we deal with it.

    -   Where does the cursor get it's style from?
        The text before or after it?

        The style should be choosen by `text_placement` not later.

        -   Look how LibreOffice does it.

### Features

-   Add supports for the remaining input methods.
    Before doing that I should think about simplifying and testing the `events` module.

    -   Delete.

    -   Enter.

    -   Cursor Left.

    -   Cursor Right.

    -   (Cursor Up.)

    -   (Cursor Down.)

### Tweaks

-   I could cache the word groups in the model paragraph nodes.

-   I should add a ton of helper methods to `tree.Position` like `Position.previous_sibling`.
    That should make interactions with the model tree significantly easier.

-   Create a lossless video to show of the project.

-   Currently, we merge spaces when creating `WhitespacePlacementInstruction`.

-   The document should be defined in terms of millimeters or points and should then be sampled into pixels.

-   Reuse the layout nodes from the previous render.
