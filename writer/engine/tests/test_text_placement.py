import writer.engine.text_placement as text_placement
import writer.engine.model as model

def test_algorithm_terminates_1():
    text_placement.compute_placement_instructions_for_paragraph(
        model.ParagraphModelNode(
            style=None,
            children=[
                model.TextChunkModelNode(
                    style=None,
                    text="Hello, world!",
                    cursor_offset=None,
                    children=[],
                ),
                model.TextChunkModelNode(
                    style=None,
                    text="More text.",
                    cursor_offset=None,
                    children=[],
                ),
            ],
        ),
    )
