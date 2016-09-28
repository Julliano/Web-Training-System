import os

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
MEDIA_FOLDER = 'media'
JINJA_START_STRING = "--{"
JINJA_END_STRING = "}--"
SQLALCHEMY_MIGRATE_REPO = os.path.join(PROJECT_ROOT, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = False
WTF_CSRF_ENABLED = True
WTF_CSRF_METHODS = ['DELETE', 'POST', 'PUT', 'PATCH']
UPLOAD_FOLDER = os.path.join(PROJECT_ROOT,'uploads')
ALLOWED_EXTENSIONS = ['csv','txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif']
SECURITY_TRACKABLE = True