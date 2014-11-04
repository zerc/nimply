# coding: utf-8
import json

from pygments.formatters import HtmlFormatter


__ALL__ = ('WithCommentsHtmlFormatter',)


class WithCommentsHtmlFormatter(HtmlFormatter):
    """
    Special formatter class for render reviewers comments.
    """
    def __init__(self, original_filename, *args, **kwargs):
        self.comments = load_format_file(original_filename)
        return super(WithCommentsHtmlFormatter, self).__init__(*args, **kwargs)

    def wrap(self, source, outfile):
        return self._wrap_div(self._wrap_pre(self._wrap_code(source)))

    def _get_comments_for_line(self, line):
        # TODO: rewrite method with normal algoritm (this is just DRAFT)
        rows = [c for c in self.comments if int(c['line']) == line]
        if rows:
            tmpl = '<span class="comments hidden">{date}, {author}, {message}</span>'
            return ''.join(tmpl.format(**row) for row in rows)

    def _wrap_code(self, source):
        for line, row in enumerate(source, 1):
            i, t = row
            comments = self._get_comments_for_line(line)
            yield row

            if comments:
                yield 1, comments



def load_format_file(original_filename):
    """
    Load ours `format` file for selected `original_filename`.
    """
    format_filename = get_format_filename(original_filename)

    with open(format_filename, 'r') as f:
        return json.loads(f.read())


def get_format_filename(original_filename):
    """
    Get filename based on given `original_filename`.
    """
    return original_filename.split('.')[0] + '.format'
