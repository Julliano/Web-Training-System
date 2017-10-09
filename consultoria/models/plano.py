# coding: utf-8
from datetime import date

from ..models import BaseSchema
from ..modules import db, ma


class Plano(db.Model):
    __tablename__ = 'plano'    
    id = db.Column(db.Integer, primary_key=True)
    data_cadastro = db.Column(db.Date, default=date.today)
    titulo = db.Column(db.String(255), nullable=False)
    valor = db.Column(db.Float) 
    n_treinos = db.Column(db.Float) 
    

class PlanoSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = Plano
    
    planos = ma.Nested("PlanoSchema", many=True)
