import pytest
from click.testing import CliRunner

from excluded_words_lint import cli


@pytest.fixture
def runner():
    return CliRunner()


def test_cli_with_word(runner):
    result = runner.invoke(cli.main, ['finibus', '--path', 'tests/example/second_level'])
    assert result.exit_code == 0
    assert not result.exception
    expected_output = \
        'tests/example/second_level/2.md line 2: Morbi finibus purus finibus ultricies consectetur.'
    assert result.output.strip() == expected_output


def test_cli_with_word_twice_in_the_same_line(runner):
    result = runner.invoke(cli.main, ['finibus', '--path', 'tests/example/second_level'])
    assert result.exit_code == 0
    assert not result.exception
    expected_output = \
        'tests/example/second_level/2.md line 2: Morbi finibus purus finibus ultricies consectetur.'
    assert result.output.strip() == expected_output


def test_cli_with_word_in_multiple_files(runner):
    result = runner.invoke(cli.main, ['finibus', '--path', 'tests/example'])
    assert result.exit_code == 0
    assert not result.exception
    expected_output = \
        'tests/example/1.txt line 2: Morbi finibus purus finibus ultricies consectetur.\n' \
        '\ntests/example/second_level/2.md line 2: Morbi finibus purus finibus ultricies consectetur.'
    assert result.output.strip() == expected_output


def test_cli_with_multiple_words(runner):
    result = runner.invoke(cli.main, ['finibus,tincidunt', '--path', 'tests/example/second_level'])
    assert result.exit_code == 0
    assert not result.exception
    expected_output = \
        'tests/example/second_level/2.md line 2: Morbi finibus purus finibus ultricies consectetur.\n' \
        '\ntests/example/second_level/2.md line 7: Fusce nec tincidunt nunc, ut ornare eros.'
    assert result.output.strip() == expected_output


def test_cli_without_words(runner):
    result = runner.invoke(cli.main)
    assert result.exit_code == 2
    assert result.exception


def test_cli_word_does_not_exist(runner):
    result = runner.invoke(cli.main, ['random', '--path', 'tests/example/second_level'])
    assert result.exit_code == 0
    expected_output = ''
    assert result.output.strip() == expected_output


def test_cli_match_case_word_exists(runner):
    result = runner.invoke(cli.main, ['Proin', '--path', 'tests/example/second_level', '--match_case'])
    assert result.exit_code == 0
    assert not result.exception
    expected_output = \
        'tests/example/second_level/2.md line 8: Proin lectus tellus, sodales in scelerisque non, hendrerit ut lectus.'
    assert result.output.strip() == expected_output


def test_cli_match_case_word_does_not_exist(runner):
    result = runner.invoke(cli.main, ['proin', '--path', 'tests/example/second_level', '--match_case'])
    assert result.exit_code == 0
    assert not result.exception
    expected_output = ''
    assert result.output.strip() == expected_output


def test_cli_case_match_word_inactive(runner):
    result = runner.invoke(cli.main, ['nibus', '--path', 'tests/example/second_level'])
    assert result.exit_code == 0
    assert not result.exception
    expected_output = 'tests/example/second_level/2.md line 2: Morbi finibus purus finibus ultricies consectetur.'
    assert result.output.strip() == expected_output


def test_cli_case_match_word_active_and_word_exists(runner):
    result = runner.invoke(cli.main, ['finibus', '--path', 'tests/example/second_level', '--match_word'])
    assert result.exit_code == 0
    assert not result.exception
    expected_output = 'tests/example/second_level/2.md line 2: Morbi finibus purus finibus ultricies consectetur.'
    assert result.output.strip() == expected_output


def test_cli_case_match_word_active_word_does_not_exist(runner):
    result = runner.invoke(cli.main, ['nibus', '--path', 'tests/example/second_level', '--match_word'])
    assert result.exit_code == 0
    assert not result.exception
    expected_output = ''
    assert result.output.strip() == expected_output


def test_cli_case_filter_by_extension(runner):
    result = runner.invoke(cli.main, ['finibus', '--path', 'tests/example/', '--extensions', 'txt'])
    assert result.exit_code == 0
    assert not result.exception
    expected_output = 'tests/example/1.txt line 2: Morbi finibus purus finibus ultricies consectetur.'
    assert result.output.strip() == expected_output


def test_cli_case_filter_by_multiple_extensions(runner):
    result = runner.invoke(cli.main, ['finibus', '--path', 'tests/example/', '--extensions', 'txt,md'])
    assert result.exit_code == 0
    assert not result.exception
    expected_output = 'tests/example/1.txt line 2: Morbi finibus purus finibus ultricies consectetur.\n' \
        '\ntests/example/second_level/2.md line 2: Morbi finibus purus finibus ultricies consectetur.'
    assert result.output.strip() == expected_output


def test_cli_case_extension_does_not_exist(runner):
    result = runner.invoke(cli.main, ['finibus', '--path', 'tests/example/second_level/', '--extensions', 'rst'])
    assert result.exit_code == 0
    assert not result.exception
    expected_output = ''
    assert result.output.strip() == expected_output


def test_cli_case_custom_regex(runner):
    result = runner.invoke(cli.main, ['finibus', '--path', 'tests/example/second_level/', '--regex'])
    assert result.exit_code == 0
    assert not result.exception
    expected_output = 'tests/example/second_level/2.md line 2: Morbi finibus purus finibus ultricies consectetur.'
    assert result.output.strip() == expected_output


def test_cli_throw_error(runner):
    result = runner.invoke(cli.main, ['finibus', '--path', 'tests/example/second_level', '--throw'])
    assert result.exit_code == 1
    expected_output = 'tests/example/second_level/2.md line 2: Morbi finibus purus finibus ultricies consectetur.\n' \
        '\nError: The word(s) have been found in some of your files.'
    assert result.output.strip() == expected_output


def test_cli_throw_error_without_error(runner):
    result = runner.invoke(cli.main, ['random', '--path', 'tests/example/second_level', '--throw'])
    assert result.exit_code == 0
    expected_output = ''
    assert result.output.strip() == expected_output


def test_cli_error_in_regex(runner):
    result = runner.invoke(cli.main, ['[', '--path', 'tests/example/second_level', '--regex'])
    assert result.exit_code == 1
    expected_output = 'Error: The regular expression is invalid.'
    assert result.output.strip() == expected_output

