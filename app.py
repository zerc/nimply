# coding: utf-8
import json

from flask import Flask, render_template
from flask.ext.script import Manager
from flask.ext.pymongo import PyMongo

app = Flask(
    __name__,
    instance_relative_config=True,
    static_folder='static/build/',
    static_url_path='/static')

app.config.from_object('settings')
app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')
app.jinja_env.filters['jsonify'] = json.dumps


mongo = PyMongo(app)
manager = Manager(app)


def register_blueprints(app):
    from files import files_app
    from nimply import nimply_app
    from comments import comments_app

    app.register_blueprint(nimply_app)
    app.register_blueprint(files_app)
    app.register_blueprint(comments_app)

register_blueprints(app)


from files.formatters import WithCommentsHtmlFormatter
@app.context_processor
def get_code_styles():
    formatter = WithCommentsHtmlFormatter('')
    return dict(code_styles=formatter.get_style_defs('.highlight'))
