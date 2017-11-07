# coding: utf-8
from datetime import date

from flask import jsonify
from flask.globals import request
from flask.helpers import make_response
from flask.templating import render_template
from flask_login import fresh_login_required, current_user, login_required
from flask_mail import Message
from flask_security.decorators import roles_required
from sqlalchemy.orm import joinedload, contains_eager

from consultoria.models.treino import Treino, TreinoSchema
from consultoria.models.usuario import Usuario
from consultoria.models.venda import Venda
from consultoria.modules import mail

from ..modules import db, admin_permission


class TreinoController:
    
    @admin_permission.require(http_exception=403)
    def salvar(self, data): 
        treino, errors= TreinoSchema().load(data)
        treino.usuario_id = data['usuario_id']
        if errors.__len__() > 0 :
            return make_response("Dado de %s inválido" % treino.errors[-1], 500)        
        db.session.add(treino)
        db.session.commit()
        return make_response("Dúvida adicionada com sucesso", 200)
        
    @admin_permission.require(http_exception=403)
    def listar_admin(self, pagina=1):
        if request.args:
            pagina = int(dict(request.args).get('pagina')[0])
        stmt = Treino.query.options(joinedload('venda')).order_by(Treino.id)            
        if pagina:
            result = stmt.paginate(pagina, 20, False)
        else:
            result = stmt.all()
        return jsonify(por_pagina=result.per_page, total_items = result.total, pagina_atual=result.page, total_paginas=result.pages,items=TreinoSchema().dump(result.items,True))

    @login_required
    def listar(self):
        schema = TreinoSchema()
        lista = Treino().query.join(Treino.venda).filter(Venda.usuario_id == current_user.id, Treino.status == 'ativa').all()        
        return schema.jsonify(lista, True)
    
    @login_required
    def buscar(self, id):
        return TreinoSchema().jsonify(Treino.query.get(id))
    
    @admin_permission.require(http_exception=403)
    def admin_editar(self, data):
        with db.session.no_autoflush:
            schema = TreinoSchema().load(data, instance=Treino().query.get(data['id']), partial=True)        
            if schema.errors.__len__() > 0:
                return make_response(schema.errors[0], 500)        
            treino = schema.data
            treino.data_disponibilizado = date.today()
            treino.status = 'ativa'
            db.session.add(treino)
            db.session.commit()
            self.emailLiberacaoTreino(treino)
            return TreinoSchema().jsonify(treino)                

    def emailLiberacaoTreino(self, treino):
        try:
            msg = Message('Treino liberado.', recipients=[treino.venda.usuario.email])
            msg.html = render_template('app/emailTreinoLiberado.html', enviado='Treinos', email='jullianoVolpato@gmail.com' , treino=treino) 
            mail.send(msg)
            return make_response("E-mail enviado com sucesso", 200)
        except Exception:
            pass
            return make_response("Erro no envio do e-mail", 500)
