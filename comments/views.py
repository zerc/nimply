# coding: utf-8
from flask_restful import Resource
from flask import request

from .bl.wrapper import FormatWrapper
from .app import api


class CommentsResource(Resource):
    def get(self, fname):
        """ Fetch comments for file.
        """
        return FormatWrapper(fname).all()

    def post(self, fname):
        """
        Add comment to selected to `filename`.
        Expected POST params:
            :line: souce line (str)
            :author: author's name (str)
            :message: message (str)
        Returns:
            Status by jsonify string
        """
        wrapper = FormatWrapper(fname)
        comment = wrapper.add_comment(request.form['line'],
                                      request.form['author'],
                                      request.form['message'])
        wrapper.save()
        return comment

api.add_resource(CommentsResource, '/api/comments/<string:fname>')
