# coding: utf-8
import importlib
from functools import wraps

from flask import render_template
from werkzeug.wrappers import BaseResponse


def render_to(template=None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            status_code = 200
            ctx = f(*args, **kwargs) or {}

            if isinstance(ctx, BaseResponse):
                return ctx

            if isinstance(ctx, tuple):
                ctx, status_code = ctx

            template_name = template
            if template_name is None:
                template_name = f.__name__ + '.html'

            return render_template(template_name, **ctx), status_code
        return decorated_function
    return decorator


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
