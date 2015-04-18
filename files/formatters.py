# coding: utf-8
import os
import json
from collections import defaultdict
from datetime import datetime

from flask import render_template
from pygments.formatters import HtmlFormatter
from pygments import highlight as base_highlight
from pygments.lexers import guess_lexer_for_filename

from app import mongo
from comments.views import CommentsWrapper


__ALL__ = ('WithCommentsHtmlFormatter',)


def highlight(filename, code, uuid):
    lexer = guess_lexer_for_filename(filename, code)
    formatter = WithCommentsHtmlFormatter(filename, linenos='inline')
    result = base_highlight(code, lexer, formatter)
    comments = CommentsWrapper(mongo.db)
    return [dict(
            line=line,
            code=code,
            comments=comments.get_for_line(uuid, line)
            ) for line, code in
            enumerate(result.splitlines(), 1)]


class WithCommentsHtmlFormatter(HtmlFormatter):
    """
    Special formatter class for render reviewers comments.
    """
    def __init__(self, source_filename, *args, **kwargs):
        kwargs['linespans'] = 'line'
        return super(WithCommentsHtmlFormatter, self).__init__(*args, **kwargs)

    def wrap(self, source, outfile):
        return self._wrap_code(source)

    def _wrap_code(self, source):
        for line, row in enumerate(source, 1):
            yield row

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
                    if num % sp == 0:
                        style = 'background-color: #ffffc0; padding: 0 5px 0 5px'
                    else:
                        style = 'background-color: #f0f0f0; padding: 0 5px 0 5px'
                    yield 1, '<span style="%s">%*s</span> ' % (
                        style, mw, (num % st and ' ' or num)) + line
                    num += 1
            else:
                for t, line in lines:
                    yield 1, ('<span style="background-color: #f0f0f0; '
                              'padding: 0 5px 0 5px">%*s</span> ' % (
                                  mw, (num % st and ' ' or num)) + line)
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
