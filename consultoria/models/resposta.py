from datetime import date

from marshmallow_sqlalchemy.convert import field_for
from sqlalchemy.orm import relationship

from ..models import BaseSchema
from ..modules import db, ma


class Resposta(db.Model):
    __tablename__ = "resposta"
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.Text, nullable=False)
    data = db.Column(db.Date, default=date.today)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)
    duvida_id = db.Column(db.Integer, db.ForeignKey("duvida.id"), nullable=False)
    
    
class RespostaSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = Resposta
        
    usuario_id = field_for(Resposta, 'usuario_id', dump_only=False)
    usuario = ma.Nested("UsuarioSchema", dump_only=True, only=('id', 'nome_completo', 'email'))
    duvida_id = field_for(Resposta, 'duvida_id', dump_only=False)