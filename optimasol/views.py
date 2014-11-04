# coding: utf-8
from .app import app


@app.route("/")
def index():
    """
    View for rendering main page of service.
    """
    return base_index()


def base_index(data=None):
    """
    Low-level implemenation of main page.
    """
    return str(data)
