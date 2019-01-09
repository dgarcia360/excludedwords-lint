import click
from .commands import find_excluded_words
from .models import Regex


@click.command()
@click.option('--extensions', '-e', default='*', help='File extensions to consider, separated by commas.')
@click.option('--match_case', '-c', is_flag=True, help='Matches case sensitive words.')
@click.option('--match_word', '-w', is_flag=True, help='Matches substrings.')
@click.option('--regex', '-r', is_flag=True, help='Argument is a custom regular expression.')
@click.option('--path', '-p', default='.', help='Changes the root directory.')
@click.option('--throw', '-t', is_flag=True, help='Throws an exception if some of the words are found.')
@click.argument('words', required=True)
def main(words, extensions, match_case, match_word, regex, path, throw):
    expression = Regex(words) if regex else Regex(words, match_case=match_case, match_word=match_word, parse=True)

    if not expression.is_valid():
        raise click.ClickException('The regular expression is invalid.')

    linted_lines = find_excluded_words(expression.value, path, extensions)

    if len(linted_lines) > 0:
        for linted_line in linted_lines:
            click.echo(linted_line.to_string())
        if throw:
            raise click.ClickException('The word(s) have been found in some of your files.')
