from ..modules import db

grupo_privilegio = db.Table("grupo_privilegio", db.metadata,
                                   db.Column("grupo_id", db.Integer, db.ForeignKey("grupo.id"), primary_key=True),
                                   db.Column("privilegio_id", db.Integer, db.ForeignKey("privilegio.id"), primary_key=True),
                                   db.UniqueConstraint("grupo_id", "privilegio_id")
                                   )