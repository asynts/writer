import dataclasses
import pytest

import writer.engine.text_placement as text_placement
import writer.engine.model as model

def test_algorithm_terminates_1():
    placement_instructions = text_placement.compute_placement_instructions_for_paragraph(
        model.ParagraphModelNode(
            style=None,
            children=[
                model.TextChunkModelNode(
                    style=None,
                    text=" Hello,  world!",
                    cursor_offset=1,
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

    text_placement.print_placement_instructions(placement_instructions)

@dataclasses.dataclass(kw_only=True, frozen=True)
class Case:
    input_: model.ParagraphModelNode
    expected: list[text_placement.PlacementInstruction]

cases = [
    # [0]
    Case(
        input_=model.ParagraphModelNode(
            style=None,
            children=[
                model.TextChunkModelNode(
                    style=None,
                    text="foo ",
                    cursor_offset=None,
                    children=[],
                ),
                model.TextChunkModelNode(
                    style=None,
                    text="bar",
                    cursor_offset=None,
                    children=[],
                ),
            ],
        ),
        expected=[
            text_placement.WordPlacementInstruction(
                excerpts=[
                    text_placement.TextExcerpt(
                        model_node=None,
                        model_offset=0,
                        text="foo",
                    ),
                ],
            ),
            text_placement.WhitespacePlacementInstruction(
                model_node=None,
                model_offset=3,
            ),
            text_placement.WordPlacementInstruction(
                excerpts=[
                    text_placement.TextExcerpt(
                        model_node=None,
                        model_offset=0,
                        text="bar",
                    ),
                ],
            ),
        ]
    ),
    # [1]
    Case(
        input_=model.ParagraphModelNode(
            style=None,
            children=[
                model.TextChunkModelNode(
                    style=None,
                    children=None,
                    text="fo",
                    cursor_offset=None,
                ),
                model.TextChunkModelNode(
                    style=None,
                    children=None,
                    text="o ",
                    cursor_offset=None,
                ),
                model.TextChunkModelNode(
                    style=None,
                    children=None,
                    text=" bar",
                    cursor_offset=None,
                ),
            ],
        ),
        expected=[
            text_placement.WordPlacementInstruction(
                excerpts=[
                    text_placement.TextExcerpt(
                        model_node=None,
                        model_offset=0,
                        text="fo",
                    ),
                    text_placement.TextExcerpt(
                        model_node=None,
                        model_offset=0,
                        text="o",
                    ),
                ],
            ),
            text_placement.WhitespacePlacementInstruction(
                model_node=None,
                model_offset=1,
            ),
            text_placement.WordPlacementInstruction(
                excerpts=[
                    text_placement.TextExcerpt(
                        model_node=None,
                        model_offset=1,
                        text="bar",
                    ),
                ],
            ),
        ],
    ),
    # [2]
    Case(
        input_=model.ParagraphModelNode(
            style=None,
            children=[
                model.TextChunkModelNode(
                    style=None,
                    children=None,
                    text="foo",
                    cursor_offset=3,
                ),
                model.TextChunkModelNode(
                    style=None,
                    children=None,
                    text=" bar",
                    cursor_offset=None,
                ),
            ],
        ),
        expected=[
            text_placement.WordPlacementInstruction(
                excerpts=[
                    text_placement.TextExcerpt(
                        model_node=None,
                        model_offset=0,
                        text="foo",
                    ),
                ],
            ),
            text_placement.WhitespacePlacementInstruction(
                model_node=None,
                model_offset=0,
            ),
            text_placement.WordPlacementInstruction(
                excerpts=[
                    text_placement.TextExcerpt(
                        model_node=None,
                        model_offset=1,
                        text="bar",
                    ),
                ],
            ),
        ]
    ),
    # [3]
    Case(
        input_=model.ParagraphModelNode(
            style=None,
            children=[
                model.TextChunkModelNode(
                    style=None,
                    children=[],
                    text="foo ",
                    cursor_offset=4,
                ),
                model.TextChunkModelNode(
                    style=None,
                    children=[],
                    text=" bar",
                    cursor_offset=None,
                ),
            ],
        ),
        expected=[
            text_placement.WordPlacementInstruction(
                excerpts=[
                    text_placement.TextExcerpt(
                        model_node=None,
                        model_offset=0,
                        text="foo",
                    ),
                ],
            ),
            text_placement.WhitespacePlacementInstruction(
                model_node=None,
                model_offset=3,
            ),
            text_placement.CursorPlacementInstruction(
                model_node=None,
                model_offset=4,
            ),
            text_placement.WhitespacePlacementInstruction(
                model_node=None,
                model_offset=0,
            ),
            text_placement.WordPlacementInstruction(
                excerpts=[
                    text_placement.TextExcerpt(
                        model_node=None,
                        model_offset=1,
                        text="bar",
                    ),
                ],
            ),
        ],
    ),
    # [4]
    Case(
        input_=model.ParagraphModelNode(
            style=None,
            children=[
                model.TextChunkModelNode(
                    style=None,
                    children=[],
                    text="foo  bar",
                    cursor_offset=4,
                ),
            ],
        ),
        expected=[
            text_placement.WordPlacementInstruction(
                excerpts=[
                    text_placement.TextExcerpt(
                        model_node=None,
                        model_offset=0,
                        text="foo",
                    ),
                ],
            ),
            text_placement.WhitespacePlacementInstruction(
                model_node=None,
                model_offset=3,
            ),
            text_placement.CursorPlacementInstruction(
                model_node=None,
                model_offset=4,
            ),
            text_placement.WhitespacePlacementInstruction(
                model_node=None,
                model_offset=4,
            ),
            text_placement.WordPlacementInstruction(
                excerpts=[
                    text_placement.TextExcerpt(
                        model_node=None,
                        model_offset=5,
                        text="bar",
                    ),
                ],
            ),
        ],
    ),
    # [5]
    Case(
        input_=model.ParagraphModelNode(
            style=None,
            children=[
                model.TextChunkModelNode(
                    style=None,
                    children=[],
                    text="foo ",
                    cursor_offset=4,
                ),
            ],
        ),
        expected=[
            text_placement.WordPlacementInstruction(
                excerpts=[
                    text_placement.TextExcerpt(
                        model_node=None,
                        model_offset=0,
                        text="foo",
                    ),
                ],
            ),
            text_placement.WhitespacePlacementInstruction(
                model_node=None,
                model_offset=3,
            ),
            text_placement.CursorPlacementInstruction(
                model_node=None,
                model_offset=4,
            ),
        ],
    ),
    # [6]
    Case(
        input_=model.ParagraphModelNode(
            style=None,
            children=[
                model.TextChunkModelNode(
                    style=None,
                    children=[],
                    text="foo ",
                    cursor_offset=None,
                ),
            ],
        ),
        expected=[
            text_placement.WordPlacementInstruction(
                excerpts=[
                    text_placement.TextExcerpt(
                        model_node=None,
                        model_offset=0,
                        text="foo",
                    ),
                ],
            ),
            text_placement.WhitespacePlacementInstruction(
                model_node=None,
                model_offset=3,
            ),
        ],
    ),
]

@pytest.fixture(params=cases)
def case(request):
    return request.param

def test_compute_placement_instructions_for_paragraph(case: Case):
    actual = text_placement.compute_placement_instructions_for_paragraph(case.input_)

    print(">>> expected:")
    text_placement.print_placement_instructions(case.expected)
    print("<<<")
    print(">>> actual:")
    text_placement.print_placement_instructions(actual)
    print("<<<")

    assert len(actual) == len(case.expected)
    for placement_instruction_actual, placement_instruction_expected in zip(actual, case.expected):
        assert type(placement_instruction_actual) == type(placement_instruction_expected)

        if isinstance(placement_instruction_actual, text_placement.WordPlacementInstruction):
            assert len(placement_instruction_actual.excerpts) == len(placement_instruction_expected.excerpts)
            for excerpt_actual, excerpt_expected in zip(placement_instruction_actual.excerpts, placement_instruction_expected.excerpts):
                assert excerpt_actual.model_offset == excerpt_expected.model_offset
                assert excerpt_actual.text == excerpt_expected.text
        elif isinstance(placement_instruction_actual, text_placement.WhitespacePlacementInstruction):
            assert placement_instruction_actual.model_offset == placement_instruction_expected.model_offset
        elif isinstance(placement_instruction_actual, text_placement.CursorPlacementInstruction):
            assert placement_instruction_actual.model_offset == placement_instruction_expected.model_offset
        else:
            raise AssertionError
