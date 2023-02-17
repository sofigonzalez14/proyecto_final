import json
from flask import Flask, jsonify, Response, request
from http import HTTPStatus
import threading
import os

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

usuario_privado = False
print("BIENVENIDOS AL CINE")
print("Estas registrado en esta pagina?")

validar_registro = input("Ingresa Si/No: ")
lower_input = validar_registro.lower()
if lower_input != "si":
    print ("Como usuario publico solo podes ver los titulos de las ultimas 5 peliculas")

#----------DEVUELVE LAS ULTIMAS 5 PELIS--------------
    for pelicula in peliculas[-5:]:
        print(pelicula, end="\n")
    print("Gracias por visitarnos")
else: # Ingreso del usuario privado
    ingreso_usuario = input( "Ingrese su usuario: ")
    ingreso_contrasenia= input( "Ingrese su contraseña: ")
    for usuario in usuarios:
        if usuario == ingreso_usuario and usuario["contrasenia"] == ingreso_contrasenia:
            print("Usuario logueado con exito")
            print("Arranca tu experiencia como usuario registrado")
            usuario_privado = True

#--------------- Muestras todos los usuarios ------------------------
@app.route("/usuarios")     
def devolver_usuarios():
    lista=[]
    for usuario in usuarios:
        lista.append(usuario['usuario'])
    if len(lista)>0:
        return jsonify(lista)
    else:
        return Response("Este usuario no es valido", status=HTTPStatus.NOT_FOUND)

#--------------- Muestra todas las peliculas -------------
@app.route("/peliculas")  
def devolver_peliculas():
    mostrar_peliculas=[]
    for pelicula in peliculas:
        mostrar_peliculas.append(pelicula["titulo"])
    if len(mostrar_peliculas)>0:
        return jsonify(mostrar_peliculas)
    else:
        return Response("La pelicula no ha sido encontrada", status=HTTPStatus.NOT_FOUND)


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
        return Response("No ha sido encontrado el director", status=HTTPStatus.NOT_FOUND)

#--------------- Muestra todos los generos---------------

@app.route("/generos")      
def generos_imprimir():
    lista=[]
    for pelicula in peliculas:
        if pelicula['genero'] not in lista:
            lista.append(pelicula['genero'])
    if len(lista)>0:
        return jsonify(lista)
    else:
        return Response("No ha sido encontrado el genero buscado", status=HTTPStatus.NOT_FOUND)

#--------------- Muestra las peliculas que tienen portada---------------

@app.route("/peliculas/imagen")  
def devolver_peliculas_con_imagen():
    dic={}
    for pelicula in peliculas: 
        if "enlace" in pelicula:
            dic[pelicula['titulo']]=pelicula['enlace']
    if len(dic)>0:
        return jsonify(dic)
    else:
        return Response("Esta pelicula no tiene imagen", status=HTTPStatus.NOT_FOUND)

#--------------- Muestra las peliculas de un director en especifico---------------
@app.route("/directores/<id>")     
def devolver_peliculas_director(id):
    id_int=int(id)
    lista=[]
    for director in directores:
        if id_int==director['id']:
            variable=director['director']
    for pelicula in peliculas:
        if pelicula['director']==variable:
            lista.append(pelicula['titulo'])
    if len(lista)>0:
        return jsonify(lista)
    else:
        return Response("Este director no ha sido encontrado", status=HTTPStatus.NOT_FOUND)

#------------AGREGAR UNA PELICULA------------------
def existe_pelicula(titulo):
    peliculas = pelicula["peliculas"]
    for pelicula in peliculas:
        if pelicula['titulo'].lower() == titulo.lower():
            return pelicula
    return False

#---------------------------------------------------
@app.route("/agregar/pelicula", methods=['POST'])
def alta_pelicula():
    if usuario_privado == True:
        data = request.get_json()

        campos = {"titulo", "genero","director", "id", "sinopsis", "enlace"}
        if data.keys() < campos:
            return jsonify("Faltan campos en el pedido"), HTTPStatus.BAD_REQUEST

        if existe_pelicula(data["titulo"]):
            return jsonify("La pelicula ya existe en la base de datos."), HTTPStatus.BAD_REQUEST
        
        pelicula_nueva = {
            "id": id,
            "titulo": data["titulo"],
            "año": data["año"],
            "genero": data["genero"],
            "sinopsis": data["sinopsis"],
            "enlace": data["enlace"],
        }
        peliculas["peliculas"].append(pelicula_nueva)
        print("Se cargo una pelicula nueva")
        return jsonify(pelicula_nueva), HTTPStatus.OK
    else:
        return jsonify("Usted no es un usuario registrado"), HTTPStatus.BAD_REQUEST
    
#------------------ Elimina una pelicula por id ------------------------------
    
    @app.route("/peliculas/eliminar/<id>",methods=["DELETE"])     
    def eliminar_pelicula(id):
        id_int=int(id)
    valor=False
    for pelicula in peliculas:
        if pelicula['id']==id_int:
            peliculas.remove(pelicula)
            valor=True
    if valor==True:
        # with open("biblioteca.json",'w',encoding='utf-8') as biblioteca_json:   # Lo agregamos al json
        #     json.dump(peliculas,biblioteca_json)
        return Response("Eliminado",status=HTTPStatus.OK)
    else:  
        return Response("Solicitud incorrecta",status=HTTPStatus.BAD_REQUEST)

#--------- Modifica una pelicula----------------------------
@app.route("/peliculas/<id>", methods=['PUT'])
def modificar_pelicula(id):
    if usuario_privado == True:
        encontrado = False
        data = request.get_json()
        for pelicula in peliculas["peliculas"]:
            if pelicula["id"] == int(id):
                encontrado = True
                id_pelicula = pelicula["id"]
                
                peliculas["id"]= int(id)                                           
                peliculas["titulo"]= data["titulo"]
                peliculas["año"]= int(data["año"])
                peliculas["genero"]= data["genero"]
                peliculas["director"]= int(data["director"])
                peliculas["sinopsis"]= data["sinopsis"]
                peliculas["enlace"]=data["enlace"]
                
        if encontrado == True:
            print("Se modificaron datos de la pelicula")
            return jsonify("Se actualizaron los datos de la pelicula"), HTTPStatus.OK
        else:
            print("No se modificaron datos")
            return jsonify("No se actualizaron los datos de la película"), HTTPStatus.NOT_FOUND
    else:
        return jsonify("Usted no es un usuario registrado"), HTTPStatus.BAD_REQUEST
    
login=False
def menu():
    print("")
    while True:
        print("MENU DE CINE")
        print("1: Mostrar todas las peliculas")
        print("2: Mostrar pelicula especifica")
        print("3: Mostrar peliculas con imagenes")
        print("4: Mostrar directores")
        print("5: Mostrar peliculas de un director especifico")
        print("6: Mostrar usuarios")
        print("7: Mostrar generos")
        print("8: Eliminar pelicula")
        print("9: Publicar pelicula")
        print("10: Modificar pelicula")
        print("11: Salir")
        opcion=int(input("Ingresar opcion: "))
        print("")


        elif (opcion==1):
            r=(requests.get("http://127.0.0.1:5000/peliculas"))
            r=r.json()
            for i in r:
                print(i)

        elif (opcion==2):   
            id=input("Ingresar id de la pelicula: ")
            r=(requests.get("http://127.0.0.1:5000/peliculas/"+id))
            r=r.json()
            for key,value in r.items():
                print(key," : ",value)

        elif (opcion==3):
            r=(requests.get("http://127.0.0.1:5000/peliculas/imagen"))
            r=r.json()
            for key,value in r.items():
                print(key," : ",value)

        elif (opcion==4):
            r=(requests.get("http://127.0.0.1:5000/directores"))
            r=r.json()
            for i in r:
                print(i)

        elif (opcion==5): 
            id=input("Ingresar id del director: ")
            r=(requests.get("http://127.0.0.1:5000/directores/"+id))
            r=r.json()
            for i in r:
                print(i)

        elif (opcion==6):
            r=(requests.get("http://127.0.0.1:5000/usuarios"))
            r=r.json()
            for i in r:
                print(i)

        elif (opcion==7):
            r=(requests.get("http://127.0.0.1:5000/generos"))
            r=r.json()
            for i in r:
                print(i)

        elif (opcion==8):
            if(login==False):
                print("Permiso denegado, inicie sesion.")
            else:
                id=input("Ingresar id de la pelicula: ")
                r=(requests.delete("http://127.0.0.1:5000/peliculas/eliminar/"+id))
                print(r.content)

        elif (opcion==9):
            if(login==False):
                print("Permiso denegado, inicie sesion.")
            else:
                id=int(input("Ingresar id: "))
                titulo=input("Titulo: ")
                anio=input("Año: ")
                director=input("Director: ")
                genero=input("Genero: ")
                sinopsis=input("Sinopsis: ")
                link=input("Link imagen/portada: ")
                j={
                    "id":id,
                    "titulo":titulo,
                    "anio":anio,
                    "director":director,
                    "genero":genero,
                    "sinopsis":sinopsis,
                    "link":link
                }
                r=(requests.post("http://127.0.0.1:5000/peliculas/publicar",json=j))
                print(r.content)

        elif (opcion==10):
            if(login==False):
                print("Permiso denegado, inicie sesion.")
            else:
                id=int(input("Ingresar id de la pelicula: "))
                valor=False
                for pelicula in peliculas:
                    if id==pelicula['id']:
                        valor=True
                        dic_pelicula=pelicula
                if valor==False:
                    print("ID no encontrado")
                else:
                    respuesta=input("¿Modificar el titulo?")
                    if(respuesta=='si' or respuesta=='SI'):
                        titulo=input("Ingresar titulo: ")
                    else:
                        titulo=dic_pelicula['titulo']
                    respuesta=input("¿Modificar el año?")
                    if(respuesta=='si' or respuesta=='SI'):
                        anio=input("Ingresar año: ")
                    else:
                        anio=dic_pelicula['anio']
                    respuesta=input("¿Modificar el director?")
                    if(respuesta=='si' or respuesta=='SI'):
                        director=input("Ingresar director: ")
                    else:
                        director=dic_pelicula['director']
                    respuesta=input("¿Modificar el genero?")
                    if(respuesta=='si' or respuesta=='SI'):
                        genero=input("Ingresar genero: ")
                    else:
                        genero=dic_pelicula['genero']
                    respuesta=input("¿Modificar la sinopsis?")
                    if(respuesta=='si' or respuesta=='SI'):
                        sinopsis=input("Ingresar sinopsis: ")
                    else:
                        sinopsis=dic_pelicula['sinopsis']
                    respuesta=input("¿Modificar el link de la imagen?")
                    if(respuesta=='si' or respuesta=='SI'):
                        link=input("Ingresar link: ")
                    else:
                        link=dic_pelicula['link']
                    j={
                        "id":id,
                        "titulo":titulo,
                        "anio":anio,
                        "director":director,
                        "genero":genero,
                        "sinopsis":sinopsis,
                        "link":link
                    }
                    r=(requests.put("http://127.0.0.1:5000/peliculas/actualizar",json=j))
                    print(r.content)

        elif (opcion==11):
            print("Exit!\n")
            exit()

        else:
            print("Error al ingresar opcion")
        print("")



