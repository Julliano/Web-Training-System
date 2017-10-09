from sqlalchemy.orm import relationship

from ..models import BaseSchema
from ..modules import db, ma
from .duvida import Duvida

class Treino(db.Model):
    __tablename__ = "treino"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    data_entrega = db.Column(db.Date)
    status = db.Column(db.String(45), default="pendente")
    sessao = db.Column(db.String(3))
    alteracao = db.Column(db.Text) 
    fisio = db.Column(db.Boolean, nullable=False, default=False)
    explicacao = db.Column(db.Text)
    duvidas = db.relationship("Duvida", cascade="save-update, merge, delete", backref="treino")
    venda_id = db.Column(db.Integer, db.ForeignKey("venda.id"), nullable=False)
    
    
class TreinoSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = Treino
