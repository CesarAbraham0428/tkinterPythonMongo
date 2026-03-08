from tkinter import messagebox
from conexion import grupo
import import_export
import backup

def Buscar(txt_cveGru, txt_nomGru):
    clave = txt_cveGru.get().strip()
    if not clave:
        messagebox.showwarning("Advertencia", "Ingrese la Clave a buscar.")
        return
    
    doc = grupo.find_one({"cveGru": clave})
    if doc:
        txt_nomGru.delete(0, "end")
        txt_nomGru.insert(0, doc.get("nomGru", ""))
    else:
        messagebox.showinfo("Resultado", "No se encontró el grupo.")

#Abraham
def Agregar(txt_cveGru, txt_nomGru):
    clave = txt_cveGru.get().strip()
    nombre = txt_nomGru.get().strip()
    if not clave or not nombre:
        messagebox.showwarning("Advertencia", "Ingrese la Clave y el Nombre.")
        return
    
    doc = grupo.find_one({"cveGru": clave})
    if doc:
        txt_nomGru.delete(0, "end")
        txt_nomGru.insert(0, doc.get("nomGru", ""))
    else:
        grupo.insert_one({"cveGru": clave, "nomGru": nombre})
        messagebox.showinfo("Éxito", "Grupo agregado correctamente.")

def Modificar(txt_cveGru, txt_nomGru):
    clave = txt_cveGru.get().strip()
    nombre = txt_nomGru.get().strip()
    
    if not clave or not nombre:
        messagebox.showwarning("Advertencia", "Ingrese Clave y Nombre a modificar.")
        return
    
    result = grupo.update_one({"cveGru": clave}, {"$set": {"nomGru": nombre}})
    if result.matched_count > 0:
        messagebox.showinfo("Éxito", "Grupo modificado correctamente.")
    else:
        messagebox.showinfo("Resultado", "No se encontró el grupo para modificar.")

def Eliminar(txt_cveGru, txt_nomGru):
    clave = txt_cveGru.get().strip()
    if not clave:
        messagebox.showwarning("Advertencia", "Ingrese la Clave a eliminar.")
        return
    
    # Pendiente: Validacion de eliminacion en cascada con Alumnos.
    result = grupo.delete_one({"cveGru": clave})
    if result.deleted_count > 0:
        messagebox.showinfo("Éxito", "Grupo eliminado correctamente.")
        Limpiar(txt_cveGru, txt_nomGru)
    else:
        messagebox.showinfo("Resultado", "No se encontró el grupo para eliminar.")

def Limpiar(txt_cveGru, txt_nomGru):
    txt_cveGru.delete(0, "end")
    txt_nomGru.delete(0, "end")

def EliminarTodos():
    if messagebox.askyesno("Confirmación", "¿Está seguro de eliminar TODOS los grupos?"):
        try:
            resultado = grupo.delete_many({})
            messagebox.showinfo("Éxito", f"Se eliminaron {resultado.deleted_count} grupos.")
        except Exception as e:
            messagebox.showerror("Error", f"Fallo al eliminar: {e}")