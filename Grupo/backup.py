#Abraham
from tkinter import messagebox


import os


def ejecutar_backup_completo():
    comando_mongodump = '"C:\\Program Files\\MongoDB\\Tools\\100\\bin\\mongodump.exe" --db BD_GrupoAlumno --out C:\\Backup_Mongo'

    os.system(comando_mongodump)
    messagebox.showinfo("Éxito", f"Se Realizo el Backup Correctamente.")


def restaurar_todos_los_grupos():
    comando_mongorestore = '"C:\\Program Files\\MongoDB\\Tools\\100\\bin\\mongorestore.exe" --db BD_GrupoAlumno --collection Grupo C:\\Backup_Mongo\\BD_GrupoAlumno\\Grupo.bson'
    os.system(comando_mongorestore)
    messagebox.showinfo("Éxito", f"Se Restauraron todos los grupos correctamente.")
