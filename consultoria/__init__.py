# coding: utf-8
from os import path

from flask import Flask
from flask_migrate import MigrateCommand
from flask_security.core import Security
from flask_security.datastore import SQLAlchemyUserDatastore
from itsdangerous import URLSafeSerializer

from blueprints.consultoria_blueprint import consultoria_app 
from consultoria.controller.grupo_controller import GrupoController
from consultoria.models.usuario import UsuarioSchema
from consultoria.modules import mail
from modules import db, ma, migrate, manager, login_manager, csrf


def create_app(mode="production"):
    from models.grupo import Grupo
    from models.usuario import Usuario
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
    ctx = app.app_context()
    ctx.push()
    db.create_all()
#     usuario, errors = UsuarioSchema().load({'nome':'Admin', 'grupo_id':1, 'sobrenome':'Agrosatélite', 'email':'admin@agrosatelite.com.br','atividade':'Admin','logado':False, 'senha':123}, partial=True)
#     usuario.senha = usuario.hash_pass(123)
#     db.session.add(usuario) 
#     db.session.commit()
    login_manager.init_app(app)
    login_manager.login_view = "login"    
    ma.init_app(app)
    migrate.init_app(app, db)    
    datastore = SQLAlchemyUserDatastore(db, Usuario, Grupo)
    Security(app=app, datastore=datastore)
    mail.init_app(app)
    return app

