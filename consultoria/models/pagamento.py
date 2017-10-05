# coding: utf-8
from datetime import date

from ..models import BaseSchema
from ..modules import db, ma


class Pagamento(db.Model):
    __tablename__ = 'pagamento'    
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(255), nullable=False)


class PagamentoSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = Pagamento