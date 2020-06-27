# -*- coding: utf-8 -*-
# Aula 01 - Instalando o Flask

from flask import Flask, request, abort, redirect, url_for
from json import dumps

app = Flask(__name__, static_folder='public')


@app.route("/")
def index():
    return "Hello world"

@app.route("/page", methods=["GET"])
def page():
    """
        Converte para dicionario
        opc1 = request.args.to_dict()
        opc2 = dict(request.args)
        print opc1['nome'] // rafael
    """
    return dumps(request.args)

@app.route("/login", methods=["GET",'POST'])
def login():
    if request.method == "POST":
        print request.form
        if (request.form['email'] == 'admin@email.com' and request.form['password'] == '1234'):
            return redirect(url_for('painel'), code=302)
        else:
            abort(401)
    return dumps({"status": False, "message": "Algo de errado não está certo"})

@app.route('/painel')
def painel():
    return '<h1>Bem vindo ao painel administrativo</h1>'

def teste():
    return "<p>Testando 1</p>"

def teste2():
    return "<h1>Testando 2</h1>"

@app.route("/hello/")
@app.route("/hello/<nome>")
def hello(nome="World"):
    return "<h1>Hello {}</h1>".format(nome)

@app.route("/blog/")
@app.route("/blog/<int:postID>")
def blog(postID=None):
    if postID:
        return "blog info {}".format(postID)
    else:
        return "Blog todo"

@app.route("/blog2/")
@app.route("/blog2/<float:postID>")
def blog2(postID=None):
    if postID:
        return "blog info {}".format(postID)
    else:
        return "Blog todo"




app.add_url_rule("/teste", "teste", teste)
app.add_url_rule("/teste-2", "teste2", teste2)

if __name__ == '__main__':
    app.run(debug=True, port="3000")