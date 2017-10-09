# coding: utf-8
from flask import jsonify
from flask.helpers import make_response
from flask_login import fresh_login_required, current_user, login_required
from flask_security.decorators import roles_required

from ..modules import db, admin_permission
from consultoria.models.duvida import Duvida, DuvidaSchema


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
    
    @fresh_login_required
    def editar(self, data):
        with db.session.no_autoflush:
            schema = DuvidaSchema().load(data, instance=Duvida().query.get(data['id']), partial=True)        
            if schema.errors.__len__() > 0:
                return make_response(schema.errors[0], 500)        
            duvida = schema.data
            db.session.add(duvida)
            db.session.commit()                
            return make_response("Informações alteradas com sucesso", 200)
