from DAL.Infrastructure.ConexionDB import ConexionDB    

class VehiculoRepository():
    def __init__(self,vista,modelo):
        self.vista = vista
        self.modelo = modelo

    def RegistroVehiculos(self, IdVehiculo, Marca, Modelo, Año, Tipo, Precio_diario, Estado):
        try:
            conexion = ConexionDB()
            conexion.CrearConnection()
            db = conexion.getConnection()
            cursor = db.cursor()
            sql = "INSERT INTO VEHICULOS (ID_VEHICULO,MARCA,MODELO,AÑO,TIPO,PRECIO_POR_DIA,ESTADO) VALUES (%s,%s,%s,%s,%s,%s,%s)"
            datos =(IdVehiculo,Marca,Modelo,Año,Tipo,Precio_diario,Estado)
            cursor.execute(sql, datos)
            db.commit()
            cursor.close()
            conexion.CerrarConnection()
            return True, "Vehiculo registrado"
        except Exception as e:
            return False, f"Error al registrar el Vehiculo {e}"

    def EliminarVehiculo(self, idVehiculo):
        try:
            conexion = ConexionDB()
            conexion.CrearConnection()
            db = conexion.getConnection()
            cursor = db.cursor()
            sql = "DELETE FROM VEHICULOS WHERE ID_VEHICULO = %s"
            cursor.execute(sql, (idVehiculo,))
            db.commit()
            cursor.close()
            conexion.CerrarConnection()
            return True, "Vehiculo eliminado"
        except Exception as e:
            return False, f"Error al eliminar el Vehiculo {e}"

    def ActualizarVehiculo(conn, idVehiculo, marca, modelo, año, tipo, precio_diario, estado):
        try:
            conexion = ConexionDB()
            conexion.CrearConnection()
            db = conexion.getConnection()
            cursor = db.cursor()
            sql = "UPDATE VEHICULOS SET MARCA=%s, MODELO=%s, AÑO=%s, TIPO=%s, PRECIO_POR_DIA=%s, ESTADO=%s WHERE ID_VEHICULO=%s"
            datos =(marca, modelo, año, tipo, precio_diario, estado, idVehiculo)
            cursor.execute(sql, datos)
            db.commit()
            cursor.close()
            conexion.CerrarConnection()
            return True, "Vehiculo modificado"
        except Exception as e:
            return False, f"Error al modificar el Vehiculo {e}"

    def obtener_vehiculos(conn):
        cursor = conn.cursor()
        cursor.execute("""
            SELECT IdVehiculo, Marca, Modelo, Año, Tipo, Precio_diario, Estado 
            FROM Vehiculos
        """)
        return cursor.fetchall()

    def AlquilaVehiculo(idVehiculo):
        try:
            conexion = ConexionDB()
            conexion.CrearConnection()
            conn = conexion.getConnection()
            cursor = conn.cursor()
            vehiculo_repo = VehiculoRepository()
            cursor.execute("UPDATE Vehiculos SET Estado = 'Alquilado' WHERE idVehiculo = %s", (idVehiculo,))

        except Exception as e:
            return False, "no se puedo alquilar el vehiculo"
        finally:
            conexion.CerrarConnection()

    def mostrar_vehiculos(self):
        try:
            conexion = ConexionDB()
            conexion.CrearConnection()
            conn = conexion.getConnection()
            cursor = conn.cursor()
            cursor.execute("SELECT Id_Vehiculo, Marca, Modelo, Año, Tipo, Precio_Por_Dia, Estado FROM Vehiculos")
            filas = cursor.fetchall()
            return [
                {
                    "id":     f[0],
                    "placa": str(f[0]),
                    "marca":  f[1],
                    "modelo": f[2],
                    "año":   f[3],
                    "tipo":   f[4],
                    "precio": float(f[5]),
                    "estado": f[6]
                }
                for f in filas
            ]
        except Exception as e:
            raise e
        finally:
            self.modelo.CerrarConnection()