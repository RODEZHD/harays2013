import os
from datetime import datetime
from PIL import Image
from pyzbar.pyzbar import decode
import sys
import argparse

# ----------------------------------------------------------------------
# 1. IMPORTACIÓN DEL CONECTOR DB
# ----------------------------------------------------------------------
# Asumiendo que tu estructura de importación es la siguiente,
# donde conectordb es el paquete que contiene sql_server_connector.py:
try:
    from conectordb.sql_server_connector import ConectorSQLServer
except ImportError as e:
    print(f"Error de importación: {e}")
    print("Asegúrate de que 'conectordb/sql_server_connector.py' exista y que tu entorno de Python esté configurado correctamente.")
    sys.exit(1)

# ----------------------------------------------------------------------
# 2. CONFIGURACIÓN DE LA BASE DE DATOS
# ----------------------------------------------------------------------
# Configuración que te funcionó (usando 'localhost' para conexión local)
DB_HOST = r"localhost\DESARROLOSM"
DB_USER = "SACA"
DB_PASS = "Ise123"
DB_NAME = "SACA"

def get_db_connection():
    """Retorna una instancia conectada de ConectorSQLServer."""
    conn = ConectorSQLServer(DB_HOST, DB_USER, DB_PASS, DB_NAME)
    conn.conectar()
    return conn

# ----------------------------------------------------------------------
# 3. LÓGICA PRINCIPAL DE LECTURA Y REGISTRO
# ----------------------------------------------------------------------

def leer_qr_y_registrar(ruta_archivo_imagen):
    """Procesa la imagen, lee el QR y registra la marca de tiempo en la DB."""
    
    if not os.path.exists(ruta_archivo_imagen):
        print(f"Error: El archivo no existe en la ruta: {ruta_archivo_imagen}")
        return

    print(f"Iniciando lectura del archivo: {ruta_archivo_imagen}")

    try:
        # 3.1. Leer el código QR de la imagen
        qr_data = decode(Image.open(ruta_archivo_imagen))
        
        if not qr_data:
            print("❌ Lectura fallida: No se encontró ningún código QR en la imagen.")
            return

        # Obtener el texto del primer código QR encontrado
        texto_qr = qr_data[0].data.decode('utf-8')
        
        # 3.2. Capturar Fecha y Hora
        fecha_hora = datetime.now()
        fecha_hora_str = fecha_hora.strftime('%Y-%m-%d %H:%M:%S')

        print(f"✅ QR Decodificado: {texto_qr}")
        print(f"⏰ Fecha/Hora: {fecha_hora_str}")
        
        # 3.3. Insertar Datos en la DB
        conn = get_db_connection()
        if conn.conexion:
            
            # Ajusta 'Lecturas' al nombre real de tu tabla y los nombres de las columnas
            consulta = "INSERT INTO Lecturas (TextoQR, FechaHoraLectura) VALUES (?, ?)"
            parametros = (texto_qr, fecha_hora_str)

            filas_afectadas = conn.ejecutar_consulta(consulta, parametros)
            conn.cerrar_conexion()
            
            if filas_afectadas:
                print(f"🎉 Éxito: Registro guardado en DB (Filas afectadas: {filas_afectadas}).")
            else:
                print("❌ Error: No se pudo insertar el registro en la base de datos.")

    except Exception as e:
        print(f"🚨 Error fatal durante el procesamiento del QR o la DB: {e}")

# ----------------------------------------------------------------------
# 4. EJECUCIÓN DEL SCRIPT
# ----------------------------------------------------------------------

if __name__ == '__main__':
    # Usar argparse para manejar la ruta del archivo desde la línea de comandos
    parser = argparse.ArgumentParser(description="Lector de Códigos QR y registrador de base de datos.")
    parser.add_argument("archivo", type=str, help="Ruta completa al archivo de imagen del Código QR.")
    
    args = parser.parse_args()
    
    # Llamar a la función principal con la ruta proporcionada
    leer_qr_y_registrar(args.archivo)