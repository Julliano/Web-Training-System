# coding: utf-8
from flask import jsonify
from flask.helpers import make_response
from flask_login import fresh_login_required, current_user, login_required
from flask_security.decorators import roles_required

from ..models.grupo import Grupo
from ..models.usuario import Usuario, UsuarioSchema
from ..modules import db, admin_permission


class UsuarioController:
    
    @admin_permission.require(http_exception=403)
    def salvar(self, data): 
        usuario, errors= UsuarioSchema().load(data)
        if errors.__len__() > 0 :
            return make_response("Dado de %s inválido" % usuario.errors[-1], 500)        
        self.handle_grupos(usuario, data['grupoSelecionado'])  
        db.session.add(usuario)
        db.session.commit()
        return make_response("Usuário adicionado com sucesso", 200)
        
    @admin_permission.require(http_exception=403)
    def listar(self):
        schema = UsuarioSchema(only=('id','nome', 'sobrenome','email','grupos'))
        lista = Usuario().query.filter().all()        
        return schema.jsonify(lista, True)
    
    @login_required
    def buscar(self, id):
        return UsuarioSchema().jsonify(Usuario.query.get(id))
    
    @fresh_login_required
    def editar(self, data):
        usuarioSchema = UsuarioSchema().load(data, instance=Usuario().query.get(data['id']), partial=True)
        if usuarioSchema.errors.__len__() > 0:
            return make_response(usuarioSchema.errors[0], 500)
        usuario = usuarioSchema.data        
        if 'senhaAtual' not in data:
            return make_response("Informe a senha atual", 500)        
        if usuario.is_correct_passwd(data['senhaAtual']) or usuario.is_correct_crypt_passwd(data['senhaAtual']):
            if 'novaSenha' in data:
                usuario.senha = usuario.hash_pass(data['novaSenha'])
            db.session.add(usuario)
            db.session.commit()                
            return make_response("Informações alteradas com sucesso", 200)
        return make_response("Senha atual incorreta",500)
    
    @admin_permission.require(http_exception=403)
    def admin_editar(self, data):
        usuarioSchema = UsuarioSchema().load(data, instance=Usuario().query.get(data['id']), partial=True)        
        if usuarioSchema.errors.__len__() > 0:
            return make_response(usuarioSchema.errors[0], 500)        
        usuario = usuarioSchema.data
        self.handle_grupos(usuario,data['grupoSelecionado'])
        db.session.add(usuario)
        db.session.commit()                
        return make_response("Informações alteradas com sucesso", 200)
        
    @admin_permission.require(http_exception=403)
    def deletar(self, id):
        db.session.delete(Usuario.query.get(id))
        db.session.commit()
        return make_response("Usuário removido com sucesso", 200)
    
    def handle_grupos(self,usuario,grupo):
        usuario.grupos = []            
        usuario.grupos.append(Grupo().query.get(grupo))
        
    def remove_notificacao(self, id):
        current_user.notificacoes = [item for item in current_user.notificacoes if item.id != id]
        db.session.add(current_user)
        db.session.commit()
        return UsuarioSchema().jsonify(current_user)
        
        
