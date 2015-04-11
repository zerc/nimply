# coding: utf-8
""" Manage ways for getting source files for review.
"""
import os

from werkzeug import secure_filename
from flask import request, redirect

from .base import BaseVariant, UploadMixin


class UploadVariant(UploadMixin, BaseVariant):
    """
    Allow users to uploading files.
    """
    url = '/upload/'
    methods = ('POST',)
    template = 'upload_form.html'

    def __call__(self, *args, **kwargs):
        filename, filepath = self.upload(request)
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
