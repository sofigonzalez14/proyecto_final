from flask import Flask, jsonify, request, Response, JSON
app = Flask(__name__)

@app.route("/usuarios")
def devolver_usuarios():
return jsonify("JSON/usuarios")

@app.route("/usuarios")
def loguearse(usuario, contrasena):

