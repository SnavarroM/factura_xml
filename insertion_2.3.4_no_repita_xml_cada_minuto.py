import os
import sqlite3
from lxml import etree

def crear_tablas():
    #! Crear la tabla si no existe
    conn = sqlite3.connect('xmls.db')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS facturas (nombre TEXT, direccion TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS archivos_procesados (nombre TEXT UNIQUE)")
    conn.commit()
    conn.close()

def verificar_archivo_procesado(archivo, archivos_procesados):
    #! Verificar si el archivo ya ha sido procesado
    if archivo in archivos_procesados:
        #! El archivo ya ha sido procesado en esta sesión, saltar al siguiente archivo
        return True
    else:
        conn = sqlite3.connect('xmls.db')
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM archivos_procesados WHERE nombre=?", (archivo,))
        resultado = c.fetchone()[0]
        conn.close()
        if resultado > 0:
            #! El archivo ya ha sido procesado en una sesión anterior, saltar al siguiente archivo
            return True
        else:
            return False

def procesar_archivo_xml(archivo, archivos_procesados):
    #! Leer el archivo XML
    tree = etree.parse(archivo)
    #! Obtener una lista de todas las filas en el archivo
    filas = tree.xpath('//fila')
    #! Procesar cada fila y agregar los datos a la base de datos
    conn = sqlite3.connect('xmls.db')
    c = conn.cursor()
    for fila in filas:
        #! Obtener los valores de columna1 y columna2 para esta fila
        valor1 = fila.xpath('nombre/text()')[0]
        valor2 = fila.xpath('direccion/text()')[0]
        #! Insertar los valores en la base de datos
        try:
            c.execute('INSERT INTO facturas (nombre, direccion) VALUES (?, ?)', (valor1, valor2))
            conn.commit()
        except sqlite3.IntegrityError:
            #! El registro ya existe, saltar al siguiente registro
            pass
    #! Registrar el archivo como procesado
    try:
        c.execute('INSERT INTO archivos_procesados (nombre) VALUES (?)', (archivo,))
        conn.commit()
        #! Agregar el archivo a la lista de archivos procesados en esta sesión
        archivos_procesados.append(archivo)
    except sqlite3.IntegrityError:
        #! El archivo ya ha sido procesado, saltar al siguiente archivo
        pass
    conn.close()

def leer_archivos_xml(carpeta):
    try:
        crear_tablas()
        #! Leer archivos XML
        archivos_xml = []
        archivos_procesados = []
        conn = sqlite3.connect('xmls.db')
        c = conn.cursor()
        c.execute("SELECT nombre FROM archivos_procesados")
        archivos_procesados = [registro[0] for registro in c.fetchall()]
        conn.close()
        for archivo in os.listdir(carpeta):
            if archivo.endswith('.xml'):
                if verificar_archivo_procesado(archivo, archivos_procesados):
                    continue
                else:
                    archivos_xml.append(os.path.join(carpeta, archivo))
        #! Procesar los archivos XML en orden cronológico
        archivos_xml = sorted(archivos_xml, key=os.path.getctime)
        for archivo in archivos_xml:
            if archivo in archivos_procesados:
                #! El archivo ya ha sido procesado, saltar al siguiente archivo
                continue
            else:
                procesar_archivo_xml(archivo, archivos_procesados)
    except Exception as e:
        print(f"An error occurred: {e}")

leer_archivos_xml(r'C:\Users\snavarro\Desktop\toma de requerimientos\xml sii\script\scripts cenabast\decargas_gmail_python')