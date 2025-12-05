from api_lector_qr import app

# El servidor Gunicorn buscará la variable 'app' para iniciar la aplicación.
# Esta es la única línea importante.
if __name__ == "__main__":
    app.run()

