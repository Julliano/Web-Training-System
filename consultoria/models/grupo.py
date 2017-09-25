# coding: utf-8
from flask.helpers import url_for
from marshmallow_sqlalchemy.convert import field_for

from ..modules import db, ma
from ..models import BaseSchema

class Grupo(db.Model):
    __tablename__ = "grupo"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(45), nullable=False)  
    info = db.Column(db.String(255))

        
    @property
    def url(self):
        return url_for('Grupo', id=self.id)
    
    @property
    def name(self):
        return self.nome
  
class GrupoSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = Grupo
    
    id = field_for(Grupo, 'id', dump_only=False)
#     grupos = ma.Nested(PrivilegioSchema, many=True)    
