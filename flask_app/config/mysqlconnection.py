import os
import pymysql.cursors

class ConexionMySQL:
    def __init__(self, bd):
        # Parametros de conexion leidos desde variables de entorno
        host = os.getenv("MYSQL_HOST", "localhost")
        user = os.getenv("MYSQL_USER", "root")
        password = os.getenv("MYSQL_PASSWORD", "")
        
        self.conexion = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=bd,
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )

    def consultar_bd(self, consulta, datos=None):
        with self.conexion.cursor() as cursor:
            try:
                cursor.execute(consulta, datos or {})
                sql = consulta.strip().lower()

                if sql.startswith("select"):
                    return cursor.fetchall()
                if sql.startswith("insert"):
                    return cursor.lastrowid
                return cursor.rowcount
            except Exception as e:
                print("Error en SQL:", e)
                return False
            finally:
                self.conexion.close()

def conectar_mysql(bd=None):
    if bd is None:
        bd = os.getenv("MYSQL_DB", "esquema_cinepedia")
    return ConexionMySQL(bd)