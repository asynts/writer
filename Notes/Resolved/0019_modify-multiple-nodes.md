With an immutable model tree, we are not able to make multiple changes easily because all references break.

### Notes

-   I should research, how this is done by other people.

-   https://www.reddit.com/r/scala/comments/gxqvtr/addressing_and_manipulating_an_immutable_tree/

-   https://github.com/lukasbuenger/immutable-treeutils

    -   I think that having a list of nodes to visit instead of the `Position` thing is better.
        In other words:

        ```python
        Position = list[Node]
        ```

    -   This mentions the concept of immutable cursors, I should look at that further.

-   This mentions the concept of an "atom" in closure:

    https://github.com/redbadger/immutable-cursor

    The idea seems to be that we add callback functions that update the cursors.
    That's even more complexity, what a nightmare.

### Ideas

-   I should create a prototype for immutable cursors.

-   Stuff I want to look at:

    -   https://github.com/redbadger/immutable-cursor

    -   https://github.com/stanch/reftree

    -   https://github.com/stanch/zipper

### Result

-   The key here is, that we keep a `key` property in every node which is unique upon creation.
    If we want to modify a node we can copy this key to the new one.
    Therefore, all the references will stay intact.
