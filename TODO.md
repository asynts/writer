### Current

-   Implement `events.mouse_click_event` properly.

    With the new immutable model, it is no longer trivial to implement this.
    The model nodes themselves do not know their parent and thus we need to keep track of the
    parent node while processing the event.

    However, we are walking through the layout tree and not the model tree which makes things even more difficult.

### Next Up

-   I should build some validation logic that verifies that the parent hierachy is correct.

    For each model node, I should collect the correct parent hierachy and then use this to verify the hierachy in the layout tree.

    It would be nice, if I find some way of documenting this in some clear invariant.

### Backlog

-   I should add a ton of helper methods to `tree.Position` like `Position.previous_sibling`.
    That should make interactions with the model tree significantly easier.

-   At some point, I need to go through the codebase

    -   Add comments to each module in the codebase.

    -   What is good or bad about the codebase?

-   Create a lossless video to show of the project.

-   Reuse paragraphs during layout.
