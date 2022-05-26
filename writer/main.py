import model
import layout
import engine

import pygame

COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_RED = (255, 0, 0)

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

def create_layout_tree(document: model.DocumentModelNode):
    return engine.generate_layout_tree(document)

def draw_layout_node(screen: pygame.Surface, layout_node: layout.LayoutNode):
    if isinstance(layout_node, layout.TextLayoutNode):
        x, y = layout_node.absolute_x(), layout_node.absolute_y()
        width, height = layout.normal_font.size(layout_node.text)

        pygame.draw.rect(screen, COLOR_RED, (x, y, width, height), width=1)

        text_surface = layout.normal_font.render(layout_node.text, False, COLOR_BLACK)
        screen.blit(text_surface, (x, y))
    elif isinstance(layout_node, layout.BlockLayoutNode):
        # FIXME: How do we get the width/height here?
        #        We need to measure the width of the text at some point.
        pass

    for child_node in layout_node.children:
        draw_layout_node(screen, child_node)

def main():
    pygame.display.init()
    pygame.font.init()

    layout.normal_font = pygame.font.SysFont("monospace", 12)
    layout.font_width, layout.font_height = layout.normal_font.size("x")

    model_tree = create_model_tree()
    layout_tree = create_layout_tree(model_tree)

    print("MODEL:")
    print(model_tree, end="")

    print("LAYOUT:")
    print(layout_tree, end="")

    screen = pygame.display.set_mode([ 500, 500 ])

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                return

        screen.fill(COLOR_WHITE)

        draw_layout_node(screen, layout_tree)

        pygame.display.flip()

if __name__ == "__main__":
    main()
