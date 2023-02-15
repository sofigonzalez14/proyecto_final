import json
from flask import Flask, jsonify, Response, request
from http import HTTPStatus
import requests

app = Flask(__name__)

with open("directores.json",encoding='utf-8') as directores.json:
    directores=json.load(directores_json)
directores=directores[0]['directores']

with open("peliculas.json",encoding='utf-8') as peliculas.json:
    peliculas=json.load(biblioteca_json) 
peliculas=peliculas[0]['peliculas']

with open("usuarios.json",encoding='utf-8') as usuarios.json:
    usuarios=json.load(usuarios.json)
usuarios=usuarios[0]['usuarios']

print("CARTELERA\n")
ultimas_peliculas_agregadas=[]
@app.route("/json/usuarios")
