# coding: utf-8
from datetime import date, timedelta

from flask import jsonify
from flask.helpers import make_response
from flask.globals import request, current_app
from flask_login import fresh_login_required, current_user, login_required

from ..models.formulario import Formulario, FormularioSchema
from ..models.pagamento import Pagamento, PagamentoSchema
from ..models.pagamento import Pagamento, PagamentoSchema
from ..models.plano import Plano, PlanoSchema
from ..models.treino import Treino, TreinoSchema
from ..models.usuario import Usuario, UsuarioSchema
from ..models.venda import Venda, VendaSchema
from ..modules import db, admin_permission


class CompraController:
    
    @login_required
    def planoMes(self):
        with db.session.no_autoflush:
            venda = Venda()
            venda.usuario_id = current_user.id
            venda.plano = Plano().query.filter(Plano.n_treinos == 1).first()
            venda.pagamento = Pagamento() #Incluir logica de pagamento;
            formulario , errors = FormularioSchema().loads(request.form['formulario'])
            formulario.preenchido = True
            venda.formulario = formulario
            for treino in range(0,int(venda.plano.n_treinos)):
                treino = Treino()
                treino.data_entrega = date.today() + timedelta(days=2) #mudar para ser preenchido na confirmação do pagamento.
                treino.sessao = '1/1'
                venda.treinos.append(treino)
            db.session.add(venda)
            db.session.commit()
            return make_response("Compra efetuada, assim que o pagamento for confirmado começarei a trabalhar no seu treino.", 200)

    @login_required
    def planoTri(self):
        with db.session.no_autoflush:
            venda = Venda()
            venda.usuario_id = current_user.id
            venda.plano = Plano().query.filter(Plano.n_treinos == 3).first()
            venda.pagamento = Pagamento() #Incluir logica de pagamento;
            venda.formulario = Formulario()
            for treino in range(0,int(venda.plano.n_treinos)):
                treino = Treino()
                treino.data_entrega = date.today + timedelta(days=2) #mudar para ser preenchido na confirmação do pagamento.
                treino.sessao = '1/1'
                venda.treinos.append(treino)
            db.session.add(venda)
            db.session.commit()
            return make_response("Compra efetuada, assim que o pagamento for confirmado farei seu treino.", 200)
    
