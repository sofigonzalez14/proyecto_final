from flask import Flask, jsonify, request, Response
app = Flask(__name__)
@app.route('/')

def index():
    return '<h1>Hola!<h1>'

@app.route("/usuarios")
<<<<<<< HEAD
    def devolver_usuarios():
    return jsonify("JSON/usuarios")
=======
def devolver_usuarios():
    return jsonify('usuarios')

