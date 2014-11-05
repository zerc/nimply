# coding: utf-8
from pygments import highlight
from pygments.lexers import guess_lexer, guess_lexer_for_filename
from pygments.formatters import HtmlFormatter
from flask import request, jsonify

from .app import app
from .utils import render_to
from .formatters import WithCommentsHtmlFormatter, FormatWrapper


@app.route('/')
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

    formatter = WithCommentsHtmlFormatter(filename, linenos='inline')

    code = highlight(data, lexer, formatter)

    # TODO: generate this by command before start app
    code_styles = formatter.get_style_defs('.highlight')

    return locals()


@app.route('/comment/', methods=['POST'])
def add_comment():
    """
    Add comment to selected `line` of `filename`.
    Expected POST params:
        :line: souce line (str)
        :filename: source code filename (str)
        :author: author's name (str)
        :message: message (str)
    Returns:
        Status by jsonify string
    """
    # TODO: add some validation and error handling
    wrapper = FormatWrapper(request.form['filename'])
    wrapper.add_comment(
        request.form['line'], request.form['author'], request.form['message'])
    wrapper.save()
    return jsonify({'status': True})
