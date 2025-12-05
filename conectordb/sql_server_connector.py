import pyodbc
from .basedb import BaseDeDatos

class ConectorSQLServer(BaseDeDatos):
    """Maneja la conexión y operaciones con SQL Server."""
    
#   def __init__(self, host, usuario, contrasena, bd, driver="{ODBC Driver 17 for SQL Server}"):

    def __init__(self, host, usuario, contrasena, bd, driver="{SQL Server Native Client 11.0}"):
        super().__init__(host, usuario, contrasena, bd)
        self.driver = driver

    def conectar(self):
        """Conecta a SQL Server usando pyodbc."""
        try:
            # Cadena de conexión DSN-less
            conn_str = (
                f'DRIVER={self.driver};'
                f'SERVER={self.host};'
                f'DATABASE={self.bd};'
                f'UID={self.usuario};'
                f'PWD={self.contrasena};'
            )
            self.conexion = pyodbc.connect(conn_str)
            self.cursor = self.conexion.cursor()
            print(f"Conexión exitosa a SQL Server: {self.bd}")
            return self.conexion
        except pyodbc.Error as ex:
            print(f"Error de conexión a SQL Server: {ex}")
            return None

    def ejecutar_consulta(self, consulta, parametros=None):
        """Ejecuta una consulta y devuelve los resultados (o commit la transacción)."""
        try:
            if parametros:
                self.cursor.execute(consulta, parametros)
            else:
                self.cursor.execute(consulta)

            if consulta.strip().upper().startswith(("SELECT", "EXEC")):
                # Si es SELECT, devuelve los resultados
                return self.cursor.fetchall()
            else:
                # Si es INSERT, UPDATE, DELETE, commitea y devuelve el número de filas afectadas
                self.conexion.commit()
                return self.cursor.rowcount
        except Exception as e:
            print(f"Error al ejecutar consulta en SQL Server: {e}")
            self.conexion.rollback() # Deshacer cambios en caso de error
            return None