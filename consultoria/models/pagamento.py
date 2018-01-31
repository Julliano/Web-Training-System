# coding: utf-8
from datetime import date

from ..models import BaseSchema
from ..modules import db, ma
from .venda import Venda


class Pagamento(db.Model):
    __tablename__ = 'pagamento'    
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(255), default="aguardando pagamento")
    codigo = db.Column(db.String(255))
    motivo = db.Column(db.String(55))
    cupom = db.Column(db.String(255))
    referencia = db.Column(db.String(255))
    vendas = db.relationship("Venda", cascade="save-update, merge, delete", backref="pagamento")


class PagamentoSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = Pagamento