# coding: utf-8
from random import choice
import string

from flask import jsonify
from flask.helpers import make_response
from flask.templating import render_template
from flask_login import fresh_login_required, current_user, login_required
from flask_mail import Message
from flask_security.decorators import roles_required

from ..modules import mail

from ..models.grupo import Grupo
from ..models.usuario import Usuario, UsuarioSchema
from ..modules import db, admin_permission


class UsuarioController:
    
#     @admin_permission.require(http_exception=403)
    def salvar(self, data): 
        with db.session.no_autoflush:
            jaExiste = Usuario().query.filter(Usuario.email == data['email']).first()
            if jaExiste is not None:
                return make_response("Email já cadastrado, se esse email é seu, tente recuperar a senha.", 500)
            usuario, errors= UsuarioSchema().load(data)
            if errors.__len__() > 0 :
                return make_response("Dado de %s inválido" % usuario.errors[-1], 500)        
            self.handle_grupos(usuario)  
            usuario.grupo_id = usuario.grupos[0].id
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
    
    def resetarSenha(self, data):
        try:
            usuario = Usuario().query.filter(Usuario.recuperarSenha == data['recuperar']).first()
            usuario.senha = usuario.hash_pass(data['novaSenha'])
            usuario.recuperarSenha = None
            db.session.add(usuario)
            db.session.commit()
            return make_response("Senha alterada com sucesso", 200)
        except Exception:
            return make_response("Talvez tenha expirado seu prazo, solicite um novo e-mail de recuperação de senha.", 500)

    def emailRecuperacao(self, data):
        size = 50
        usuario = Usuario().query.filter(Usuario.email == data['email']).first()
        usuario.recuperarSenha = ''.join([choice(string.letters + string.digits) for i in range(size)])
        db.session.add(usuario)
        db.session.commit()
        return self.send_email_analista(usuario)
    
    def send_email_analista(self, usuario):
        try:
            msg = Message('Email de recuperação de senha', recipients=[usuario.email])
            msg.html = render_template('app/emailSenhaCliente.html', enviado='Suporte', email='jullianoVolpato@gmail.com' , form=request.form) 
            mail.send(msg)
            return make_response("E-mail enviado com sucesso", 200)
        except Exception:
            pass
            return make_response("Erro no envio do e-mail", 500)
    
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
    
    def handle_grupos(self,usuario):
        usuario.grupos = [] 
        usuario.grupos.append(Grupo().query.filter(Grupo.nome == 'usuario').first())
        
    def remove_notificacao(self, id):
        current_user.notificacoes = [item for item in current_user.notificacoes if item.id != id]
        db.session.add(current_user)
        db.session.commit()
        return UsuarioSchema().jsonify(current_user)
        
        
