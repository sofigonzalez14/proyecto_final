from flask import Flask, jsonify, request, Response
app = Flask(__name__)
@app.route('/')

@app.route("/usuarios")
<<<<<<< HEAD
    def devolver_usuarios():
    return jsonify("JSON/usuarios")
=======
def devolver_usuarios():
    return jsonify('usuarios')

