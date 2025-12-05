from flask import Flask, render_template, request, redirect, url_for, flash, Blueprint, session
from datetime import datetime

#-- importando todas as funções do data_manager.py
from models.data_manager import save_data,load_data,quote_get,save_info,load_info

# Cria um Blueprint para as rotas
front_controller = Blueprint('front_controller', __name__)
# Blueprint (front_controller) no controlador (front_controller.py) é um módulo que agrupa rotas relacionadas.
# Flask precisa saber que o front_controller existe, então você o registra, no APP.PY, com app.register_blueprint(front_controller).


#-- rota principal
@front_controller.route('/')
def index():
    return render_template('index.html')

@front_controller.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

@front_controller.route('/login',  methods=["GET", "POST"])
def login():
    return render_template('login.html')

@front_controller.route('/album',  methods=["GET", "POST"])
def album():
    info = load_info()
    if not info:
        fotos = []
        for i in range(1,21):
            fotos.append(url_for('static', filename=f'img/fotos/foto{i}.webp'))
        nomes = [
            "Leitura",
            "Leite",
            "Persistencia",
            "Uniao",
            "Admiracao",
            "Lanche",
            "De outro mundo",
            "Amizade",
            "Sem foco",
            "Semelhancas",
            "Descanso",
            "Todos",
            "Competir",
            "Arte",
            "Foco",
            "Bobeira",
            "Amor",
            "Novo comeco",
            "Magnum Opus",
            "Vergonha"
        ]
        desc = quote_get()
        info =[]
        for i in range(20):
            dic = {
                "foto": fotos[i],
                "nome": nomes[i],
                "desc": desc[i]
            } 
            info.append(dic)
        save_info(info)
    return render_template('album.html', info=info)

@front_controller.route('/delete_foto/<int:foto_id>', methods=["POST"])
def delete_foto(foto_id):
    info = load_info()
    if 0 <= foto_id < len(info):
        info.pop(foto_id)
        save_info(info)
    return redirect(url_for('front_controller.album'))


@front_controller.route('/sair',  methods=["GET", "POST"])
def sair():
    session.pop('usuario_ativo')
    return redirect(url_for('front_controller.index'))

@front_controller.route('/autenticar', methods=["GET", "POST"])
def autenticar():
    dados = load_data()
    if (request.method == "POST"):
        usuario_email = request.form.get('email')
        usuario_senha = request.form.get('senha')
        if usuario_email and usuario_senha:
                for usuario in dados:
                    if usuario['email'] == usuario_email and usuario['senha'] == usuario_senha:
                        session['usuario_ativo'] = usuario_email
                        flash(usuario_email + ", logado com sucesso!", "success")
                        return(redirect(url_for('front_controller.album')))    
                flash("usuario não existente!", "danger")
                return(redirect(url_for('front_controller.login')))
        else:
                flash("Confira seu usuário e/ou senha. Erro de login.", "danger")
                return(redirect(url_for('front_controller.login')))
        
@front_controller.route('/cadastrar', methods=["GET", "POST"])
def cadastrar():
    if (request.method == "POST"):
        usuario_email = request.form.get('email')
        usuario_senha = request.form.get('senha')
        if usuario_email and usuario_senha:
            dados = load_data()
            cadastro = {
                'email': usuario_email,
                'senha': usuario_senha
            }
            existente = False
            for usuario in dados:
                if usuario['email'] == usuario_email:
                    existente = True
                    break
            if existente == False:
                dados.append(cadastro)
                save_data(dados)
                flash("Cadastro feito com sucesso!", "success")
                return render_template('login.html')
            else:
                flash("Cadastro ja existente!", "danger")
            return render_template('cadastro.html')
        else:
            flash("Campos não podem ser vazios", "danger")
            return render_template('cadastro.html')

@front_controller.route('/sobre', methods=["GET","POST"])
def sobre():
    return render_template('sobre.html')

@front_controller.route('/edit/<int:foto_id>', methods=["GET","POST"])
def edit(foto_id):
    if session.get('usuario_ativo'):
        return render_template("edit.html", foto_id=foto_id)
    else:
        flash("Conta necessária", "danger")
        return render_template("index.html")

@front_controller.route('/edit_foto/<int:foto_id>', methods=["GET","POST"])
def edit_foto(foto_id):
    info = load_info()
    nome = request.form.get("nome")
    desc = request.form.get("desc")
    if 0 <= foto_id < len(info):
        info[foto_id]["nome"] = nome
        info[foto_id]["desc"] = desc
        save_info(info)

    return redirect(url_for('front_controller.album'))

@front_controller.route('/secret')
def secret_start():
    return redirect(url_for('front_controller.secret_show', n=1))

@front_controller.route('/secret/<int:n>')
def secret_show(n):
    total = 12
    proxima = n + 1
    if proxima > total:
        proxima = 1

    atual = f"img/secret/foto{n}.webp"
    
    return render_template("secret.html",atual=atual, proxima=proxima)
