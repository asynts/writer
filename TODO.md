### Current

### Done

-   Do some dependency injection to avoid global variables.

### Next Up

-   Implement the cursor properly.

    -   Create some clear documentation about how the cursor is tracked and how we deal with it.

    -   Where does the cursor get it's style from?
        The text before or after it?

        The style should be choosen by `text_placement` not later.

        -   Look how LibreOffice does it.

### Features

### Tweaks

-   I could cache the word groups in the model paragraph nodes.

-   I should add a ton of helper methods to `tree.Position` like `Position.previous_sibling`.
    That should make interactions with the model tree significantly easier.

-   Create a lossless video to show of the project.

-   Update the README file to present the current state of the application.

-   Currently, we merge spaces when creating `WhitespacePlacementInstruction`.

-   The document should be defined in terms of millimeters or points and should then be sampled into pixels.
