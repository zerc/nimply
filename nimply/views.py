# coding: utf-8
import os

from flask import Blueprint

from core import render_to

nimply_app = Blueprint('nimply', __name__, template_folder='templates')


@nimply_app.route('/')
@render_to('index.jade')
def index():
    """ View for rendering main page of service.
    """
    # source_variants = app.app.source_variants
    source_variants = []
    return locals()
