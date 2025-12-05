import mysql.connector
from .basedb import BaseDeDatos

class ConectorMySQL(BaseDeDatos):
    """Maneja la conexión y operaciones con MySQL."""

    def conectar(self):
        """Conecta a MySQL usando mysql.connector."""
        try:
            self.conexion = mysql.connector.connect(
                host=self.host,
                user=self.usuario,
                password=self.contrasena,
                database=self.bd
            )
            self.cursor = self.conexion.cursor()
            print(f"Conexión exitosa a MySQL: {self.bd}")
            return self.conexion
        except mysql.connector.Error as err:
            print(f"Error de conexión a MySQL: {err}")
            return None

    def ejecutar_consulta(self, consulta, parametros=None):
        """Ejecuta una consulta y devuelve los resultados (o Actualiza la transacción)."""
        try:
            if parametros:
                self.cursor.execute(consulta, parametros)
            else:
                self.cursor.execute(consulta)

            if consulta.strip().upper().startswith("SELECT"):
                # Si es SELECT, devuelve los resultados
                return self.cursor.fetchall()
            else:
                # Si es INSERT, UPDATE, DELETE, commit y devuelve el número de filas afectadas
                self.conexion.commit()
                return self.cursor.rowcount
        except Exception as e:
            print(f"Error al ejecutar consulta en MySQL: {e}")
            self.conexion.rollback() # Deshacer cambios en caso de error
            return None