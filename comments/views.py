# coding: utf-8
from flask_restful import Resource
from flask import request

from .bl.wrapper import MongoCommentsWrapper as CommentsWrapper
from .app import api, app


class CommentsResource(Resource):
    def get(self, fname):
        """ Fetch comments for file.
        """
        return CommentsWrapper(app.app.mongo.db, fname).all()

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
        wrapper = CommentsWrapper(app.app.mongo.db, fname)
        comment = wrapper.add_comment(request.form['line'],
                                      request.form['author'],
                                      request.form['message'])
        return comment

api.add_resource(CommentsResource, '/api/comments/<string:fname>')
