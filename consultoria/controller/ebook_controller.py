# coding: utf-8
from random import choice
import string

from flask import jsonify
from flask.globals import request
from flask.helpers import make_response
from flask.templating import render_template
from flask_login import fresh_login_required, current_user, login_required
from flask_mail import Message
from flask_security.decorators import roles_required

from consultoria.models.listaEmail import Lista

from ..models.grupo import Grupo
from ..models.usuario import Usuario, UsuarioSchema
from ..modules import db, admin_permission
from ..modules import mail


class EbookController:
    
    def salvarNaLista(self, data):
        try:
            size = 50
            obj = Lista().query.filter(Lista.email == data['email']).first()
            if obj is not None:
                obj.validarEmail = ''.join([choice(string.letters + string.digits) for i in range(size)])
                obj.valido = False
            else:
                obj = Lista()
                obj.email = data['email']
                obj.emagrecimento = True
                obj.validarEmail = ''.join([choice(string.letters + string.digits) for i in range(size)]) 
            db.session.add(obj)
            db.session.commit()
#             return self.send_email(obj)
            return self.send_ebook(obj)
        except Exception:
            return make_response("Email não encontrado na base", 500)
    
    def enviarEbook(self, data):
        try:
            obj = Lista().query.filter(Lista.validarEmail == data['ebook']).first()
            obj.validarEmail = None
            obj.valido = True
            db.session.add(obj)
            db.session.commit()
            return self.send_ebook(obj)
        except Exception:
            return make_response("Talvez tenha expirado seu prazo, solicite um novo e-mail de recuperação de senha.", 500)
    
    def send_email(self, obj):
        try:
            msg = Message('Email de confirmação', recipients=[obj.email])
            msg.html = render_template('app/confirmacaoEbook.html', enviado='Suporte', email='jullianoVolpato@gmail.com' , obj=obj) 
            mail.send(msg)
            return make_response("E-mail de confirmação foi enviado para você.", 200)
        except Exception:
            pass
            return make_response("Erro no envio do e-mail", 500)

    def send_ebook(self, obj):
        try:
            msg = Message('Chegou o seu E-book', recipients=[obj.email])
            msg.html = render_template('app/enviarEbook.html', enviado='Suporte', email='jullianoVolpato@gmail.com' , url='https://drive.google.com/open?id=1HlWLtdZ5f-CyYkQ6NNFDJvVNCIaRyfGq') 
            mail.send(msg)
            return make_response("E-mail com ebook foi enviado para você.", 200)
        except Exception:
            pass
            return make_response("Erro no envio do e-mail", 500)
    
