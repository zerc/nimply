# coding: utf-8
import os

from werkzeug import secure_filename
from flask_restful import Resource
from flask import request, abort
from gridfs import GridFS, NoFile

from .formatters import highlight
from .bl.wrapper import SourceFile
from .app import api, app


class FilesResource(Resource):
    def get(self):
        """ List of files.
        """
        upload_dir = app.config['UPLOAD_FOLDER']
        return os.listdir(upload_dir)

    def post(self):
        """ Upload new file.
        """
        file = request.files.get('file', None)
        if not file or not self.allowed_file(file.filename):
            return {}, 400

        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return {'filename': filename}

    def allowed_file(self, fname):
        ext = os.path.splitext(fname)[-1]
        return ext in app.config['ALLOWED_EXTENSIONS']

api.add_resource(FilesResource, '/api/files/')


class FileDetailResource(Resource):
    def get(self, uuid):
        """ Detail file.
        """
        storage = GridFS(app.app.mongo.db)

        try:
            fobject = storage.get_version(uuid=uuid, version=0)
        except NoFile:
            abort(404)

        code, filename = fobject.read(), fobject.filename
        return dict(code=highlight(filename, code.decode('utf-8'), uuid=uuid),
                    filename=filename)

api.add_resource(FileDetailResource, '/api/files/<string:uuid>/')
