import pytest

import writer.engine.model
import writer.engine.converter
import writer.engine.style

@pytest.fixture(autouse=True)
def enable_test_mode():
    # Using the actual font metrics class from PyQt doesn't work from a test environment.
    writer.engine.converter.b_simplify_font_metrics = True

@pytest.fixture
def paragraph_1_input():
    paragraph_node = writer.engine.model.ParagraphModelNode(style=writer.engine.style.LayoutStyle())

    paragraph_node.add_child(writer.engine.model.TextChunkModelNode(text="Hello, ", style=writer.engine.style.LayoutStyle()))
    paragraph_node.add_child(writer.engine.model.TextChunkModelNode(text="world", style=writer.engine.style.LayoutStyle()))
    paragraph_node.add_child(writer.engine.model.TextChunkModelNode(text="!", style=writer.engine.style.LayoutStyle()))

    return paragraph_node

@pytest.fixture
def paragraph_1_output(paragraph_1_input):
    text_chunks = paragraph_1_input.get_children()

    return [
        writer.engine.converter.WordGroup(
            excerpts=[
                writer.engine.converter.TextExcerpt(
                    text_chunk_model_node=text_chunks[0],
                    offset_into_model_node=0,
                    text="Hello,"
                ),
            ],
        ),
        writer.engine.converter.WordGroup(
            excerpts=[
                writer.engine.converter.TextExcerpt(
                    text_chunk_model_node=text_chunks[1],
                    offset_into_model_node=0,
                    text="world",
                ),
                writer.engine.converter.TextExcerpt(
                    text_chunk_model_node=text_chunks[2],
                    offset_into_model_node=0,
                    text="!",
                ),
            ],
        ),
    ]

def test_paragraph_1(paragraph_1_input, paragraph_1_output):
    word_groups = writer.engine.converter.compute_word_groups_in_paragraph(paragraph_1_input)
    assert word_groups == paragraph_1_output

@pytest.fixture
def paragraph_2_input():
    paragraph_node = writer.engine.model.ParagraphModelNode(style=writer.engine.style.LayoutStyle())

    paragraph_node.add_child(writer.engine.model.TextChunkModelNode(text="foo", style=writer.engine.style.LayoutStyle()))
    paragraph_node.add_child(writer.engine.model.TextChunkModelNode(text="bar", style=writer.engine.style.LayoutStyle()))
    paragraph_node.add_child(writer.engine.model.TextChunkModelNode(text="baz", style=writer.engine.style.LayoutStyle()))

    return paragraph_node

@pytest.fixture
def paragraph_2_output(paragraph_2_input):
    text_chunks = paragraph_2_input.get_children()

    return [
        writer.engine.converter.WordGroup(
            excerpts=[
                writer.engine.converter.TextExcerpt(
                    text_chunk_model_node=text_chunks[0],
                    offset_into_model_node=0,
                    text="foo"
                ),
                writer.engine.converter.TextExcerpt(
                    text_chunk_model_node=text_chunks[1],
                    offset_into_model_node=0,
                    text="bar"
                ),
                writer.engine.converter.TextExcerpt(
                    text_chunk_model_node=text_chunks[2],
                    offset_into_model_node=0,
                    text="baz"
                ),
            ],
        ),
    ]

def test_paragraph_2(paragraph_2_input, paragraph_2_output):
    word_groups = writer.engine.converter.compute_word_groups_in_paragraph(paragraph_2_input)
    assert word_groups == paragraph_2_output

@pytest.fixture
def paragraph_3_input():
    paragraph_node = writer.engine.model.ParagraphModelNode(style=writer.engine.style.LayoutStyle())

    paragraph_node.add_child(writer.engine.model.TextChunkModelNode(text="This is a much longer paragraph with", style=writer.engine.style.LayoutStyle()))
    paragraph_node.add_child(writer.engine.model.TextChunkModelNode(text=" emphasis ", style=writer.engine.style.LayoutStyle()))
    paragraph_node.add_child(writer.engine.model.TextChunkModelNode(text="applied to some of the text chunks. ", style=writer.engine.style.LayoutStyle()))

    return paragraph_node

@pytest.fixture
def paragraph_3_output(paragraph_3_input):
    text_chunks = paragraph_3_input.get_children()

    return [
        writer.engine.converter.WordGroup(
            excerpts=[
                writer.engine.converter.TextExcerpt(
                    text_chunk_model_node=text_chunks[0],
                    offset_into_model_node=0,
                    text="This"
                ),
            ],
        ),
        writer.engine.converter.WordGroup(
            excerpts=[
                writer.engine.converter.TextExcerpt(
                    text_chunk_model_node=text_chunks[0],
                    offset_into_model_node=5,
                    text="is"
                ),
            ],
        ),
        writer.engine.converter.WordGroup(
            excerpts=[
                writer.engine.converter.TextExcerpt(
                    text_chunk_model_node=text_chunks[0],
                    offset_into_model_node=8,
                    text="a"
                ),
            ],
        ),
        writer.engine.converter.WordGroup(
            excerpts=[
                writer.engine.converter.TextExcerpt(
                    text_chunk_model_node=text_chunks[0],
                    offset_into_model_node=10,
                    text="much"
                ),
            ],
        ),
        writer.engine.converter.WordGroup(
            excerpts=[
                writer.engine.converter.TextExcerpt(
                    text_chunk_model_node=text_chunks[0],
                    offset_into_model_node=15,
                    text="longer"
                ),
            ],
        ),
        writer.engine.converter.WordGroup(
            excerpts=[
                writer.engine.converter.TextExcerpt(
                    text_chunk_model_node=text_chunks[0],
                    offset_into_model_node=22,
                    text="paragraph"
                ),
            ],
        ),
        writer.engine.converter.WordGroup(
            excerpts=[
                writer.engine.converter.TextExcerpt(
                    text_chunk_model_node=text_chunks[0],
                    offset_into_model_node=32,
                    text="with"
                ),
            ],
        ),
        writer.engine.converter.WordGroup(
            excerpts=[
                writer.engine.converter.TextExcerpt(
                    text_chunk_model_node=text_chunks[1],
                    offset_into_model_node=1,
                    text="emphasis"
                ),
            ],
        ),
        writer.engine.converter.WordGroup(
            excerpts=[
                writer.engine.converter.TextExcerpt(
                    text_chunk_model_node=text_chunks[2],
                    offset_into_model_node=0,
                    text="applied"
                ),
            ],
        ),
        writer.engine.converter.WordGroup(
            excerpts=[
                writer.engine.converter.TextExcerpt(
                    text_chunk_model_node=text_chunks[2],
                    offset_into_model_node=8,
                    text="to"
                ),
            ],
        ),
        writer.engine.converter.WordGroup(
            excerpts=[
                writer.engine.converter.TextExcerpt(
                    text_chunk_model_node=text_chunks[2],
                    offset_into_model_node=11,
                    text="some"
                ),
            ],
        ),
        writer.engine.converter.WordGroup(
            excerpts=[
                writer.engine.converter.TextExcerpt(
                    text_chunk_model_node=text_chunks[2],
                    offset_into_model_node=16,
                    text="of"
                ),
            ],
        ),
        writer.engine.converter.WordGroup(
            excerpts=[
                writer.engine.converter.TextExcerpt(
                    text_chunk_model_node=text_chunks[2],
                    offset_into_model_node=19,
                    text="the"
                ),
            ],
        ),
        writer.engine.converter.WordGroup(
            excerpts=[
                writer.engine.converter.TextExcerpt(
                    text_chunk_model_node=text_chunks[2],
                    offset_into_model_node=23,
                    text="text"
                ),
            ],
        ),
        writer.engine.converter.WordGroup(
            excerpts=[
                writer.engine.converter.TextExcerpt(
                    text_chunk_model_node=text_chunks[2],
                    offset_into_model_node=28,
                    text="chunks."
                ),
            ],
        ),
    ]

def test_paragraph_3(paragraph_3_input, paragraph_3_output):
    word_groups = writer.engine.converter.compute_word_groups_in_paragraph(paragraph_3_input)
    assert word_groups == paragraph_3_output

@pytest.fixture
def paragraph_4_input():
    paragraph_node = writer.engine.model.ParagraphModelNode(style=writer.engine.style.LayoutStyle())

    return paragraph_node

@pytest.fixture
def paragraph_4_output(paragraph_3_input):
    return []

def test_paragraph_4(paragraph_4_input, paragraph_4_output):
    word_groups = writer.engine.converter.compute_word_groups_in_paragraph(paragraph_4_input)
    assert word_groups == paragraph_4_output
