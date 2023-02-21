import json
import requests
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

@app.route("/peliculas/publicar", methods=["POST"])     # Publica nueva pelicula 
def comprar_entrada():                                  
    datos=request.get_json()                            
    for director in directores:         
        id=director['id']
    id+=1
    if datos['director'] not in directores:     
        directores.append({
            "id":id,
            "director":datos['director']
            })
        # with open("directores.json",'w',encoding='utf-8') as directores_json:
        #     json.dump(directores,directores_json)

    if (datos['id'] not in peliculas):      # Post
        peliculas.append(datos)
        # with open("biblioteca.json",'w',encoding='utf-8') as biblioteca_json:   # Lo agregamos al json
        #     json.dump(peliculas,biblioteca_json)
        return Response("OK",status=HTTPStatus.OK)
    else:
        return Response("Solicitud incorrecta",status=HTTPStatus.BAD_REQUEST)

#------------------ Elimina una pelicula por id ------------------------------

@app.route("/peliculas/eliminar/<int:id>",methods=["DELETE"])      # Elimina una pelicula por id 
def eliminar_pelicula(id):
    id_int=int(id)
    valor=False
    for pelicula in peliculas:
        if pelicula['id']==id_int:
            peliculas.remove(pelicula)
            valor=True
    if valor==True:
        with open("peliculas.json",'w',encoding='utf-8') as peliculas_json:   # Lo eliminamos del json
            json.dump(peliculas,peliculas_json)
        return Response("Eliminado",status=HTTPStatus.OK)
    else:  
        return Response("Solicitud incorrecta",status=HTTPStatus.BAD_REQUEST)


#--------- Modifica una pelicula----------------------------

@app.route("/peliculas/actualizar", methods=["PUT"])    # Modifica pelicula especifica segun id 
def modificar_pelicula():
    datos=request.get_json()
    if "id" in datos:
        for pelicula in peliculas:
            if(datos['id']==pelicula['id']):
                if "titulo" in datos:
                    pelicula['titulo']=datos["titulo"]
                if "año" in datos:
                    pelicula['año']=datos["año"]
                if "director" in datos:
                    pelicula['director']=datos["director"]
                    if datos['director'] not in directores:
                        for director in directores:
                            id=director['id']
                            id+=1
                        directores.append({
                            "id":id,
                            "director":datos['director']
                        })
                if "genero" in datos:
                    pelicula['genero']=datos["genero"]
                if "sinopsis" in datos:
                    pelicula['sinopsis']=datos["sinopsis"]
                if "enlace" in datos:
                    pelicula['enlace']=datos["enlace"]
                
                # with open("biblioteca.json",'w',encoding='utf-8') as biblioteca_json:   # Modificamos el json
                #     json.dump(peliculas,biblioteca_json)

                return Response("OK",status=HTTPStatus.OK)
    else:
        return Response("ID no encontrado",status=HTTPStatus.NOT_FOUND)

#------------Agrega un usuario------------------

@app.route("/usuarios/agregar", methods=["POST"])     # Publica nueva pelicula 
def agregar_usuario():                                  
    datos=request.get_json()                            
    if datos['usuario'] not in usuarios:     
        usuarios.append({
            "usuario":datos['usuario']
            })
        # with open("directores.json",'w',encoding='utf-8') as directores_json:
        #     json.dump(directores,directores_json)

    if (datos['usuario'] not in usuarios):      # Post
        usuarios.append(datos)
        # with open("biblioteca.json",'w',encoding='utf-8') as biblioteca_json:   # Lo agregamos al json
        #     json.dump(peliculas,biblioteca_json)
        return Response("OK",status=HTTPStatus.OK)
    else:
        return Response("Solicitud incorrecta",status=HTTPStatus.BAD_REQUEST)

#------------------ Elimina usuario ------------------------------

"""@app.route("/usuarios/eliminar",methods=["DELETE"])      
def eliminar_usuario():
    valor=False
    for usuario in usuarios:
        if usuario['usuario']==usuarios:
            usuarios.remove(usuarios)
            valor=True
    if valor==True:
        with open("usuarios.json",'w',encoding='utf-8') as usuarios_json:   # Lo eliminamos del json
            json.dump(usuarios,usuarios_json)
        return Response("Eliminado",status=HTTPStatus.OK)
    else:  
        return Response("Solicitud incorrecta",status=HTTPStatus.BAD_REQUEST)"""

#--------- Modifica una pelicula----------------------------

@app.route("/usuarios/actualizar", methods=["PUT"])    # Modifica pelicula especifica segun id 
def modificar_pelicula():
    datos=request.get_json()
    if "usuarios" in datos:
        for usuario in usuario:
            if(datos['usuario']==usuario['usuario']):
                if "titulo" in datos:
                    pelicula['titulo']=datos["titulo"]
                if "año" in datos:
                    pelicula['año']=datos["año"]
                if "director" in datos:
                    pelicula['director']=datos["director"]
                    if datos['director'] not in directores:
                        for director in directores:
                            id=director['id']
                            id+=1
                        directores.append({
                            "id":id,
                            "director":datos['director']
                        })
                if "genero" in datos:
                    pelicula['genero']=datos["genero"]
                if "sinopsis" in datos:
                    pelicula['sinopsis']=datos["sinopsis"]
                if "enlace" in datos:
                    pelicula['enlace']=datos["enlace"]
                
                # with open("biblioteca.json",'w',encoding='utf-8') as biblioteca_json:   # Modificamos el json
                #     json.dump(peliculas,biblioteca_json)

                return Response("OK",status=HTTPStatus.OK)
    else:
        return Response("ID no encontrado",status=HTTPStatus.NOT_FOUND)


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

usuario_privado=True

def menu():
    print("")
    while True:
        print("           MENU             ")
        print("----------------------------")
        print("1: Mostrar todas las peliculas")
        print("2: Mostrar ultimas peliculas agregadas")
        print("3: Mostrar peliculas con imagenes")
        print("4: Mostrar directores")
        print("5: Mostrar peliculas de un director especifico")
        print("6: Mostrar usuarios")
        print("7: Mostrar generos")
        print("8: Agregar usuario")
        print("9: Modificar usuario")
        print("10: Eliminar usuario")
        print("11: Agregar director")
        print("12: Modificar director")
        print("13: Eliminar director")
        print("14: Agregar genero")
        print("15: Modificar genero")
        print("16: Eliminar genero")
        print("17: Eliminar pelicula")
        print("18: Publicar pelicula")
        print("19: Modificar pelicula")
        print("20: Salir")
        opcion=int(input("Ingresar opcion: "))
        print("")

        if (opcion==1):
            r=(requests.get("http://127.0.0.1:5000/peliculas"))
            r=r.json()
            for i in r:
                print(i)


        elif (opcion==2):
            r=(requests.get("http://127.0.0.1:5000"))
            r=r.json()
            for i in r:
                print(i)

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
            if(usuario_privado==False):
                print("Permiso denegado, inicie sesion.")
            else:
                usuario=input("Usuario: ")
                contrasena=input("contrasena: ")
                j={
                    "usuario":usuario,
                }
                r=(requests.post("http://127.0.0.1:5000/usuarios/agregar",json=j))
                print(r.content)

        elif (opcion==9):
            if(usuario_privado==False):
                print("Permiso denegado, inicie sesion.")
            else:
                usuario=input("Ingresar usuario: ")
                valor=False
                for usuario in usuarios:
                    if usuario==usuario['usuario']:
                        valor=True
                if valor==False:
                    print("Usuario no encontrado")
                else:
                    respuesta=input("¿Modificar el usuario?")
                    if(respuesta=='si' or respuesta=='SI'):
                        usuario=input("Ingresar usuario: ")
                    else:
                        respuesta=input("¿Modificar el contrasena?")
                    if(respuesta=='si' or respuesta=='SI'):
                        contrasena=input("Ingresar contrasena: ")
                    j={
                        "usuario":usuario,
                        "contrasena":contrasena,
                    }
                    r=(requests.put("http://127.0.0.1:5000/peliculas/actualizar",json=j))
                    print(r.content)


                

        elif (opcion==10):
            if(usuario_privado==False):
                print("Permiso denegado, inicie sesion.")
            else:
                usuario=input("Ingresar usuario: ")
                r=(requests.delete("http://127.0.0.1:5000/usuarios/eliminar"))
                print(r.content)

        elif (opcion==17):
            if(usuario_privado==False):
                print("Permiso denegado, inicie sesion.")
            else:
                id=input("Ingresar id de la pelicula: ")
                r=(requests.delete("http://127.0.0.1:5000/peliculas/eliminar/"+id))
                print(r.content)

        elif (opcion==18):
            if(usuario_privado==False):
                print("Permiso denegado, inicie sesion.")
            else:
                id=int(input("Ingresar id: "))
                titulo=input("Titulo: ")
                año=input("Año: ")
                director=input("Director: ")
                genero=input("Genero: ")
                sinopsis=input("Sinopsis: ")
                enlace=input("Link imagen/portada: ")
                j={
                    "id":id,
                    "titulo":titulo,
                    "año":año,
                    "director":director,
                    "genero":genero,
                    "sinopsis":sinopsis,
                    "enlace":enlace
                }
                r=(requests.post("http://127.0.0.1:5000/peliculas/publicar",json=j))
                print(r.content)

        elif (opcion==19):
            if(usuario_privado==False):
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
                        año=input("Ingresar año: ")
                    else:
                        año=dic_pelicula['año']
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
                        enlace=input("Ingresar link: ")
                    else:
                        enlace=dic_pelicula['enlace']
                    j={
                        "id":id,
                        "titulo":titulo,
                        "año": año,
                        "director":director,
                        "genero":genero,
                        "sinopsis":sinopsis,
                        "enlace":enlace
                    }
                    r=(requests.put("http://127.0.0.1:5000/peliculas/actualizar",json=j))
                    print(r.content)

        elif (opcion==20):
            print("Exit!\n")
            exit()

        else:
            print("Error al ingresar opcion")
        print("")

m = threading.Timer(1, menu)    # Ejecutar el menu 1 segundo despues para darle tiempo a crear local server
m.start()
