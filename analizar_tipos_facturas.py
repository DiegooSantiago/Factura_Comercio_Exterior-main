import os
from collections import defaultdict
import csv

# Función para analizar un archivo .txt y extraer todos los campos con información
def analizar_factura(ruta_archivo):
    campos_factura = defaultdict(str)
    
    try:
        # Intentar leer el archivo con UTF-8
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            for linea in archivo:
                if linea.strip() and not linea.startswith("#"):
                    if "=" in linea:
                        clave, valor = linea.split('=', 1)
                        valor = valor.strip()
                        if valor:
                            campos_factura[clave.strip()] = valor
    except UnicodeDecodeError:
        # Si falla, intentar con ISO-8859-1 (latin-1)
        with open(ruta_archivo, 'r', encoding='ISO-8859-1') as archivo:
            for linea in archivo:
                if linea.strip() and not linea.startswith("#"):
                    if "=" in linea:
                        clave, valor = linea.split('=', 1)
                        valor = valor.strip()
                        if valor:
                            campos_factura[clave.strip()] = valor

    return campos_factura

# Función para identificar el "tipo" de factura basado en los campos presentes
def obtener_tipo_factura(campos_factura):
    tipo = tuple(sorted(campos_factura.keys()))  # Una combinación única de campos
    return tipo

# Función para recorrer un directorio y analizar todos los archivos .txt
def analizar_directorio(directorio):
    tipos_facturas = defaultdict(list)
    campos_totales = set()
    
    for archivo in os.listdir(directorio):
        if archivo.endswith(".txt"):
            ruta_archivo = os.path.join(directorio, archivo)
            print(f"Analizando archivo: {ruta_archivo}")
            campos_factura = analizar_factura(ruta_archivo)
            tipo_factura = obtener_tipo_factura(campos_factura)
            tipos_facturas[tipo_factura].append(ruta_archivo)
            # Agregar todos los campos encontrados a la lista de campos totales
            campos_totales.update(campos_factura.keys())
    
    return tipos_facturas, campos_totales

# Función para obtener los campos faltantes para cada tipo de factura
def obtener_campos_faltantes_por_tipo(tipos_facturas, campos_totales):
    campos_faltantes_por_tipo = {}
    
    for tipo, _ in tipos_facturas.items():
        campos_presentes = set(tipo)
        campos_faltantes = campos_totales - campos_presentes
        campos_faltantes_por_tipo[tipo] = campos_faltantes
    
    return campos_faltantes_por_tipo

# Función para guardar los resultados en un archivo CSV
def guardar_resultados_csv(tipos_facturas, campos_totales, campos_faltantes_por_tipo, nombre_csv):
    with open(nombre_csv, mode='w', newline='', encoding='utf-8') as archivo_csv:
        writer = csv.writer(archivo_csv)
        writer.writerow(['Tipo', 'Campos presentes', 'Número de facturas', 'Primera factura', 'Campos faltantes'])

        for i, (tipo, facturas) in enumerate(tipos_facturas.items(), 1):
            campos_presentes = ', '.join(tipo)
            campos_faltantes = ', '.join(campos_faltantes_por_tipo[tipo])
            num_facturas = len(facturas)
            primera_factura = facturas[0]
            writer.writerow([f'Tipo {i}', campos_presentes, num_facturas, primera_factura, campos_faltantes])

# Función principal
if __name__ == "__main__":
    directorio = "C:/Users/Usuario1/Desktop/Requerimentos/JPrieto/xml_to_pdf_dcruz/pruebas/TXTs"  # Cambiar por el path del directorio
    nombre_csv = "resultados_tipos_facturas.csv"  # Nombre del archivo CSV
    
    tipos_facturas, campos_totales = analizar_directorio(directorio)
    
    # Obtener los campos faltantes por tipo de factura
    campos_faltantes_por_tipo = obtener_campos_faltantes_por_tipo(tipos_facturas, campos_totales)
    
    print("\nCampos totales encontrados:")
    print(", ".join(sorted(campos_totales)))

    print("\nTipos de facturas encontradas:")
    for i, (tipo, facturas) in enumerate(tipos_facturas.items(), 1):
        print(f"\nTipo {i}:")
        print(f"Campos presentes: {', '.join(tipo)}")
        print(f"Número de facturas: {len(facturas)}")
        print(f"Primera factura: {facturas[0]}")
        print(f"Campos faltantes: {', '.join(campos_faltantes_por_tipo[tipo])}")
    
    guardar_resultados_csv(tipos_facturas, campos_totales, campos_faltantes_por_tipo, nombre_csv)
    print(f"\nResultados guardados en el archivo: {nombre_csv}")
