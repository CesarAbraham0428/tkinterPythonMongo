import json
import xml.etree.ElementTree as ET
import csv

import os

from tkinter import filedialog, messagebox

from conexion import grupo


def Exportar_JSON():
    docs = list(grupo.find({}, {"_id": 0, "cveGru": 1, "nomGru": 1}))
    if not docs:
        messagebox.showinfo("Exportar", "No hay grupos para exportar.")
        return

    carpeta = r"C:\Backup_Mongo"
    archivo = os.path.join(carpeta, "grupos.json")

    os.makedirs(carpeta, exist_ok=True)

    try:
        with open(archivo, "w", encoding="utf-8") as f:
            json.dump(docs, f, ensure_ascii=False, indent=4)
        messagebox.showinfo("Éxito", f"Exportación a JSON completada en:\n{archivo}")
    except Exception as e:
        messagebox.showerror("Error", f"Error al exportar JSON: {e}")


def Importar_JSON():
    carpeta = r"C:\Backup_Mongo"
    ruta = os.path.join(carpeta, "grupos.json")

    if not os.path.exists(ruta):
        messagebox.showerror("Error", f"No se encontró el archivo:\n{ruta}")
        return

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
    docs = list(grupo.find({}, {"_id": 0, "cveGru": 1, "nomGru": 1}))
    if not docs:
        messagebox.showinfo("Exportar", "No hay grupos para exportar.")
        return

    carpeta = r"C:\Backup_Mongo"
    archivo = os.path.join(carpeta, "grupos.xml")

    # crear carpeta si no existe
    os.makedirs(carpeta, exist_ok=True)

    try:
        root = ET.Element("Grupos")
        for g in docs:
            grupo_elem = ET.SubElement(root, "Grupo")
            ET.SubElement(grupo_elem, "Clave").text = str(g.get("cveGru", ""))
            ET.SubElement(grupo_elem, "Nombre").text = str(g.get("nomGru", ""))

        tree = ET.ElementTree(root)
        tree.write(archivo, encoding="utf-8", xml_declaration=True)
        messagebox.showinfo("Éxito", f"Exportación a XML completada en:\n{archivo}")
    except Exception as e:
        messagebox.showerror("Error", f"Error al exportar XML: {e}")


def Importar_XML():
    carpeta = r"C:\Backup_Mongo"
    ruta = os.path.join(carpeta, "grupos.xml")

    if not os.path.exists(ruta):
        messagebox.showerror("Error", f"No se encontró el archivo:\n{ruta}")
        return

    try:
        tree = ET.parse(ruta)
        root = tree.getroot()
        insertados = 0
        for g in root.findall("Grupo"):
            clave = g.find("Clave").text
            nombre = g.find("Nombre").text
            if clave and not grupo.find_one({"cveGru": clave}):
                grupo.insert_one({"cveGru": clave, "nomGru": nombre or ""})
                insertados += 1
        messagebox.showinfo("Éxito", f"Se importaron {insertados} grupos desde XML.")
    except Exception as e:
        messagebox.showerror("Error", f"Error al importar XML: {e}")

def Exportar_CSV():
    docs = list(grupo.find({}, {"_id": 0, "cveGru": 1, "nomGru": 1}))
    if not docs:
        messagebox.showinfo("Exportar", "No hay grupos para exportar.")
        return

    carpeta = r"C:\Backup_Mongo"
    archivo = os.path.join(carpeta, "grupos.csv")

    os.makedirs(carpeta, exist_ok=True)

    try:
        with open(archivo, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Clave", "Nombre"])
            for g in docs:
                writer.writerow([g.get("cveGru", ""), g.get("nomGru", "")])
        messagebox.showinfo("Éxito", f"Exportación a CSV completada en:\n{archivo}")
    except Exception as e:
        messagebox.showerror("Error", f"Error al exportar CSV: {e}")

def Importar_CSV():
    carpeta = r"C:\Backup_Mongo"
    ruta = os.path.join(carpeta, "grupos.csv")

    if not os.path.exists(ruta):
        messagebox.showerror("Error", f"No se encontró el archivo:\n{ruta}")
        return

    try:
        with open(ruta, mode="r", encoding="utf-8") as file:
            lector = csv.DictReader(file)
            insertados = 0
            for fila in lector:
                cve = fila.get("Clave")
                nom = fila.get("Nombre")
                if cve and not grupo.find_one({"cveGru": cve}):
                    grupo.insert_one({"cveGru": cve, "nomGru": nom or ""})
                    insertados += 1
        messagebox.showinfo("Éxito", f"Se importaron {insertados} grupos desde CSV.")
    except Exception as e:
        messagebox.showerror("Error", f"Error al importar CSV: {e}")
