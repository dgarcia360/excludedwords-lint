import glob
import re

from .models import LintLine


def _get_files(root_dir, extensions):
    files = []
    valid_extensions = extensions.split(',')
    for extension in valid_extensions:
        files.extend(glob.iglob(root_dir+'/**/*.' + extension, recursive=True))
    return files


def find_excluded_words(regex, root_dir, extensions):
    linted_lines = []
    files = _get_files(root_dir, extensions)
    for file in files:
        with open(file, encoding='utf-8') as f:
            line_number = 1
            lines = f.readlines()
            for line in lines:
                search = re.search(regex, line)
                if search:
                    linted_lines.append(LintLine(f.name, line_number, search.string))
                line_number += 1
    return linted_lines
