# -*- coding: utf-8 -*-
# Curso básico de Flask

from flask import Flask, request, abort, redirect, url_for, render_template, send_file, make_response, session
from json import dumps
import os
from werkzeug.utils import secure_filename

app = Flask(__name__, static_folder='public', template_folder='templates')
app.secret_key = "12345678" # Caso utilize sessão defina uma hash token aqui
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')


@app.route("/")
def index():
    logged = None
    if "logged" in session:
        logged = session['logged']
    return render_template('index.html', logged=logged)

""" Efetua upload de arquivo e salva na pasta uploads """
@app.route("/upload", methods=['GET','POST'])
def upload():
    if request.method == "GET":
        return render_template('upload.html')
    file = request.files['files']
    savePath = os.path.join(UPLOAD_FOLDER, secure_filename(file.filename))
    file.save(savePath)
    return 'Upload feito com sucesso'

""" Efetua download do arquivo passando o nome + extensao no parametro ex: /download/logo_flask.png"""
@app.route("/download/<filename>")
def download(filename):
    file = os.path.join(UPLOAD_FOLDER, filename)
    return send_file(file, mimetype="imagem/png")


""" Exibe o formulario para dar valor ao cookie que será salvo no browser do cliente """
@app.route("/cookie")
def cookie():
    return render_template("viewCookie.html")

""" Salva um cookie no browser do usuário com nome testecookie e com valor que foi passado via post no formulario """
@app.route("/setcookie", methods=['GET', 'POST'])
def setcookie():
    resp = make_response(render_template('setcookie.html'))
    if request.method == 'POST':
        dados = request.form['c']
        resp.set_cookie('testecookie', dados)

    return resp

""" Busca o cookie testecookie que foi salvo no browser do usuario e mostra seu valor na tela """
@app.route("/getcookie")
def getcookie():
    cookieName = request.cookies.get('testecookie')
    return '<h1>Valor do cookie é: {}</h1>'.format(cookieName)

""" Passando parametros na routa page?nome=rafael&idade=90 retorna os dados em json """
@app.route("/page", methods=["GET"])
def page():
    """
        Converte para dicionario
        opc1 = request.args.to_dict()
        opc2 = dict(request.args)
        print opc1['nome'] // rafael
    """
    # return dumps({"status": False, "message": "Algo de errado não está certo"})
    return dumps(request.args)

""" Efetua o login e regista a senha, caso seja um GET exibe a página de login """
@app.route("/login", methods=["GET",'POST'])
def login():
    if request.method == "POST":
        if (request.form['email'] == 'admin@email.com' and request.form['password'] == '1234'):
            session['logged'] = request.form['email']
            return redirect(url_for('index'), code=302)
        else:
            abort(401)
    if 'logged' in session: return redirect(url_for('index'))
    return render_template('login.html')

""" Desloga o usuário do sistema """
@app.route("/logout", methods=["GET"])
def logout():
    session.pop('logged', None)
    return redirect(url_for('index'))

""" Altera o usuário logado passando um novo email """
@app.route("/setsession/<email>")
def setsession(email):
    session['logged'] = email;
    return redirect(url_for('index'))

""" Exibe um html básico na tela """
@app.route('/painel')
def painel():
    return '<h1>Bem vindo ao painel administrativo</h1>'

""" Passando parametros string na routa, caso passado algum parametro exibe caso contrario exibe World no lugar do nome """
@app.route("/hello/")
@app.route("/hello/<nome>")
def hello(nome="World"):
    return "<h1>Hello {}</h1>".format(nome)

""" Passando apenas inteiro na rota ex: /blog/1010 """
@app.route("/blog/")
@app.route("/blog/<int:postID>")
def blog(postID=None):
    if postID:
        return "blog info {}".format(postID)
    else:
        return "Blog todo"

""" Passando apenas float na rota ex: /blog2/1.5 """
@app.route("/blog2/")
@app.route("/blog2/<float:postID>")
def blog2(postID=None):
    if postID:
        return "blog info {}".format(postID)
    else:
        return "Blog todo"


""" Forma diferente de chama uma forma no flask """
def teste():
    return "<p>Testando 1</p>"

def pessoas():
    nomes = ['Rafael', 'Angela', 'Gustavo', 'Julia']
    sobrenomes = ['Jeferson', 'Angelica', 'Henrique', 'Isabelly']
    nomesCompletos = [n+' '+s for n,s in list(map(lambda n,s: (n,s), nomes, sobrenomes))]
    return render_template('modelo.html', nomes=nomes, sobrenomes=sobrenomes, nomesCompletos=nomesCompletos)


app.add_url_rule("/teste", "teste", teste)
app.add_url_rule("/pessoas", "pessoas", pessoas)

if __name__ == '__main__':
    app.run(debug=True, port="3000")