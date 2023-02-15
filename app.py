from flask import Flask, jsonify, request, Response
app = Flask(__name__)
@app.route('/')

<<<<<<< HEAD

=======
@app.route("/usuarios")
def devolver_usuarios():
    return jsonify(usuarios)
    
sadasd
>>>>>>> 73a328e5fdd3c6a799bfcda8bfa574c33b44d3fe
