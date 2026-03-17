#Abraham
from tkinter import messagebox

import os


def ejecutar_backup_completo():
    comando_mongodump = '"C:\\Program Files\\MongoDB\\Tools\\100\\bin\\mongodump.exe" --db BD_GrupoAlumno --out C:\\Backup_Mongo'

    os.system(comando_mongodump)
    messagebox.showinfo("Éxito", f"Se Realizo el Backup Correctamente.")


def restaurar_todos_los_alumnos():

    ruta_backup = r"C:\Backup_Mongo\BD_GrupoAlumno\Alumno.bson"

    # Validar si existe el archivo de respaldo
    if not os.path.exists(ruta_backup):
        messagebox.showwarning("Advertencia", "No existe el archivo de respaldo para restaurar.")
        return

    comando_mongorestore = '"C:\\Program Files\\MongoDB\\Tools\\100\\bin\\mongorestore.exe" --db BD_GrupoAlumno --collection Alumno C:\\Backup_Mongo\\BD_GrupoAlumno\\Alumno.bson'
    
    os.system(comando_mongorestore)

    messagebox.showinfo("Éxito", "Se restauraron todos los alumnos correctamente.")
