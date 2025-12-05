import qrcode
import qrcode.constants
# 1. SOLUCIÓN: Cambiar a importación absoluta
from conectordb.sql_server_connector import ConectorSQLServer

#Conexion a base de datos
sqlserver_conn = ConectorSQLServer(r"localhost\DESARROLOSM", "SACA", "Ise123", "SACA")
sqlserver_conn.conectar()

id_arc =101
nom_arc = "serverOVH"+ str(id_arc) +".png"
dire_QR = f"./almacenQR/{nom_arc}"

# Aqui se indica la URL del sitio web
dire_arc = "20259876543210"

qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4
)

qr.add_data(dire_arc)
qr.make(fit=True)

img = qr.make_image(fill="black", back_color="white")
img.save(dire_QR)

print('ok')
