import json
from flask import Flask, jsonify, Response, request
from http import HTTPStatus
import requests
import threading
import os

app = Flask(__name__)

path, _ = ps.path.split(os.path.abspath(__file__))

with open(path+'/JSON/usuarios.json') as usuarios:
    data = json

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
 
a