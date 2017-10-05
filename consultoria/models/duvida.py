# coding: utf-8
from ..models import BaseSchema
from ..modules import db, ma
from .resposta import Resposta

class Duvida(db.Model):
    __tablename__ = 'duvida'    
#     __table_args__ = {'extend_existing': True} 
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(45), nullable=False)  
    descricao = db.Column(db.String(45), nullable=False)  
    status = db.Column(db.String(45), default="pendente")  
    respostas = db.relationship("Resposta", cascade="save-update, merge, delete", backref="duvida")
    data = db.Column(db.Date, nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)  
    treino_id = db.Column(db.Integer, db.ForeignKey("treino.id"))

class DuvidaSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = Duvida
