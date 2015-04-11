# coding: utf-8
from core import Blueprint, load_object_from_string
from flask_restful import Api


def registrator(state, app, self):
    """ Register extra source variants.
    """
    app.source_variants = app.source_variants = []
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


app = Blueprint('files', __name__,
                template_folder='templates', extra_setup_state=registrator)
api = Api(app)
