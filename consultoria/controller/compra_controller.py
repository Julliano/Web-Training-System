# coding: utf-8
from datetime import date, timedelta
import requests
import xmltodict

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
    
    def retornoPagSeguro(self):
        notificacao = request.json or request.form 
        url = 'https://ws.pagseguro.uol.com.br/v3/transactions/notifications/%s?email=jullianovosorio@gmail.com&token=1DF98935374845F2B18992B39A1B8B0F' % notificacao['notificationCode']
        header = {'Content-Type': 'application/xml; charset=ISO-8859-1'}
        response = requests.get(url, data=url, headers=header, verify=True, timeout=120)
        print('oi')
        print(response.content)
        if response.status_code == 200:
            resp = xmltodict.parse(response.content)
            status = resp['transaction']['status']
            referencia = resp['transaction']['reference']
            print(status)
            print(referencia)
            try:
                pagamento = Pagamento().query.filter(Pagamento.referencia == referencia).first()
                if int(status) == 1:
                    pagamento.status = 'Aguardando pagamento'
                if int(status) == 2:
                    pagamento.status = 'Em análise'
                if int(status) == 3:
                    pagamento.status = 'Paga'
                if int(status) == 4:
                    pagamento.status = 'Disponível'
                if int(status) == 5:
                    pagamento.status = 'Em disputa'
                if int(status) == 6:
                    pagamento.status = 'Devolvida'
                if int(status) == 7:
                    pagamento.status = 'Cancelada'
                if int(status) == 8:
                    pagamento.status = 'Debitado'
                if int(status) == 9:
                    pagamento.status = 'Retenção temporária'
                db.session.add(pagamento)
                db.session.commit()
            except Exception:
                pass
        return make_response("Pagamento atualizado", 200)
                
    
    @login_required
    def pagSeguro(self, venda):
        if venda.plano.n_treinos == 1:
            xml = """<?xml version="1.0"?> <checkout> <currency>BRL</currency> <items> <item> <id>01</id> <description>Plano de consultoria Mensal</description> <amount>%s0</amount> <quantity>1</quantity> </item> </items> <reference>Plano1%s</reference> <receiver> <email>jullianovosorio@gmail.com</email> </receiver> </checkout>""" % (float(venda.plano.valor), venda.pagamento.id)
            referencia = 'Plano1%s' % venda.pagamento.id
        elif venda.plano.n_treinos == 3:
            xml = """<?xml version="1.0"?> <checkout> <currency>BRL</currency> <items> <item> <id>01</id> <description>Plano de consultoria Trimestral</description> <amount>%s0</amount> <quantity>1</quantity> </item> </items> <reference>Plano3%s</reference> <receiver> <email>jullianovosorio@gmail.com</email> </receiver> </checkout>""" % (float(venda.plano.valor), venda.pagamento.id)
            referencia = 'Plano3%s' % venda.pagamento.id
#       substituir pelo token verdadeiro depois (está no sandBox)
#         url = 'https://ws.pagseguro.uol.com.br/v2/checkout?email=jullianovosorio@gmail.com&token=51E9D7E8918A4DB1B718EE9D017F4EFE'
        url = 'https://ws.sandbox.pagseguro.uol.com.br/v2/checkout?email=jullianovosorio@gmail.com&token=1DF98935374845F2B18992B39A1B8B0F'
        header = {'Content-Type': 'application/xml; charset=ISO-8859-1'}
        response = requests.post(url, data=xml, headers=header, verify=True, timeout=120)
        if response.status_code == 200:
            resp = xmltodict.parse(response.content)
            codigo = resp['checkout']['code']
#             urlPagamento = 'https://pagseguro.uol.com.br/v2/checkout/payment.html?code=%s' % codigo
            urlPagamento = 'https://sandbox.pagseguro.uol.com.br/v2/checkout/payment.html?code=%s' % codigo
        return [urlPagamento, codigo, referencia]
#         else:
#             return make_response("Erro na conexão com o PagSeguro, tente realizar o pagamento novamente mais tarde.", 500)
    
    @login_required
    def planoMes(self):
        with db.session.no_autoflush:
            venda = Venda()
            venda.usuario_id = current_user.id
            venda.plano = Plano().query.filter(Plano.n_treinos == 1).first()
            venda.pagamento = Pagamento() #Incluir logica de pagamento;
            formulario , errors = FormularioSchema().loads(request.form['formulario'])
            formulario.status = 'ativa'
            formulario.preenchido = True
            venda.formulario = formulario
            for treino in range(0,int(venda.plano.n_treinos)):
                treino = Treino()
                treino.data_entrega = date.today() + timedelta(days=2) #mudar para ser preenchido na confirmação do pagamento.
                treino.sessao = '1/1'
                venda.treinos.append(treino)
            db.session.add(venda)
            db.session.commit()
            resposta = self.pagSeguro(venda)
            venda.pagamento.codigo = resposta[1]
            venda.pagamento.referencia = resposta[2]
            db.session.add(venda)
            db.session.commit()
            return jsonify(resposta[0])

    @login_required
    def planoTri(self):
        with db.session.no_autoflush:
            venda = Venda()
            venda.usuario_id = current_user.id
            venda.plano = Plano().query.filter(Plano.n_treinos == 3).first()
            venda.pagamento = Pagamento() #Incluir logica de pagamento;
            venda.formulario = Formulario()
            for index in range(0,int(venda.plano.n_treinos)):
                treino = Treino()
                if index == 0:
                    treino.data_entrega = date.today() + timedelta(days=2) #mudar para ser preenchido na confirmação do pagamento.
                    treino.sessao = '1/3'
                if index == 1:
                    treino.data_entrega = date.today() + timedelta(days=32) #mudar para ser preenchido na confirmação do pagamento.
                    treino.sessao = '2/3'
                if index == 2:
                    treino.data_entrega = date.today() + timedelta(days=62) #mudar para ser preenchido na confirmação do pagamento.
                    treino.sessao = '3/3'
                venda.treinos.append(treino)
            db.session.add(venda)
            db.session.commit()
            return make_response("Compra efetuada, assim que o pagamento for confirmado farei seu treino.", 200)
    
