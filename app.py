# coding: utf-8
import json
from flask import Flask

from nimply.app import app as nimply
from files.app import app as files_app
from comments.app import app as comments_app

from files.formatters import WithCommentsHtmlFormatter

app = Flask(
    __name__,
    instance_relative_config=True,
    static_folder='static/build/',
    static_url_path='/static')

app.config.from_object('settings')

app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')
app.jinja_env.filters['jsonify'] = json.dumps

app.register_blueprint(nimply)
app.register_blueprint(files_app)
app.register_blueprint(comments_app)


@app.context_processor
def get_code_styles():
    formatter = WithCommentsHtmlFormatter('')
    return dict(code_styles=formatter.get_style_defs('.highlight'))
