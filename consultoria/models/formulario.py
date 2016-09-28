# coding: utf-8
from datetime import date
from flask_security import UserMixin

from ..models import BaseSchema
from ..modules import db, ma


class Formulario(db.Model, UserMixin):
    __tablename__ = 'formulario'    
    id = db.Column(db.Integer, primary_key=True)
    data_cadastro = db.Column(db.Date, default=date.today)
    status = db.Column(db.String(45), default="pendente")
    peso = db.Column(db.Float)
    gordura_corporal = db.Column(db.Float)
    disponibilidade = db.Column(db.ARRAY(db.String))
    experiencia = db.Column(db.String(25))
    fumante = db.Column(db.Boolean, nullable=False, default=False)
    bebe = db.Column(db.Boolean, nullable=False, default=False)
    bebe_frequencia = db.Column(db.String(25))
    melhorTreino = db.Column(db.Text)
    exerGosta = db.Column(db.Text)
    exerOdeia = db.Column(db.Text)
    aerobico = db.Column(db.Boolean, nullable=False, default=False)
    aerobicoPreferido = db.Column(db.String(25))
    alimentacao = db.Column(db.Text)
    objetivo = db.Column(db.Text)
    articulacao = db.Column(db.Text)
    patologia = db.Column(db.Text)
    ultimoTreino = db.Column(db.Text)
    
class FormularioSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = Formulario
