commitid eb71755d3010f72a2743fdbe1cd0df579fe77d62

Somehow, when I juse my fancy `mutate` function it doesn't appear to do anything.

### Notes

-   It seems that the root node is new, but all the children are old:

    ```none
    >>> before
    VerticalLayoutNode@140653272649792(background_color=(200, 200, 200))
    VerticalLayoutNode@140653272243328(background_color=(255, 255, 255))
    VerticalLayoutNode@140653272243392(background_color=None)
    HorizontalLayoutNode@140653272241344(background_color=None)
        TextLayoutNode@140653272121600(background_color=None, text='Hello, ')
        TextLayoutNode@140653272104576(background_color=None, text='world')
        TextLayoutNode@140653272103184(background_color=None, text='!')
    <<<
    mutate position.node=<__main__.TextLayoutNode object at 0x7fec6451fe80>
    mutate position.node=<__main__.HorizontalLayoutNode object at 0x7fec645414c0>
    mutate position.node=<__main__.VerticalLayoutNode object at 0x7fec64541cc0>
    mutate position.node=<__main__.VerticalLayoutNode object at 0x7fec64541c80>
    mutate position.node=<__main__.VerticalLayoutNode object at 0x7fec645a5040>
    >>> after
    VerticalLayoutNode@140653272651968(background_color=(200, 200, 200))
    VerticalLayoutNode@140653272243328(background_color=(255, 255, 255))
    VerticalLayoutNode@140653272243392(background_color=None)
    HorizontalLayoutNode@140653272241344(background_color=None)
        TextLayoutNode@140653272121600(background_color=None, text='Hello, ')
        TextLayoutNode@140653272104576(background_color=None, text='world')
        TextLayoutNode@140653272103184(background_color=None, text='!')
    <<<
    ```

-   In the Python version, this is fairly easy to implement, but I imagine this will be really tough in the C++ version.

### Ideas

### Theories

-   I suspect that my partition helper function doesn't work correctly.

### Actions

-   The problem was that I had this `isinstance(value, Some)` check in there which was always false.
    I originally added this to be able to distinguish between values that have `None` and values that are not assigned.
