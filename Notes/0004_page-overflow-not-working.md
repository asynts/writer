commitid 23829317a3055ae8ef82d0379a0b7585d55a6c05

Somehow, the page overflow is not working.

### Notes

-   The calculated `remaining_space` is incorrect, it is always very high which makes no sense.

### Theories

-   I suspect, that the `get_max_inner_height` calculation doesn't take the relative position of the node into account.
