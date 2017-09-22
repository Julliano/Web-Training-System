# -*- coding: utf-8 -*-

from flask.globals import request, current_app
from flask.helpers import make_response

from models.treino import Treino
from modules import db


class AltereacaoStatusController():
    
    def status_operacao(self):        
        data = request.json
        operacao = Operacao.query.get(data['id'])
        operacao.status = data['status']
        db.session.add(operacao)
        db.session.commit()
        return make_response("", 200);
    
    def status_relatorio(self):
        data = request.json
        relatorio = Relatorio.query.get(data['id'])
        operacao = Operacao.query.get(data['idOp'])
        relatorio.status = data['status']
        db.session.add(relatorio)
        db.session.commit()
        self.checarStatus(operacao)
        return make_response("", 200)
    
    def checarStatus(self, operacao):
        count = 0
        for rel in operacao.relatorios:
            if(rel.status == 'ativa'):
                count += 1
        if(count == 0):
            operacao.status = 'pendente'
            db.session.add(operacao)
            db.session.commit()
        if(count > 0):
            operacao.status = 'ativa'
            db.session.add(operacao)
            db.session.commit()