from marshmallow_sqlalchemy.convert import field_for
from sqlalchemy.orm import relationship

from ..models import BaseSchema
from ..modules import db, ma
from .duvida import Duvida


class Treino(db.Model):
    __tablename__ = "treino"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255))
    data_entrega = db.Column(db.Date)
    data_disponibilizado = db.Column(db.Date)
    status = db.Column(db.String(45), default="pendente")
    sessao = db.Column(db.String(3))
    alteracao = db.Column(db.Text) 
    fisio = db.Column(db.Boolean, default=False)
    explicacao = db.Column(db.Text)
    duvidas = db.relationship("Duvida", cascade="save-update, merge, delete", backref="treino")
    venda_id = db.Column(db.Integer, db.ForeignKey("venda.id"), nullable=False)
    
    
    
    @property
    def url(self):
        return 'www.jullianovolpato.com.br/?#!/app/treino/'+self.id.__str__()
    
class TreinoSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = Treino
        
    venda_id = field_for(Treino, 'venda_id', dump_only=False)    
    venda = ma.Nested("VendaSchema", dump_only=True)
