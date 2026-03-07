import tkinter as tk

from logica_interfaz import Modificar, Agregar, Exportar, Importar

ventana = tk.Tk()
ventana.title("Admon Grupo")
ventana.geometry("600x300")
ventana.resizable(0,0)
ventana.config(cursor="hand2")


#Labels

lbl_cveGru = tk.Label(ventana, text="Clave:", font=("Arial", 11))

lbl_cveGru.grid(row=0, column=1)

lbl_nomGru = tk.Label(ventana, text="Nombre:", font=("Arial", 11))

lbl_nomGru.grid(row=1, column=1)

# Cajas de texto
txt_cveGru = tk.Entry(ventana, 
                      width=20,
                      font=("Arial", 12))
txt_cveGru.grid(row=0, column=2)

txt_nomGru=tk.Entry(ventana,
                    width=20,
                    font=("Arial", 12))
txt_nomGru.grid(row=1, column=2)

# Botones

btn_Agregar = tk.Button(ventana,
                        text="Agregar",
                        font=("Arial", 12,"bold"),
                        bg="white",
                        fg="black",
                        command=Agregar)
btn_Agregar.grid(row=3, column=0)

btn_ExportarCSV = tk.Button(ventana,
                        text="Exportar csv",
                        font=("Arial", 12,"bold"),
                        bg="white",
                        fg="black",
                        command=Exportar)
btn_ExportarCSV.grid(row=4, column=0)

btn_Importar = tk.Button(ventana,
                        text="Importar csv",
                        font=("Arial", 12,"bold"),
                        bg="white",
                        fg="black",
                        command=Importar)
btn_Importar.grid(row=5, column=0)

#Columna 2

btn_Modificar = tk.Button(ventana,
                        text="Modificar",
                        font=("Arial", 12,"bold"),
                        bg="white",
                        fg="black",
                        command=Modificar)
btn_Modificar.grid(row=3, column=2)

btn_ExportarJSON = tk.Button(ventana,
                        text="Exportar json",
                        font=("Arial", 12,"bold"),
                        bg="white",
                        fg="black",
                        command=Exportar)
btn_ExportarJSON.grid(row=4, column=2)

btn_ImportarJSON = tk.Button(ventana,
                        text="Importar json",
                        font=("Arial", 12,"bold"),
                        bg="white",
                        fg="black",
                        command=Importar)
btn_ImportarJSON.grid(row=5, column=2)

btn_Modificar = tk.Button(ventana,
                        text="Modificar",
                        font=("Arial", 12,"bold"),
                        bg="white",
                        fg="black",
                        command=Modificar)
btn_Modificar.grid(row=3, column=2)


# Columna 3

btn_Buscar = tk.Button(ventana,
                        text="Buscar",
                        font=("Arial", 12,"bold"),
                        bg="white",
                        fg="black",
                        command=Exportar)
btn_Buscar.grid(row=0, column=3)

btn_Limpiar = tk.Button(ventana,
                        text="Limpiar",
                        font=("Arial", 12,"bold"),
                        bg="white",
                        fg="black",
                        command=Importar)
btn_Limpiar.grid(row=1, column=3)

btn_Eliminar = tk.Button(ventana,
                        text="Eliminar",
                        font=("Arial", 12,"bold"),
                        bg="white",
                        fg="black",
                        command=Exportar)
btn_Eliminar.grid(row=2, column=3)

btn_ExportarXML = tk.Button(ventana,
                        text="Exportar xml",
                        font=("Arial", 12,"bold"),
                        bg="white",
                        fg="black",
                        command=Exportar)
btn_ExportarXML.grid(row=3, column=3)

btn_ImportarXML = tk.Button(ventana,
                        text="Importar xml",
                        font=("Arial", 12,"bold"),
                        bg="white",
                        fg="black",
                        command=Importar)
btn_ImportarXML.grid(row=4, column=3)

ventana.mainloop()