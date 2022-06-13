commitid b73e64efddfb15fab6a90421663838f3dcc87fa6

It turns out that it's quite a bit more difficult to reuse layout nodes than I thought.

### Notes

-   I can't have back references if I want the tree to be immutable.

-   I need some way of creating a copy of a layout node with some modifications applied.

-   https://stackoverflow.com/a/2587202/8746648

### Ideas

-   I could add an additional phase where the object can be mutated freely.

-   I could add another object which can be modified freely but when it's assigned to a layout node,
    we promise not to change it.

-   I could get rid of back references by memorizing the parent hierachy when iterating the tree.
    When computing mouse events, I would always keep track of the parent node.

-   I should create a small prototype of such a tree modification before implementing this here.
