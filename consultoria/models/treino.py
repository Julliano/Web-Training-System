from os import listdir
from os import path
from os.path import isfile, join

from flask.globals import current_app
from flask.helpers import send_from_directory, make_response
from marshmallow import fields
from marshmallow_sqlalchemy.convert import field_for
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import desc

from ..models import BaseSchema
from ..modules import db, ma
from .duvida import Duvida


class Treino(db.Model):
    __tablename__ = "treino"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255))
    data_entrega = db.Column(db.Date)
    data_disponibilizado = db.Column(db.Date)
    status = db.Column(db.String(45), default="pendente")
    sessao = db.Column(db.String(3))
    alteracao = db.Column(db.Text) 
    fisio = db.Column(db.Boolean, default=False)
    explicacao = db.Column(db.Text)
    ver = db.Column(db.String(45), nullable=True)
    duvidas = db.relationship("Duvida", cascade="save-update, merge, delete", backref="treino")
    venda_id = db.Column(db.Integer, db.ForeignKey("venda.id"), nullable=False)
    
    
    @property
    def url(self):
        return 'www.jullianovolpato.com.br/'

    @property
    def urlDescricao(self):
        return 'www.jullianovolpato.com.br/?#!/app/'+self.ver.__str__()

    @property
    def urldownload(self):
        caminho = path.join(current_app.config.get('MEDIA_ROOT'), str(self.venda.usuario.nome), str(self.id))
        if not path.exists(caminho):
            return make_response('Pasta ou arquivo inexistente.', 404)
        return send_from_directory(caminho, 'treino'+str(self.id)+'.pdf')
    
    @property
    def arquivos(self):
        caminho = path.join(current_app.config.get('MEDIA_ROOT'), 'Arquivos' ,str(self.venda_id))
        return [f for f in listdir(caminho) if isfile(join(caminho, f))]
    
class TreinoSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = Treino
        
    venda_id = field_for(Treino, 'venda_id', dump_only=False)    
    venda = ma.Nested("VendaSchema", dump_only=True)
