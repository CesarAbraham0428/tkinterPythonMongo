import tkinter as tk
from tkinter import ttk
import logica_interfaz as li
import import_export as ie
import backup as bk

ventana = tk.Tk()
ventana.title("Admon Grupos")
ventana.geometry("750x650")
ventana.resizable(False, False)

# Colores y fuentes base
BG_COLOR = "#F4F6F9"
FG_DARK = "#2B2D42"
ACCENT_GREEN = "#4CAF50"
ACCENT_BLUE = "#2196F3"
ACCENT_ORANGE = "#FF9800"
ACCENT_RED = "#F44336"
BTN_TEXT_COLOR = "#FFFFFF"

FONT_TITLE = ("Segoe UI", 16, "bold")
FONT_LABEL = ("Segoe UI", 11)
FONT_ENTRY = ("Segoe UI", 12)
FONT_BTN = ("Segoe UI", 11, "bold")

ventana.config(bg=BG_COLOR)

# ======= ESTILOS TTK =======
style = ttk.Style()
style.theme_use('clam')

# Estilo para Frames
style.configure("TFrame", background=BG_COLOR)
style.configure("Card.TFrame", background="#FFFFFF", relief="flat")

# Estilos universales para Entries
style.configure("TEntry", fieldbackground="#FFFFFF", font=FONT_ENTRY, padding=5)

# Función helper para crear botones tkinter con Hover
def crear_boton(parent, text, command, bg_color, fg_color=BTN_TEXT_COLOR, width=15):
    btn = tk.Button(parent, text=text, font=FONT_BTN, command=command,
                    bg=bg_color, fg=fg_color, width=width,
                    relief="flat", cursor="hand2", pady=8)
    
    # Hover effects
    def on_enter(e):
        btn['bg'] = color_variant(bg_color, -20)
    
    def on_leave(e):
        btn['bg'] = bg_color
        
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    return btn

def color_variant(hex_color, brightness_offset=1):
    """ Función auxiliar para oscurecer colores en el hover """
    if len(hex_color) != 7: return hex_color
    rgb_hex = [hex_color[x:x+2] for x in [1, 3, 5]]
    new_rgb_int = [int(hex_value, 16) + brightness_offset for hex_value in rgb_hex]
    new_rgb_int = [min([255, max([0, i])]) for i in new_rgb_int]
    return "#" + "".join([hex(i)[2:].zfill(2) for i in new_rgb_int])

# ======= HEADER =======
header_frame = tk.Frame(ventana, bg=FG_DARK, pady=15)
header_frame.pack(fill="x", side="top")
lbl_title = tk.Label(header_frame, text="Gestión de Grupos", bg=FG_DARK, fg="#FFFFFF", font=FONT_TITLE)
lbl_title.pack()

container_frame = ttk.Frame(ventana)
container_frame.pack(fill="both", expand=True)

canvas = tk.Canvas(container_frame, bg=BG_COLOR, highlightthickness=0)
canvas.pack(side="left", fill="both", expand=True)

# Crear la Scrollbar
scrollbar = ttk.Scrollbar(container_frame, orient="vertical", command=canvas.yview)
scrollbar.pack(side="right", fill="y")
canvas.configure(yscrollcommand=scrollbar.set)

# Crear el frame que realmente tendrá los widgets (se alojará en el Canvas)
main_container = ttk.Frame(canvas, padding=20)
style.configure("TFrame", background=BG_COLOR) # Asegurar bg

canvas_window = canvas.create_window((0, 0), window=main_container, anchor="nw")

# Funciones para actualizar la región de scroll automáticamente
def on_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

def on_canvas_configure(event):
    # Hacer que el main_container tome el ancho del canvas si es menor
    canvas.itemconfig(canvas_window, width=event.width)

main_container.bind("<Configure>", on_configure)
canvas.bind("<Configure>", on_canvas_configure)

# Soporte para rueda del ratón
def _on_mousewheel(event):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")
ventana.bind_all("<MouseWheel>", _on_mousewheel)

# BÚSQUEDA Y DATOS
search_frame = tk.Frame(main_container, bg="#FFFFFF", padx=20, pady=20, relief="solid", bd=1)
search_frame.pack(fill="x", pady=(0, 15))

# Campos
tk.Label(search_frame, text="Clave del Grupo:", bg="#FFFFFF", font=FONT_LABEL, fg=FG_DARK).grid(row=0, column=0, sticky="w", pady=5)
txt_cveGru = tk.Entry(search_frame, font=FONT_ENTRY, width=25, relief="solid", bd=1)
txt_cveGru.grid(row=0, column=1, padx=10, pady=5)

tk.Label(search_frame, text="Nombre del Grupo:", bg="#FFFFFF", font=FONT_LABEL, fg=FG_DARK).grid(row=1, column=0, sticky="w", pady=5)
txt_nomGru = tk.Entry(search_frame, font=FONT_ENTRY, width=25, relief="solid", bd=1)
txt_nomGru.grid(row=1, column=1, padx=10, pady=5)

# Botones
btn_Buscar = crear_boton(search_frame, "🔍 Buscar", lambda: li.Buscar(txt_cveGru, txt_nomGru), ACCENT_BLUE)
btn_Buscar.grid(row=0, column=2, padx=(20,5), pady=5)
btn_Limpiar = crear_boton(search_frame, "🧹 Limpiar", lambda: li.Limpiar(txt_cveGru, txt_nomGru), "#9E9E9E")
btn_Limpiar.grid(row=1, column=2, padx=(20,5), pady=5)


#OPERACIONES CRUD Y ARCHIVOS
ops_frame = tk.Frame(main_container, bg=BG_COLOR)
ops_frame.pack(fill="x", pady=(0, 15))

ops_frame.grid_columnconfigure(0, weight=1)
ops_frame.grid_columnconfigure(1, weight=1)

# Acciones de Registro
crud_frame = tk.LabelFrame(ops_frame, text=" Acciones de Registro ", bg=BG_COLOR, font=FONT_LABEL, fg=FG_DARK, pady=10, padx=10)
crud_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

crear_boton(crud_frame, "➕ Agregar", lambda: li.Agregar(txt_cveGru, txt_nomGru), ACCENT_GREEN, width=20).pack(pady=5)
crear_boton(crud_frame, "✏️ Modificar", lambda: li.Modificar(txt_cveGru, txt_nomGru), ACCENT_ORANGE, width=20).pack(pady=5)
crear_boton(crud_frame, "❌ Eliminar", lambda: li.Eliminar(txt_cveGru, txt_nomGru), ACCENT_RED, width=20).pack(pady=5)

# Importación y Exportación
export_frame = tk.LabelFrame(ops_frame, text=" Importación / Exportación ", bg=BG_COLOR, font=FONT_LABEL, fg=FG_DARK, pady=10, padx=10)
export_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

# Subdividir para CSV, JSON, XML
def make_data_btn(parent, text, cmd):
    return crear_boton(parent, text, cmd, "#607D8B", width=18).pack(pady=4)

tk.Label(export_frame, text="Formato JSON", bg=BG_COLOR, font=("Segoe UI", 9, "bold")).pack(anchor="w")
make_data_btn(export_frame, "↘️ Exportar JSON", ie.Exportar_JSON)
make_data_btn(export_frame, "↗️ Importar JSON", ie.Importar_JSON)

tk.Label(export_frame, text="Formatos CSV / XML", bg=BG_COLOR, font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(10,0))
make_data_btn(export_frame, "↘️ Exportar CSV", ie.Exportar_CSV)
make_data_btn(export_frame, "↗️ Importar CSV", ie.Importar_CSV)
make_data_btn(export_frame, "↘️ Exportar XML", ie.Exportar_XML)
make_data_btn(export_frame, "↗️ Importar XML", ie.Importar_XML) 

#PELIGRO Y SISTEMA
danger_frame = tk.LabelFrame(main_container, text=" Opciones de Sistema ", bg="#FFF3F3", fg=ACCENT_RED, font=FONT_LABEL, pady=15, padx=10)
danger_frame.pack(fill="x", pady=(10, 0))

btn_Backup = crear_boton(danger_frame, "💾 Ejecutar Backup Completo", bk.Ejecutar_Backup, "#3F51B5", width=35)
btn_Backup.pack(pady=5)

btn_EliminarTodos = crear_boton(danger_frame, "⚠️ Eliminar TODOS los Grupos", li.EliminarTodos, "#D32F2F", width=35)
btn_EliminarTodos.pack(pady=5)

btn_RestaurarTodos = crear_boton(danger_frame, "🔄 Restaurar TODOS los Grupos", bk.Restaurar_Todos, "#F57C00", width=35)
btn_RestaurarTodos.pack(pady=5)

ventana.mainloop()