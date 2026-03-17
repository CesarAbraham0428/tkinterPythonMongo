import tkinter as tk
from tkinter import ttk

import logica_interfaz as li
import import_export as ie

import backup as bk

ventana_principal = tk.Tk()
ventana_principal.title("Admon Alumnos")
ventana_principal.geometry("750x650")
ventana_principal.resizable(False, False)

# Colores y fuentes base
COLOR_FONDO = "#F4F6F9"
COLOR_OSCURO = "#2B2D42"
VERDE = "#4CAF50"
AZUL = "#2196F3"
NARANJA = "#FF9800"
ROJO = "#F44336"
COLOR_TEXTO_BOTON = "#FFFFFF"

FONT_TITLE = ("Segoe UI", 16, "bold")
FONT_LABEL = ("Segoe UI", 11)
FONT_ENTRY = ("Segoe UI", 12)
FONT_BTN = ("Segoe UI", 11, "bold")

ventana_principal.config(bg=COLOR_FONDO)

estilo_interfaz = ttk.Style()
estilo_interfaz.theme_use('clam')

# Estilo para Frames
estilo_interfaz.configure("TFrame", background=COLOR_FONDO)
estilo_interfaz.configure("Card.TFrame", background="#FFFFFF", relief="flat")

# Estilos universales para Entries
estilo_interfaz.configure("TEntry", fieldbackground="#FFFFFF", font=FONT_ENTRY, padding=5)

# Función helper para crear botones tkinter con Hover
def crear_boton_personalizado(contenedor_padre, texto_boton, comando_boton, color_fondo_boton, color_texto_boton=COLOR_TEXTO_BOTON, ancho_boton=15):
    boton_personalizado = tk.Button(contenedor_padre, text=texto_boton, font=FONT_BTN, command=comando_boton,
                    bg=color_fondo_boton, fg=color_texto_boton, width=ancho_boton,
                    relief="flat", cursor="hand2", pady=8)

        
    boton_personalizado.bind("<Enter>")
    boton_personalizado.bind("<Leave>")
    return boton_personalizado


# ======= HEADER =======
marco_encabezado = tk.Frame(ventana_principal, bg=COLOR_OSCURO, pady=15)
marco_encabezado.pack(fill="x", side="top")
etiqueta_titulo = tk.Label(marco_encabezado, text="Gestión de Alumnos", bg=COLOR_OSCURO, fg="#FFFFFF", font=FONT_TITLE)
etiqueta_titulo.pack()

marco_contenedor = ttk.Frame(ventana_principal)
marco_contenedor.pack(fill="both", expand=True)

lienzo_interfaz = tk.Canvas(marco_contenedor, bg=COLOR_FONDO, highlightthickness=0)
lienzo_interfaz.pack(side="left", fill="both", expand=True)

# Crear la Scrollbar
barra_desplazamiento = ttk.Scrollbar(marco_contenedor, orient="vertical", command=lienzo_interfaz.yview)
barra_desplazamiento.pack(side="right", fill="y")
lienzo_interfaz.configure(yscrollcommand=barra_desplazamiento.set)

# Crear el frame que realmente tendrá los widgets
contenedor_principal = ttk.Frame(lienzo_interfaz, padding=20)
estilo_interfaz.configure("TFrame", background=COLOR_FONDO)

ventana_lienzo = lienzo_interfaz.create_window((0, 0), window=contenedor_principal, anchor="nw")

# Funciones para actualizar la región de scroll automáticamente
def al_configurar_contenedor(evento):
    lienzo_interfaz.configure(scrollregion=lienzo_interfaz.bbox("all"))

def al_configurar_lienzo(evento):
    # Hacer que el contenedor_principal tome el ancho del lienzo_interfaz si es menor
    lienzo_interfaz.itemconfig(ventana_lienzo, width=evento.width)

contenedor_principal.bind("<Configure>", al_configurar_contenedor)
lienzo_interfaz.bind("<Configure>", al_configurar_lienzo)

# Soporte para rueda del ratón
def _al_mover_rueda_ratón(evento):
    lienzo_interfaz.yview_scroll(int(-1*(evento.delta/120)), "units")
ventana_principal.bind_all("<MouseWheel>", _al_mover_rueda_ratón)

# BÚSQUEDA Y DATOS

marco_busqueda = tk.Frame(contenedor_principal, bg="#FFFFFF", padx=20, pady=20, relief="solid", bd=1)
marco_busqueda.pack(fill="x", pady=(0, 15))

# Campos

tk.Label(marco_busqueda, text="Clave del Alumno:", bg="#FFFFFF", font=FONT_LABEL, fg=COLOR_OSCURO).grid(row=0, column=0, sticky="w", pady=5)
campo_clave_alumno = tk.Entry(marco_busqueda, font=FONT_ENTRY, width=25, relief="solid", bd=1)
campo_clave_alumno.grid(row=0, column=1, padx=10, pady=5)

tk.Label(marco_busqueda, text="Nombre del Alumno:", bg="#FFFFFF", font=FONT_LABEL, fg=COLOR_OSCURO).grid(row=1, column=0, sticky="w", pady=5)
campo_nombre_alumno = tk.Entry(marco_busqueda, font=FONT_ENTRY, width=25, relief="solid", bd=1)
campo_nombre_alumno.grid(row=1, column=1, padx=10, pady=5)

tk.Label(marco_busqueda, text="Edad del Alumno:", bg="#FFFFFF", font=FONT_LABEL, fg=COLOR_OSCURO).grid(row=2, column=0, sticky="w", pady=5)
campo_edad_alumno = tk.Entry(marco_busqueda, font=FONT_ENTRY, width=25, relief="solid", bd=1)
campo_edad_alumno.grid(row=2, column=1, padx=10, pady=5)

tk.Label(marco_busqueda, text="Clave Grupo:", bg="#FFFFFF", font=FONT_LABEL, fg=COLOR_OSCURO).grid(row=3, column=0, sticky="w", pady=5)
campo_clave_grupo = tk.Entry(marco_busqueda, font=FONT_ENTRY, width=25, relief="solid", bd=1)
campo_clave_grupo.grid(row=3, column=1, padx=10, pady=5)

# Botones

boton_buscar = crear_boton_personalizado(marco_busqueda, "Buscar", lambda: li.buscar_alumno_por_clave(campo_clave_alumno, campo_nombre_alumno), AZUL)
boton_buscar.grid(row=0, column=2, padx=(20,5), pady=5)

boton_limpiar = crear_boton_personalizado(marco_busqueda, "Limpiar", lambda: li.limpiar_campos_alumno(campo_clave_alumno, campo_nombre_alumno), "#9E9E9E")
boton_limpiar.grid(row=1, column=2, padx=(20,5), pady=5)

#OPERACIONES CRUD Y ARCHIVOS

marco_operaciones = tk.Frame(contenedor_principal, bg=COLOR_FONDO)
marco_operaciones.pack(fill="x", pady=(0, 15))

marco_operaciones.grid_columnconfigure(0, weight=1)
marco_operaciones.grid_columnconfigure(1, weight=1)

# Acciones de Registro

marco_crud = tk.LabelFrame(marco_operaciones, text=" Acciones de Registro ", bg=COLOR_FONDO, font=FONT_LABEL, fg=COLOR_OSCURO, pady=10, padx=10)
marco_crud.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

crear_boton_personalizado(marco_crud, "Agregar", lambda: li.agregar_alumno(campo_clave_alumno, campo_nombre_alumno, campo_edad_alumno, campo_clave_alumno), VERDE, ancho_boton=20).pack(pady=5)
crear_boton_personalizado(marco_crud, "Modificar", lambda: li.modificar_alumno(campo_clave_alumno, campo_nombre_alumno, campo_edad_alumno, campo_clave_alumno), NARANJA, ancho_boton=20).pack(pady=5)
crear_boton_personalizado(marco_crud, "Eliminar", lambda: li.eliminar_alumno(campo_clave_alumno, campo_nombre_alumno), ROJO, ancho_boton=20).pack(pady=5)

# Importación y Exportación
marco_exportacion = tk.LabelFrame(marco_operaciones, text=" Importación / Exportación ", bg=COLOR_FONDO, font=FONT_LABEL, fg=COLOR_OSCURO, pady=10, padx=10)
marco_exportacion.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

# Subdividir para CSV, JSON, XML
def crear_boton_datos(contenedor_padre, texto_boton, comando_boton):
    return crear_boton_personalizado(contenedor_padre, texto_boton, comando_boton, "#607D8B", ancho_boton=18).pack(pady=4)

tk.Label(marco_exportacion, text="Formato JSON", bg=COLOR_FONDO, font=("Segoe UI", 9, "bold")).pack(anchor="w")
crear_boton_datos(marco_exportacion, "Exportar JSON", ie.exportar_json)
crear_boton_datos(marco_exportacion, "Importar JSON", ie.importar_json)

tk.Label(marco_exportacion, text="Formatos CSV / XML", bg=COLOR_FONDO, font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(10,0))
crear_boton_datos(marco_exportacion, "Exportar CSV", ie.exportar_csv)
crear_boton_datos(marco_exportacion, "Importar CSV", ie.importar_csv)
crear_boton_datos(marco_exportacion, "Exportar XML", ie.exportar_xml)
crear_boton_datos(marco_exportacion, "Importar XML", ie.importar_xml) 

#PELIGRO Y SISTEMA
marco_peligro = tk.LabelFrame(contenedor_principal, text=" Opciones de Sistema ", bg="#FFF3F3", fg=ROJO, font=FONT_LABEL, pady=15, padx=10)
marco_peligro.pack(fill="x", pady=(10, 0))

boton_backup = crear_boton_personalizado(marco_peligro, "Ejecutar Backup Completo", bk.ejecutar_backup_completo, "#3F51B5", ancho_boton=35)
boton_backup.pack(pady=5)

boton_eliminar_todos = crear_boton_personalizado(marco_peligro, "Eliminar TODOS los Alumnos", li.eliminar_todos_los_alumnos, "#D32F2F", ancho_boton=35)
boton_eliminar_todos.pack(pady=5)

boton_restaurar_todos = crear_boton_personalizado(marco_peligro, "Restaurar TODOS los Alumnos", bk.restaurar_todos_los_alumnos, "#F57C00", ancho_boton=35)
boton_restaurar_todos.pack(pady=5)

ventana_principal.mainloop()