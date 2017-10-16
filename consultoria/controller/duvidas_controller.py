# coding: utf-8
from flask import jsonify
from flask.helpers import make_response
from flask.templating import render_template
from flask_login import fresh_login_required, current_user, login_required
from flask_mail import Message
from flask_security.decorators import roles_required

from consultoria.models.duvida import Duvida, DuvidaSchema
from consultoria.modules import mail

from ..modules import db, admin_permission


class DuvidasController:
    
    @admin_permission.require(http_exception=403)
    def salvar(self, data): 
        duvida, errors= DuvidaSchema().load(data)
        duvida.usuario_id = data['usuario_id']
        if errors.__len__() > 0 :
            return make_response("Dado de %s inválido" % duvida.errors[-1], 500)        
        db.session.add(duvida)
        db.session.commit()
        return make_response("Dúvida adicionada com sucesso", 200)
        
    @admin_permission.require(http_exception=403)
    def listar_admin(self):
        schema = DuvidaSchema()
        lista = Duvida().query.filter().all()        
        return schema.jsonify(lista, True)

    @login_required
    def listar(self):
        schema = DuvidaSchema()
        lista = Duvida().query.filter(Duvida.usuario_id == current_user.id).all()        
        return schema.jsonify(lista, True)
    
    @login_required
    def buscar(self, id):
        return DuvidaSchema().jsonify(Duvida.query.get(id))
    
    @admin_permission.require(http_exception=403)
    def admin_editar(self, data):
        with db.session.no_autoflush:
            schema = DuvidaSchema().load(data, instance=Duvida().query.get(data['id']), partial=True)        
            if schema.errors.__len__() > 0:
                return make_response(schema.errors[0], 500)        
            duvida = schema.data
            duvida.status = 'ativa'
            db.session.add(duvida)
            db.session.commit()
            self.emailRespostaDudiva(duvida)
            return DuvidaSchema().jsonify(duvida)                
#             return make_response("Informações alteradas com sucesso", 200)

    @fresh_login_required
    def editar(self, data):
        with db.session.no_autoflush:
            schema = DuvidaSchema().load(data, instance=Duvida().query.get(data['id']), partial=True)        
            if schema.errors.__len__() > 0:
                return make_response(schema.errors[0], 500)        
            duvida = schema.data
            duvida.status = 'pendente'
            db.session.add(duvida)
            db.session.commit()
            return DuvidaSchema().jsonify(duvida)                
#             return make_response("Informações alteradas com sucesso", 200)

    def emailRespostaDudiva(self, duvida):
        try:
            msg = Message('Sua dúvida foi respondida.', recipients=[duvida.usuario.email])
            msg.html = render_template('app/emailNotificaRespostaDuvida.html', enviado='Dúvidas', email='jullianoVolpato@gmail.com' , duvida=duvida) 
            mail.send(msg)
            return make_response("E-mail enviado com sucesso", 200)
        except Exception:
            pass
            return make_response("Erro no envio do e-mail", 500)
