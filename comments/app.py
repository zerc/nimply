# coding: utf-8
from core import Blueprint
from flask_restful import Api

app = Blueprint('comments', __name__)
api = Api(app)
