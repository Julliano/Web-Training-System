from marshmallow import fields
from marshmallow.decorators import post_load
from marshmallow_sqlalchemy import ModelSchema, ModelConverter

from modules import db, ma

    
class BaseSchema(ma.ModelSchema):    
    class Meta:
        sqla_session = db.session    
    
