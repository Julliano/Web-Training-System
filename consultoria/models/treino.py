from datetime import date
from marshmallow import fields
from marshmallow.decorators import post_load, pre_load
from marshmallow_sqlalchemy.convert import field_for
from sqlalchemy.orm import relationship

from models import BaseSchema
from modules import db, ma
from duvida import Duvida

class Treino(db.Model):
    __tablename__ = "treino"
    id = db.Column(db.Integer, primary_key=True)
    plano_id = db.Column(db.Integer, db.ForeignKey("plano.id"), primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    data_entregue = db.Column(db.Date)
    status = db.Column(db.String(45), default="pendente")
    sessao = db.Column(db.String(1))
    explicacao = db.Column(db.Text)
    duvidas = db.relationship("Duvida", cascade="save-update, merge, delete", backref="usuario")
    modelo_id = db.Column(db.Integer, db.ForeignKey("modelo_treino.id"), nullable=False)
    
    
class TreinoSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = Treino
        
    proprietario = ma.Nested('ProprietarioSchema')
