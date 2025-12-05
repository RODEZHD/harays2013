from abc import ABC, abstractmethod

class BaseDeDatos(ABC):
    """Clase base abstracta para conexiones a bases de datos."""

    def __init__(self, host, usuario, contrasena, bd):
        self.host = host
        self.usuario = usuario
        self.contrasena = contrasena
        self.bd = bd
        self.conexion = None
        self.cursor = None

    @abstractmethod
    def conectar(self):
        """Método abstracto para establecer la conexión."""
        pass

    @abstractmethod
    def ejecutar_consulta(self, consulta, parametros=None):
        """Método abstracto para ejecutar una consulta SQL."""
        pass

    def cerrar_conexion(self):
        """Cierra el cursor y la conexión."""
        if self.cursor:
            self.cursor.close()
        if self.conexion:
            self.conexion.close()
        print(f"Conexión a '{self.bd}' cerrada.")