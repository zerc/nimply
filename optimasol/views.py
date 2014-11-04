# coding: utf-8
from pygments import highlight
from pygments.lexers import guess_lexer, guess_lexer_for_filename
from pygments.formatters import HtmlFormatter

from .app import app
from .utils import render_to
from .format import WithCommentsHtmlFormatter


@app.route("/")
def index():
    """
    View for rendering main page of service.
    """
    return base_index()


@render_to('index.html')
def base_index(data=None, filename=None):
    """
    Low-level implemenation of main page.
    """
    if data is None:
        return locals()

    if data and filename:
        lexer = guess_lexer_for_filename(filename, data)
    elif data:
        lexer = guess_lexer(data)

    formatter = WithCommentsHtmlFormatter(filename, linenos='table')

    code = highlight(data, lexer, formatter)

    # TODO: generate this by command before start app
    code_styles = formatter.get_style_defs('.highlight')

    return locals()
