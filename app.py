from flask import Flask, jsonify, response, Request
app = Flask(__name__)
@app.route('/')
    def index():
    return '<h1>Hola!<h1>'

@app.route("/usuarios")
def devolver_usuarios():
    return jsonify(usuarios)
    
sadasd
