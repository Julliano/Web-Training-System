from datetime import date

from marshmallow import fields
from marshmallow.decorators import post_load, pre_load
from marshmallow_sqlalchemy.convert import field_for
from sqlalchemy.orm import relationship

from ..models import BaseSchema
from ..modules import db, ma
from .proprietario import Proprietario

class Treino(db.Model):
    __tablename__ = "treino"
    id = db.Column(db.Integer, primary_key=True)
    plano_id = db.Column(db.Integer, db.ForeignKey("plano.id"), primary_key=True)
    plano = db.relationship("Plano")
    data_cadastro = db.Column(db.Date, default=date.today)
    status = db.Column(db.String(45), default="pendente")
    sessao = db.Column(db.String(45))
    
    
class TreinoSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = Treino
        
    proprietario = ma.Nested('ProprietarioSchema')
