# coding: utf-8
from models import BaseSchema
from modules import db, ma

class Profissional(db.Model):
    __tablename__ = 'profissional'    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)  
    sobrenome = db.Column(db.String(50), nullable=False)  
    email = db.Column(db.String(60), nullable=False, unique=True)
        
    def __repr__(self):
        return "<Usuario(nome=%s)>" % self.nome
    
    @property
    def nome_completo(self):
        return self.nome + " " + self.sobrenome

class ProfissionalSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = Profissional
