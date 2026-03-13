from pymongo import MongoClient as ClienteMongo

cliente_mongodb = ClienteMongo("mongodb://localhost:27017/")

base_datos_grupos = cliente_mongodb["BD_GrupoAlumno"]

coleccion_grupos = base_datos_grupos["Grupo"]
