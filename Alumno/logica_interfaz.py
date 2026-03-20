from tkinter import messagebox
from conexion import coleccion_alumnos


def buscar_alumno_por_clave(campo_clave_alumno, campo_nombre_alumno, campo_edad_alumno, campo_clave_grupo):

    clave_alumno_str = campo_clave_alumno.get().strip()

    if not clave_alumno_str:
        messagebox.showwarning("Advertencia", "Ingrese la Clave a buscar.")
        return
    
    try:
        clave_alumno = int(clave_alumno_str)
    except ValueError:
        messagebox.showwarning("Advertencia", "La clave debe ser un número entero.")
        return
    
    documento_alumno = coleccion_alumnos.find_one({"cveAlu": clave_alumno})

    if documento_alumno:
        campo_nombre_alumno.delete(0, "end")
        campo_nombre_alumno.insert(0, documento_alumno.get("nomAlu", ""))
        campo_edad_alumno.delete(0, "end")
        campo_edad_alumno.insert(0, str(documento_alumno.get("edadAlu", "")))
        campo_clave_grupo.delete(0, "end")
        campo_clave_grupo.insert(0, str(documento_alumno.get("cveGru", "")))
        
    else:
        messagebox.showinfo("Resultado", "No se encontró el alumno.")



def agregar_alumno(campo_clave_alumno, campo_nombre_alumno, campo_edad_alumno, campo_clave_grupo):
    
    clave_alumno_str = campo_clave_alumno.get().strip()
    nombre_alumno = campo_nombre_alumno.get().strip()
    edad_alumno_str = campo_edad_alumno.get().strip()
    clave_grupo = campo_clave_grupo.get().strip()

    if not clave_alumno_str or not nombre_alumno or not edad_alumno_str or not clave_grupo:
        messagebox.showwarning("Advertencia", "Ingrese todos los datos del Alumno.")
        return
    
    try:
        clave_alumno = int(clave_alumno_str)
        edad_alumno = int(edad_alumno_str)
    except ValueError:
        messagebox.showwarning("Advertencia", "La clave del Alumno y la edad deben ser números enteros.")
        return
    
    # Validar que el nombre sea texto y no números
    if nombre_alumno.isdigit():
        messagebox.showwarning("Advertencia", "El nombre del alumno debe ser texto, no números.")
        return
    
    documento_existente = coleccion_alumnos.find_one({"cveAlu": clave_alumno})

    if documento_existente:
        messagebox.showwarning("Advertencia", "Clave de alumno repetida ya existe un alumno con esa clave.")
    else:
        coleccion_alumnos.insert_one({"cveAlu": clave_alumno, "nomAlu": nombre_alumno, "edadAlu": int(edad_alumno), "cveGru": clave_grupo})
        messagebox.showinfo("Éxito", "alumno agregado correctamente.")
        limpiar_campos_alumno(campo_clave_alumno, campo_nombre_alumno, campo_edad_alumno, campo_clave_grupo)



def modificar_alumno(campo_clave_alumno, campo_nombre_alumno, campo_edad_alumno, campo_clave_grupo):
    clave_alumno_str = campo_clave_alumno.get().strip()
    nombre_alumno = campo_nombre_alumno.get().strip()
    edad_alumno_str = campo_edad_alumno.get().strip()
    clave_grupo = campo_clave_grupo.get().strip()
    
    if not clave_alumno_str:
        messagebox.showwarning("Advertencia", "Ingrese Clave del Alumno a modificar.")
        return
    
    try:
        clave_alumno = int(clave_alumno_str)
    except ValueError:
        messagebox.showwarning("Advertencia", "La clave debe ser un número entero.")
        return
    
    # Verificar si el alumno existe
    alumno_existente = coleccion_alumnos.find_one({"cveAlu": clave_alumno})
    if not alumno_existente:
        messagebox.showinfo("Resultado", "No se encontró el alumno para modificar.")
        return
    
    # Construir dinámicamente los campos a modificar
    campos_a_modificar = {}
    
    if nombre_alumno:
        # Validar que el nombre sea texto y no números
        if nombre_alumno.isdigit():
            messagebox.showwarning("Advertencia", "El nombre del alumno debe ser texto, no números.")
            return
        campos_a_modificar["nomAlu"] = nombre_alumno
    
    if edad_alumno_str:
        try:
            campos_a_modificar["edadAlu"] = int(edad_alumno_str)
        except ValueError:
            messagebox.showwarning("Advertencia", "La edad debe ser un número entero.")
            return
    
    if clave_grupo:
        campos_a_modificar["cveGru"] = clave_grupo
    
    if not campos_a_modificar:
        messagebox.showwarning("Advertencia", "Ingrese al menos un campo para modificar (nombre, edad o clave del grupo).")
        return
    
    # Realizar la modificación solo con los campos proporcionados
    resultado_modificacion = coleccion_alumnos.update_one({"cveAlu": clave_alumno}, {"$set": campos_a_modificar})
    if resultado_modificacion.matched_count > 0:
        messagebox.showinfo("Éxito", "alumno modificado correctamente.")
        # Limpiar todos los campos después de una modificación exitosa
        limpiar_campos_alumno(campo_clave_alumno, campo_nombre_alumno, campo_edad_alumno, campo_clave_grupo)
    else:
        messagebox.showinfo("Resultado", "No se pudo modificar el alumno.")



def eliminar_alumno(campo_clave_alumno, campo_nombre_alumno, campo_edad_alumno, campo_clave_grupo):
    clave_alumno_str = campo_clave_alumno.get().strip()
    if not clave_alumno_str:
        messagebox.showwarning("Advertencia", "Ingrese la Clave a eliminar.")
        return
    
    try:
        clave_alumno = int(clave_alumno_str)
    except ValueError:
        messagebox.showwarning("Advertencia", "La clave debe ser un número entero.")
        return
    
    resultado_eliminacion = coleccion_alumnos.delete_one({"cveAlu": clave_alumno})
    if resultado_eliminacion.deleted_count > 0:
        messagebox.showinfo("Éxito", "alumno eliminado correctamente.")
        limpiar_campos_alumno(campo_clave_alumno, campo_nombre_alumno, campo_edad_alumno, campo_clave_grupo)
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