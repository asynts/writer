import pytest

import writer.engine.converter

def test_merge_multiple_spaces():
    assert writer.engine.converter.normalize_whitespace("hello  world") == "hello world"

def test_keep_leading_and_trailing_whitespace():
    assert writer.engine.converter.normalize_whitespace(" hello world ") == " hello world "

def test_replace_other_whitespace():
    assert writer.engine.converter.normalize_whitespace("hello\nworld") == "hello world"

def test_replace_and_merge_other_whitespace():
    assert writer.engine.converter.normalize_whitespace("\t\thello\n world \t") == " hello world "
