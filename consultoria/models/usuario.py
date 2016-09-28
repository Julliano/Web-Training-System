# coding: utf-8
from flask.helpers import url_for
from flask_login import make_secure_token
from flask_security import UserMixin
from flask_security.utils import encrypt_password, verify_password
from marshmallow import fields
from marshmallow.decorators import pre_load
from sqlalchemy import DateTime

from ..models import BaseSchema
from ..modules import db, ma
from .plano import Plano
from .grupo import Grupo
from .usuario_grupo import usuario_grupo
from .consultoria.modules import admin_permission


class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuario'    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(45), nullable=False)  
    nascimento = db.Column(db.Date, nullable=False)
    altura = db.Column(db.String(45), nullable=False)
    sexo = db.Column(db.Boolean, nullable=False, default=False)
    cpf = db.Column(db.String(45))
    email = db.Column(db.String(60), nullable=False, unique=True)
    endereco = db.Column(db.String(155), nullable=False)
    complemento = db.Column(db.String(155), nullable=False)
    cep = db.Column(db.String(45), nullable=False)
    bairro = db.Column(db.String(45), nullable=False)
    cidade = db.Column(db.String(45), nullable=False)
    estado = db.Column(db.String(45), nullable=False)
    senha = db.Column(db.String(130), nullable=False)
    logado = db.Column(db.Boolean, nullable=False, default=False)
    duvidas = db.relationship("Duvida", cascade="save-update, merge, delete", backref="usuario")
    formulario_id = db.Column(db.Integer, db.ForeignKey("formulario.id"), nullable=False)

    # Flask-Security SECURITY_TRACKABLE
    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    login_count = db.Column(db.Integer)
    # Why 45 characters for IP Address ?
    # See http://stackoverflow.com/questions/166132/maximum-length-of-the-textual-representation-of-an-ipv6-address/166157#166157
    last_login_ip = db.Column(db.String(45))    
    current_login_ip = db.Column(db.String(45))
    
    #Relationships   
    grupos = db.relationship("Grupo",
                               secondary="usuario_grupo",
                               backref=db.backref("usuarios")                               
                               )
        
        
    def __repr__(self):
        return "<Usuario(nome=%s)>" % self.nome
    
    @property
    def url(self):
        return url_for('.usuarios', id=self.id)
    
    @property
    def roles(self):
        return self.grupos
    
    @property
    def is_authenticated(self):        
        return self.logado;
    
    @property
    def is_anonymous(self):
        return False
    
    @property
    def nome_completo(self):
        return self.nome + " " + self.sobrenome

    @property
    def password(self):
        return self.senha
    
    #===========================================================================
    # def get_auth_token(self):
    #     print make_secure_token(str(self.id), self.senha)
    #     return make_secure_token(str(self.id), self.senha)
    #===========================================================================

    def is_active(self):
        """Returns `True` if the user is active."""
        return True
    
    def is_correct_passwd(self, senha):
        return self.senha == senha    
    
    def is_correct_crypt_passwd(self, senha):
        return verify_password(senha, self.senha)
    
    def hash_pass(self, password):
        return encrypt_password(password)
    
class UsuarioSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = Usuario
        load_only = ("senha",)
    
    @pre_load
    def pre_load(self, data):
        if 'senha' in data:
            data['senha'] = encrypt_password(data['senha'])
        if 'email' in data:
            data['email'] = data['email'].lower()            
    
    grupos = ma.Nested("GrupoSchema", many=True)
    is_admin = fields.Method("is_admin", dump_only=True)
    
    def is_admin(self, data):
        return admin_permission.can()        

