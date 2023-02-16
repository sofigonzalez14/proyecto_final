import json
from flask import Flask, jsonify, Response, request
from http import HTTPStatus
import threading

app = Flask(__name__)

with open("usuarios.json",encoding='utf-8') as usuarios_json:
    usuarios=json.load(usuarios_json)
usuarios=usuarios[0]['usuarios']