# coding: utf-8
from flask import jsonify
from flask.helpers import make_response
from flask_login import fresh_login_required, current_user, login_required
from flask_security.decorators import roles_required

from consultoria.models.plano import PlanoSchema, Plano
from consultoria.models.venda import Venda, VendaSchema
from consultoria.models.usuario import Usuario, UsuarioSchema

from ..modules import db, admin_permission


class PlanoController:
    
    @admin_permission.require(http_exception=403)
    def salvar(self, data): 
        plano, errors= PlanoSchema().load(data)
        if errors.__len__() > 0 :
            return make_response("Dado de %s inválido" % plano.errors[-1], 500)        
        db.session.add(plano)
        db.session.commit()
        return make_response("Plano adicionado com sucesso", 200)
        
    @admin_permission.require(http_exception=403)
    def listar(self):
        schema = PlanoSchema()
        lista = Plano().query.filter().all()        
        return schema.jsonify(lista, True)
    
    def listarCliente(self):
        lista = db.session.query(Venda).filter(Venda.usuario_id == current_user.id).all()      
        return jsonify(VendaSchema(exclude=('usuario','pagamento.vendas','treinos')).dump(lista, True).data)
    
    @login_required
    def buscar(self, id):
        return PlanoSchema().jsonify(Plano.query.get(id))
    
    @fresh_login_required
    def editar(self, data):
        planoSchema = PlanoSchema().load(data, instance=Plano().query.get(data['id']), partial=True)
        if planoSchema.errors.__len__() > 0:
            return make_response(planoSchema.errors[0], 500)
        plano = planoSchema.data        
        return make_response("Informações alteradas com sucesso", 200)
    
    @admin_permission.require(http_exception=403)
    def admin_editar(self, data):
        planoSchema = PlanoSchema().load(data, instance=Plano().query.get(data['id']), partial=True)        
        if planoSchema.errors.__len__() > 0:
            return make_response(planoSchema.errors[0], 500)        
        plano = planoSchema.data
        db.session.add(plano)
        db.session.commit()                
        return make_response("Informações alteradas com sucesso", 200)
        
    @admin_permission.require(http_exception=403)
    def deletar(self, id):
        db.session.delete(Plano.query.get(id))
        db.session.commit()
        return make_response("Planos removido com sucesso", 200)
        
