import json
import xml.etree.ElementTree as ET
import csv

import os

from tkinter import messagebox

from conexion import coleccion_alumnos


def exportar_json():
    documentos_alumnos = list(coleccion_alumnos.find({}, {"_id": 0, "cveAlu": 1, "nomAlu": 1}))
    if not documentos_alumnos:
        messagebox.showinfo("Exportar", "No hay alumnos para exportar.")
        return

    carpeta_backup = r"C:\Backup_Mongo"
    ruta_archivo = os.path.join(carpeta_backup, "alumnos.json")

    os.makedirs(carpeta_backup, exist_ok=True)

    try:
        with open(ruta_archivo, "w", encoding="utf-8") as archivo_json:
            json.dump(documentos_alumnos, archivo_json, ensure_ascii=False, indent=4)
        messagebox.showinfo("Éxito", f"Exportación a JSON completada en:\n{ruta_archivo}")
    except Exception as error_excepcion:
        messagebox.showerror("Error", f"Error al exportar JSON: {error_excepcion}")



def importar_json():
    carpeta_backup = r"C:\Backup_Mongo"
    ruta_archivo = os.path.join(carpeta_backup, "alumnos.json")

    if not os.path.exists(ruta_archivo):
        messagebox.showerror("Error", f"No se encontró el archivo:\n{ruta_archivo}")
        return

    try:
        with open(ruta_archivo, "r", encoding="utf-8") as archivo_json:
            datos_importacion = json.load(archivo_json)

        alumnos_insertados = 0
        for documento_alumno in datos_importacion:
            clave_alumno = documento_alumno.get("cveAlu")
            if clave_alumno and not coleccion_alumnos.find_one({"cveAlu": clave_alumno}):
                coleccion_alumnos.insert_one({"cveAlu": clave_alumno, "nomAlu": documento_alumno.get("nomAlu", "")})
                alumnos_insertados += 1
        messagebox.showinfo("Éxito", f"Se importaron {alumnos_insertados} alumnos desde JSON.")
    except Exception as error_excepcion:
        messagebox.showerror("Error", f"Error al importar JSON: {error_excepcion}")



def exportar_xml():
    documentos_alumnos = list(coleccion_alumnos.find({}, {"_id": 0, "cveAlu": 1, "nomAlu": 1}))
    if not documentos_alumnos:
        messagebox.showinfo("Exportar", "No hay alumnos para exportar.")
        return

    carpeta_backup = r"C:\Backup_Mongo"
    ruta_archivo = os.path.join(carpeta_backup, "alumnos.xml")

    # crear carpeta si no existe
    os.makedirs(carpeta_backup, exist_ok=True)

    try:
        elemento_raiz = ET.Element("alumnos")
        for datos_alumno in documentos_alumnos:
            elemento_alumno = ET.SubElement(elemento_raiz, "alumno")
            ET.SubElement(elemento_alumno, "Clave").text = str(datos_alumno.get("cveAlu", ""))
            ET.SubElement(elemento_alumno, "Nombre").text = str(datos_alumno.get("nomAlu", ""))

        arbol_xml = ET.ElementTree(elemento_raiz)
        arbol_xml.write(ruta_archivo, encoding="utf-8", xml_declaration=True)
        messagebox.showinfo("Éxito", f"Exportación a XML completada en:\n{ruta_archivo}")
    except Exception as error_excepcion:
        messagebox.showerror("Error", f"Error al exportar XML: {error_excepcion}")



def importar_xml():
    carpeta_backup = r"C:\Backup_Mongo"
    ruta_archivo = os.path.join(carpeta_backup, "alumnos.xml")

    if not os.path.exists(ruta_archivo):
        messagebox.showerror("Error", f"No se encontró el archivo:\n{ruta_archivo}")
        return

    try:
        arbol_xml = ET.parse(ruta_archivo)
        elemento_raiz = arbol_xml.getroot()
        alumnos_insertados = 0
        for elemento_alumno in elemento_raiz.findall("alumno"):
            clave_alumno = elemento_alumno.find("Clave").text
            nombre_alumno = elemento_alumno.find("Nombre").text
            if clave_alumno and not coleccion_alumnos.find_one({"cveAlu": clave_alumno}):
                coleccion_alumnos.insert_one({"cveAlu": clave_alumno, "nomAlu": nombre_alumno or ""})
                alumnos_insertados += 1
        messagebox.showinfo("Éxito", f"Se importaron {alumnos_insertados} alumnos desde XML.")
    except Exception as error_excepcion:
        messagebox.showerror("Error", f"Error al importar XML: {error_excepcion}")



def exportar_csv():
    documentos_alumnos = list(coleccion_alumnos.find({}, {"_id": 0, "cveAlu": 1, "nomAlu": 1}))
    if not documentos_alumnos:
        messagebox.showinfo("Exportar", "No hay alumnos para exportar.")
        return

    carpeta_backup = r"C:\Backup_Mongo"
    ruta_archivo = os.path.join(carpeta_backup, "alumnos.csv")

    os.makedirs(carpeta_backup, exist_ok=True)

    try:
        with open(ruta_archivo, mode="w", newline="", encoding="utf-8") as archivo_csv:
            escritor_csv = csv.writer(archivo_csv)
            escritor_csv.writerow(["Clave", "Nombre"])
            for datos_alumno in documentos_alumnos:
                escritor_csv.writerow([datos_alumno.get("cveAlu", ""), datos_alumno.get("nomAlu", "")])
        messagebox.showinfo("Éxito", f"Exportación a CSV completada en:\n{ruta_archivo}")
    except Exception as error_excepcion:
        messagebox.showerror("Error", f"Error al exportar CSV: {error_excepcion}")



def importar_csv():
    carpeta_backup = r"C:\Backup_Mongo"
    ruta_archivo = os.path.join(carpeta_backup, "alumnos.csv")

    if not os.path.exists(ruta_archivo):
        messagebox.showerror("Error", f"No se encontró el archivo:\n{ruta_archivo}")
        return

    try:
        with open(ruta_archivo, mode="r", encoding="utf-8") as archivo_csv:
            lector_csv = csv.DictReader(archivo_csv)
            alumnos_insertados = 0
            for fila_datos in lector_csv:
                clave_alumno = fila_datos.get("Clave")
                nombre_alumno = fila_datos.get("Nombre")
                if clave_alumno and not coleccion_alumnos.find_one({"cveAlu": clave_alumno}):
                    coleccion_alumnos.insert_one({"cveAlu": clave_alumno, "nomAlu": nombre_alumno or ""})
                    alumnos_insertados += 1
        messagebox.showinfo("Éxito", f"Se importaron {alumnos_insertados} alumnos desde CSV.")
    except Exception as error_excepcion:
        messagebox.showerror("Error", f"Error al importar CSV: {error_excepcion}")
