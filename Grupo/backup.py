#Abraham
from tkinter import messagebox


import os


def Ejecutar_Backup():
    comando = '"C:\\Program Files\\MongoDB\\Tools\\100\\bin\\mongodump.exe" --db BD_GrupoAlumno --out C:\\Backup_Mongo'

    os.system(comando)
    messagebox.showinfo("Éxito", f"Se Realizo el Backup Correctamente.")


def Restaurar_Todos():
    comando = '"C:\\Program Files\\MongoDB\\Tools\\100\\bin\\mongorestore.exe" --db BD_GrupoAlumno --collection Grupo C:\\Backup_Mongo\\BD_GrupoAlumno\\Grupo.bson'
    os.system(comando)
    messagebox.showinfo("Éxito", f"Se Restauraron todos los grupos correctamente.")
