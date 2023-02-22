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

#--------------- Muestra todas las peliculas ---------------
@app.route("/peliculas")  
def devolver_peliculas():
    mostrar_peliculas=[]
    for pelicula in peliculas:
        mostrar_peliculas.append(pelicula["titulo"])
    if len(mostrar_peliculas)>0:
        return jsonify(mostrar_peliculas)
    else:
        return Response("La pelicula no ha sido encontrada", status=HTTPStatus.NOT_FOUND)

#--------------- Muestra las peliculas que tienen portada ---------------

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


#--------------- Muestra las peliculas de un director en especifico ---------------
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

#--------------- Muestras todos los usuarios ---------------
@app.route("/usuarios")     
def devolver_usuarios():
    lista=[]
    for usuario in usuarios:
        lista.append(usuario['usuario'])
    if len(lista)>0:
        return jsonify(lista)
    else:
        return Response("Este usuario no es valido", status=HTTPStatus.NOT_FOUND)

#--------------- Muestra todos los generos ---------------

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

#--------------- Agrega un usuario ---------------

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
        return Response("Agregado",status=HTTPStatus.OK)
    else:
        return Response("Ocurrio un error",status=HTTPStatus.BAD_REQUEST)

#--------------- Elimina un usuario ---------------

@app.route("/usuarios/eliminar/<usuario>",methods=["DELETE"])      
def eliminar_usuario(usuario):
    usuarioa=usuario
    valor=False
    for usuario in usuarios:
        if usuario['usuario']==usuarioa:
            usuarios.remove(usuario)
            valor=True
    if valor==True:
        with open("usuarios.json",'w',encoding='utf-8') as usuarios_json:   
            json.dump(usuarios,usuarios_json)
        return Response("Eliminado",status=HTTPStatus.OK)
    else:  
        return Response("Solicitud incorrecta",status=HTTPStatus.BAD_REQUEST)

#---------------Agrega un director---------------
@app.route("/director/agregar", methods=["POST"])   
def agregar_director():                                  
    datos=request.get_json()                            
    if datos['director'] not in directores:     
        directores.append({
            "director":datos['director']
            })
        with open("directores.json",'w',encoding='utf-8') as directores_json:
            json.dump(directores,directores_json)

    if (datos['director'] not in directores):      # Post
        directores.append(datos)
        # with open("directores.json",'w',encoding='utf-8') as directores_json:   
        #     json.dump(directores,directores)
        return Response("OK",status=HTTPStatus.OK)
    else:
        return Response("Solicitud incorrecta",status=HTTPStatus.BAD_REQUEST)

#--------------- Elimina un director ---------------

@app.route("/director/eliminar/<director>",methods=["DELETE"])      
def eliminar_director(director):
    directora=director
    valor=False
    for director in directores:
        if director['director']==directora:
            directores.remove(director)
            valor=True
    if valor==True:
        with open("directores.json",'w',encoding='utf-8') as directores_json:   
            json.dump(directores,directores_json)
        return Response("Eliminado",status=HTTPStatus.OK)
    else:  
        return Response("Solicitud incorrecta",status=HTTPStatus.BAD_REQUEST)

#------------Agrega un genero------------------
@app.route("/genero/agregar", methods=["POST"])   
def agregar_genero():                                  
    datos=request.get_json()                            
    if datos['genero'] not in peliculas:     
        peliculas.append({
            "peliculas":datos['genero']
            })
        with open("peliculas.json",'w',encoding='utf-8') as peliculas_json:
            json.dump(peliculas,peliculas_json)

    if (datos['genero'] not in peliculas):      # Post
        peliculas.append(datos)
        # with open("directores.json",'w',encoding='utf-8') as directores_json:   
        #     json.dump(directores,directores)
        return Response("OK",status=HTTPStatus.OK)
    else:
        return Response("Solicitud incorrecta",status=HTTPStatus.BAD_REQUEST)

#------------------ Elimina un genero ------------------

@app.route("/peliculas/eliminar/<genero>",methods=["DELETE"])      
def eliminar_genero(genero):
    generoa=genero
    valor=False
    for genero in peliculas:
        if peliculas['genero']==generoa:
            peliculas.remove(genero)
            valor=True
    if valor==True:
        with open("peliculas.json",'w',encoding='utf-8') as peliculas_json:  
            json.dump(peliculas,peliculas_json)
        return Response("Eliminado",status=HTTPStatus.OK)
    else:  
        return Response("Solicitud incorrecta",status=HTTPStatus.BAD_REQUEST)

#------------------ Elimina una pelicula por id ------------------

@app.route("/peliculas/eliminar/<int:id>",methods=["DELETE"])      
def eliminar_pelicula(id):
    id_int=int(id)
    valor=False
    for pelicula in peliculas:
        if pelicula['id']==id_int:
            peliculas.remove(pelicula)
            valor=True
    if valor==True:
        with open("peliculas.json",'w',encoding='utf-8') as peliculas_json:   
            json.dump(peliculas,peliculas_json)
        return Response("Eliminado",status=HTTPStatus.OK)
    else:  
        return Response("Solicitud incorrecta",status=HTTPStatus.BAD_REQUEST)

#------------------ AGREGAR UNA PELICULA ------------------

@app.route("/peliculas/publicar", methods=["POST"])     
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
        # with open("biblioteca.json",'w',encoding='utf-8') as biblioteca_json:   
        #     json.dump(peliculas,biblioteca_json)
        return Response("OK",status=HTTPStatus.OK)
    else:
        return Response("Solicitud incorrecta",status=HTTPStatus.BAD_REQUEST)

#------------------ Modifica una pelicula ------------------

@app.route("/peliculas/actualizar", methods=["PUT"])    
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
                
                # with open("biblioteca.json",'w',encoding='utf-8') as biblioteca_json:   
                #     json.dump(peliculas,biblioteca_json)

                return Response("OK",status=HTTPStatus.OK)
    else:
        return Response("ID no encontrado",status=HTTPStatus.NOT_FOUND)

#----------------------------

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
        print("2: Mostrar peliculas con imagenes")
        print("3: Mostrar directores")
        print("4: Mostrar peliculas de un director especifico")
        print("5: Mostrar usuarios")
        print("6: Mostrar generos")
        print("7: Agregar usuario")
        print("8: Modificar usuario")
        print("9: Eliminar usuario")
        print("10: Agregar director")
        print("11: Modificar director")
        print("12: Eliminar director")
        print("13: Agregar genero")
        print("14: Modificar genero")
        print("15: Eliminar genero")#
        print("16: Eliminar pelicula")
        print("17: Agregar pelicula")#
        print("18: Modificar pelicula")
        print("19: Salir")
        opcion=int(input("Ingresar opcion: "))
        print("")

        if (opcion==1):
            r=(requests.get("http://127.0.0.1:5000/peliculas"))
            r=r.json()
            for i in r:
                print(i)

        elif (opcion==2):
            r=(requests.get("http://127.0.0.1:5000/peliculas/imagen"))
            r=r.json()
            for key,value in r.items():
                print(key," : ",value)

        elif (opcion==3):
            r=(requests.get("http://127.0.0.1:5000/directores"))
            r=r.json()
            for i in r:
                print(i)

        elif (opcion==4): 
            id=input("Ingresar id del director: ")
            r=(requests.get("http://127.0.0.1:5000/directores/"+id))
            r=r.json()
            for i in r:
                print(i)

        elif (opcion==5):
            r=(requests.get("http://127.0.0.1:5000/usuarios"))
            r=r.json()
            for i in r:
                print(i)

        elif (opcion==6):
            r=(requests.get("http://127.0.0.1:5000/generos"))
            r=r.json()
            for i in r:
                print(i)
        

        elif (opcion==7):
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

        #elif (opcion==8):

        elif (opcion==9):
            if(usuario_privado==False):
                print("Permiso denegado, inicie sesion.")
            else:
                usuario=input("Ingresar usuario: ")
                r=(requests.delete("http://127.0.0.1:5000/usuarios/eliminar/"+usuario))
                print(r.content)

        elif (opcion==10):
            if(usuario_privado==False):
                print("Permiso denegado, inicie sesion.")
            else:
                director=input("Director: ")
                j={
                    "director":director,
                }
                r=(requests.post("http://127.0.0.1:5000/director/agregar",json=j))
                print(r.content)

        #elif (opcion==11):

        elif (opcion==12):
            if(usuario_privado==False):
                print("Permiso denegado, inicie sesion.")
            else:
                director=input("Ingresar director: ")
                r=(requests.delete("http://127.0.0.1:5000/director/eliminar/"+director))
                print(r.content)

        elif (opcion==13):
            if(usuario_privado==False):
                print("Permiso denegado, inicie sesion.")
            else:
                genero=input("Genero: ")
                j={
                    "genero":genero,
                }
                r=(requests.post("http://127.0.0.1:5000/genero/agregar",json=j))
                print(r.content)

        #elif (opcion==14):

        elif (opcion==15):
            if(usuario_privado==False):
                print("Permiso denegado, inicie sesion.")
            else:
                genero=input("Ingresar genero: ")
                r=(requests.delete("http://127.0.0.1:5000/peliculas/eliminar/"+genero))
                print(r.content)

        elif (opcion==16):
            if(usuario_privado==False):
                print("Permiso denegado, inicie sesion.")
            else:
                id=input("Ingresar id de la pelicula: ")
                r=(requests.delete("http://127.0.0.1:5000/peliculas/eliminar/"+id))
                print(r.content)

        elif (opcion==17):
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
                r=(requests.post("http://127.0.0.1:5000/usuarios/publicar",json=j))
                print(r.content)

        elif (opcion==18):
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
            
        elif (opcion==19):
            print("Nos vemos!\n")
            exit()

        else:
            print("Error al ingresar opcion")
        print("")

m = threading.Timer(1, menu)    # Ejecutar el menu 1 segundo despues para darle tiempo a crear local server
m.start()
