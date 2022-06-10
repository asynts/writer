commitid f0b0af93dcbce30418ece993920f045a0a6b097d

My goal is to continue the optimization efforts, but in a more structured way, focused on the "Study in Scarlet" benchmark.

### Notes

-   I created a proper benchmark to have more reproduciable results, here is the initial result:

    ```none
    initial_layout                    0.3905s    390533375ns
    layout_unchanged_1                0.3735s    373455650ns
    layout_change_start               0.3868s    386801800ns
    layout_unchanged_2                0.3845s    384506701ns
    layout_change_end                 0.3789s    378916188ns
    layout_unchanged_3                0.3773s    377349250ns
    ```

-   After caching the font in the model nodes, this is the current result:

    ```none
    initial_layout                    0.3295s    329464474ns
    layout_unchanged_1                0.3119s    311860668ns
    layout_change_start               0.3216s    321573964ns
    layout_unchanged_2                0.3153s    315336605ns
    layout_change_end                 0.3186s    318620339ns
    layout_unchanged_3                0.3096s    309575365ns
    ```

-   After caching the remaining width in the `HorizontalLayoutNode`, this is the current result:

    ```none
    initial_layout                    0.2521s    252105829ns
    layout_unchanged_1                0.2360s    235982229ns
    layout_change_start               0.2515s    251532266ns
    layout_unchanged_2                0.2497s    249661256ns
    layout_change_end                 0.2427s    242692955ns
    layout_unchanged_3                0.2289s    228929265ns
    ```

-   The following inefficencies have been resolved:

    -   `WordGroup.add_excerpt` takes up a significant amount of the execution time.

        It should be possible to cache the font in the model nodes.

    -   `get_max_remaining_width` when trying to place words in the current line.

        -   This could be cached in the layout node.

-   I am aware of the following inefficencies:

    -   `LayoutStyle.__init__` is extremely slow, not sure what causes this.

    -   It should be possible to store the layout nodes that are generated for paragraphs with the model nodes.
        Most paragraphs will not change, but are only placed in a different position.

        Therefore, if only one layout node is used for that paragraph, we try to use it again and recompute the result otherwise.
        That will not decrease the initial loading time, however, it will drastically reduce the time it takes to do incremental layout changes.

        To implement this, I should replicate the placement code and figure out how to merge both implementations later on.

### Actions

-   I started caching the font in the `TextChunkModelNode`.
    This was another noticable improvement, now, we only need to do the style cascade once for each model node.

-   I started caching the remaining width in `HorizontalLayoutNode`, this was another drastic improvement.
