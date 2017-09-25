# coding: utf-8
from datetime import date

from ..models import BaseSchema
from ..modules import db, ma


class ModeloTreino(db.Model):
    __tablename__ = 'modelo_treino'    
    id = db.Column(db.Integer, primary_key=True)
    data_cadastro = db.Column(db.Date, default=date.today)
    titulo = db.Column(db.String(255), nullable=False)
    explicacao = db.Column(db.Text)  


class ModeloTreinoSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = ModeloTreino