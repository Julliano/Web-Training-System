# -*- coding: utf-8 -*-

from flask.globals import request, current_app
from flask.helpers import make_response

from models.plano import Plano
from models.treino import Treino
from modules import db


class AltereacaoStatusController():
    
    def status_relatorio(self):
        data = request.json
        treino = Treino.query.get(data['id'])
        plano = Plano.query.get(data['idOp'])
        treino.status = data['status']
        db.session.add(treino)
        db.session.commit()
        self.checarStatus(plano)
        return make_response("", 200)
