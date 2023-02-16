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

#--------------- Muestras todos los usuarios ------------------------
@app.route("/usuarios")     
def devolver_usuarios():
    lista=[]
    for usuario in usuarios:
        lista.append(usuario['usuario'])
    if len(lista)>0:
        return jsonify(lista)
    else:
        return Response("No encontrado", status=HTTPStatus.NOT_FOUND)

#--------------- Muestra todas las peliculas -------------
@app.route("/peliculas")  
def devolver_peliculas():
    mostrar_peliculas=[]
    for pelicula in peliculas:
        mostrar_peliculas.append(pelicula['titulo'])
    if len(mostrar_peliculas)>0:
        return jsonify(mostrar_peliculas)
    else:
        return Response("No encontrado", status=HTTPStatus.NOT_FOUND)

#--------------- Muestra todos los directores ---------------
@app.route("/directores")   
def directores_imprimir():
    lista=[]
    for pelicula in peliculas:
        if pelicula['director'] not in lista:
            lista.append(pelicula['director'])
    if len(lista)>0:
        return jsonify(lista)
    else:
        return Response("No encontrado", status=HTTPStatus.NOT_FOUND)