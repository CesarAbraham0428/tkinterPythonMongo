from pymongo import MongoClient as ClienteMongo

cliente_mongodb = ClienteMongo("mongodb://localhost:27017/")

bd = cliente_mongodb["BD_GrupoAlumno"]

coleccion_grupos = bd["Grupo"]
