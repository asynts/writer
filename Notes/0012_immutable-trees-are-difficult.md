commitid b73e64efddfb15fab6a90421663838f3dcc87fa6

It turns out that it's quite a bit more difficult to reuse layout nodes than I thought.

### Notes

-   I can't have back references if I want the tree to be immutable.

-   I need some way of creating a copy of a layout node with some modifications applied.

-   https://stackoverflow.com/a/2587202/8746648

-   I started working on a prototype for immutable trees (`0001_immutable-tree`):

    -   When iterating the tree, I need to keep track of the parent nodes because the child nodes are immutable and thus can not
        reference their parent nodes.

-   It may not be the right call to use immutable trees for the layout because this could add a ton of complexity in the converter logic.
    However, it may be more flexible when more features are added to the engine later on.

### Ideas

-   I could add an additional phase where the object can be mutated freely.

-   I could add another object which can be modified freely but when it's assigned to a layout node,
    we promise not to change it.

-   I could get rid of back references by memorizing the parent hierachy when iterating the tree.
    When computing mouse events, I would always keep track of the parent node.

-   I should create a small prototype of such a tree modification before implementing this here.
