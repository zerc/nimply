# coding: utf-8
"""
    Manage ways for getting source files for review.
"""
import os

from werkzeug import secure_filename
from flask import render_template, request, redirect


class BaseVariant(object):
    url = None
    methods = None
    template = None

    def __init__(self, app, *args, **kwargs):
        self.app = app

    def render(self):
        if self.template is None:
            raise AttributeError('Setup template attribute!')
        return render_template(self.template, variant=self)


class UploadVariant(BaseVariant):
    """
    Allow users to uploading files.
    """
    url = '/upload/'
    methods = ('POST',)
    template = 'upload_form.html'

    def __init__(self, *args, **kwargs):
        super(UploadVariant, self).__init__(*args, **kwargs)
        self.allowed_ext = self.app.config['ALLOWED_EXTENSIONS']
        self.upload_dir = self.app.config['UPLOAD_FOLDER']

        if not os.path.exists(self.upload_dir):
            os.path.mkdir(self.upload_dir)

    def allowed_file(self, fname):
        return '.' in fname and fname.rsplit('.', 1)[1] in fname

    def __call__(self, *args, **kwargs):
        file = request.files['file']
        if file and self.allowed_file(file.filename):
            filename = secure_filename(file.filename)
        file.save(os.path.join(self.upload_dir, file.filename))
        return redirect('/')


class ListVariant(UploadVariant):
    """
    Provide are list of files to select.
    """
    url = None
    template = 'files_list.html'

    @property
    def files_list(self):
        return os.listdir(self.upload_dir)
