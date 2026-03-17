from tkinter import messagebox
from conexion import coleccion_grupos


def buscar_grupo_por_clave(campo_clave_grupo):
    
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



def eliminar_grupo(campo_clave_grupo):

    clave_grupo = campo_clave_grupo.get().strip()

    if not clave_grupo:
        messagebox.showwarning("Advertencia", "Ingrese la Clave a eliminar.")
        return
    
    # Verificar si el grupo existe
    grupo_existente = coleccion_grupos.find_one({"cveGru": clave_grupo})
    if not grupo_existente:
        messagebox.showinfo("Resultado", "No se encontró el grupo a eliminar.")
        return
    
    # Buscar si hay alumnos asociados al grupo
    alumnos_asociados = list(coleccion_alumnos.find({"cveGru": clave_grupo}))
    cantidad_alumnos = len(alumnos_asociados)
    
    # Confirmar eliminación con información de alumnos asociados
    mensaje_confirmacion = f"¿Está seguro de eliminar el grupo '{clave_grupo}'?"
    if cantidad_alumnos > 0:
        mensaje_confirmacion += f"\n\nTambién se eliminarán {cantidad_alumnos} alumno(s) asociado(s) a este grupo."
    
    if not messagebox.askyesno("Confirmación de Eliminación", mensaje_confirmacion):
        return
    
    try:
        # Eliminar en cascada: primero los alumnos asociados al grupo
        if cantidad_alumnos > 0:
            resultado_eliminacion_alumnos = coleccion_alumnos.delete_many({"cveGru": clave_grupo})
            print(f"Se eliminaron {resultado_eliminacion_alumnos.deleted_count} alumnos asociados al grupo {clave_grupo}")
        
        # Luego eliminar el grupo
        resultado_eliminacion_grupo = coleccion_grupos.delete_one({"cveGru": clave_grupo})
        
        if resultado_eliminacion_grupo.deleted_count > 0:
            mensaje_exito = f"Grupo eliminado correctamente."
            if cantidad_alumnos > 0:
                mensaje_exito += f"\nTambién se eliminaron {cantidad_alumnos} alumno(s) asociado(s)."
            messagebox.showinfo("Éxito", mensaje_exito)
            limpiar_campos_grupo(campo_clave_grupo, campo_nombre_grupo)
        else:
            messagebox.showerror("Error", "No se pudo eliminar el grupo.")
            
    except Exception as error_excepcion:
        messagebox.showerror("Error", f"Fallo al eliminar el grupo: {error_excepcion}")



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