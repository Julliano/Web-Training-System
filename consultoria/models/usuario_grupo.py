# -*- coding: utf-8 -*-
from modules import db

usuario_grupo = db.Table("usuario_grupo", db.metadata,
                                   db.Column("usuario_id", db.Integer, db.ForeignKey("usuario.id"), primary_key=True),
                                   db.Column("grupo_id", db.Integer, db.ForeignKey("grupo.id"), primary_key=True),
                                   db.UniqueConstraint("usuario_id", "grupo_id")
                                   )