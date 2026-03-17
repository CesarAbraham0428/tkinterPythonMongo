from pymongo import MongoClient as MC

cliente_mongodb = MC("mongodb://localhost:27017/")

bd = cliente_mongodb["BD_GrupoAlumno"]

coleccion_alumnos = bd["Alumno"]
