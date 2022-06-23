### Current

-   I should build some validation logic that verifies that the parent hierachy is correct.

    For each model node, I should collect the correct parent hierachy and then use this to verify the hierachy in the layout tree.

    It would be nice, if I find some way of documenting this in some clear invariant.

### Next Up

-   Reuse paragraphs during layout.

### Backlog

-   I should add a ton of helper methods to `tree.Position` like `Position.previous_sibling`.
    That should make interactions with the model tree significantly easier.

-   At some point, I need to go through the codebase

    -   Add comments to each module in the codebase.

    -   What is good or bad about the codebase?

-   Create a lossless video to show of the project.

-   Implement undo and redo logic.
