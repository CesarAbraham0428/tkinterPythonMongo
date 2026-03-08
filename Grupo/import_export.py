import json
import xml.etree.ElementTree as ET
from tkinter import filedialog, messagebox
from conexion import grupo

def Exportar_JSON():
    docs = list(grupo.find({}, {"_id": 0, "cveGru": 1, "nomGru": 1}))
    if not docs:
        messagebox.showinfo("Exportar", "No hay grupos para exportar.")
        return
        
    ruta = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
    if ruta:
        try:
            with open(ruta, "w", encoding="utf-8") as f:
                json.dump(docs, f, ensure_ascii=False, indent=4)
            messagebox.showinfo("Éxito", "Exportación a JSON completada.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar: {e}")

def Importar_JSON():
    ruta = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    if ruta:
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                datos = json.load(f)
            
            insertados = 0
            for doc in datos:
                cve = doc.get("cveGru")
                if cve and not grupo.find_one({"cveGru": cve}):
                    grupo.insert_one({"cveGru": cve, "nomGru": doc.get("nomGru", "")})
                    insertados += 1
            messagebox.showinfo("Éxito", f"Se importaron {insertados} grupos desde JSON.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al importar JSON: {e}")

def Exportar_XML():
    pass

def Importar_XML():
    ruta = filedialog.askopenfilename(filetypes=[("XML files", "*.xml")])
    if ruta:
        try:
            tree = ET.parse(ruta)
            root = tree.getroot()
            insertados = 0
            for g in root.findall('Grupo'):
                clave = g.find('Clave').text
                nombre = g.find('Nombre').text
                if clave and not grupo.find_one({"cveGru": clave}):
                    grupo.insert_one({"cveGru": clave, "nomGru": nombre or ""})
                    insertados += 1
            messagebox.showinfo("Éxito", f"Se importaron {insertados} grupos desde XML.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al importar XML: {e}")
