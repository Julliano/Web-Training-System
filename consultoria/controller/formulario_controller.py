# coding: utf-8
from flask import jsonify
from flask.helpers import make_response
from flask.templating import render_template
from flask_login import fresh_login_required, current_user, login_required
from flask_mail import Message
from flask_security.decorators import roles_required

from consultoria.models.formulario import Formulario, FormularioSchema
from consultoria.modules import mail

from ..models.venda import Venda

from ..modules import db, admin_permission


class FormularioController:
    
    @admin_permission.require(http_exception=403)
    def salvar(self, data): 
        formulario, errors= FormularioSchema().load(data)
        formulario.usuario_id = data['usuario_id']
        if errors.__len__() > 0 :
            return make_response("Dado de %s inválido" % formulario.errors[-1], 500)        
        db.session.add(formulario)
        db.session.commit()
        return make_response("Dúvida adicionada com sucesso", 200)
        
    @admin_permission.require(http_exception=403)
    def listar_admin(self):
        schema = FormularioSchema()
        lista = Formulario().query.filter().all()        
        return schema.jsonify(lista, True)

    @login_required
    def listar(self):
        schema = FormularioSchema()
        lista = Formulario().query.outerjoin(Formulario.vendas).filter(Venda.usuario_id == current_user.id).all()        
        return schema.jsonify(lista, True)
    
    @login_required
    def buscar(self, id):
        form = Formulario().query.outerjoin(Formulario.vendas).filter(Venda.usuario_id == current_user.id, Formulario.id == id).first()
        return FormularioSchema().jsonify(form)

    @login_required
    def buscarUltimo(self, id):
        array = []
        array.append(Formulario().query.join(Formulario.vendas).filter(Formulario.preenchido == False, Venda.usuario_id == current_user.id).order_by(Venda.id).first())
        array.append(Formulario().query.join(Formulario.vendas).filter(Formulario.preenchido == True, Venda.usuario_id == current_user.id).order_by(Venda.id).first())
        return FormularioSchema().jsonify(array, True)
    
    @login_required
    def editar(self, data):
        with db.session.no_autoflush:
            schema = FormularioSchema().load(data, instance=Formulario().query.get(data['id']), partial=True)        
            if schema.errors.__len__() > 0:
                return make_response(schema.errors[0], 500)        
            formulario = schema.data
            formulario.status = 'ativa'
            formulario.preenchido = True
            db.session.add(formulario)
            db.session.commit()
            return make_response("Formulario editado com sucesso", 200)

    @admin_permission.require(http_exception=403)
    def admin_editar(self, data):
        with db.session.no_autoflush:
            schema = FormularioSchema().load(data, instance=Formulario().query.get(data['id']), partial=True)        
            if schema.errors.__len__() > 0:
                return make_response(schema.errors[0], 500)        
            formulario = schema.data
            formulario.status = 'ativa'
            db.session.add(formulario)
            db.session.commit()
            self.emailLiberacaoFormulario(formulario)
            return FormularioSchema().jsonify(formulario)                

    def emailAjusteFormulario(self, formulario):
        try:
            msg = Message('Ajuste de formulário.', recipients=[formulario.venda.usuario.email])
            msg.html = render_template('app/emailAjusteFormulario.html', enviado='Formulario', email='jullianoVolpato@gmail.com' , formulario=formulario) 
            mail.send(msg)
            return make_response("E-mail enviado com sucesso", 200)
        except Exception:
            pass
            return make_response("Erro no envio do e-mail", 500)
