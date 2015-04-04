# coding: utf-8
import os
from pygments import highlight
from pygments.lexers import guess_lexer, guess_lexer_for_filename
from pygments.formatters import HtmlFormatter
from flask import request, jsonify
from flask_restful import Resource

from nimply.app import nimply as app, api
from nimply.utils import render_to
from nimply.formatters import WithCommentsHtmlFormatter, FormatWrapper
from nimply.bl.wrapper import SourceFile


@app.route('/')
def index():
    """
    View for rendering main page of service.
    """
    data = filename = None

    if request.args.get('filename'):
        fname = request.args['filename']

        wrapper = SourceFile(app, fname)
        data, filename = wrapper.data, wrapper.fname

    source_variants = app.source_variants
    return base_index(data, filename, extra=locals())


@render_to('index.jade')
def base_index(data=None, filename=None, extra=None):
    """
    Low-level implemenation of main page.
    """
    result = locals()
    if extra:
        result.update(extra)

    if data is None:
        return result

    if data and filename:
        lexer = guess_lexer_for_filename(filename, data)
    elif data:
        lexer = guess_lexer(data)

    result['formatter'] = WithCommentsHtmlFormatter(filename, linenos='inline')

    result['code'] = highlight(data, lexer, result['formatter'])

    # TODO: generate this by command before start app
    result['code_styles'] = result['formatter'].get_style_defs('.highlight')

    return result


class FileResource(Resource):
    def get(self, fname):
        result = {}
        wrapper = SourceFile(app.app, fname)
        data, filename = wrapper.data, wrapper.fname
        lexer = guess_lexer_for_filename(filename, data)
        formatter = WithCommentsHtmlFormatter(filename, linenos='inline')
        result['code'] = highlight(data, lexer, formatter).splitlines()
        # result['code'] = (highlight(data, lexer, formatter)
        #                   .replace('\n', '')
        #                   .replace('</span></span>', '</span></span>\n')
        #                   .splitlines())
        # result['code_styles'] = formatter.get_style_defs('.highlight')
        return result


api.add_resource(FileResource, '/api/media/<string:fname>')


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


@app.context_processor
def get_code_styles():
    formatter = WithCommentsHtmlFormatter('')
    return dict(code_styles=formatter.get_style_defs('.highlight'))
