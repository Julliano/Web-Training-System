# coding: utf-8
from datetime import date
from os import listdir
from os import path, makedirs
from os.path import isfile, join

from flask import jsonify
from flask.globals import request, current_app
from flask.helpers import make_response, send_from_directory
from flask.json import dumps
from flask.templating import render_template
from flask_login import fresh_login_required, current_user, login_required
from flask_mail import Message
from flask_security.decorators import roles_required
import pdfkit
from sqlalchemy.orm import joinedload, contains_eager
from sqlalchemy.sql.elements import and_
from werkzeug.utils import secure_filename

from consultoria.models.formulario import Formulario
from consultoria.models.pagamento import Pagamento
from consultoria.models.treino import Treino, TreinoSchema
from consultoria.models.usuario import Usuario
from consultoria.models.venda import Venda, VendaSchema
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
    def listar_admin(self, pagina=1, status='pendente'):
        and_form = and_(Formulario.status == 'ativa')
        if request.args:
            if request.args.get('pagina'):
                pagina = int(dict(request.args).get('pagina')[0])
            if request.args.get('status'):
                status = dict(request.args).get('status')[0]
        stmt = Treino.query.options(joinedload('venda')).order_by(Treino.data_entrega.asc()).join(Treino.venda).join(Venda.formulario).join(Venda.pagamento).filter(Pagamento.status == 'Paga', Formulario.status == "ativa", Treino.status == status)        
        if pagina:
            result = stmt.paginate(pagina, 15, False)
        else:
            result = stmt.all()
        return jsonify(por_pagina=result.per_page, total_items = result.total, pagina_atual=result.page, total_paginas=result.pages,items=TreinoSchema().dump(result.items,True))

    @login_required
    def listar(self):
        schema = TreinoSchema()
        lista = Treino().query.join(Treino.venda).filter(Venda.usuario_id == current_user.id, Treino.status == 'ativa').all()        
        return schema.jsonify(lista, True)
    
    @login_required
    def arquivos(self, data):
        venda = Venda().query.get(data)
        caminho = path.join(current_app.config.get('MEDIA_ROOT'), 'Arquivos' ,str(venda.id))
        return dumps(listdir(caminho))

    @login_required
    def downloadArquivo(self):
        data = request.form
        caminho = path.join(current_app.config.get('MEDIA_ROOT'), 'Arquivos' ,request.form['id'])
        return send_from_directory(caminho, request.form['nome'])
    
    @login_required
    def downloadTreino(self, id):
        treino = Treino().query.get(id)
        if treino is not None:
            caminho = path.join(current_app.config.get('MEDIA_ROOT'), str(secure_filename(treino.venda.usuario.nome)), str(treino.id))
            if not path.exists(caminho):
                return make_response('Pasta ou arquivo inexistente.', 404)
            return send_from_directory(caminho, 'treino'+str(id)+'.pdf')
        else:
            return make_response('Treino não encontrado.', 404)

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
            caminho = path.join(current_app.config.get('MEDIA_ROOT'), str(secure_filename(treino.venda.usuario.nome)), str(treino.id))
            if not path.exists(caminho):
                makedirs(caminho)
#             config = r'/usr/local/bin/wkhtmltopdf'
            config = r'C:\Python27\wkhtmltopdf\bin\wkhtmltopdf.exe'
            config = pdfkit.configuration(wkhtmltopdf=config)
            pdfkit.from_string('<meta http-equiv="Content-type" content="text/html; charset=utf-8" />'+treino.explicacao, path.join(caminho, 'treino'+str(treino.id)+'.pdf'), configuration=config)
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
