from flask import Flask, jsonify, request, Response
from http import HTTPStatus
import json
import urllib

app = Flask(__name__)

if __name__ == "__main__":
    app.run(debug = True)

@app.route('/')
def home():
 return '<h1>Hola!<h1>'