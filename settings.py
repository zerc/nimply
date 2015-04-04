# coding: utf-8
import os

BASE_DIR = os.path.dirname(__file__)

UPLOAD_FOLDER = os.path.join(BASE_DIR, 'upload')

ALLOWED_EXTENSIONS = ['py']

DEBUG = True

ALLOW_SOURCE_VARIANTS = (
    # 'nimply.bl.variants.UploadVariant',
    # 'nimply.bl.variants.ListVariant',
    # 'nimply.bl.variants.SimpleReactVariant',
    'nimply.bl.variants.ListReactVariant',
    'nimply.bl.variants.UploadReactVariant',
)
