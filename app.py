import json
import funciones as fc
from flask import Flask, jsonify, Response, request
from http import HTTPStatus
import threading
import os

app = Flask(__name__)


with open("usuarios.json",encoding='utf-8') as usuarios_json:
    usuarios=json.load(usuarios_json)
usuarios=usuarios[0]['usuarios']

with open("directores.json",encoding='utf-8') as directores_json:
    directores=json.load(directores_json)
directores=directores[0]['directores']

with open("peliculas.json",encoding='utf-8') as peliculas_json:
    peliculas=json.load(peliculas_json) 
peliculas=peliculas[0]['peliculas']


@app.route("/")
def menu():
    login=False
    def menu():
        print("")
        while True:
            print("Sistema de entradas: CINE")
            print("----------------------------")
            print("1: Mostrar todas las peliculas")
            print("2: Mostrar peliculas con imagenes")
            print("3: Mostrar directores")
            print("4: Mostrar peliculas de un director especifico")
            print("5: Mostrar usuarios")
            print("6: Mostrar generos")
            print("7: Eliminar pelicula")
            print("8: Publicar pelicula")
            print("9: Modificar pelicula")
            print("10: Salir")
            opcion=int(input("Ingresar opcion: "))
            print("")

            if (opcion==0):
                global login
                if(login==False):
                    user=input("Ingresar usuario: ")
                    password=input('Ingresar contraseña: ')
                    for usuario in usuarios:
                        if(user in usuario['usuario'] and password in usuario['contrasenia']):
                            login=True
                    if (login==True):
                        print("Inicio de sesion exitoso")
                    else:
                        print("Error al iniciar sesion")
                else:
                    login=False
                    print("Sesion cerrada")

            elif (opcion==1):
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
                if(login==False):
                    print("Permiso denegado, inicie sesion.")
                else:
                    id=input("Ingresar id de la pelicula: ")
                    r=(requests.delete("http://127.0.0.1:5000/peliculas/eliminar/"+id))
                    print(r.content)

            elif (opcion==8):
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

            elif (opcion==9):
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

            elif (opcion==10):
                print("Exit!\n")
                exit()

            else:
                print("Error al ingresar opcion")
            print("")


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
        mostrar_peliculas.append(pelicula['titulo'])
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
    
#--------------- Eliminar pelicula por id---------------
    
@app.route("/peliculas/eliminar/<int:id>",methods=["DELETE"])      # Elimina una pelicula por id 
def eliminar_pelicula(id):
    id_int=int(id)
    valor=False
    for pelicula in peliculas:
        if pelicula['id']==id_int:
            peliculas.remove(pelicula)
            valor=True
    if valor==True:
        # with open("biblioteca.json",'w',encoding='utf-8') as biblioteca_json:   # Lo eliminamos del json
        #     json.dump(peliculas,biblioteca_json)
        return Response("Eliminado",status=HTTPStatus.OK)
    else:
        return Response("No se pudo elimianr este pelicula",status=HTTPStatus.BAD_REQUEST)
    
#ABM 
@app.route("/comentario/create/idPelicula/<idPelicula>", methods=['POST'])
def createComentarios(idPelicula):
    #Obteneniendo JSONs
    comentarios = fc.obtenerComentarios()
    peliculas = fc.obtenerPeliculas()
    id = fc.nuevoIdComentario()

    comentarioNuevo = request.get_json()
    comentarioNuevo["id"] = id
    comentarios.append(comentarioNuevo)

for pelicula in peliculas:
    if pelicula['id'] == idPelicula:
        pelicula['idComentarios'].append(id)
