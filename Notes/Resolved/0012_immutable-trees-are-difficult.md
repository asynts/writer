commitid b73e64efddfb15fab6a90421663838f3dcc87fa6

It turns out that it's quite a bit more difficult to reuse layout nodes than I thought.

### Notes

-   I can't have back references if I want the tree to be immutable.

-   I need some way of creating a copy of a layout node with some modifications applied.

-   https://stackoverflow.com/a/2587202/8746648

-   I started working on a prototype for immutable trees (`0001_immutable-tree`):

    -   When iterating the tree, I need to keep track of the parent nodes because the child nodes are immutable and thus can not
        reference their parent nodes.

    -   When modifying the tree, we need to be able to create a derived version of a node, this is quite involved and I don't know how I could
        implement this in C++ without tons of boilerplate.

        It's quite likely that some amount of code generation will be mandatory.

    -   It may not be the right call to use immutable trees for the layout because this could add a ton of complexity in the converter logic.
        However, it may be more flexible when more features are added to the engine later on.

        We have to create a ton of intermediate lists, just to be able to iterate the tree.
        This is likely necessary for the model tree but for the layout tree this is really bad.

    -   I tried adding an additional phase where the object can be mutated and this is probably the way to go.
        At this point, I should try to implement this in the actual writer application.

-   I started implementing everything in the actual writer application.

    -   There is another problem that I did not think of.

        I need to construct the parent hierachy because the nodes can not reference their parents.
        The problem is, that I am not actually iterating through the model tree but through the layout tree.
        In other words, I am only able to indirectly build this parent hierachy.

### Ideas

-   I could add another object which can be modified freely but when it's assigned to a layout node,
    we promise not to change it.

-   I should update the layout and converter code to be able to handle the immutable model tree next.

### Actions

-   I made the model tree immutable.
    This seemed simpler than messing with the layout tree and I am confident that this will stay, since undo/redo logic mandates it.
