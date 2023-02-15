import json
from flask import Flask, jsonify, Response, request
from http import HTTPStatus
import requests

app = Flask(__name__)

with open("usuarios.json",encoding='utf-8') as usuarios.json:
    usuarios=json.load(usuarios.json)
usuarios=usuarios[0]["usuarios"]

with open("biblioteca.json",encoding='utf-8') as biblioteca_json:
    peliculas=json.load(biblioteca_json) 
peliculas=peliculas[0]['peliculas']

@app.route("/usuarios")
def devolver_usuarios():
return jsonify("JSON/usuarios")

@app.route("/usuarios")
def loguearse(usuario, contrasena):

