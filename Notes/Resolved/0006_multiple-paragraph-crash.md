commitid 7916aaa6a3fae35acfd5baf8f82fcfd15c87a212

Placing a single paragraph works fine, but the second one isn't placed correctly.

### Notes

-   The `get_max_remaining_width` call returns zero which causes the crash.
    That method was newly added by me and might be broken.

-   I've inspected the `_current_page.get_content_node()` structure and the output seems fine:

    ```none
    >>> place_paragraph: content_node
    BlockLayoutNode(relative_x=None, relative_y=None, id=140025355959840 phase=Phase.PHASE_1_CREATED)
    <<<
    case 1: enough space
    self._current_line.get_max_remaining_width()=394.8503937055 word_group.width=73.3125
    case 1: enough space
    self._current_line.get_max_remaining_width()=319.5378937055 word_group.width=85.5
    >>> place_paragraph: content_node
    BlockLayoutNode(relative_x=None, relative_y=None, id=140025355959840 phase=Phase.PHASE_1_CREATED)
        BlockLayoutNode(relative_x=0, relative_y=0, id=140025355959168 phase=Phase.PHASE_2_PLACED)
            BlockLayoutNode(relative_x=0, relative_y=0, id=140025355958544 phase=Phase.PHASE_2_PLACED)
                InlineTextChunkLayoutNode(relative_x=0, relative_y=0, id=140025355956720 phase=Phase.PHASE_2_PLACED)
                InlineTextChunkLayoutNode(relative_x=63.125, relative_y=0, id=140025355956768 phase=Phase.PHASE_2_PLACED)
                InlineTextChunkLayoutNode(relative_x=75.3125, relative_y=0, id=140025355956048 phase=Phase.PHASE_2_PLACED)
                InlineTextChunkLayoutNode(relative_x=128.25, relative_y=0, id=140025355955856 phase=Phase.PHASE_2_PLACED)
                InlineTextChunkLayoutNode(relative_x=140.4375, relative_y=0, id=140025355956096 phase=Phase.PHASE_2_PLACED)
    <<<
    ```

    When the first paragraph is placed, nothing is placed, but the second paragraph already sees the first placed paragraph.
    Notice that there are five inline text nodes which is correct: `[ "Hello,", " ", "world", "!", " " ]`, that confused me for a moment.

-   It seems, that the state of the `Placer` class is fine too:

    ```none
    place_paragraph: self._current_page=<writer.engine.layout.PageLayoutNode object at 0x7fa58f19e890> self._current_paragraph=None self._current_line=None
    place_paragraph: self._current_page=<writer.engine.layout.PageLayoutNode object at 0x7fa58f19e890> self._current_paragraph=None self._current_line=None
    ```

    This is what I would expect, the page hasn't been placed yet but the line and paragraph have been before each call happens.

-   It seems that the `self._current_line.get_max_remaining_width()` actually changed after I fixed the parent hierachy, now it's negative:

    ```none
    self._current_line.get_max_remaining_width()=-394.8503937055 word_group.width=42.75
    ```

-   I printed out some values in the `get_max_remaining_width` method:

    ```none
    >>> place_word_group_in_current_line
    get_max_remaining_width: case 3, fixed width: self.get_fixed_width()=396.8503937055 self.get_min_inner_width()=0 self.get_inner_spacing().x=2
    get_max_remaining_width: case 1, flexible with parent: self.get_parent_node().get_max_remaining_width()=394.8503937055 self.get_min_inner_width()=394.8503937055 self.get_all_spacing().x=0
    get_max_remaining_width: case 3, fixed width: self.get_fixed_width()=396.8503937055 self.get_min_inner_width()=0 self.get_inner_spacing().x=2
    get_max_remaining_width: case 1, flexible with parent: self.get_parent_node().get_max_remaining_width()=0.0 self.get_min_inner_width()=394.8503937055 self.get_all_spacing().x=0
    get_max_remaining_width: case 3, fixed width: self.get_fixed_width()=396.8503937055 self.get_min_inner_width()=0 self.get_inner_spacing().x=2
    get_max_remaining_width: case 1, flexible with parent: self.get_parent_node().get_max_remaining_width()=394.8503937055 self.get_min_inner_width()=394.8503937055 self.get_all_spacing().x=0
    get_max_remaining_width: case 3, fixed width: self.get_fixed_width()=396.8503937055 self.get_min_inner_width()=0 self.get_inner_spacing().x=2
    get_max_remaining_width: case 1, flexible with parent: self.get_parent_node().get_max_remaining_width()=-394.8503937055 self.get_min_inner_width()=0 self.get_all_spacing().x=0
    get_max_remaining_width: case 3, fixed width: self.get_fixed_width()=396.8503937055 self.get_min_inner_width()=0 self.get_inner_spacing().x=2
    get_max_remaining_width: case 1, flexible with parent: self.get_parent_node().get_max_remaining_width()=394.8503937055 self.get_min_inner_width()=394.8503937055 self.get_all_spacing().x=0
    get_max_remaining_width: case 3, fixed width: self.get_fixed_width()=396.8503937055 self.get_min_inner_width()=0 self.get_inner_spacing().x=2
    get_max_remaining_width: case 1, flexible with parent: self.get_parent_node().get_max_remaining_width()=0.0 self.get_min_inner_width()=394.8503937055 self.get_all_spacing().x=0
    get_max_remaining_width: case 3, fixed width: self.get_fixed_width()=396.8503937055 self.get_min_inner_width()=0 self.get_inner_spacing().x=2
    get_max_remaining_width: case 1, flexible with parent: self.get_parent_node().get_max_remaining_width()=394.8503937055 self.get_min_inner_width()=394.8503937055 self.get_all_spacing().x=0
    get_max_remaining_width: case 3, fixed width: self.get_fixed_width()=396.8503937055 self.get_min_inner_width()=0 self.get_inner_spacing().x=2
    self._current_line.get_max_remaining_width()=-394.8503937055 word_group.width=42.75
    <<<
    ```

-   I got really confused from the previous result and it turns out, that I was recursively calling the method for debugging:

    ```none
    >>> place_word_group_in_current_line
    get_max_remaining_width: id(self)=140720171623968
    get_max_remaining_width: id(self)=140720171621760
    get_max_remaining_width: id(self)=140720171619024
    get_max_remaining_width: id(self)=140720171618592
    get_max_remaining_width: id(self)=140720171618592 case 3, fixed width: self.get_fixed_width()=396.8503937055 self.get_min_inner_width()=0 self.get_inner_spacing().x=2
    get_max_remaining_width: id(self)=140720171619024 case 1, flexible with parent: self.get_parent_node().get_max_remaining_width()=394.8503937055 self.get_min_inner_width()=394.8503937055 self.get_all_spacing().x=0
    get_max_remaining_width: id(self)=140720171618592
    get_max_remaining_width: id(self)=140720171618592 case 3, fixed width: self.get_fixed_width()=396.8503937055 self.get_min_inner_width()=0 self.get_inner_spacing().x=2
    get_max_remaining_width: id(self)=140720171621760 case 1, flexible with parent: self.get_parent_node().get_max_remaining_width()=0.0 self.get_min_inner_width()=394.8503937055 self.get_all_spacing().x=0
    get_max_remaining_width: id(self)=140720171619024
    get_max_remaining_width: id(self)=140720171618592
    get_max_remaining_width: id(self)=140720171618592 case 3, fixed width: self.get_fixed_width()=396.8503937055 self.get_min_inner_width()=0 self.get_inner_spacing().x=2
    get_max_remaining_width: id(self)=140720171619024 case 1, flexible with parent: self.get_parent_node().get_max_remaining_width()=394.8503937055 self.get_min_inner_width()=394.8503937055 self.get_all_spacing().x=0
    get_max_remaining_width: id(self)=140720171618592
    get_max_remaining_width: id(self)=140720171618592 case 3, fixed width: self.get_fixed_width()=396.8503937055 self.get_min_inner_width()=0 self.get_inner_spacing().x=2
    get_max_remaining_width: id(self)=140720171623968 case 1, flexible with parent: self.get_parent_node().get_max_remaining_width()=-394.8503937055 self.get_min_inner_width()=0 self.get_all_spacing().x=0
    get_max_remaining_width: id(self)=140720171621760
    get_max_remaining_width: id(self)=140720171619024
    get_max_remaining_width: id(self)=140720171618592
    get_max_remaining_width: id(self)=140720171618592 case 3, fixed width: self.get_fixed_width()=396.8503937055 self.get_min_inner_width()=0 self.get_inner_spacing().x=2
    get_max_remaining_width: id(self)=140720171619024 case 1, flexible with parent: self.get_parent_node().get_max_remaining_width()=394.8503937055 self.get_min_inner_width()=394.8503937055 self.get_all_spacing().x=0
    get_max_remaining_width: id(self)=140720171618592
    get_max_remaining_width: id(self)=140720171618592 case 3, fixed width: self.get_fixed_width()=396.8503937055 self.get_min_inner_width()=0 self.get_inner_spacing().x=2
    get_max_remaining_width: id(self)=140720171621760 case 1, flexible with parent: self.get_parent_node().get_max_remaining_width()=0.0 self.get_min_inner_width()=394.8503937055 self.get_all_spacing().x=0
    get_max_remaining_width: id(self)=140720171619024
    get_max_remaining_width: id(self)=140720171618592
    get_max_remaining_width: id(self)=140720171618592 case 3, fixed width: self.get_fixed_width()=396.8503937055 self.get_min_inner_width()=0 self.get_inner_spacing().x=2
    get_max_remaining_width: id(self)=140720171619024 case 1, flexible with parent: self.get_parent_node().get_max_remaining_width()=394.8503937055 self.get_min_inner_width()=394.8503937055 self.get_all_spacing().x=0
    get_max_remaining_width: id(self)=140720171618592
    get_max_remaining_width: id(self)=140720171618592 case 3, fixed width: self.get_fixed_width()=396.8503937055 self.get_min_inner_width()=0 self.get_inner_spacing().x=2
    self._current_line.get_max_remaining_width()=-394.8503937055 word_group.width=42.75
    <<<
    ```

    I've fixed it and it makes sense now:

    ```none
    >>> place_word_group_in_current_line
    get_max_remaining_width: id(self)=140522102204128
    get_max_remaining_width: id(self)=140522102204128 case 1, flexible with parent: self.get_min_inner_width()=0 self.get_all_spacing().x=0
    get_max_remaining_width: id(self)=140522102201728
    get_max_remaining_width: id(self)=140522102201728 case 1, flexible with parent: self.get_min_inner_width()=394.8503937055 self.get_all_spacing().x=0
    get_max_remaining_width: id(self)=140522102198992
    get_max_remaining_width: id(self)=140522102198992 case 1, flexible with parent: self.get_min_inner_width()=394.8503937055 self.get_all_spacing().x=0
    get_max_remaining_width: id(self)=140522102198560
    get_max_remaining_width: id(self)=140522102198560 case 3, fixed width: self.get_fixed_width()=396.8503937055 self.get_min_inner_width()=0 self.get_inner_spacing().x=2
    self._current_line.get_max_remaining_width()=-394.8503937055 word_group.width=42.75
    <<<
    ```

-   I understand the problem now, I need to distinguish between the `BlockLayoutNode` and the `InlineLayoutNode`.
    Or a better name might be `HorizontalLayoutNode` and `VerticalLayoutNode`.

### Ideas:

-   Print out the parent hierarchy.

### Theories

-   I suspect, that the newly created paragraph has the wrong parent somehow.

-   I suspect, that the logic in `get_max_remaining_width` is broken somehow.

### Actions

-   I found one issue that seemed to be unrelated, the line layout node had the wrong parent.
    That did not resolve the issue though.

-   The problem was that I had this one big `BlockLayoutNode` that either layed out children horizontally or vertically.
    That logic got mixed up and it didn't really make sense anymore.
    I've split it into two classes: `HorizontalLayoutNode` and `VerticalLayoutNode` which solves all the issues.
