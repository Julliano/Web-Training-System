# coding: utf-8
from datetime import date

from ..models import BaseSchema
from ..modules import db, ma
from .treino import Treino


class Venda(db.Model):
    __tablename__ = 'venda'    
    id = db.Column(db.Integer, primary_key=True)
    data_compra = db.Column(db.Date, default=date.today)
    pagamento_id = db.Column(db.Integer, db.ForeignKey("pagamento.id"), nullable=True)
    plano_id = db.Column(db.Integer, db.ForeignKey("plano.id"), nullable=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=True)
    formulario_id = db.Column(db.Integer, db.ForeignKey("formulario.id"), nullable=True)
    treinos = db.relationship("Treino", cascade="save-update, merge, delete", backref="plano")
    

class VendaSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = Venda
    
    vendas = ma.Nested("VendaSchema", many=True)
    plano = ma.Nested("PlanoSchema", dump_only=True)
    usuario = ma.Nested("UsuarioShchema", dump_only=True)
    formulario = ma.Nested("FormularioShchema", dump_only=True)
    pagamento = ma.Nested("PagamentoShchema", dump_only=True)
