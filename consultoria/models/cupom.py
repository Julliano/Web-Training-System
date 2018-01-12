# coding: utf-8
from datetime import date

from ..models import BaseSchema
from ..modules import db, ma

class Cupom(db.Model):
    __tablename__ = 'cupom'    
    id = db.Column(db.Integer, primary_key=True)
    cupom = db.Column(db.String(255))
    valor = db.Column(db.Float) 
    quantidade = db.Column(db.Integer) 
