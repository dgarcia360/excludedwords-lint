import re


class LintLine:

    def __init__(self, file_name, line_number, line_content):
        self.file_name = file_name.replace("\\", "/")
        self.line_number = line_number
        self.line_content = line_content

    def to_string(self):
        return '{0} line {1}: {2}'.format(self.file_name, self.line_number, self.line_content)


class Regex:

    def __init__(self, words, match_case=True, match_word=False, parse=True):
        self.value = r''
        if parse:
            words = words.split(',')
            if not match_case:
                self.value += r'(?i)'
            for i, word in enumerate(words):
                if i != 0:
                    self.value += r'|'
                if match_word:
                    self.value += r'^(.*?(\b'
                self.value += word
                if match_word:
                    self.value += r'\b)[^$]*)$'
        else:
            self.value += words

    def is_valid(self):
        try:
            re.compile(self.value)
            is_valid = True
        except re.error:
            is_valid = False
        return is_valid
