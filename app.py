import json
from flask import Flask, jsonify, Response, request
from http import HTTPStatus
import threading

app = Flask(__name__)

with open("peliculas.json",encoding='utf-8') as peliculas_json:
    peliculas=json.load(peliculas_json)
peliculas=peliculas[0]['peliculas']

with open("usuarios.json",encoding='utf-8') as usuarios_json:
    usuarios=json.load(usuarios_json)
usuarios=usuarios[0]['usuarios']

with open("directores.json",encoding='utf-8') as directores_json:
    directores=json.load(directores_json)
directores=directores[0]['directores']


