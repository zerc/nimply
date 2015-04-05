# coding: utf-8
import os
import json
from collections import defaultdict
from datetime import datetime

from flask import render_template
from pygments.formatters import HtmlFormatter
from pygments import highlight as base_highlight


__ALL__ = ('WithCommentsHtmlFormatter', 'FormatWrapper')


def highlight(code, lexer, formatter):
    result = base_highlight(code, lexer, formatter)
    # affected_lines = self.comments.affected_lines
    return [dict(
            line=line,
            code=code,
            comments=formatter.comments.get_for_line(line)
            ) for line, code in
            enumerate(result.splitlines(), 1)]


class WithCommentsHtmlFormatter(HtmlFormatter):
    """
    Special formatter class for render reviewers comments.
    """
    def __init__(self, source_filename, *args, **kwargs):
        self.comments = FormatWrapper(source_filename)
        # kwargs['hl_lines'] = self.comments.affected_lines
        kwargs['linespans'] = 'line'
        # kwargs['anchorlinenos'] = True
        return super(WithCommentsHtmlFormatter, self).__init__(*args, **kwargs)

    def wrap(self, source, outfile):
        return self._wrap_code(source)
        # return self._wrap_div(self._wrap_pre(self._wrap_code(source)))

    def _wrap_code(self, source):
        for line, row in enumerate(source, 1):
            yield row

            # comments = self.comments.get_for_line(line)
            # if comments:
            #     yield 1, comments

    def _wrap_inlinelinenos(self, inner):
        # need a list of lines since we need the width of a single number :(
        lines = list(inner)
        sp = self.linenospecial
        st = self.linenostep
        num = self.linenostart
        mw = len(str(len(lines) + num - 1))

        if self.noclasses:
            if sp:
                for t, line in lines:
                    if num%sp == 0:
                        style = 'background-color: #ffffc0; padding: 0 5px 0 5px'
                    else:
                        style = 'background-color: #f0f0f0; padding: 0 5px 0 5px'
                    yield 1, '<span style="%s">%*s</span> ' % (
                        style, mw, (num%st and ' ' or num)) + line
                    num += 1
            else:
                for t, line in lines:
                    yield 1, ('<span style="background-color: #f0f0f0; '
                              'padding: 0 5px 0 5px">%*s</span> ' % (
                              mw, (num%st and ' ' or num)) + line)
                    num += 1
        elif sp:
            for t, line in lines:
                yield 1, line
                num += 1
        else:
            for t, line in lines:
                yield 1, line
                num += 1

    def _wrap_linespans(self, inner):
        s = self.linespans
        i = self.linenostart - 1
        for t, line in inner:
            yield 1, line


class FormatWrapper(object):
    """
    Are wrapper for doing some things with `format_file`.
    """
    def __init__(self, source_filename):
        """
        :`source_filename`: are reviewed file
        """
        self.filename = get_format_filename(source_filename)

        # TODO: add exception handling
        if not os.path.exists(self.filename):
            self._raw_data = {'format': '0.1', 'comments': {}}
        else:
            with open(self.filename, 'r') as f:
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
        return comments
        if comments is None:
            return

        return render_template('comments.jade', **locals())

    def add_comment(self, line, author, message):
        """
        Add comment by `author` to selected `line`.
        """
        self._raw_data['comments'].setdefault(line, []).append(
            {
                'date': str(datetime.now()),
                'author': author,
                'message': message
            }
        )
        return self._raw_data['comments'][line][-1]

    def save(self):
        with open(self.filename, 'w') as f:
            f.write(json.dumps(self._raw_data))

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
