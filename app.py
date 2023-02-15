from flask import Flask, jsonify, request, Response
app = Flask(__name__)
@app.route('/')

@app.route("/usuarios")
    def devolver_usuarios():
    return jsonify("JSON/usuarios")
a