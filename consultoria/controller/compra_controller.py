# coding: utf-8
from flask import jsonify
from flask.helpers import make_response
from flask_login import fresh_login_required, current_user, login_required

from ..models.venda import Venda, VendaSchema
from ..models.pagamento import Pagamento, PagamentoSchema
from ..models.treino import Treino, TreinoSchema
from ..models.plano import Plano, PlanoSchema
from ..models.pagamento import Pagamento, PagamentoSchema
from ..models.formulario import Formulario, FormularioSchema
from ..models.usuario import Usuario, UsuarioSchema
from ..modules import db, admin_permission


class CompraController:
    
#     @admin_permission.require(http_exception=403)
#     def logado(self, data): 
#         with db.session.no_autoflush:
#             jaExiste = Usuario().query.filter(Usuario.email == data['email']).first()
#             if jaExiste is not None:
#                 return make_response("Email já cadastrado, se esse email é seu, tente recuperar a senha.", 500)
#             usuario, errors= UsuarioSchema().load(data)
#             if errors.__len__() > 0 :
#                 return make_response("Dado de %s inválido" % usuario.errors[-1], 500)        
#             self.handle_grupos(usuario)  
#             usuario.grupo_id = usuario.grupos[0].id
#             db.session.add(usuario)
#             db.session.commit()
#             return make_response("Usuário adicionado com sucesso", 200)
        
    @login_required
    def planoMes(self):
        with db.session.no_autoflush:
            venda = Venda()
            venda.usuario_id = current_user.id
            venda.plano = Plano().query.filter(Plano.n_treinos == 1).first()
            venda.pagamento = Pagamento() #Incluir logica de pagamento;
            venda.formulario = Formulario()
            for treino in range(0,int(venda.plano.n_treinos)):
                treino = Treino()
                treino.sessao = '1/1'
                venda.treinos.append(treino)
            db.session.add(venda)
            db.session.commit()
            return make_response("Compra efetuada, assim que o pagamento for confirmado farei seu treino.", 200)

    @login_required
    def planoTri(self):
        pass
    
        
        
