# coding: utf-8
from flask_security import UserMixin

from ..models import BaseSchema
from ..modules import db, ma


class Duvida(db.Model, UserMixin):
    __tablename__ = 'duvida'    
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(45), nullable=False)  
    descricao = db.Column(db.String(45), nullable=False)  
    status = db.Column(db.String(45), default="pendente")  
    resposta = db.Column(db.String(45))
    data = db.Column(db.Date, nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)  

class DuvidaSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = Duvida
