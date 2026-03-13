import json
import xml.etree.ElementTree as ET
import csv

import os

from tkinter import filedialog, messagebox

from conexion import coleccion_grupos


def exportar_json():
    documentos_grupos = list(coleccion_grupos.find({}, {"_id": 0, "cveGru": 1, "nomGru": 1}))
    if not documentos_grupos:
        messagebox.showinfo("Exportar", "No hay grupos para exportar.")
        return

    carpeta_backup = r"C:\Backup_Mongo"
    ruta_archivo = os.path.join(carpeta_backup, "grupos.json")

    os.makedirs(carpeta_backup, exist_ok=True)

    try:
        with open(ruta_archivo, "w", encoding="utf-8") as archivo_json:
            json.dump(documentos_grupos, archivo_json, ensure_ascii=False, indent=4)
        messagebox.showinfo("Éxito", f"Exportación a JSON completada en:\n{ruta_archivo}")
    except Exception as error_excepcion:
        messagebox.showerror("Error", f"Error al exportar JSON: {error_excepcion}")


def importar_json():
    carpeta_backup = r"C:\Backup_Mongo"
    ruta_archivo = os.path.join(carpeta_backup, "grupos.json")

    if not os.path.exists(ruta_archivo):
        messagebox.showerror("Error", f"No se encontró el archivo:\n{ruta_archivo}")
        return

    try:
        with open(ruta_archivo, "r", encoding="utf-8") as archivo_json:
            datos_importacion = json.load(archivo_json)

        grupos_insertados = 0
        for documento_grupo in datos_importacion:
            clave_grupo = documento_grupo.get("cveGru")
            if clave_grupo and not coleccion_grupos.find_one({"cveGru": clave_grupo}):
                coleccion_grupos.insert_one({"cveGru": clave_grupo, "nomGru": documento_grupo.get("nomGru", "")})
                grupos_insertados += 1
        messagebox.showinfo("Éxito", f"Se importaron {grupos_insertados} grupos desde JSON.")
    except Exception as error_excepcion:
        messagebox.showerror("Error", f"Error al importar JSON: {error_excepcion}")


def exportar_xml():
    documentos_grupos = list(coleccion_grupos.find({}, {"_id": 0, "cveGru": 1, "nomGru": 1}))
    if not documentos_grupos:
        messagebox.showinfo("Exportar", "No hay grupos para exportar.")
        return

    carpeta_backup = r"C:\Backup_Mongo"
    ruta_archivo = os.path.join(carpeta_backup, "grupos.xml")

    # crear carpeta si no existe
    os.makedirs(carpeta_backup, exist_ok=True)

    try:
        elemento_raiz = ET.Element("Grupos")
        for datos_grupo in documentos_grupos:
            elemento_grupo = ET.SubElement(elemento_raiz, "Grupo")
            ET.SubElement(elemento_grupo, "Clave").text = str(datos_grupo.get("cveGru", ""))
            ET.SubElement(elemento_grupo, "Nombre").text = str(datos_grupo.get("nomGru", ""))

        arbol_xml = ET.ElementTree(elemento_raiz)
        arbol_xml.write(ruta_archivo, encoding="utf-8", xml_declaration=True)
        messagebox.showinfo("Éxito", f"Exportación a XML completada en:\n{ruta_archivo}")
    except Exception as error_excepcion:
        messagebox.showerror("Error", f"Error al exportar XML: {error_excepcion}")


def importar_xml():
    carpeta_backup = r"C:\Backup_Mongo"
    ruta_archivo = os.path.join(carpeta_backup, "grupos.xml")

    if not os.path.exists(ruta_archivo):
        messagebox.showerror("Error", f"No se encontró el archivo:\n{ruta_archivo}")
        return

    try:
        arbol_xml = ET.parse(ruta_archivo)
        elemento_raiz = arbol_xml.getroot()
        grupos_insertados = 0
        for elemento_grupo in elemento_raiz.findall("Grupo"):
            clave_grupo = elemento_grupo.find("Clave").text
            nombre_grupo = elemento_grupo.find("Nombre").text
            if clave_grupo and not coleccion_grupos.find_one({"cveGru": clave_grupo}):
                coleccion_grupos.insert_one({"cveGru": clave_grupo, "nomGru": nombre_grupo or ""})
                grupos_insertados += 1
        messagebox.showinfo("Éxito", f"Se importaron {grupos_insertados} grupos desde XML.")
    except Exception as error_excepcion:
        messagebox.showerror("Error", f"Error al importar XML: {error_excepcion}")

def exportar_csv():
    documentos_grupos = list(coleccion_grupos.find({}, {"_id": 0, "cveGru": 1, "nomGru": 1}))
    if not documentos_grupos:
        messagebox.showinfo("Exportar", "No hay grupos para exportar.")
        return

    carpeta_backup = r"C:\Backup_Mongo"
    ruta_archivo = os.path.join(carpeta_backup, "grupos.csv")

    os.makedirs(carpeta_backup, exist_ok=True)

    try:
        with open(ruta_archivo, mode="w", newline="", encoding="utf-8") as archivo_csv:
            escritor_csv = csv.writer(archivo_csv)
            escritor_csv.writerow(["Clave", "Nombre"])
            for datos_grupo in documentos_grupos:
                escritor_csv.writerow([datos_grupo.get("cveGru", ""), datos_grupo.get("nomGru", "")])
        messagebox.showinfo("Éxito", f"Exportación a CSV completada en:\n{ruta_archivo}")
    except Exception as error_excepcion:
        messagebox.showerror("Error", f"Error al exportar CSV: {error_excepcion}")

def importar_csv():
    carpeta_backup = r"C:\Backup_Mongo"
    ruta_archivo = os.path.join(carpeta_backup, "grupos.csv")

    if not os.path.exists(ruta_archivo):
        messagebox.showerror("Error", f"No se encontró el archivo:\n{ruta_archivo}")
        return

    try:
        with open(ruta_archivo, mode="r", encoding="utf-8") as archivo_csv:
            lector_csv = csv.DictReader(archivo_csv)
            grupos_insertados = 0
            for fila_datos in lector_csv:
                clave_grupo = fila_datos.get("Clave")
                nombre_grupo = fila_datos.get("Nombre")
                if clave_grupo and not coleccion_grupos.find_one({"cveGru": clave_grupo}):
                    coleccion_grupos.insert_one({"cveGru": clave_grupo, "nomGru": nombre_grupo or ""})
                    grupos_insertados += 1
        messagebox.showinfo("Éxito", f"Se importaron {grupos_insertados} grupos desde CSV.")
    except Exception as error_excepcion:
        messagebox.showerror("Error", f"Error al importar CSV: {error_excepcion}")
