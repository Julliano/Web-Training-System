from os import urandom

RUN_DEBUG = True
RUN_USE_RELOADER = False
RUN_HOST = '0.0.0.0'
RUN_PORT = 80
CSRF_ENABLED = False
SQLALCHEMY_ECHO = False
SQLALCHEMY_DATABASE_URI = 'postgresql://gisuser:eusorox@localhost/consultoriaProd?client_encoding=utf8'
SECRET_KEY = '@Consultor14'
SECURITY_PASSWORD_HASH = 'pbkdf2_sha512'
SECURITY_PASSWORD_SALT = SECRET_KEY
SECURITY_TRACKABLE = True
SESSION_PROTECTION = "strong"
SEND_FILE_MAX_AGE_DEFAULT = 0
