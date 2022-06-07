commitid 96287e5054897ffc50f462e15785de24d2f17e4e

### Theories

-   I suspect, that we try to get the maximum width from the parent before being inserted into the parent, that can not work.

    My immutable strategy does not appear to pan out.

### Actions

-   I now splitted the placing process up.
    First, we add the child node, then we place it into the parent.

    After placement, it can not be changed anymore, before that, it's fair game
