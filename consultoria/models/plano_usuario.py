from datetime import date

from marshmallow import fields
from marshmallow_sqlalchemy.convert import field_for
from sqlalchemy.orm import relationship

from . import BaseSchema
from ..modules import db, ma
from .plano import Plano, PlanoSchema

class PlanoUsuario(db.Model):
    __tablename__ = "plano_usuario"
    id = db.Column(db.Integer, primary_key=True)
    plano_id = db.Column(db.Integer, db.ForeignKey("plano.id"), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)
    status_plano = db.Column(db.Boolean, nullable=False, default=False)
    status_pagamento = db.Column(db.Boolean, nullable=False, default=False)
    plano = db.relationship("Plano")
    treinos = db.relationship("Treino", backref="PlanoUsuario", cascade="all, delete-orphan")
    
    
class PlanoUsuarioSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = PlanoUsuario

    plano = ma.Nested('PlanoSchema')
