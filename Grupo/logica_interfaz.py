from tkinter import messagebox
from conexion import coleccion_grupos
import import_export
import backup

def buscar_grupo_por_clave(campo_clave_grupo, campo_nombre_grupo):
    clave_grupo = campo_clave_grupo.get().strip()
    if not clave_grupo:
        messagebox.showwarning("Advertencia", "Ingrese la Clave a buscar.")
        return
    
    documento_grupo = coleccion_grupos.find_one({"cveGru": clave_grupo})
    if documento_grupo:
        campo_nombre_grupo.delete(0, "end")
        campo_nombre_grupo.insert(0, documento_grupo.get("nomGru", ""))
    else:
        messagebox.showinfo("Resultado", "No se encontró el grupo.")

#Abraham
def agregar_grupo(campo_clave_grupo, campo_nombre_grupo):
    clave_grupo = campo_clave_grupo.get().strip()
    nombre_grupo = campo_nombre_grupo.get().strip()
    if not clave_grupo or not nombre_grupo:
        messagebox.showwarning("Advertencia", "Ingrese la Clave y el Nombre.")
        return
    
    documento_existente = coleccion_grupos.find_one({"cveGru": clave_grupo})
    if documento_existente:
        messagebox.showwarning("Advertencia", "Clave de grupo repetida ya existe un grupo con esa clave.")
    else:
        coleccion_grupos.insert_one({"cveGru": clave_grupo, "nomGru": nombre_grupo})
        messagebox.showinfo("Éxito", "Grupo agregado correctamente.")
        limpiar_campos_grupo(campo_clave_grupo, campo_nombre_grupo)

def modificar_grupo(campo_clave_grupo, campo_nombre_grupo):
    clave_grupo = campo_clave_grupo.get().strip()
    nombre_grupo = campo_nombre_grupo.get().strip()
    
    if not clave_grupo or not nombre_grupo:
        messagebox.showwarning("Advertencia", "Ingrese Clave y Nombre a modificar.")
        return
    
    resultado_modificacion = coleccion_grupos.update_one({"cveGru": clave_grupo}, {"$set": {"nomGru": nombre_grupo}})
    if resultado_modificacion.matched_count > 0:
        messagebox.showinfo("Éxito", "Grupo modificado correctamente.")
    else:
        messagebox.showinfo("Resultado", "No se encontró el grupo para modificar.")

def eliminar_grupo(campo_clave_grupo, campo_nombre_grupo):
    clave_grupo = campo_clave_grupo.get().strip()
    if not clave_grupo:
        messagebox.showwarning("Advertencia", "Ingrese la Clave a eliminar.")
        return
    
    # Pendiente: Validacion de eliminacion en cascada con Alumnos.
    resultado_eliminacion = coleccion_grupos.delete_one({"cveGru": clave_grupo})
    if resultado_eliminacion.deleted_count > 0:
        messagebox.showinfo("Éxito", "Grupo eliminado correctamente.")
        limpiar_campos_grupo(campo_clave_grupo, campo_nombre_grupo)
    else:
        messagebox.showinfo("Resultado", "No se encontró el grupo para eliminar.")

def limpiar_campos_grupo(campo_clave_grupo, campo_nombre_grupo):
    campo_clave_grupo.delete(0, "end")
    campo_nombre_grupo.delete(0, "end")

def eliminar_todos_los_grupos():
    if messagebox.askyesno("Confirmación", "¿Está seguro de eliminar TODOS los grupos?"):
        try:
            resultado_eliminacion = coleccion_grupos.delete_many({})
            messagebox.showinfo("Éxito", f"Se eliminaron {resultado_eliminacion.deleted_count} grupos.")
        except Exception as error_excepcion:
            messagebox.showerror("Error", f"Fallo al eliminar: {error_excepcion}")