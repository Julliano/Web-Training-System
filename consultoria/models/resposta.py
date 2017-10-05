from sqlalchemy.orm import relationship

from ..models import BaseSchema
from ..modules import db, ma

class Resposta(db.Model):
    __tablename__ = "resposta"
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(45), nullable=False)  
    data = db.Column(db.Date, nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)
    
    
class RespostaSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = Resposta
