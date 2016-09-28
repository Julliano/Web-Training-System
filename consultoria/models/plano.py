# coding: utf-8
from flask_security import UserMixin

from ..models import BaseSchema
from ..modules import db, ma


class Plano(db.Model, UserMixin):
    __tablename__ = 'plano'    
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(45), nullable=False)  
    descricao = db.Column(db.String(45), nullable=False)  
    

class PlanoSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = Plano
    
    planos = ma.Nested("PlanoSchema", many=True)
