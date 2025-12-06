import sys
from flask import Flask, request, jsonify, send_from_directory, Response
from datetime import datetime
import json
import os
import io # <--- ¡IMPORTACIÓN AÑADIDA!
import qrcode 

# ----------------------------------------------------------------------
# 1. Importación del Conector DB (¡Cambiado a MySQL!)
# ----------------------------------------------------------------------
try:
    from conectordb.mysql_connector import ConectorMySQL
except ImportError as e:
    print(f"Error fatal de importación del conector: {e}")
    sys.exit(1)

app = Flask(__name__)

# ----------------------------------------------------------------------
# 2. Configuración de la Base de Datos (MySQL)
# ----------------------------------------------------------------------
# *** DEBES REEMPLAZAR ESTOS VALORES CON LOS DE TU INSTANCIA MYSQL ***
DB_HOST = "127.0.0.1"       # O la IP de tu servidor MySQL
DB_USER = "root" # Reemplaza con tu usuario
DB_PASS = "Rh11163539*"  # Reemplaza con tu contraseña
DB_NAME = "tbl_regasiste"            # Tu base de datos
# *******************************************************************

def get_db_connection():
    """Retorna una instancia conectada de ConectorMySQL."""
    conn = ConectorMySQL(DB_HOST, DB_USER, DB_PASS, DB_NAME)
    conn.conectar()
    return conn

# ----------------------------------------------------------------------
# 3.5. Endpoint para la Página Web (Index)
# ----------------------------------------------------------------------
@app.route('/')
@app.route('/')
def index():
    """Sirve el archivo index.html."""
    # Asume que index.html está en el mismo directorio del script
    # return send_from_directory('.', 'index.html') esta es la correcta
    return send_from_directory('.', 'index.html')

@app.route('/generador')
def generador():
    """Sirve el archivo generador_qr.html."""
    # Asume que generador_qr.html está en el mismo directorio del script
    return send_from_directory('.', 'generador_qr.html')

@app.route('/<path:filename>')
def serve_static(filename):
    """Sirve archivos estáticos (como el JS) desde el directorio raíz."""
    return send_from_directory('.', filename)


# ----------------------------------------------------------------------
# 3. Endpoint del API para Registro
# ----------------------------------------------------------------------

@app.route('/api/generar-qr', methods=['GET'])
def generar_qr_imagen():
    """
    Recibe el 'contenido' por parámetro GET, genera el QR y lo devuelve como imagen.
    """
    contenido = request.args.get('contenido')
    
    if not contenido:
        return jsonify({"error": "Falta el parámetro 'contenido' en la URL."}), 400

    try:
        # Crea el objeto QR
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(contenido)
        qr.make(fit=True)

        # Crea la imagen QR (en blanco y negro)
        img = qr.make_image(fill_color="black", back_color="white")

        # Guarda la imagen en memoria (buffer)
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        
        # Devuelve la imagen como respuesta HTTP
        return Response(buffer.getvalue(), mimetype='image/png')

    except Exception as e:
        print(f"Error al generar QR: {e}")
        return jsonify({"error": "Error interno del servidor al generar el QR."}), 500


# ----------------------------------------------------------------------
# 5. Endpoint del API para Registro
# ----------------------------------------------------------------------

@app.route('/api/registrar-lectura', methods=['POST'])
def registrar_lectura():
    """
    Endpoint que recibe el texto del QR y registra la lectura en MySQL.
    """
    
    if not request.is_json:
        return jsonify({"mensaje": "Error: El contenido debe ser JSON"}), 400
    
    data = request.get_json()
    texto_qr = data.get('texto_qr')

    if not texto_qr:
        return jsonify({"mensaje": "Error: Falta el campo 'texto_qr'"}), 400

    # Capturar Fecha y Hora (Hora del servidor API)
    vcodigo = '11163539'
    vnombre = 'ROBERTO HERNANDEZ'
    fecha_hora = datetime.now()
    fecha_hora_str = fecha_hora.strftime('%Y-%m-%d %H:%M:%S')
    vcodempre = '01'
    vcodigo_qr = texto_qr

    try:
        conn = get_db_connection()
        if not conn.conexion:
            return jsonify({"mensaje": "Error: No se pudo conectar a la base de datos."}), 500

        # ATENCIÓN: En MySQL usamos %s como placeholder
        consulta = "INSERT INTO tbl_regasiste (codigo, nombre, fecha, codempre, codigo_qr) VALUES (%s, %s, %s, %s, %s)"
        parametros = (vcodigo, vnombre, fecha_hora_str, vcodempre, vcodigo_qr)

        filas_afectadas = conn.ejecutar_consulta(consulta, parametros)
        conn.cerrar_conexion()
        
        if filas_afectadas:
            return jsonify({
                "mensaje": "Registro exitoso.",
                "qr_leido": texto_qr,
                "timestamp_servidor": fecha_hora_str
            }), 201
        else:
            return jsonify({"mensaje": "Error: La DB no registró el cambio."}), 500

    except Exception as e:
        print(f"Error DB/API: {e}")
        return jsonify({"mensaje": f"Error interno del servidor: {e}"}), 500

# ----------------------------------------------------------------------
# 6. Ejecución
# ----------------------------------------------------------------------

#   if __name__ == '__main__':
    # Usar host='0.0.0.0' para que el celular en la misma red pueda acceder
    # app.run(host='0.0.0.0', port=5000, debug=True,  ssl_context=('cert.pem', 'key.pem'))