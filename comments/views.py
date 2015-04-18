# coding: utf-8
from datetime import datetime

from flask import request, Blueprint
from flask_restful import Resource, Api

from app import app, mongo

comments_app = Blueprint('comments', __name__)
api = Api(comments_app)


class CommentsWrapper(object):
    def __init__(self, db, *args, **kwargs):
        self.db = db
        self.collection = db.comments

    def fetch(self, uuid):
        """ Returns all comments for selected file.
        """
        return map(self.post_read, self.collection.find({'uuid': uuid}))

    def post_read(self, c):
        c.pop('_id')
        c['date'] = c['date'].strftime('%d-%m-%Y %H:%M')
        return c

    def add(self, uuid, data):
        comment = self.pre_save(data)
        comment['uuid'] = uuid
        self.collection.insert(comment)
        return self.post_read(comment)

    def pre_save(self, data):
        # TODO: add schema validation
        default = {'date': datetime.now()}
        default['line'] = [data['line']]
        default['message'] = data['message']
        default['author'] = data['author']
        return default

    def get_for_line(self, uuid, line):
        return self.grouped_by_line(uuid)(str(line))

    def grouped_by_line(self, uuid):
        if getattr(self, '__grouped_by_line_cache', None) is None:
            self.__grouped_by_line_cache = {}

        if uuid not in self.__grouped_by_line_cache:
            self.__grouped_by_line_cache[uuid] = {}

            comments = self.fetch(uuid)
            for c in comments:
                for l in c['line']:
                    self.__grouped_by_line_cache[uuid].setdefault(
                        l, []).append(c)

        def _get(line):
            comments = self.__grouped_by_line_cache[uuid].setdefault(line, [])
            return sorted(comments, key=lambda c: c['date'], reverse=True)

        return _get


class CommentsResource(Resource):
    def get(self, uuid):
        """ Fetch comments for file.
        """
        wrapper = CommentsWrapper(mongo.db)
        return wrapper.fetch(uuid)

    def post(self, uuid):
        """
        Add comment to selected to `filename`.
        Expected POST params:
            :line: souce line (str)
            :author: author's name (str)
            :message: message (str)
        """
        wrapper = CommentsWrapper(mongo.db)
        comment = wrapper.add(uuid, {
            'line': request.form['line'],
            'author': request.form['author'],
            'message': request.form['message']
        })
        return comment

api.add_resource(CommentsResource, '/api/comments/<string:uuid>')
