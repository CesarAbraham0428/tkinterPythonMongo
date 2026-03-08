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

    ruta = filedialog.asksaveasfilename(
        defaultextension=".json", filetypes=[("JSON files", "*.json")]
    )
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
            messagebox.showinfo(
                "Éxito", f"Se importaron {insertados} grupos desde JSON."
            )
        except Exception as e:
            messagebox.showerror("Error", f"Error al importar JSON: {e}")

#Abraham
def Exportar_XML():
    grupos = grupo.find()

    root = ET.Element("Grupos")

    for grupo in grupos:
        grupo_elem = ET.SubElement(root, "Grupo")
        ET.SubElement(grupo_elem, "Clave").text = grupo["cveGru"]
        ET.SubElement(grupo_elem, "Nombre").text = grupo["nomGru"]

    tree = ET.ElementTree(root)

    carpeta = r"C:\Backup_Mongo"
    archivo = os.path.join(carpeta, "grupos.xml")

    # crear carpeta si no existe
    os.makedirs(carpeta, exist_ok=True)

    tree.write(archivo, encoding="utf-8", xml_declaration=True)

    messagebox.showinfo("Exportación", f"Archivo exportado en:\n{archivo}")
    grupos = grupo.find()

    root = ET.Element("Grupos")
    for g in grupos:
        grupo_elem = ET.SubElement(root, "Grupo")
        ET.SubElement(grupo_elem, "Clave").text = g["cveGru"]
        ET.SubElement(grupo_elem, "Nombre").text = g["nomGru"]

    tree = ET.ElementTree(root)
    ruta = filedialog.asksaveasfilename(
        defaultextension=".xml", filetypes=[("XML files", "*.xml")]
    )
    if ruta:
        tree.write(ruta, encoding="utf-8", xml_declaration=True)


def Importar_XML():
    ruta = filedialog.askopenfilename(filetypes=[("XML files", "*.xml")])
    if ruta:
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
            messagebox.showinfo(
                "Éxito", f"Se importaron {insertados} grupos desde XML."
            )
        except Exception as e:
            messagebox.showerror("Error", f"Error al importar XML: {e}")

#Abraham
def Exportar_CSV():

    grupos = grupo.find()

    carpeta = r"C:\Backup_Mongo"
    archivo = os.path.join(carpeta, "grupos.csv")

    os.makedirs(carpeta, exist_ok=True)

    with open(archivo, mode="w", newline="", encoding="utf-8") as file:

        writer = csv.writer(file)

        # encabezados
        writer.writerow(["Clave", "Nombre"])

        # datos
        for g in grupos:
            writer.writerow([g["cveGru"], g["nomGru"]])

    messagebox.showinfo("Exportación", f"CSV exportado en:\n{archivo}")

#Abraham
def Importar_CSV():

    ruta = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])

    if not ruta:
        return

    with open(ruta, mode="r", encoding="utf-8") as file:

        lector = csv.DictReader(file)

        datos = []

        for fila in lector:
            documento = {"cveGru": fila["Clave"], "nomGru": fila["Nombre"]}
            datos.append(documento)

        if datos:
            grupo.insert_many(datos)

    messagebox.showinfo("Importación", "Datos importados correctamente")
