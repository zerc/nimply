# coding: utf-8
import os


class SourceFile(object):
    """
    Wrapper for working with source file.
    """
    def __init__(self, app, fname, *args, **kwargs):
        self.fname = fname
        self.dir = app.config['UPLOAD_FOLDER']
        self.full_path = os.path.join(self.dir, self.fname)

        with open(self.full_path, 'r') as f:
            self.data = f.read()
