# coding: utf-8
from datetime import date

from ..models import BaseSchema
from ..modules import db, ma
from .treino import Treino


class Plano(db.Model):
    __tablename__ = 'plano'    
    id = db.Column(db.Integer, primary_key=True)
    data_compra = db.Column(db.Date, default=date.today)
    titulo = db.Column(db.String(255), nullable=False)
    n_treinos = db.Column(db.Float)  
    valor = db.Column(db.Float)
    treinos = db.relationship("Treino", cascade="save-update, merge, delete", backref="plano")
    pagamento = db.Column(db.Boolean, nullable=True, default=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=True)
    formulario_id = db.Column(db.Integer, db.ForeignKey("formulario.id"), nullable=True)
    

class PlanoSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = Plano
    
    planos = ma.Nested("PlanoSchema", many=True)
