# coding: utf-8
from flask import jsonify
from flask.helpers import make_response
from flask_login import fresh_login_required, current_user, login_required
from flask_security.decorators import roles_required

from consultoria.models.plano import PlanoSchema, Plano

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
        schema = PlanoSchema(only=('id','nome', 'sobrenome','email','grupos'))
        lista = Plano().query.filter().all()        
        return schema.jsonify(lista, True)
    
    @login_required
    def buscar(self, id):
        return PlanoSchema().jsonify(Plano.query.get(id))
    
    @fresh_login_required
    def editar(self, data):
        planoSchema = PlanoSchema().load(data, instance=Plano().query.get(data['id']), partial=True)
        if planoSchema.errors.__len__() > 0:
            return make_response(planoSchema.errors[0], 500)
        plano = planoSchema.data        
        if 'senhaAtual' not in data:
            return make_response("Informe a senha atual", 500)        
        if plano.is_correct_passwd(data['senhaAtual']) or plano.is_correct_crypt_passwd(data['senhaAtual']):
            if 'novaSenha' in data:
                plano.senha = plano.hash_pass(data['novaSenha'])
            db.session.add(plano)
            db.session.commit()                
            return make_response("Informações alteradas com sucesso", 200)
        return make_response("Senha atual incorreta",500)
    
    @admin_permission.require(http_exception=403)
    def admin_editar(self, data):
        planoSchema = PlanoSchema().load(data, instance=Plano().query.get(data['id']), partial=True)        
        if planoSchema.errors.__len__() > 0:
            return make_response(planoSchema.errors[0], 500)        
        plano = planoSchema.data
        self.handle_grupos(plano,data['grupoSelecionado'])
        db.session.add(plano)
        db.session.commit()                
        return make_response("Informações alteradas com sucesso", 200)
        
    @admin_permission.require(http_exception=403)
    def deletar(self, id):
        db.session.delete(Plano.query.get(id))
        db.session.commit()
        return make_response("Planos removido com sucesso", 200)
        
