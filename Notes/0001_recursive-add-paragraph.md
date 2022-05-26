### Notes

-   We appear to call `LayoutTreeGenerator.add_paragraph` recursively.
    Or we are calling `try_place_word` recursively, it's difficult to tell.

-   We hit the loop in `generate_layout_tree` only once.

### Theory

-   We are adding to `document.content_nodes` and thus the for loop in `generate_layout_tree` continues for ever.
    My understanding is, that we are adding the region node in the wrong place.
