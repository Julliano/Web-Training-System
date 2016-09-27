# coding: utf-8
from flask_login import LoginManager
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_principal import Permission, RoleNeed
from flask_script import Manager
from flask_security.datastore import SQLAlchemyUserDatastore
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CsrfProtect


db = SQLAlchemy()
login_manager = LoginManager()
csrf = CsrfProtect()
ma = Marshmallow()
migrate = Migrate()
manager = Manager()

#Permissões
admin_permission = Permission(RoleNeed('admin'))

