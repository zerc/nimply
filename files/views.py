# coding: utf-8
import os
from uuid import uuid4

from werkzeug import secure_filename
from flask_restful import Resource, Api
from flask import request, abort, Blueprint
from gridfs import GridFS, NoFile

from app import mongo, app
from comments import CommentsWrapper
from .formatters import highlight


files_app = Blueprint('files',  __name__, template_folder='templates')
api = Api(files_app)


class FilesWrapper(object):
    def __init__(self, db, *args, **kwargs):
        self.storage = GridFS(db)
        self.comments_wrapper = CommentsWrapper(db)

    def list(self):
        """ Returns are list of files.
        """
        uuids = {f.uuid: {'name': f.filename, 'uuid': f.uuid,
                          'comments': 0, 'version': f.version}
                 for f in self.storage.find()}

        comments = self.comments_wrapper.get_grouped_counts(uuids.keys())

        def _up(uuid, count):
            uuids[uuid]['comments'] = count
            return uuids[uuid]

        return [_up(*c) for c in comments]

    def get(self, uuid, version=0):
        """ Return selected file or None if they does not exists.
        """
        try:
            return self.storage.get_version(uuid=uuid, version=version)
        except NoFile:
            return None

    def add(self, file):
        """ Save file into storage. Give him uuid.
        """
        uuid = unicode(uuid4())
        self.storage.put(file, filename=file.filename,  uuid=uuid, version=0)
        return uuid


@api.resource('/api/files/')
class FilesResource(Resource):
    def get(self):
        """ List of files.
        """
        wrapper = FilesWrapper(mongo.db)
        return wrapper.list()

    def post(self):
        """ Upload new file.
        """
        file = request.files.get('file', None)
        if not file or not self.allowed_file(file.filename):
            return {}, 400

        wrapper = FilesWrapper(mongo.db)
        uuid = wrapper.add(file)
        return {'uuid': uuid}

    def allowed_file(self, fname):
        ext = os.path.splitext(fname)[-1]
        return ext in app.config['ALLOWED_EXTENSIONS']


@api.resource('/api/files/<string:uuid>/')
class FileDetailResource(Resource):
    def get(self, uuid):
        """ Detail file.
        """
        wrapper = FilesWrapper(mongo.db)
        fobject = wrapper.get(uuid)
        if not fobject:
            abort(404)

        code, filename = fobject.read(), fobject.filename
        return dict(code=highlight(filename, code.decode('utf-8'), uuid=uuid),
                    filename=filename)
