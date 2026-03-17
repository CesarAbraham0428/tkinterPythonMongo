from tkinter import messagebox
from conexion import coleccion_alumnos


def buscar_alumno_por_clave(campo_clave_alumno):

    clave_alumno = campo_clave_alumno.get().strip()

    if not clave_alumno:
        messagebox.showwarning("Advertencia", "Ingrese la Clave a buscar.")
        return
    
    documento_alumno = coleccion_alumnos.find_one({"cveAlu": clave_alumno})

    if documento_alumno:
        campo_nombre_alumno.delete(0, "end")
        campo_nombre_alumno.insert(0, documento_alumno.get("nomAlu", ""))
        campo_edad_alumno.delete(0, "end")
        campo_edad_alumno.insert(0, documento_alumno.get("edad", ""))
        campo_clave_grupo.delete(0, "end")
        campo_clave_grupo.insert(0, documento_alumno.get("cveGrp", ""))
        
    else:
        messagebox.showinfo("Resultado", "No se encontró el alumno.")



def agregar_alumno(campo_clave_alumno, campo_nombre_alumno, campo_edad_alumno, campo_clave_grupo):
    
    clave_alumno = campo_clave_alumno.get().strip()
    nombre_alumno = campo_nombre_alumno.get().strip()
    edad_alumno = campo_edad_alumno.get().strip()
    clave_grupo = campo_clave_grupo.get().strip()

    if not clave_alumno or not nombre_alumno or not edad_alumno or not clave_grupo:
        messagebox.showwarning("Advertencia", "Ingrese todos los datos del Alumno.")
        return
    
    documento_existente = coleccion_alumnos.find_one({"cveAlu": clave_alumno})

    if documento_existente:
        messagebox.showwarning("Advertencia", "Clave de alumno repetida ya existe un alumno con esa clave.")
    else:
        coleccion_alumnos.insert_one({"cveAlu": clave_alumno, "nomAlu": nombre_alumno, "edad": edad_alumno, "cveGrp": clave_grupo})
        messagebox.showinfo("Éxito", "alumno agregado correctamente.")
        limpiar_campos_alumno(campo_clave_alumno, campo_nombre_alumno, campo_edad_alumno, campo_clave_grupo)



def modificar_alumno(campo_clave_alumno, campo_nombre_alumno, campo_edad_alumno, campo_clave_grupo):
    clave_alumno = campo_clave_alumno.get().strip()
    nombre_alumno = campo_nombre_alumno.get().strip()
    edad_alumno = campo_edad_alumno.get().strip()
    clave_grupo = campo_clave_grupo.get().strip()
    
    if not clave_alumno:
        messagebox.showwarning("Advertencia", "Ingrese Clave del Alumno a modificar.")
        return
    
    resultado_modificacion = coleccion_alumnos.update_one({"cveAlu": clave_alumno}, {"$set": {"nomAlu": nombre_alumno, "edad": edad_alumno, "cveGrp": clave_grupo}})
    if resultado_modificacion.matched_count > 0:
        messagebox.showinfo("Éxito", "alumno modificado correctamente.")
    else:
        messagebox.showinfo("Resultado", "No se encontró el alumno para modificar.")



def eliminar_alumno(campo_clave_alumno):
    clave_alumno = campo_clave_alumno.get().strip()
    if not clave_alumno:
        messagebox.showwarning("Advertencia", "Ingrese la Clave a eliminar.")
        return
    
    resultado_eliminacion = coleccion_alumnos.delete_one({"cveAlu": clave_alumno})
    if resultado_eliminacion.deleted_count > 0:
        messagebox.showinfo("Éxito", "alumno eliminado correctamente.")
        limpiar_campos_alumno()
    else:
        messagebox.showinfo("Resultado", "No se encontró el alumno para eliminar.")



def limpiar_campos_alumno(campo_clave_alumno, campo_nombre_alumno, campo_edad_alumno, campo_clave_grupo):
    campo_clave_alumno.delete(0, "end")
    campo_nombre_alumno.delete(0, "end")
    campo_edad_alumno.delete(0, "end")
    campo_clave_grupo.delete(0,"end")



def eliminar_todos_los_alumnos():
    if messagebox.askyesno("Confirmación", "¿Está seguro de eliminar TODOS los alumnos?"):
        try:
            resultado_eliminacion = coleccion_alumnos.delete_many({})
            messagebox.showinfo("Éxito", f"Se eliminaron {resultado_eliminacion.deleted_count} alumnos.")
        except Exception as error_excepcion:
            messagebox.showerror("Error", f"Fallo al eliminar: {error_excepcion}")