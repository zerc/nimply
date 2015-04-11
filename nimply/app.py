# coding: utf-8
""" Portal module. Contains common views.
"""
from core import Blueprint, load_object_from_string

app = Blueprint('nimply', __name__, template_folder='templates')
