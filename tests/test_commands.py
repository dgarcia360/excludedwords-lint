import pytest

from excluded_words_lint import commands

from excluded_words_lint.commands import find_excluded_words, _get_files


def test_helpers_find_excluded_words():
    linted_lines = find_excluded_words('Lorem', 'tests/example/second_level', '*')
    assert linted_lines[0].file_name == 'tests/example/second_level/2.md'
    assert linted_lines[0].line_number == 1
    assert linted_lines[0].line_content == 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.\n'


def test_get_files_all_extensions():
    files = _get_files('tests/example/', '*')
    assert len(files) == 2


def test_get_files_one_extension():
    files = _get_files('tests/example/', 'md')
    assert len(files) == 1


def test_get_files_multiple_extensions():
    files = _get_files('tests/example/', 'md,txt')
    assert len(files) == 2


