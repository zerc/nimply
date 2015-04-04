# coding: utf-8
import os

from werkzeug import secure_filename
from flask import render_template


class BaseVariant(object):
    url = None
    methods = None
    template = None

    def __init__(self, app, *args, **kwargs):
        self.app = app
        self.base_template = 'base.jade'

    def get_template(self, template_name=None):
        return os.path.join('variants', template_name or self.template)

    def get_rendered_variant(self):
        return render_template(self.get_template(), variant=self)

    def render(self):
        if self.template is None:
            raise AttributeError('Setup template attribute!')

        return render_template(
            self.get_template(self.base_template),
            rendered_variant=self.get_rendered_variant())


class BaseReactVariant(BaseVariant):
    """ Variant class for renders in reactjs template.
    """
    def __init__(self, *args, **kwargs):
        super(BaseReactVariant, self).__init__(*args, **kwargs)
        self.base_template = 'base_react.jade'


class UploadMixin(object):
    def __init__(self, *args, **kwargs):
        super(UploadMixin, self).__init__(*args, **kwargs)
        self.allowed_ext = self.app.config['ALLOWED_EXTENSIONS']
        self.upload_dir = self.app.config['UPLOAD_FOLDER']

        if not os.path.exists(self.upload_dir):
            os.path.mkdir(self.upload_dir)

    def allowed_file(self, fname):
        return '.' in fname and fname.rsplit('.', 1)[1] in fname

    def upload(self, request):
        file = request.files['file']
        default = filename = filepath = None

        if file and self.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(self.upload_dir, filename)
            file.save(filepath)
            return filename, filepath

        return default

        # file.save(os.path.join(self.upload_dir, file.filename))
