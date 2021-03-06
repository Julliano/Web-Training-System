# coding: utf-8
from datetime import date, timedelta
from os import path, makedirs

from flask import jsonify
from flask.globals import request, current_app
from flask.helpers import make_response
from flask.templating import render_template
from flask_login import fresh_login_required, current_user, login_required
from flask_mail import Message
import requests
from werkzeug.utils import secure_filename
import xmltodict

from consultoria.modules import mail

from ..models.cupom import Cupom
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
        url = 'https://ws.sandbox.pagseguro.uol.com.br/v3/transactions/notifications/%s' % notificacao['notificationCode']
        parametros = {'email':'sample@gmail.com', 'token':"1DF98935374845F2B18992B39A1B8B0F"}
        response = requests.get(url, params=parametros, verify=True, timeout=120)
        venda = None
        if response.status_code == 200:
            resp = xmltodict.parse(response.content)
            status = resp['transaction']['status']
            referencia = resp['transaction']['reference']
            pagamento = Pagamento().query.filter(Pagamento.referencia == referencia).first()
            if int(status) == 1:
                pagamento.status = 'Aguardando pagamento'
            if int(status) == 2:
                pagamento.status = 'Em análise'
            if int(status) == 3:
                pagamento.status = 'Paga'
                venda = Venda().query.filter(Venda.pagamento_id == pagamento.id).first()
                usu = Usuario().query.get(venda.usuario_id)
            if int(status) == 4:
            	pagamento.status = 'Paga'
                #pagamento.status = 'Disponível'
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
            if venda is not None:
                count = 0
                ultimaData = None
                if usu.ultimoTreino:
                    if usu.ultimoTreino.data_entrega is not None:
                        ultimaData = usu.ultimoTreino.data_entrega
                        if date.today() > ultimaData:
                            ultimaData = None  
                if ultimaData is not None:
                    for treino in venda.treinos:
                        treino.data_entrega = ultimaData + timedelta(days=(count*30)+30)
                        count += 1
                else:
                    for treino in venda.treinos:
                        if count == 0:
                            treino.data_entrega = date.today() + timedelta(2)
                        else:
                            treino.data_entrega = date.today() + timedelta(days=(count*30))
                        count += 1
                db.session.add(venda)
                db.session.commit()
            else:
                return make_response("Status" + pagamento.status, 200)
            return make_response("Pagamento atualizado", 200)
        return make_response("Erro no codigo 200", 500)
                
    
    @login_required
    def pagSeguro(self, venda, cupom):
        if cupom is not None:
            desconto = cupom.valor
            cupomUsado = cupom.cupom
        else:
            desconto = 0
            cupomUsado = None
        if venda.plano.n_treinos == 1:
            xml = """<?xml version="1.0"?> <checkout> <currency>BRL</currency> <items> <item> <id>01</id> <description>Plano de consultoria Mensal</description> <amount>%s0</amount> <quantity>1</quantity> </item> </items> <reference>Plano1%s</reference> <receiver> <email>jullianovosorio@gmail.com</email> </receiver> </checkout>""" % (float(venda.plano.valor) - desconto, venda.pagamento.id)
            referencia = 'Plano1%s' % venda.pagamento.id
        elif venda.plano.n_treinos == 3:
            xml = """<?xml version="1.0"?> <checkout> <currency>BRL</currency> <items> <item> <id>01</id> <description>Plano de consultoria Trimestral</description> <amount>%s0</amount> <quantity>1</quantity> </item> </items> <reference>Plano3%s</reference> <receiver> <email>jullianovosorio@gmail.com</email> </receiver> </checkout>""" % (float(venda.plano.valor) - desconto, venda.pagamento.id)
            referencia = 'Plano3%s' % venda.pagamento.id
        url = 'https://ws.pagseguro.uol.com.br/v2/checkout?email=jullianovosorio@gmail.com&token=51E9D7E8918A4DB1B718EE9D017F4EFE'
#         url = 'https://ws.sandbox.pagseguro.uol.com.br/v2/checkout?email=jullianovosorio@gmail.com&token=1DF98935374845F2B18992B39A1B8B0F'
        header = {'Content-Type': 'application/xml; charset=ISO-8859-1'}
        response = requests.post(url, data=xml, headers=header, verify=True, timeout=120)
        if response.status_code == 200:
            resp = xmltodict.parse(response.content)
            codigo = resp['checkout']['code']
            urlPagamento = 'https://pagseguro.uol.com.br/v2/checkout/payment.html?code=%s' % codigo
#             urlPagamento = 'https://sandbox.pagseguro.uol.com.br/v2/checkout/payment.html?code=%s' % codigo
        return [urlPagamento, codigo, referencia, cupomUsado]
    
    @login_required
    def planoMes(self):
        with db.session.no_autoflush:
            venda = Venda()
            venda.usuario_id = current_user.id
            venda.plano = Plano().query.filter(Plano.n_treinos == 1).first()
            venda.pagamento = Pagamento()
            formulario , errors = FormularioSchema().loads(request.form['formulario'])
            formulario.status = 'ativa'
            formulario.preenchido = True
            if 'dietaFile' in request.files:
                formulario.dietaFile = request.files['dietaFile']
            else:
                formulario.dietaFile = None
            venda.formulario = formulario
            for treino in range(0,int(venda.plano.n_treinos)):
                treino = Treino()
                treino.sessao = '1/1'
                venda.treinos.append(treino)
            db.session.add(venda)
            db.session.commit()
            if formulario.dietaFile:
                caminho = path.join(current_app.config.get('MEDIA_ROOT'), 'Arquivos' ,str(venda.id))
                if not path.exists(caminho):
                    makedirs(caminho)
                formulario.dietaFile.save(path.join(caminho, secure_filename(formulario.dietaFile.filename)))
            try:
                cupom = Cupom().query.filter(Cupom.cupom == formulario.cupom.upper(), Cupom.plano == 1).first()
            except:
                cupom = None
            if cupom is not None:
                if cupom.quantidade > 0:
                    cupom.quantidade -=1;
                    db.session.add(cupom)
                    db.session.commit()
                    resposta = self.pagSeguro(venda, cupom)
                else:
                    resposta = self.pagSeguro(venda, None)
            else:
                resposta = self.pagSeguro(venda, None)
            venda.pagamento.codigo = resposta[1]
            venda.pagamento.referencia = resposta[2]
            venda.pagamento.cupom = resposta[3]
            venda.pagamento.motivo = formulario.motivo
            db.session.add(venda)
            db.session.commit()
            self.emailCompraFinalizada(venda)
            return jsonify(resposta[0])

    @login_required
    def planoTri(self):
        with db.session.no_autoflush:
            venda = Venda()
            venda.usuario_id = current_user.id
            venda.plano = Plano().query.filter(Plano.n_treinos == 3).first()
            venda.pagamento = Pagamento() #Incluir logica de pagamento;
            formulario , errors = FormularioSchema().loads(request.form['formulario'])
            formulario.status = 'ativa'
            formulario.preenchido = True
            venda.formulario = formulario
            if 'dietaFile' in request.files:
                formulario.dietaFile = request.files['dietaFile']
            else:
                formulario.dietaFile = None
            for index in range(0,int(venda.plano.n_treinos)):
                treino = Treino()
                if index == 0:
                    treino.sessao = '1/3'
                if index == 1:
                    treino.sessao = '2/3'
                if index == 2:
                    treino.sessao = '3/3'
                venda.treinos.append(treino)
            db.session.add(venda)
            db.session.commit()
            if formulario.dietaFile:
                caminho = path.join(current_app.config.get('MEDIA_ROOT'), 'Arquivos' ,str(venda.id))
                if not path.exists(caminho):
                    makedirs(caminho)
                formulario.dietaFile.save(path.join(caminho, secure_filename(formulario.dietaFile.filename)))
            try:
                cupom = Cupom().query.filter(Cupom.cupom == formulario.cupom.upper(), Cupom.plano == 3).first()
            except:
                cupom = None
            if cupom is not None:
                if cupom.quantidade > 0:
                    cupom.quantidade -=1
                    db.session.add(cupom)
                    db.session.commit()
                    resposta = self.pagSeguro(venda, cupom)
                else:
                    resposta = self.pagSeguro(venda, None)
            else:
                resposta = self.pagSeguro(venda, None)
            venda.pagamento.codigo = resposta[1]
            venda.pagamento.referencia = resposta[2]
            venda.pagamento.cupom = resposta[3]
            venda.pagamento.motivo = formulario.motivo
            db.session.add(venda)
            db.session.commit()
            self.emailCompraFinalizada(venda)
            return jsonify(resposta[0])
        
    def emailCompraFinalizada(self, venda):
        try:
            msg = Message('Solicitação de plano.', recipients=[venda.usuario.email])
            msg.html = render_template('app/emailConfirmacaoCompra.html', enviado='Plano', email='jullianoVolpato@gmail.com' , venda=venda) 
            mail.send(msg)
            return make_response("E-mail enviado com sucesso", 200)
        except Exception:
            pass
            return make_response("Erro no envio do e-mail", 500)
    
