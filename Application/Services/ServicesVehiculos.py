from DAL.Infrastructure.ConexionDB import ConexionDB
from DAL.Repository.VehiculoRepository import VehiculoRepository

class ServicesVehiculos():
    def __init__(self, modelo):
        self.modelo = modelo

    def eliminarVehiculo(idVehiculo):
        try:
            conexion = ConexionDB()
            conexion.CrearConnection()
            conn = conexion.getConnection()
            vehiculo = VehiculoRepository()

            vehiculo.eliminar_vehiculo(conn, idVehiculo)

            return True, "Vehiculo eliminado"

        except Exception as e:
            return False, str(e)

        finally:
            conexion.CerrarConnection()


    def listar_vehiculos(self):
        try:
            self.modelo.CrearConnection()
            conn = self.modelo.getConnection()
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