# coding: utf-8
from datetime import date

from marshmallow_sqlalchemy.convert import field_for

from ..models import BaseSchema
from ..modules import db, ma
from .resposta import Resposta


class Duvida(db.Model):
    __tablename__ = 'duvida'    
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(45), nullable=False)  
    descricao = db.Column(db.Text)  
    status = db.Column(db.String(45), default="pendente")  
    respostas = db.relationship("Resposta", cascade="save-update, merge, delete", backref="duvida")
    data = db.Column(db.Date, default=date.today)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)  
    treino_id = db.Column(db.Integer, db.ForeignKey("treino.id"))

class DuvidaSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = Duvida

    usuario_id = field_for(Duvida, 'usuario_id', dump_only=False)    
    usuario = ma.Nested("UsuarioSchema", dump_only=True, only=('id', 'nome_completo', 'email'))
    respostas = ma.Nested("RespostaSchema", many=True, exclude=('duvida_id',))
