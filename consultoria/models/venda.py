# coding: utf-8
from datetime import date

from ..models import BaseSchema
from ..modules import db, ma
from .treino import Treino


class Venda(db.Model):
    __tablename__ = 'venda'    
    id = db.Column(db.Integer, primary_key=True)
    data_compra = db.Column(db.Date, default=date.today)
    pagamento_id = db.Column(db.Integer, db.ForeignKey("pagamento.id"), nullable=True)
    plano_id = db.Column(db.Integer, db.ForeignKey("plano.id"), nullable=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=True)
    formulario_id = db.Column(db.Integer, db.ForeignKey("formulario.id"), nullable=True)
    treinos = db.relationship("Treino", cascade="save-update, merge, delete", backref="plano")
    

class PlanoSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = Plano
    
    planos = ma.Nested("PlanoSchema", many=True)
