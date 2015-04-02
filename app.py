# coding: utf-8
import json
from flask import Flask

from nimply.app import nimply

app = Flask(
    __name__,
    instance_relative_config=True,
    static_folder='static/build/',
    static_url_path='/static')

app.config.from_object('settings')

app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')
app.jinja_env.filters['jsonify'] = json.dumps
app.register_blueprint(nimply)
