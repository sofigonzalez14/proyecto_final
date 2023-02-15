from flask import Flask, jsonify, request, Response
app = Flask(__name__)
@app.route('/')
def index():
 return '<h1>Hola!<h1>'

@ aplicación . ruta ( "/usuarios" )
def  devolver_usuarios ():
    volver  jsonify ( usuarios )