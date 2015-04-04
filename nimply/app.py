# coding: utf-8
from flask import Blueprint as BaseBlueprint
from flask_restful import Api

from nimply.utils import load_object_from_string


class Blueprint(BaseBlueprint):
    def make_setup_state(self, app, options, first_registration=False):
        state = super(Blueprint, self).make_setup_state(
            app, options, first_registration)
        registrator(state, app, self)
        self.app = app
        return state

nimply = Blueprint('nimply', __name__, template_folder='templates')
api = Api(nimply)


def registrator(state, app, self):
    self.source_variants = app.source_variants = []
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

        self.source_variants.append(var)
