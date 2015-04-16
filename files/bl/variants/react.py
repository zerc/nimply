# coding: utf-8
import os
import json

from flask import request
from .base import BaseReactVariant, UploadMixin, MongoUploadMixin

__ALL__ = ('ListReactVariant', 'UploadReactVariant')


class ListReactVariant(BaseReactVariant):
    template = 'react_files_list.js'
    url = None

    def __init__(self, *args, **kwargs):
        super(ListReactVariant, self).__init__(*args, **kwargs)
        self.allowed_ext = self.app.config['ALLOWED_EXTENSIONS']
        self.upload_dir = self.app.config['UPLOAD_FOLDER']

        if not os.path.exists(self.upload_dir):
            os.path.mkdir(self.upload_dir)

    @property
    def files_list(self):
        return os.listdir(self.upload_dir)


class UploadReactVariant(MongoUploadMixin, BaseReactVariant):
    template = 'react_upload.js'
    url = '/api/upload/'
    methods = ('POST',)

    def __call__(self, *args, **kwargs):
        filename, filepath = self.upload(request)
        return json.dumps({'filename': filename})
