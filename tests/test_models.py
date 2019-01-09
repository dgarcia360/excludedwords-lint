from excluded_words_lint.models import Regex, LintLine


def test_model_regex():
    regex = Regex('test')
    assert regex.value == 'test'


def test_model_regex_match_case_insensitive():
    regex = Regex('test', match_case=False)
    assert regex.value == '(?i)test'


def test_model_regex_match_case_sensitive():
    regex = Regex('Test', match_case=True)
    assert regex.value == 'Test'


def test_model_regex_match_word():
    regex = Regex('Test', match_word=True)
    assert regex.value == r'^(.*?(\b' + r'Test' + r'\b)[^$]*)$'


def test_model_regex_multiple_words():
    regex = Regex('Test,test', match_case = False, match_word=True)
    assert regex.value == r'(?i)^(.*?(\b' + r'Test'+r'\b)[^$]*)$|^(.*?(\b' + r'test' + r'\b)[^$]*)$'


def test_model_regex_is_valid():
    regex = Regex('test', parse=False)
    assert regex.is_valid()


def test_model_regex_is_not_valid():
    regex = Regex('[', parse=False)
    assert not regex.is_valid()


def test_model_lint_line():
    lint_line = LintLine('test\\', 1, 'test')
    assert lint_line.file_name == 'test/'
    assert lint_line.line_number == 1
    assert lint_line.line_content == 'test'


def test_model_lint_line_to_string():
    lint_line = LintLine('test\\', 1, 'test')
    assert lint_line.to_string() == 'test/ line 1: test'


