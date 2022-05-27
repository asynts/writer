import model
import layout
import engine

import pygame

COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_RED = (255, 0, 0)
COLOR_GRAY = (200, 200, 200)

def create_model_tree():
    document = model.DocumentModelNode()

    header_node_1 = document.set_header_node(model.ParagraphModelNode())

    footer_node_1 = document.set_footer_node(model.ParagraphModelNode())

    footer_node_1.append_child(model.TextChunkModelNode(text="Page "))
    footer_node_1.append_child(model.FieldChunkModelNode(field="page_number"))
    footer_node_1.append_child(model.TextChunkModelNode(text="more text that will hopefully overflow the footer."))

    paragraph_1 = document.add_content_node(model.ParagraphModelNode())
    paragraph_1.append_child(model.TextChunkModelNode(text="Hello, "))
    paragraph_1.append_child(model.TextChunkModelNode(text="world"))
    paragraph_1.append_child(model.TextChunkModelNode(text="!"))

    paragraph_2 = document.add_content_node(model.ParagraphModelNode())
    paragraph_2.append_child(model.TextChunkModelNode(text="This is another paragraph."))

    return document

def create_layout_tree_1(document: model.DocumentModelNode):
    return engine.generate_layout_tree(document)

def create_layout_tree_2():
    layout_tree = layout.PageLayoutNode()

    # FIXME: Get actual paragraphs working.
    paragraph_1 = layout.BlockLayoutNode(
        fixed_height=1 * layout.font_height
    )
    layout_tree.get_content_node().place_block_node(paragraph_1)

    return layout_tree

def draw_layout_node(screen: pygame.Surface, layout_node: layout.LayoutNode):
    rect = (
        layout_node.get_absolute_x(),
        layout_node.get_absolute_y(),
        layout_node.get_width(),
        layout_node.get_height(),
    )

    if layout_node.get_background_color() is not None:
        screen.fill(layout_node.get_background_color(), rect)

    for child_node in layout_node.get_children():
        draw_layout_node(screen=screen, layout_node=child_node)

def main():
    pygame.display.init()
    pygame.font.init()

    layout.normal_font = pygame.font.SysFont("monospace", 12)
    layout.font_width, layout.font_height = layout.normal_font.size("x")

    layout_tree = create_layout_tree_2()

    screen = pygame.display.set_mode([ 500, 500 ])

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                return

        screen.fill(COLOR_GRAY)

        draw_layout_node(screen, layout_tree)

        pygame.display.flip()

if __name__ == "__main__":
    main()
