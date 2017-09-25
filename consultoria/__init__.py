from os import path

from flask import Flask
from flask_migrate import MigrateCommand
from flask_security.core import Security
from flask_security.datastore import SQLAlchemyUserDatastore
from itsdangerous import URLSafeSerializer

from blueprints.consultoria_blueprint import consultoria_app 
from modules import db, ma, migrate, manager, login_manager, csrf

from models.grupo import Grupo
from models.usuario import Usuario

def create_app(mode="development"):
    instance_path = path.join(
        path.abspath(path.dirname(__file__)), "%s_instance" % mode
    )

    app = Flask("consultoria",
                instance_path=instance_path,
                instance_relative_config=True)

    app.config.from_object('consultoria.default_settings')
    app.config.from_pyfile('config.py')

    app.config['MEDIA_ROOT'] = path.join(
        app.config.get('PROJECT_ROOT'),
        app.config.get('MEDIA_FOLDER')
    )
    
    app.config['TEMP'] = path.join(app.config.get('PROJECT_ROOT'), 'tmp')        
    app.jinja_env.variable_start_string = app.config.get('JINJA_START_STRING')
    app.jinja_env.variable_end_string = app.config.get('JINJA_END_STRING')
     
    app.register_blueprint(consultoria_app)
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "login"    
    ma.init_app(app)
    migrate.init_app(app, db)    
    datastore = SQLAlchemyUserDatastore(db, Usuario, Grupo)
    Security(app=app, datastore=datastore)
    return app

