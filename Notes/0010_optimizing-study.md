commitid f0b0af93dcbce30418ece993920f045a0a6b097d

My goal is to continue the optimization efforts, but in a more structured way, focused on the "Study in Scarlet" benchmark.

### Notes

-   I created a proper benchmark to have more reproduciable results, here is the initial result:

    ```none
    initial_layout                    0.4103s    410282404ns
    layout_unchanged_1                0.3925s    392546171ns
    layout_change_start               0.4008s    400800516ns
    layout_unchanged_2                0.3968s    396805364ns
    layout_change_end                 0.4003s    400318044ns
    layout_unchanged_3                0.3912s    391235661ns
    ```

-   I am aware of the following inefficencies:

    -   `get_max_remaining_width` when trying to place words in the current line.

        -   This could be cached in the layout node.

    -   `WordGroup.add_excerpt` takes up a significant amount of the execution time.

        It should be possible to cache the font in the model nodes.

    -   `LayoutStyle.__init__` is extremely slow, not sure what causes this.
