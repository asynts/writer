import pytest

import writer.engine.model
import writer.engine.converter

@pytest.fixture
def paragraph_1_input():
    paragraph_node = writer.engine.model.ParagraphModelNode()

    paragraph_node.add_child(writer.engine.model.TextChunkModelNode(text="Hello, "))
    paragraph_node.add_child(writer.engine.model.TextChunkModelNode(text="world"))
    paragraph_node.add_child(writer.engine.model.TextChunkModelNode(text="!"))

    return paragraph_node

@pytest.fixture
def paragraph_1_output(paragraph_1_input):
    text_chunks = paragraph_1_input.get_children()

    return [
        writer.engine.converter.WordGroup(
            excerpts=[
                writer.engine.converter.TextExcerpt(
                    text_chunk_model_node=text_chunks[0],
                    text="Hello,"
                ),
            ],
        ),
        writer.engine.converter.WordGroup(
            excerpts=[
                writer.engine.converter.TextExcerpt(
                    text_chunk_model_node=text_chunks[1],
                    text="world",
                ),
                writer.engine.converter.TextExcerpt(
                    text_chunk_model_node=text_chunks[2],
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
    paragraph_node = writer.engine.model.ParagraphModelNode()

    paragraph_node.add_child(writer.engine.model.TextChunkModelNode(text="foo"))
    paragraph_node.add_child(writer.engine.model.TextChunkModelNode(text="bar"))
    paragraph_node.add_child(writer.engine.model.TextChunkModelNode(text="baz"))

    return paragraph_node

@pytest.fixture
def paragraph_2_output(paragraph_2_input):
    text_chunks = paragraph_2_input.get_children()

    return [
        writer.engine.converter.WordGroup(
            excerpts=[
                writer.engine.converter.TextExcerpt(
                    text_chunk_model_node=text_chunks[0],
                    text="foo"
                ),
                writer.engine.converter.TextExcerpt(
                    text_chunk_model_node=text_chunks[1],
                    text="bar"
                ),
                writer.engine.converter.TextExcerpt(
                    text_chunk_model_node=text_chunks[2],
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
    paragraph_node = writer.engine.model.ParagraphModelNode()

    paragraph_node.add_child(writer.engine.model.TextChunkModelNode(text="This is a much longer paragraph with"))
    paragraph_node.add_child(writer.engine.model.TextChunkModelNode(text=" emphasis "))
    paragraph_node.add_child(writer.engine.model.TextChunkModelNode(text="applied to some of the text chunks. "))

    return paragraph_node

@pytest.fixture
def paragraph_3_output(paragraph_3_input):
    text_chunks = paragraph_3_input.get_children()

    return [
        writer.engine.converter.WordGroup(
            excerpts=[
                writer.engine.converter.TextExcerpt(
                    text_chunk_model_node=text_chunks[0],
                    text="This"
                ),
            ],
        ),
        writer.engine.converter.WordGroup(
            excerpts=[
                writer.engine.converter.TextExcerpt(
                    text_chunk_model_node=text_chunks[0],
                    text="is"
                ),
            ],
        ),
        writer.engine.converter.WordGroup(
            excerpts=[
                writer.engine.converter.TextExcerpt(
                    text_chunk_model_node=text_chunks[0],
                    text="a"
                ),
            ],
        ),
        writer.engine.converter.WordGroup(
            excerpts=[
                writer.engine.converter.TextExcerpt(
                    text_chunk_model_node=text_chunks[0],
                    text="much"
                ),
            ],
        ),
        writer.engine.converter.WordGroup(
            excerpts=[
                writer.engine.converter.TextExcerpt(
                    text_chunk_model_node=text_chunks[0],
                    text="longer"
                ),
            ],
        ),
        writer.engine.converter.WordGroup(
            excerpts=[
                writer.engine.converter.TextExcerpt(
                    text_chunk_model_node=text_chunks[0],
                    text="paragraph"
                ),
            ],
        ),
        writer.engine.converter.WordGroup(
            excerpts=[
                writer.engine.converter.TextExcerpt(
                    text_chunk_model_node=text_chunks[0],
                    text="with"
                ),
            ],
        ),
        writer.engine.converter.WordGroup(
            excerpts=[
                writer.engine.converter.TextExcerpt(
                    text_chunk_model_node=text_chunks[1],
                    text="emphasis"
                ),
            ],
        ),
        writer.engine.converter.WordGroup(
            excerpts=[
                writer.engine.converter.TextExcerpt(
                    text_chunk_model_node=text_chunks[2],
                    text="applied"
                ),
            ],
        ),
        writer.engine.converter.WordGroup(
            excerpts=[
                writer.engine.converter.TextExcerpt(
                    text_chunk_model_node=text_chunks[2],
                    text="to"
                ),
            ],
        ),
        writer.engine.converter.WordGroup(
            excerpts=[
                writer.engine.converter.TextExcerpt(
                    text_chunk_model_node=text_chunks[2],
                    text="some"
                ),
            ],
        ),
        writer.engine.converter.WordGroup(
            excerpts=[
                writer.engine.converter.TextExcerpt(
                    text_chunk_model_node=text_chunks[2],
                    text="of"
                ),
            ],
        ),
        writer.engine.converter.WordGroup(
            excerpts=[
                writer.engine.converter.TextExcerpt(
                    text_chunk_model_node=text_chunks[2],
                    text="the"
                ),
            ],
        ),
        writer.engine.converter.WordGroup(
            excerpts=[
                writer.engine.converter.TextExcerpt(
                    text_chunk_model_node=text_chunks[2],
                    text="text"
                ),
            ],
        ),
        writer.engine.converter.WordGroup(
            excerpts=[
                writer.engine.converter.TextExcerpt(
                    text_chunk_model_node=text_chunks[2],
                    text="chunks."
                ),
            ],
        ),
    ]

def test_paragraph_3(paragraph_3_input, paragraph_3_output):
    word_groups = writer.engine.converter.compute_word_groups_in_paragraph(paragraph_3_input)
    assert word_groups == paragraph_3_output
