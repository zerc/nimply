# coding: utf-8
from flask import Flask

from nimply.utils import load_object_from_string

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('settings')


def registrator(app):
    app.source_variants = []
    for path in app.config['ALLOW_SOURCE_VARIANTS']:
        var = load_object_from_string(path)(app)

        if var.url:
            rule = app.url_rule_class(
                var.url,
                methods=var.methods or ['GET'],
                endpoint=var.__class__.__name__
            )
            rule.provide_automatic_options = True
            app.url_map.add(rule)
            app.view_functions[var.__class__.__name__] = var

        app.source_variants.append(var)


registrator(app)
