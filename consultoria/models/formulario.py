# coding: utf-8
from datetime import date

from ..models import BaseSchema
from ..modules import db, ma
from sqlalchemy.types import ARRAY
from .venda import Venda

class Formulario(db.Model):
    __tablename__ = 'formulario'    
    id = db.Column(db.Integer, primary_key=True)
    data_cadastro = db.Column(db.Date, default=date.today)
    data_entrega = db.Column(db.Date, default=date.today)
    status = db.Column(db.String(45), default="pendente")
    peso = db.Column(db.String(15))
    ajuste = db.Column(db.String(255))
    bf = db.Column(db.String(15))
    cardapio = db.Column(db.Text)
    disponibilidade = db.Column(db.ARRAY(db.String), default=[])
    extra = db.Column(db.Boolean, nullable=False, default=False)
    extra_disponibilidade = db.Column(db.ARRAY(db.String), default=[])
    extra_descricao = db.Column(db.Text)
    treinando = db.Column(db.Boolean, nullable=False, default=False)
    experiencia = db.Column(db.String(25))
    fumante = db.Column(db.Boolean, nullable=False, default=False)
    bebe = db.Column(db.Boolean, nullable=False, default=False)
    preenchido = db.Column(db.Boolean, default=False)
    bebe_frequencia = db.Column(db.String(25))
    cupom = db.Column(db.String(55))
    motivo = db.Column(db.String(55))
    melhorTreino = db.Column(db.Text)
    exerGosta = db.Column(db.Text)
    exerOdeia = db.Column(db.Text)
    aerobico = db.Column(db.Boolean, nullable=False, default=False)
    aerobicoPreferido = db.Column(db.String(25))
    patologia = db.Column(db.Text)
    articulacao = db.Column(db.Text)
    ultimoTreino = db.Column(db.Text)
    objetivo = db.Column(db.Text)
    obs = db.Column(db.Text)
    vendas = db.relationship("Venda", cascade="save-update, merge, delete", backref="formulario")
    
class FormularioSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = Formulario
