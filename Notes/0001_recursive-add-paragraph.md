### Notes

-   We appear to call `LayoutTreeGenerator.add_paragraph` recursively.
    Or we are calling `try_place_word` recursively, it's difficult to tell.

-   We hit the loop in `generate_layout_tree` only once.

-   After adding some debug print statements, it appears that creating a new region causes us to create a new region:

    ```none
    Creating new region
    Adding word in current line offset_x=0 offset_y=0
    Adding word in current line offset_x=35 offset_y=0
    Adding word in next line offset_x=0 offset_y=14
    Adding word in current line offset_x=0 offset_y=14
    Adding word in current line offset_x=35 offset_y=14
    Adding word in next line offset_x=0 offset_y=28
    Adding word in current line offset_x=0 offset_y=28
    Adding word in next line offset_x=0 offset_y=42
    Adding word in current line offset_x=0 offset_y=42
    Adding word in next line offset_x=0 offset_y=56
    Creating new region (AFTER)
    Adding word in next line offset_x=0 offset_y=14
    Creating new region
    Adding word in current line offset_x=0 offset_y=0
    Adding word in current line offset_x=35 offset_y=0
    Adding word in next line offset_x=0 offset_y=14
    Adding word in current line offset_x=0 offset_y=14
    Adding word in current line offset_x=35 offset_y=14
    Adding word in next line offset_x=0 offset_y=28
    Adding word in current line offset_x=0 offset_y=28
    Adding word in next line offset_x=0 offset_y=42
    Adding word in current line offset_x=0 offset_y=42
    Adding word in next line offset_x=0 offset_y=56
    Creating new region (AFTER)
    Adding word in next line offset_x=0 offset_y=14
    ```

### Theory

-   We are adding to `document.content_nodes` and thus the for loop in `generate_layout_tree` continues for ever.
    My understanding is, that we are adding the region node in the wrong place.
