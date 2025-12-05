#Este script genera certificados SSL autofirmados (cert.pem y key.pem)
# para que el servidor Flask pueda correr usando HTTPS.

from OpenSSL import crypto
import datetime

# --- Configuración del Certificado ---
CERT_FILE = "cert.pem"
KEY_FILE = "key.pem"
C = "MX"  # País
ST = "CDMX" # Estado
L = "CDMX" # Ciudad
O = "QRSACA" # Organización
OU = "Desarrollo Local" # Unidad Organizacional
CN = "localhost" # Nombre Común (debe ser localhost o la IP de tu PC)
# ------------------------------------

def generate_cert():
    # Crear un par de claves (privada)
    k = crypto.PKey()
    # Usar RSA con 2048 bits
    k.generate_key(crypto.TYPE_RSA, 2048)

    # Crear el certificado (x509)
    cert = crypto.X509()
    cert.get_subject().C = C
    cert.get_subject().ST = ST
    cert.get_subject().L = L
    cert.get_subject().O = O
    cert.get_subject().OU = OU
    cert.get_subject().CN = CN
    
    # Asignar una fecha de validez (hoy hasta dentro de un año)
    cert.set_serial_number(1000)
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(365 * 24 * 60 * 60) # Válido por 1 año
    
    # Asignar la clave pública al certificado
    cert.set_issuer(cert.get_subject())
    cert.set_pubkey(k)
    cert.sign(k, 'sha256')

    # Guardar la clave privada
    with open(KEY_FILE, "wb") as f:
        f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, k))
    
    # Guardar el certificado
    with open(CERT_FILE, "wb") as f:
        f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))

    print("-" * 50)
    print(f"✅ Certificados generados con éxito en la carpeta QRSACA:")
    print(f"   - {CERT_FILE} (Certificado público)")
    print(f"   - {KEY_FILE} (Clave privada)")
    print("El servidor Flask ahora se puede ejecutar con HTTPS.")
    print("-" * 50)

if __name__ == "__main__":
    try:
        generate_cert()
    except ImportError:
        print("ERROR: La librería 'pyOpenSSL' no está instalada.")
        print("Ejecuta 'pip install pyOpenSSL' en tu terminal.")
    except Exception as e:
        print(f"Ocurrió un error al generar los certificados: {e}")