from pymongo import MongoClient as MC

cliente = MC("mongodb://localhost:27017/")

db = cliente["BD_GrupoAlumno"]

alumno = db["Alumno"]
