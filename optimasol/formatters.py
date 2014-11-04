# coding: utf-8
import json
from collections import defaultdict

from flask import render_template
from pygments.formatters import HtmlFormatter


__ALL__ = ('WithCommentsHtmlFormatter',)


class WithCommentsHtmlFormatter(HtmlFormatter):
    """
    Special formatter class for render reviewers comments.
    """
    def __init__(self, source_filename, *args, **kwargs):
        self.comments = FormatWrapper(source_filename)
        kwargs['hl_lines'] = self.comments.affected_lines
        return super(WithCommentsHtmlFormatter, self).__init__(*args, **kwargs)

    def wrap(self, source, outfile):
        return self._wrap_div(self._wrap_pre(self._wrap_code(source)))

    def _wrap_code(self, source):
        for line, row in enumerate(source, 1):
            yield row

            comments = self.comments.get_for_line(line)
            if comments:
                yield 1, comments


class FormatWrapper(object):
    """
    Are wrapper for doing some things with `format_file`.
    """
    def __init__(self, source_filename):
        """
        :`source_filename`: are reviewed file
        """
        filename = get_format_filename(source_filename)

        # TODO: add exception handling
        with open(filename, 'r') as f:
            self._raw_data = json.loads(f.read())

        # special dict for getting comments for line
        self._dict_for_get = defaultdict(list)
        for line_code, c in self._raw_data['comments'].items():
            key = int(line_code.split('-')[-1])
            self._dict_for_get[key].extend(c)

    @property
    def affected_lines(self):
        """
        Return list of lines numbers who have comments.
        """
        # TODO: cached_property?
        result = []
        for l in self._raw_data['comments'].keys():
            result.extend(self._unwrap_line(l))
        return result

    def get_for_line(self, line):
        """
        Return formatted string of comments for given `line` num.
        """
        comments = self._dict_for_get.get(line, None)
        if comments is None:
            return
        return render_template('comments.html', **locals())

    def _unwrap_line(self, line_str):
        """
        Unwrap line code like `1-4` to truly list of int's.
        """
        chunks = map(int, line_str.split('-'))
        if len(chunks) == 2:
            return list(range(chunks[0], chunks[1]+1))
        return chunks


def get_format_filename(original_filename):
    """
    Get filename based on given `original_filename`.
    """
    return original_filename.split('.')[0] + '.format'
