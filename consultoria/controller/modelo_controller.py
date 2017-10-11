# coding: utf-8
from flask import jsonify
from flask.helpers import make_response
from flask_login import fresh_login_required, current_user, login_required
from flask_security.decorators import roles_required

from consultoria.models.modelo import ModeloTreino, ModeloTreinoSchema

from ..modules import db, admin_permission


class ModeloTreinoController:
    
    @admin_permission.require(http_exception=403)
    def salvar(self, data): 
        modelo, errors= ModeloTreinoSchema().load(data)
        if errors.__len__() > 0 :
            return make_response("Dado de %s inválido" % modelo.errors[-1], 500)        
        db.session.add(modelo)
        db.session.commit()
        return make_response("Modelo adicionado com sucesso", 200)
        
    @admin_permission.require(http_exception=403)
    def listar(self):
        schema = ModeloTreinoSchema()
        lista = ModeloTreino().query.filter().all()        
        return schema.jsonify(lista, True)
    
    @login_required
    def buscar(self, id):
        return ModeloTreinoSchema().jsonify(ModeloTreino.query.get(id))
    
    @fresh_login_required
    def editar(self, data):
        modeloSchema = ModeloTreinoSchema().load(data, instance=ModeloTreino().query.get(data['id']), partial=True)
        if modeloSchema.errors.__len__() > 0:
            return make_response(modeloSchema.errors[0], 500)
        modelo = modeloSchema.data
        db.session.add(modelo)
        db.session.commit()        
        return make_response("Informações alteradas com sucesso", 200)
    
    @admin_permission.require(http_exception=403)
    def admin_editar(self, data):
        modeloSchema = ModeloTreinoSchema().load(data, instance=ModeloTreino().query.get(data['id']), partial=True)        
        if modeloSchema.errors.__len__() > 0:
            return make_response(modeloSchema.errors[0], 500)        
        modelo = modeloSchema.data
        db.session.add(modelo)
        db.session.commit()                
        return make_response("Informações alteradas com sucesso", 200)
        
    @admin_permission.require(http_exception=403)
    def deletar(self, id):
        db.session.delete(ModeloTreino.query.get(id))
        db.session.commit()
        return make_response("Modelo removido com sucesso", 200)
        
