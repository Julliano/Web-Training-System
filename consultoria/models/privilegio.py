from ..models import BaseSchema
from ..modules import db, ma


class Privilegio(db.Model):
    __tablename__ = "privilegio"
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(45), nullable=False)  
    info = db.Column(db.String(255))
    
    def __init__(self):
        pass
    
class PrivilegioSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = Privilegio       
    