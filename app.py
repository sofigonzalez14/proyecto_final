import json
from flask import Flask, jsonify, Response, request
from http import HTTPStatus
import threading

app = Flask(__name__)
@app.route("/usuarios")
def devolver_usuarios():
   return jsonify('usuarios')