# coding: utf-8
from flask.json import jsonify
from flask_login import login_user, logout_user, current_user


from ..models.usuario import Usuario
from ..modules import db 


class SessionController:
      
    def login(self, data):
        try:
            usuario = Usuario.query.filter_by(email=data['email']).first_or_404()
            if usuario.is_correct_passwd(data['senha']) or usuario.is_correct_crypt_passwd(data['senha']):
                usuario.logado = True
                db.session.add(usuario)
                db.session.commit()
                login_user(usuario, remember=data['lembrar'])
                return jsonify(auth=True)            
            return jsonify(auth=False, message="Usuário ou senha inválidos")
        except KeyError as e:
            print e
            return jsonify(auth=False, message="Usuário ou senha inválidos")
        except Exception as e:
            print e
            return jsonify(auth=False, message="Usuário ou senha inválidos")
    
    @staticmethod
    def logout():
        usuario = current_user
        usuario.logado = False
        db.session.add(usuario)
        db.session.commit()
        logout_user()        
        return "Logout success"
    
