# coding: utf-8
import os

from core import render_to
from .app import app


@app.route('/')
@render_to('index.jade')
def index():
    """ View for rendering main page of service.
    """
    source_variants = app.app.source_variants
    return locals()
