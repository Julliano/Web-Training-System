from geoalchemy2.types import Geometry
from marshmallow import fields
from marshmallow.decorators import post_load
from marshmallow_sqlalchemy import ModelSchema, ModelConverter

from ..modules import db, ma


class GEOAlchemyUtilsConverter(ModelConverter):
    SQLA_TYPE_MAPPING = dict(
        list(ModelConverter.SQLA_TYPE_MAPPING.items()) +
        [(Geometry, fields.Str)]
    )
    
class BaseSchema(ma.ModelSchema):    
    class Meta:
        sqla_session = db.session    
        model_converter = GEOAlchemyUtilsConverter
    
