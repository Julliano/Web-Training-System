# coding: utf-8
from flask import jsonify
from flask_security.decorators import roles_accepted

from ..models.grupo import GrupoSchema, Grupo
from ..modules import db


class GrupoController():
    
    
    @roles_accepted('admin')
    def salvar(self,data):
        grupo, errors = GrupoSchema().load(data)        
        db.session.add(grupo)
        db.session.commit()
        return grupo        
    
    def editar(self,data):
        raise Exception('Não implementado')
    
    @roles_accepted('admin')
    def deletar(self,id):
        db.session.query.find(id=id).delete()
        db.session.commit()
        
    @roles_accepted('admin')
    def buscar(self,id):
        schema = GrupoSchema()
        grupo = Grupo().query.get(id)
        return schema.jsonify(grupo)
    
    @roles_accepted('admin')
    def listar(self):
        schema = GrupoSchema()
        grupos = db.session.query(Grupo).all()
        return schema.jsonify(grupos, True)
    