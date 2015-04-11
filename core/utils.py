# coding: utf-8
import importlib

from flask import Blueprint as BaseBlueprint

__ALL__ = ('Blueprint', 'load_object_from_string')

# cache for imported modules
_IMPORTED = {}


def load_object_from_string(full_path):
    """
    Load object (class, function and other) from dot separated string.
    """
    path, obj_name = full_path.rsplit('.', 1)

    try:
        module = _IMPORTED[path]
    except KeyError:
        module = _IMPORTED[path] = importlib.import_module(path)

    return getattr(module, obj_name)


class Blueprint(BaseBlueprint):
    def __init__(self, *args, **kwargs):
        """
            :extra_setup_state: function used in `make_setup_state` method
            with state, app, self args.
        """
        self.extra_setup_state = kwargs.pop('extra_setup_state', None)
        super(Blueprint, self).__init__(*args, **kwargs)

    def make_setup_state(self, app, options, first_registration=False):
        state = super(Blueprint, self).make_setup_state(
            app, options, first_registration)
        self.config = app.config
        self.app = app
        if self.extra_setup_state:
            self.extra_setup_state(state, app, self)
        return state
