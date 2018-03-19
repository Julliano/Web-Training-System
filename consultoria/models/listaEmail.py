from ..models import BaseSchema
from ..modules import db, ma


class Lista(db.Model):
    __tablename__ = 'lista'    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), nullable=False)
    validarEmail = db.Column(db.String(255), nullable=True)
    valido = db.Column(db.Boolean, default=False)
    emagrecimento = db.Column(db.Boolean, default=False)
    hipertrofia = db.Column(db.Boolean, default=False)


    @property
    def url(self):
        return 'www.jullianovolpato.com.br/?#!/ebookEmagrecimento?token='+self.validarEmail.__str__() 
    