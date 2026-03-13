
---

## 1. Librerías Principales y su Función

### 1.1 **Tkinter** (`interfaz.py`)
- **Propósito**: Crear interfaces gráficas de usuario (GUI)
- **Componentes clave**:
  - `tk.Tk()`: Ventana principal de la aplicación
  - `tk.Frame()`: Contenedores para organizar widgets
  - `tk.Label()`: Etiquetas de texto
  - `tk.Entry()`: Campos de entrada de texto
  - `tk.Button()`: Botones interactivos
  - `tk.Canvas()`: Área de dibujo con scroll
  - `ttk.Style()`: Personalización de estilos visuales

### 1.2 **Pymongo** (`conexion.py`)
- **Propósito**: Conexión y operaciones con base de datos MongoDB
- **Componentes clave**:
  - `MongoClient`: Establece conexión con el servidor MongoDB
  - `base_datos_grupos`: Referencia a la base de datos `BD_GrupoAlumno`
  - `coleccion_grupos`: Referencia a la colección `Grupo`

### 1.3 **OS** (`import_export.py`, `backup.py`)
- **Propósito**: Interacción con el sistema operativo
- **Métodos utilizados**:
  - `os.path.join()`: Une rutas de forma segura
  - `os.makedirs()`: Crea directorios recursivamente
  - `os.path.exists()`: Verifica existencia de archivos
  - `os.system()`: Ejecuta comandos del sistema

### 1.4 **JSON** (`import_export.py`)
- **Propósito**: Manipulación de archivos JSON
- **Métodos clave**:
  - `json.dump()`: Escribe datos en formato JSON
  - `json.load()`: Lee datos desde archivo JSON
  - `ensure_ascii=False`: Permite caracteres especiales (acentos, ñ)

### 1.5 **CSV** (`import_export.py`)
- **Propósito**: Manejo de archivos CSV (valores separados por comas)
- **Métodos clave**:
  - `csv.writer()`: Escribe datos en formato CSV
  - `csv.DictReader()`: Lee CSV como diccionarios
  - `newline=""`: Evita líneas en blanco en Windows

### 1.6 **XML** (`import_export.py`)
- **Propósito**: Procesamiento de archivos XML
- **Componentes clave**:
  - `ET.Element()`: Crea elementos XML
  - `ET.SubElement()`: Crea subelementos anidados
  - `ET.ElementTree()`: Representa el árbol XML completo
  - `ET.parse()`: Parsea archivos XML existentes

---

## 2. Análisis Detallado de Módulos

### 2.1 **Módulo de Conexión** (`conexion.py`)

```python
from pymongo import MongoClient as ClienteMongo

cliente_mongodb = ClienteMongo("mongodb://localhost:27017/")
base_datos_grupos = cliente_mongodb["BD_GrupoAlumno"]
coleccion_grupos = base_datos_grupos["Grupo"]
```

**Funcionamiento**:
1. Establece conexión con MongoDB en `localhost:27017`
2. Selecciona la base de datos `BD_GrupoAlumno`
3. Apunta a la colección `Grupo` donde se almacenan los documentos

**Estructura de datos en MongoDB**:
```json
{
  "cveGru": "clave_grupo",
  "nomGru": "nombre_grupo"
}
```

### 2.2 **Módulo de Interfaz Gráfica** (`interfaz.py`)

#### Configuración de la Ventana Principal
```python
ventana_principal = tk.Tk()
ventana_principal.title("Admon Grupos")
ventana_principal.geometry("750x650")
ventana_principal.resizable(False, False)
```

#### Sistema de Colores y Fuentes
- **COLOR_FONDO**: `#F4F6F9` (Gris claro)
- **COLOR_OSCURO**: `#2B2D42` (Azul oscuro)
- **VERDE**: `#4CAF50` (Para acciones exitosas)
- **AZUL**: `#2196F3` (Para acciones principales)
- **NARANJA**: `#FF9800` (Para modificaciones)
- **ROJO**: `#F44336` (Para eliminaciones)

#### Sistema de Scroll con Canvas
```python
lienzo_interfaz = tk.Canvas(marco_contenedor, bg=COLOR_FONDO)
barra_desplazamiento = ttk.Scrollbar(marco_contenedor, orient="vertical")
contenedor_principal = ttk.Frame(lienzo_interfaz)
```

**Lógica del scroll**:
1. El `Canvas` contiene el contenido principal
2. La `Scrollbar` controla el desplazamiento vertical
3. El `contenedor_principal` aloja todos los widgets
4. Eventos `<Configure>` actualizan la región de scroll automáticamente

#### Función de Botones Personalizados
```python
def crear_boton_personalizado(contenedor_padre, texto_boton, comando_boton, 
                             color_fondo_boton, color_texto_boton=COLOR_TEXTO_BOTON, 
                             ancho_boton=15):
```

**Características**:
- Efectos hover (cambio de color al pasar el mouse)
- Cursor `hand2` para indicar interactividad
- Diseño plano (`relief="flat"`)
- Padding vertical para mejor apariencia

#### Estructura de la Interfaz
1. **Header**: Título principal con fondo oscuro
2. **Búsqueda**: Campos para clave y nombre de grupo
3. **Operaciones CRUD**: Botones para agregar, modificar, eliminar
4. **Importación/Exportación**: Soporte para JSON, CSV, XML
5. **Sistema**: Backup y restauración completa

### 2.3 **Módulo de Lógica** (`logica_interfaz.py`)

#### Funciones CRUD

**Buscar Grupo**:
```python
def buscar_grupo_por_clave(campo_clave_grupo, campo_nombre_grupo):
    clave_grupo = campo_clave_grupo.get().strip()
    documento_grupo = coleccion_grupos.find_one({"cveGru": clave_grupo})
```
- Valida que la clave no esté vacía
- Busca en MongoDB usando `find_one()`
- Llena el campo de nombre si encuentra el grupo

**Agregar Grupo**:
```python
def agregar_grupo(campo_clave_grupo, campo_nombre_grupo):
    documento_existente = coleccion_grupos.find_one({"cveGru": clave_grupo})
    if documento_existente:
        messagebox.showwarning("Advertencia", "Clave de grupo repetida")
    else:
        coleccion_grupos.insert_one({"cveGru": clave_grupo, "nomGru": nombre_grupo})
```
- Verifica que no exista la clave
- Inserta nuevo documento en MongoDB
- Limpia campos después de agregar

**Modificar Grupo**:
```python
def modificar_grupo(campo_clave_grupo, campo_nombre_grupo):
    resultado_modificacion = coleccion_grupos.update_one(
        {"cveGru": clave_grupo}, 
        {"$set": {"nomGru": nombre_grupo}}
    )
```
- Usa `update_one()` con operador `$set`
- Verifica si se modificó algún documento

**Eliminar Grupo**:
```python
def eliminar_grupo(campo_clave_grupo, campo_nombre_grupo):
    resultado_eliminacion = coleccion_grupos.delete_one({"cveGru": clave_grupo})
```
- Usa `delete_one()` para eliminar un solo documento
- Nota: Pendiente implementar eliminación en cascada con alumnos

### 2.4 **Módulo de Importación/Exportación** (`import_export.py`)

#### Funciones JSON
```python
def exportar_json():
    documentos_grupos = list(coleccion_grupos.find({}, {"_id": 0, "cveGru": 1, "nomGru": 1}))
    with open(ruta_archivo, "w", encoding="utf-8") as archivo_json:
        json.dump(documentos_grupos, archivo_json, ensure_ascii=False, indent=4)
```

**Características**:
- Excluye `_id` de MongoDB
- Usa `ensure_ascii=False` para caracteres especiales
- Formato con indentación para legibilidad

#### Funciones CSV
```python
def exportar_csv():
    with open(ruta_archivo, mode="w", newline="", encoding="utf-8") as archivo_csv:
        escritor_csv = csv.writer(archivo_csv)
        escritor_csv.writerow(["Clave", "Nombre"])
        for datos_grupo in documentos_grupos:
            escritor_csv.writerow([datos_grupo.get("cveGru", ""), datos_grupo.get("nomGru", "")])
```

**Características**:
- Escribe encabezados manualmente
- Usa `newline=""` para evitar líneas extra en Windows
- Encoding UTF-8 para caracteres especiales

#### Funciones XML
```python
def exportar_xml():
    elemento_raiz = ET.Element("Grupos")
    for datos_grupo in documentos_grupos:
        elemento_grupo = ET.SubElement(elemento_raiz, "Grupo")
        ET.SubElement(elemento_grupo, "Clave").text = str(datos_grupo.get("cveGru", ""))
        ET.SubElement(elemento_grupo, "Nombre").text = str(datos_grupo.get("nomGru", ""))
```

**Estructura XML generada**:
```xml
<?xml version='1.0' encoding='utf-8'?>
<Grupos>
    <Grupo>
        <Clave>clave_grupo</Clave>
        <Nombre>nombre_grupo</Nombre>
    </Grupo>
</Grupos>
```

### 2.5 **Módulo de Backup** (`backup.py`)

#### Backup Completo
```python
def ejecutar_backup_completo():
    comando_mongodump = '"C:\\Program Files\\MongoDB\\Tools\\100\\bin\\mongodump.exe" --db BD_GrupoAlumno --out C:\\Backup_Mongo'
    os.system(comando_mongodump)
```

**Funcionamiento**:
- Usa `mongodump.exe` herramienta nativa de MongoDB
- Exporta toda la base de datos a `C:\Backup_Mongo`
- Crea estructura BSON para restauración nativa

#### Restauración
```python
def restaurar_todos_los_grupos():
    comando_mongorestore = '"C:\\Program Files\\MongoDB\\Tools\\100\\bin\\mongorestore.exe" --db BD_GrupoAlumno --collection Grupo C:\\Backup_Mongo\\BD_GrupoAlumno\\Grupo.bson'
    os.system(comando_mongorestore)
```

**Funcionamiento**:
- Usa `mongorestore.exe` para restaurar desde archivo BSON
- Restaura específicamente la colección `Grupo`
- Sobrescribe datos existentes

---

## 3. Flujo de Datos del Sistema

### 3.1 **Flujo de Operación CRUD**
```
Interfaz Gráfica → logica_interfaz.py → MongoDB (via conexion.py)
     ↓                    ↓                      ↓
  Entrada Usuario    Validación Lógica      Almacenamiento
     ↓                    ↓                      ↓
  Mensaje Resultado  Manejo Errores      Confirmación BD
```

### 3.2 **Flujo de Importación/Exportación**
```
Botón Interfaz → import_export.py → MongoDB
      ↓                ↓                ↓
   Acción        Leer/Escribir      Consultar/Insertar
      ↓                ↓                ↓
  Archivo        Formatear          Datos Procesados
```

---

## 4. Puntos Clave para Explicar al Profesor

### 4.1 **Arquitectura Modular**
- **Separación de responsabilidades**: Cada módulo tiene una función específica
- **Bajo acoplamiento**: Los módulos interactúan a través de interfaces definidas
- **Alta cohesión**: Cada módulo agrupa funcionalidades relacionadas

### 4.2 **Manejo de Datos**
- **MongoDB**: Base de datos NoSQL orientada a documentos
- **JSON**: Formato nativo de MongoDB para intercambio de datos
- **Validaciones**: Prevención de datos duplicados y nulos

### 4.3 **Interfaz de Usuario**
- **Tkinter**: Biblioteca estándar de Python para GUI
- **Diseño responsivo**: Scroll dinámico para contenido variable
- **Experiencia de usuario**: Efectos hover y colores semánticos

### 4.4 **Persistencia de Datos**
- **Múltiples formatos**: JSON, CSV, XML para diferentes necesidades
- **Backup nativo**: BSON para restauración completa
- **Importación inteligente**: Evita duplicados al importar

---

## 5. Mejoras Potenciales

### 5.1 **Seguridad**
- Encriptación de datos sensibles
- Validación de entrada más robusta
- Manejo de excepciones más granular

### 5.2 **Rendimiento**
- Conexión persistente a MongoDB
- Paginación para grandes volúmenes de datos
- Caching de consultas frecuentes

### 5.3 **Funcionalidad**
- Eliminación en cascada con alumnos
- Sistema de usuarios y permisos
- Logs de auditoría de operaciones

---

## 6. Resumen Ejecutivo

El sistema implementa una solución completa para gestión de grupos utilizando Python, Tkinter para la interfaz gráfica y MongoDB como base de datos. La arquitectura modular facilita el mantenimiento y extensión del sistema, mientras que el soporte para múltiples formatos de importación/exportación proporciona flexibilidad en el manejo de datos. El sistema de backup nativo garantiza la seguridad y recuperación de la información.
