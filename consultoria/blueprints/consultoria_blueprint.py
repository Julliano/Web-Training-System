# coding: utf-8
import ast
from os import path
import traceback

from flask.blueprints import Blueprint
from flask.globals import current_app, request, session
from flask.helpers import send_from_directory, make_response
from flask.json import jsonify
from flask.templating import render_template
from flask_login import logout_user, current_user
from flask_mail import Message
from flask_security import login_required
from sqlalchemy.sql.functions import func
from werkzeug import redirect

from consultoria.controller.modelo_controller import ModeloTreinoController
from consultoria.controller.treino_controller import TreinoController
from consultoria.modules import mail

from ..controller.compra_controller import CompraController
from ..controller.duvidas_controller import DuvidasController
from ..controller.formulario_controller import FormularioController
from ..controller.grupo_controller import GrupoController
from ..controller.plano_controller import PlanoController
from ..controller.session_controller import SessionController
from ..controller.usuario_controller import UsuarioController
from ..models.duvida import Duvida
from ..models.formulario import Formulario
from ..models.grupo import Grupo
from ..models.modelo import ModeloTreino
from ..models.pagamento import Pagamento
from ..models.plano import Plano
from ..models.resposta import Resposta
from ..models.treino import Treino
from ..models.usuario import Usuario, UsuarioSchema
from ..models.venda import Venda
from ..modules import login_manager, db, admin_permission


consultoria_app = Blueprint('consultoria_app', __name__)


def crud_request(controller, id):
    try:
        if request.method == "POST":
            return controller.salvar(request.json or request.form)
        if request.method == "PUT":        
            return controller.editar(request.json or request.form)
        if request.method == "DELETE":
            return controller.deletar(id)
        if id:
            return controller.buscar(id)
        return controller.listar()
    except Exception as error:
        print "="*50
        print traceback.print_exc()
        print "="*50
        return make_response("Desculpe, ocorreu um erro no servidor, por favor comunique o administrador do sistema", 500)

@login_manager.needs_refresh_handler
def refresh():    
    return redirect('/#/index/signin')

@login_manager.user_loader
def load_user(user_id):
    usuario = Usuario().query.get(int(user_id))
    return usuario or None   

@consultoria_app.errorhandler(403)
@login_manager.unauthorized_handler
def unauthorized(arg=None):
    return make_response("Permissão negada", 401)


@consultoria_app.route('/', methods=['GET', 'POST'])
def hello_user(): 
    return render_template('index.html')

# @consultoria_app.route('/pdf/<int:id>', methods=['GET','POST'])
# def get_pdf(id): 
#     if request.method == "POST":
#         return RelatorioController().upload_pdf(id)
#     return RelatorioController().get_pdf(id)    
    
@consultoria_app.route('/loged')
def loged():   
    uSchema = UsuarioSchema()
    return jsonify(usuario=uSchema.dump(current_user).data)

@consultoria_app.route('/check_session/')
def check_session():       
    uSchema = UsuarioSchema()
    return jsonify(usuario=uSchema.dump(current_user).data, lembrar=session['remember'])

@consultoria_app.route('/media/<path:filename>')
def media(filename):
    return send_from_directory(current_app.config.get('MEDIA_ROOT'), filename)

@consultoria_app.route('/app/<path:filename>')
@login_required
def templates_app(filename):      
    return send_from_directory(path.join(current_app.jinja_loader.searchpath[0], "app"), filename)

@consultoria_app.route('/templates/<path:filename>')
def templates_directive(filename):
    return render_template(filename, admin = admin_permission.can())

@consultoria_app.route('/login', methods=['GET', 'POST'])
def login():
    controller = SessionController()
    if request.method == "POST":        
        return controller.login(request.json)
    return redirect('/#/index/signin')
    
@consultoria_app.route('/logout')
@login_required
def logout():
    usuario = current_user
    usuario.logado = False
    db.session.add(usuario)
    db.session.commit()
    logout_user()        
    return "Logout success"

@consultoria_app.route('/cadastroNovoUsuario/', methods=["POST", "PUT"])
def cadastroNovoUsuario(id=None):
    if request.method == "POST":
        return UsuarioController().salvar(request.json or request.form)
    if request.method == "PUT":
        return UsuarioController().mudarSenha(request.json or request.form)

@consultoria_app.route('/resetarSenha/', methods=["PUT"])
def resetarSenha(id=None):
    if request.method == "PUT":
        return UsuarioController().resetarSenha(request.json or request.form)

@consultoria_app.route('/emailContato/', methods=["POST"])
def emailContato(id=None):
    if request.method == "POST":
        try:
            msg = Message('Email de contato', recipients=["jullianoVolpato@gmail.com"])
            msg.html = render_template('app/emailContato.html', enviado='formulario', email='jullianoVolpato@gmail.com' , form=request.json) 
            mail.send(msg)
            return make_response("E-mail enviado com sucesso", 200)
        except Exception:
            return make_response("Erro no envio do e-mail", 500)

@consultoria_app.route('/emailRecuperacao/', methods=["POST"])
def emailRecuperacao(id=None):
    if request.method == "POST":
        return UsuarioController().emailRecuperacao(request.json or request.form)

@consultoria_app.route('/formulariosUltimo/<int:id>', methods=["GET"])
@login_required
def formulariosUltimo(id=None):
    return FormularioController().buscarUltimo(id)

@consultoria_app.route('/formularios/', methods=['GET', "POST", "PUT", "DELETE"])
@consultoria_app.route('/formularios/<int:id>', methods=["GET", "PUT" "DELETE"])
@login_required
def formularios(id=None):
    return crud_request(FormularioController(), id)

@consultoria_app.route('/admin/formularios/', methods=['GET', "POST", "PUT", "DELETE"])
@consultoria_app.route('/admin/formularios/<int:id>', methods=["GET", "PUT" "DELETE"])
@admin_permission.require(http_exception=403)
def admin_formularios(id=None):
    if request.method == "PUT":
        return FormularioController().admin_editar(request.json or request.form)
    return crud_request(FormularioController(), id)

@consultoria_app.route('/ajustarFormulario/', methods=["PUT"])
@admin_permission.require(http_exception=403)
def ajustarFormulario():
    return FormularioController().admin_form(request.json)

@consultoria_app.route('/usuarios/', methods=['GET', "POST", "PUT", "DELETE"])
@consultoria_app.route('/usuarios/<int:id>', methods=["GET", "DELETE"])
@login_required
def usuarios(id=None):
    return crud_request(UsuarioController(), id)

@consultoria_app.route('/admin/usuarios/', methods=['GET', "POST", "PUT", "DELETE"])
@consultoria_app.route('/admin/usuarios/<int:id>', methods=["GET", "DELETE"])
@admin_permission.require(http_exception=403)
def admin_usuarios(id=None):
    if request.method == "PUT":
        return UsuarioController().admin_editar(request.json or request.form)
    return crud_request(UsuarioController(), id)

@consultoria_app.route('/admin/duvidas/', methods=['GET', "POST", "PUT", "DELETE"])
@consultoria_app.route('/admin/duvidas/<int:id>', methods=["GET", "DELETE"])
@admin_permission.require(http_exception=403)
def admin_duvidas(id=None):
    if request.method == "PUT":
        return DuvidasController().admin_editar(request.json or request.form)
    if request.method == "GET":
        return DuvidasController().listar_admin()
    return crud_request(DuvidasController(), id)

@consultoria_app.route('/duvidas/', methods=['GET', "POST", "PUT"])
@consultoria_app.route('/duvidas/<int:id>', methods=['GET', "POST", "PUT"])
@login_required
def duvidas(id=None):
    return crud_request(DuvidasController(), id)

@consultoria_app.route('/totalDuvidas/', methods=['GET'])
@login_required
def totalDuvidas():
    return DuvidasController().totalDuvidas()

@consultoria_app.route('/admin/treinos/', methods=['GET', "POST", "PUT", "DELETE"])
@consultoria_app.route('/admin/treinos/<int:id>', methods=["GET", "DELETE"])
@admin_permission.require(http_exception=403)
def admin_treinos(id=None):
    if request.method == "PUT":
        return TreinoController().admin_editar(request.json or request.form)
    if request.method == "GET":
        return TreinoController().listar_admin()
    return crud_request(TreinoController(), id)

@consultoria_app.route('/treinos/', methods=['GET', "POST", "PUT"])
@consultoria_app.route('/treinos/<int:id>', methods=['GET', "POST", "PUT"])
@login_required
def treinos(id=None):
    return crud_request(TreinoController(), id)

@consultoria_app.route('/comprarConsultoria/<int:id>', methods=['GET', "POST", "PUT"])
@login_required
def comprar(id=None):
    if id == 1:
        return CompraController().planoMes()
    elif id ==3:
        return CompraController().planoTri()

@consultoria_app.route('/linkPagSeguro/<int:id>', methods=['GET'])
@login_required
def linkPagSeguro(id=None):
        return CompraController().pagSeguro(id)

@consultoria_app.route('/retornoPagSeguro/', methods=['POST'])
def retornoPagSeguro():
    return CompraController().retornoPagSeguro()

@consultoria_app.route('/admin/modeloTreino/', methods=['GET', "POST", "PUT", "DELETE"])
@consultoria_app.route('/admin/modeloTreino/<int:id>', methods=["GET", "DELETE"])
@admin_permission.require(http_exception=403)
def admin_modeloTreino(id=None):
    return crud_request(ModeloTreinoController(), id)


@consultoria_app.route('/planosCliente/', methods=['GET', "POST", "PUT", "DELETE"])
@consultoria_app.route('/planosCliente/<int:id>', methods=["GET", "DELETE"])
@login_required
def planosCliente(id=None):
    if request.method == "GET":
        return PlanoController().listarCliente()
    else:
        return crud_request(PlanoController(), id)

@consultoria_app.route('/planos/', methods=['GET', "POST", "PUT", "DELETE"])
@consultoria_app.route('/planos/<int:id>', methods=["GET", "DELETE"])
@login_required
def planos(id=None):
    return crud_request(PlanoController(), id)

@consultoria_app.route('/admin/planos/', methods=['GET', "POST", "PUT", "DELETE"])
@consultoria_app.route('/admin/planos/<int:id>', methods=["GET", "DELETE"])
@admin_permission.require(http_exception=403)
def admin_planos(id=None):
    if request.method == "PUT":
        return PlanoController().admin_editar(request.json or request.form)
    return crud_request(PlanoController(), id)

@consultoria_app.route('/grupos/', methods=['GET', "POST", "PUT"])
@consultoria_app.route('/grupos/<int:id>')
@login_required
def grupos(id=None):
    return crud_request(GrupoController(), id)

@consultoria_app.errorhandler(400)
def not_found(error):
    return jsonify(status=error.code, response=error.name, desc=error.description), 400 
